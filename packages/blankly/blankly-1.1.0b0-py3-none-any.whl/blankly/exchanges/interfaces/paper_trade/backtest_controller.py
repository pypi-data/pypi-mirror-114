"""
    Backtesting controller for paper trading interface
    Copyright (C) 2021  Emerson Dove

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import traceback
import typing
from datetime import datetime as dt

import pandas as pd
from bokeh.layouts import column as bokeh_columns
from bokeh.models import HoverTool
from bokeh.palettes import Category10_10
from bokeh.plotting import ColumnDataSource, figure, show

import blankly.exchanges.interfaces.paper_trade.metrics as metrics
from blankly.exchanges.interfaces.paper_trade.backtest_result import BacktestResult
from blankly.exchanges.interfaces.paper_trade.paper_trade import PaperTrade
from blankly.exchanges.interfaces.paper_trade.paper_trade_interface import PaperTradeInterface
from blankly.utils.time_builder import time_interval_to_seconds
from blankly.utils.utils import load_backtest_preferences, update_progress, write_backtest_preferences


def to_string_key(separated_list):
    output = ""
    for i in range(len(separated_list) - 1):
        output += str(separated_list[i])
        output += ","
    output += str(separated_list[-1:][0])
    return output


class BackTestController:
    def __init__(self, paper_trade_exchange: PaperTrade, backtest_settings_path: str = None, callbacks: list = None):
        self.preferences = load_backtest_preferences(backtest_settings_path)
        self.backtest_settings_path = backtest_settings_path
        if not paper_trade_exchange.get_type() == "paper_trade":
            raise ValueError("Backtest controller was not constructed with a paper trade exchange object.")
        self.interface: PaperTradeInterface = paper_trade_exchange.get_interface()

        self.price_events = []

        if callbacks is None:
            callbacks = []
        self.callbacks = callbacks

        self.current_time = None
        self.initial_time = None

        self.prices = []  # [epoch, "BTC-USD", price]

        self.price_dictionary = {}

        self.pd_prices = None

        self.sync_prices()

        self.use_price = None

        self.queue_backtest_write = False

        self.quote_currency = self.preferences['settings']['quote_account_value_in']

        self.initial_account = {}

    def sync_prices(self, save=True) -> dict:
        cache_folder = self.preferences['settings']["cache_location"]
        # Make sure the cache folder exists and read files
        try:
            files = os.listdir(cache_folder)
        except FileNotFoundError:
            files = []
            os.mkdir(cache_folder)

        available_files = []
        for i in range(len(files)):
            # example file name: 'BTC-USD.1622400000.1622510793.60.csv'
            # Remove the .csv from each of the files: BTC-USD.1622400000.1622510793.60
            identifier = files[i][:-4].split(",")
            identifier[1] = float(identifier[1])
            identifier[2] = float(identifier[2])
            identifier[3] = float(identifier[3])
            available_files.append(identifier)

        assets = self.preferences['price_data']['assets']  # type: dict
        for i in assets:
            identifier = [i[0], i[1], i[2], i[3]]
            string_identifier = to_string_key(identifier)
            if identifier in available_files:
                # Read the csv here
                if tuple(identifier) not in self.price_dictionary.keys():
                    print("Including: " + string_identifier + ".csv in backtest.")
                    self.price_dictionary[tuple(identifier)] = pd.read_csv(os.path.join(cache_folder,
                                                                                        string_identifier + ".csv")
                                                                           )
            else:
                if tuple(identifier) not in self.price_dictionary.keys():
                    print("No exact cache exists for " + str(identifier[0]) + " from " + str(identifier[1]) + " to " +
                          str(identifier[2]) + " at " + str(identifier[3]) + "s resolution. Downloading...")
                    download = self.interface.get_product_history(identifier[0], identifier[1], identifier[2],
                                                                  identifier[3])
                    self.price_dictionary[tuple(identifier)] = download
                    if save:
                        download.to_csv(os.path.join(cache_folder, string_identifier + ".csv"), index=False)

        # Merge all the same asset ids into the same dictionary spots
        unique_assets = {}
        for k, v in self.price_dictionary.items():
            if k[0] in unique_assets:
                unique_assets[k[0]] = pd.concat([unique_assets[k[0]], v], ignore_index=True)
            else:
                unique_assets[k[0]] = v

        return unique_assets

    def add_prices(self, asset_id, start_time, end_time, resolution, save=False):
        # Create its unique identifier
        identifier = [asset_id, start_time, end_time, resolution]

        # If it's not loaded then write it to the file
        if tuple(identifier) not in self.price_dictionary.keys():
            self.preferences['price_data']['assets'].append(identifier)
            if save:
                self.queue_backtest_write = True
        else:
            print("already identified")

        # Ensure everything is up to date
        self.sync_prices(save)

    def append_backtest_price_event(self, callback: typing.Callable, asset_id, time_interval, state_object, ohlc):
        if isinstance(time_interval, str):
            time_interval = time_interval_to_seconds(time_interval)
        self.price_events.append([callback, asset_id, time_interval, state_object, ohlc])

    def __determine_price(self, asset_id, epoch):

        # Geeksforgeeks binary search implementation
        def binary_search(arr, low, high, x):
            # Check base case
            if high >= low:

                mid = (high + low) // 2

                # Modify this to get our sort-of-right behavior
                try:
                    if arr[mid] <= x <= arr[mid + 1]:
                        return mid
                    elif arr[mid] > x:
                        return binary_search(arr, low, mid - 1, x)
                except IndexError:
                    return len(arr) - 1

                # If element is smaller than mid, then it can only
                # be present in left subarray

                # Else the element can only be present in right subarray
                else:
                    return binary_search(arr, mid + 1, high, x)

            else:
                # Must be before this case
                return 0

        try:
            prices = self.pd_prices[asset_id][self.use_price]  # type: pd.Series
            times = self.pd_prices[asset_id]['time']  # type: pd.Series

            # Iterate and find the correct quote price
            index = binary_search(times, 0, times.size, epoch)
            return prices[index]
        except KeyError:
            return 0

    def write_setting(self, key, value, save=False):
        """
        Write a setting to the .json preferences

        Args:
            key: Key under settings
            value: Value to set that settings key to
            save: Write this new setting to the file
        """
        self.preferences['settings'][key] = value
        if save:
            self.queue_backtest_write = True

        self.sync_prices(save)

    def write_initial_price_values(self, account_dictionary):
        """
        Write in a new price dictionary for the paper trade exchange.
        """
        self.interface.override_local_account(account_dictionary)

    def format_account_data(self, local_time) -> typing.Tuple[typing.Dict[typing.Union[str, typing.Any],
                                                                          typing.Union[int, typing.Any]],
                                                              typing.Dict[typing.Union[str, typing.Any],
                                                                          typing.Union[int, typing.Any]]]:
        true_available = {}
        # Grab the account status
        true_account = self.interface.get_account()

        # Create an account total value
        value_total = 0

        no_trade_available = {}
        # No trade account total
        no_trade_value = 0

        for i in true_account.keys():
            # Funds on hold are still added
            true_available[i] = true_account[i]['available'] + true_account[i]['hold']
            no_trade_available[i] = self.initial_account[i]['available'] + self.initial_account[i]['hold']
            currency_pair = i

            # Convert to quote (this could be optimized a bit)
            currency_pair += '-'
            currency_pair += self.quote_currency

            # Get price at time
            price = self.__determine_price(currency_pair, local_time)
            value_total += price * true_available[i]
            no_trade_value += price * no_trade_available[i]

        # Make sure to add the time key in
        true_available['time'] = local_time
        no_trade_available['time'] = local_time

        value_total += true_account[self.quote_currency]['available'] + true_account[self.quote_currency]['hold']

        no_trade_value += self.initial_account[self.quote_currency]['available'] + \
                          self.initial_account[self.quote_currency]['hold']

        true_available['Account Value (' + self.quote_currency + ')'] = value_total

        no_trade_available['Account Value (No Trades)'] = no_trade_value

        return true_available, no_trade_available

    def __has_nonzero_delta(self, cycle_status, column):
        show_zero_delta = self.preferences['settings']['show_tickers_with_zero_delta']
        halfway = len(cycle_status[column])/2
        is_same = cycle_status[column].iloc[0] == cycle_status[column].iloc[-1] == cycle_status[column].iloc[
            int(halfway)] == cycle_status[column].iloc[
            int((halfway+halfway)/2)] == cycle_status[column].iloc[int(halfway/2)]
        # Return true if they are not the same or the setting is set to true
        output = (not is_same) or show_zero_delta
        return output

    def run(self) -> BacktestResult:
        """
        Setup
        """

        # Create this initial so that we can compare how our strategy performs
        self.initial_account = self.interface.get_account()

        # Write our queued edits to the file
        if self.queue_backtest_write:
            write_backtest_preferences(self.preferences, self.backtest_settings_path)

        prices = self.sync_prices(False)

        # Organize each price into this structure: [epoch, "BTC-USD", price, open, high, low, close, volume]
        use_price = self.preferences['settings']['use_price']
        self.use_price = use_price

        # Sort each column by time
        for column in prices.keys():
            prices[column] = prices[column].sort_values('time')

        self.pd_prices = {**prices}

        for k, v in prices.items():
            frame = v  # type: pd.DataFrame

            # Be sure to push these initial prices to the strategy
            self.interface.receive_price(k, v[use_price].iloc[0])

            for index, row in frame.iterrows():
                # TODO iterrows() is allegedly pretty slow
                self.prices.append([row.time, k, row[use_price],
                                    row['open'],  # (index) 3
                                    row['high'],  # 4
                                    row['low'],  # 5
                                    row['close'],  # 6
                                    row['volume']])  # 7

        # pushing these prices together makes the time go weird
        self.prices = sorted(self.prices)

        self.current_time = self.prices[0][0]
        self.initial_time = self.current_time

        # Add a section to the price events which controls the next time they run & change to array of dicts
        for i in range(len(self.price_events)):
            self.price_events[i] = {
                'function': self.price_events[i][0],
                'asset_id': self.price_events[i][1],
                'interval': self.price_events[i][2],
                'state_object': self.price_events[i][3],
                'next_run': self.initial_time,
                'ohlc': self.price_events[i][4]
            }

        if prices == {} or self.price_events == []:
            raise ValueError("Either no price data or backtest events given. "
                             "Use .append_backtest_price_data or "
                             "append_backtest_price_event to create the backtest model.")
        """
        Begin backtesting
        """
        self.interface.set_backtesting(True)
        account = self.interface.get_account()
        column_keys = list(account.keys())
        column_keys.append('time')

        # column_keys = ['time']
        # for i in account.keys():
        #     column_keys.append(i['currency'])

        cycle_status = pd.DataFrame(columns=column_keys)

        no_trade_cycle_status = pd.DataFrame(columns=column_keys)

        # Append dictionaries to this to make the pandas dataframe
        price_data = []

        # Append dictionaries to this to make the no trade dataframe
        no_trade = []

        # Add an initial account row here
        if self.preferences['settings']['save_initial_account_value']:
            available_dict = self.format_account_data(self.initial_time)
            price_data.append(available_dict)

        show_progress = self.preferences['settings']['show_progress_during_backtest']

        print("\nBacktesting...")
        price_number = len(self.prices)
        try:
            for i in range(price_number):
                price_array = self.prices[i]
                if show_progress:
                    update_progress(i / price_number)
                self.interface.receive_price(price_array[1], price_array[2])
                self.current_time = price_array[0]
                self.interface.receive_time(self.current_time)
                self.interface.evaluate_limits()

                while True:
                    # Need to go through and establish an order for each of the price events
                    self.price_events = sorted(self.price_events, key=lambda sort_key: sort_key['next_run'])

                    # Now the lowest one has to go past the current time to be invalid
                    if self.price_events[0]['next_run'] > self.current_time:
                        break

                    local_time = self.price_events[0]['next_run']

                    # This is the actual callback to the user space
                    if self.price_events[0]['ohlc']:
                        # This pulls all the price data out of the price array defined on line 260
                        self.price_events[0]['function']({'open': price_array[3],
                                                          'high': price_array[4],
                                                          'low': price_array[5],
                                                          'close': price_array[6],
                                                          'volume': price_array[7]},

                                                         self.price_events[0]['asset_id'],
                                                         self.price_events[0]['state_object'])
                    else:
                        self.price_events[0]['function'](self.interface.get_price(self.price_events[0]['asset_id']),
                                                         self.price_events[0]['asset_id'], self.price_events[0][
                                                             'state_object'])

                    # Delay the next run until after the interval
                    self.price_events[0]['next_run'] += self.price_events[0]['interval']

                    available_dict, no_trade_dict = self.format_account_data(local_time)
                    price_data.append(available_dict)

                    no_trade.append(no_trade_dict)
        except Exception:
            traceback.print_exc()

        # Push the accounts to the dataframe
        cycle_status = cycle_status.append(price_data, ignore_index=True).sort_values(by=['time'])

        cycle_status.to_csv('output.csv')

        no_trade_cycle_status = no_trade_cycle_status.append(no_trade, ignore_index=True).sort_values(by=['time'])

        figures = []
        # for i in self.prices:
        #     result_index = cycle_status['time'].sub(i[0]).abs().idxmin()
        #     for i in cycle_status.iloc[result_index]:

        hover = HoverTool(
            tooltips=[
                ('value', '@value')
            ],

            # formatters={
            #     'time': 'datetime',  # use 'datetime' formatter for 'date' field
            #     '@{value}': 'printf',   # use 'printf' formatter for '@{adj close}' field
            # },

            # display a tooltip whenever the cursor is vertically in line with a glyph
            mode='vline'
        )

        # Back up the epoch list so that it can be used later for re-sampling
        epoch_backup = cycle_status['time'].tolist()

        if self.preferences['settings']['GUI_output']:
            global_x_range = None

            color = Category10_10.__iter__()

            time = [dt.fromtimestamp(ts) for ts in cycle_status['time']]

            for column in cycle_status:
                if column != 'time' and self.__has_nonzero_delta(cycle_status, column):
                    p = figure(plot_width=900, plot_height=200, x_axis_type='datetime')
                    source = ColumnDataSource(data=dict(
                        time=time,
                        value=cycle_status[column].tolist()
                    ))
                    p.step('time', 'value',
                           source=source,
                           line_width=2,
                           color=next(color),
                           legend_label=column,
                           mode="after",
                           )

                    # Replica of whats above to add the no-trade line to the backtest
                    if column == 'Account Value (' + self.quote_currency + ')':
                        source = ColumnDataSource(data=dict(
                            time=time,
                            value=no_trade_cycle_status['Account Value (No Trades)'].tolist()
                        ))
                        p.step('time', 'value',
                               source=source,
                               line_width=2,
                               color=next(color),
                               legend_label='Account Value (No Trades)',
                               mode="before")

                    p.add_tools(hover)

                    # Format graph
                    p.legend.location = "top_left"
                    p.legend.title = column
                    p.legend.title_text_font_style = "bold"
                    p.legend.title_text_font_size = "20px"
                    if global_x_range is None:
                        global_x_range = p.x_range
                    else:
                        p.x_range = global_x_range

                    figures.append(p)

            show(bokeh_columns(figures))

        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        dataframes = {
            'history': cycle_status
        }
        metrics_indicators = {}
        user_callbacks = {}

        # Check if it needs resampling
        resample_setting = self.preferences['settings']['resample_account_value_for_metrics']
        if isinstance(resample_setting, str) or is_number(resample_setting):
            # Backing arrays. We can't append directly to the dataframe so array has to also be made
            resampled_returns = pd.DataFrame(columns=['time', 'value'])
            resampled_backing_array = []

            # Find the interval second value
            interval_value = time_interval_to_seconds(resample_setting)

            # Assign start and stop limits
            epoch_start = epoch_backup[0]
            epoch_max = epoch_backup[len(epoch_backup) - 1]

            # Going to push this in as a single column version of our price data so that __determine_price can handle it
            self.pd_prices['Account Value (' + self.quote_currency + ')'] = pd.DataFrame()
            self.pd_prices['Account Value (' + self.quote_currency + ')'][use_price] = \
                cycle_status['Account Value (' + self.quote_currency + ')']

            self.pd_prices['Account Value (' + self.quote_currency + ')']['time'] = cycle_status['time']

            while epoch_start <= epoch_max:
                # Append this dict to the array
                resampled_backing_array.append({
                    'time': epoch_start,
                    'value': self.__determine_price('Account Value (' + self.quote_currency + ')', epoch_start)
                })

                # Increase the epoch value
                epoch_start += interval_value

            # Put this in the dataframe
            resampled_returns = resampled_returns.append(resampled_backing_array, ignore_index=True)

            # This is the resampled version
            dataframes['resampled_account_value'] = resampled_returns

            # Now we need to copy it and find the differences
            returns = resampled_returns.copy(deep=True)

            # Default diff parameters should do it
            returns['value'] = returns['value'].diff()

            # Now write it to our dictionary
            dataframes['returns'] = returns

            # -----=====*****=====----- I thought I stopped doing these comments when I actually learned to code
            metrics_indicators['cagr'] = metrics.cagr(dataframes)
            try:
                metrics_indicators['cum_returns'] = metrics.cum_returns(dataframes)
            except ZeroDivisionError:
                raise ZeroDivisionError("Division by zero when calculating cum returns. "
                                        "Are there valid account datapoints?")
            metrics_indicators['sortino'] = metrics.sortino(dataframes)
            metrics_indicators['sharpe'] = metrics.sharpe(dataframes)
            metrics_indicators['calmar'] = metrics.calmar(dataframes)
            metrics_indicators['volatility'] = metrics.volatility(dataframes)
            metrics_indicators['variance'] = metrics.variance(dataframes)
            # return_dict['beta'] = metrics.beta(return_dict)
            metrics_indicators['var'] = metrics.var(dataframes)
            metrics_indicators['cvar'] = metrics.cvar(dataframes)
            # return_dict['max_drawdown'] = metrics.cagr(return_dict)
            # -----=====*****=====-----

        # Run this last so that the user can override what they want
        for callback in self.callbacks:
            user_callbacks[callback.__name__] = callback(dataframes)

        result_object = BacktestResult(dataframes, metrics_indicators, user_callbacks)

        self.interface.set_backtesting(False)
        return result_object
