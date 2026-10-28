from helpers import is_bullish

# from threading import Thread

from trade_calculator import calculate_loss_price_value, calculate_profit_price_value

# ── YOUR STRATEGY HOOK ───────────────────────────────────────────────────────
def on_candle_close(price_data: list):
    """
    Called every time a 3-minute candle closes.
    `price_data` is a DataFrame of all candles so far (most recent is last row).

    Drop your strategy logic here — e.g. EMA crossover, RSI, spike detection.
    """
    data_count = len(price_data)
    current_count = 0
    # threads = []
    while current_count < data_count:
        
        current_candle_data = price_data[current_count]
        is_bull_candle = is_bullish(current_candle_data)

        if not is_bull_candle:
            current_count += 1
            continue
        
        # eval_price_data = price_data[current_count:]
    #     thread = Thread(target=magic, args=(eval_price_data, current_count))
    #     threads.append(thread)
    # for t in threads:
    #     t.start()

# ─────────────────────────────────────────────────────────────────────────────

def poi_setup_detector(price_data: list):

    loss_amount = 10
    profit_amount = 10.3

    # Your detected trade parameters (From your backend logic)
        # trade_index = 2            # Index where trade triggered ('2026-06-17')
        # exit_index = 4             # Index where trade ended ('2026-06-19')
        # entry_price = 1.0860
        # stop_loss = 1.0800
        # take_profit = 1.0950

    poi_candles_data = []
    data_count = len(price_data)
    current_count = 0


    # Loops through each candle's data to derive valid POI's
    while current_count < data_count:
        if current_count == 0:
            print(price_data[current_count])
        curr = price_data[current_count]
        curr_close = curr["close"]
        curr_open = curr["open"]
        curr_high = curr["high"]
        curr_low = curr["low"]
        curr_midpoint_price = curr_open + ((curr_close - curr_open) / 2)

        # Confirm if candle is a bullish candle
        is_bull_candle = is_bullish(curr)

        if not is_bull_candle:
            current_count += 1
            continue
        
        

    

        # Confirm if subsequent candles either broke above the high of the bullish candle OR retraced anywhere between 50% and less than 100% of the bullish candle
        
        max_curr_override = 1
        curr_override = 0
        has_valid_retracement = False
        has_bullish_counterpart = False
        has_bearish_sig_candle = False
        sub_candles_data = price_data[current_count + 1:]


        for candle_dt in sub_candles_data:
            idx = price_data.index(candle_dt)
            # sub_close = candle_dt["close"]
            # sub_open = candle_dt["open"]  The variable was not used
            sub_candle = candle_dt
            sub_high = candle_dt["high"]
            sub_low = candle_dt["low"]

            # Current bullish candle becomes invalidated if it has been overridden once
            if curr_override > max_curr_override:
                break

            # Conditions for when subsequent candle breaks or equals the bullish High and it is only allowed to happen once.
            # The candle high that broke our old's candle High would be our new High
            if sub_high >= curr_high:
                curr_high = sub_high
                curr_override += 1
                continue


            # Conditions for what is to happen when we achieve a valid retracement
            if not has_valid_retracement:
                has_valid_retracement = sub_low <= curr_midpoint_price and sub_low > curr_low

            if has_valid_retracement and sub_low <= curr_low:
                break

            if has_valid_retracement and not has_bullish_counterpart:

                #  whilst retracement has not been invalidated we wait for a bullish candle. 
                # Candle could be the exact candle that did hit our retracement POI
                has_bullish_counterpart = is_bullish(candle_dt)

                if has_bullish_counterpart and sub_high > curr_high:
                    break

                continue
        
            
            # As soon as we gat a candle whose closing price was above it's opening price we await for the next candle to be a bearish candle
            has_bearish_sig_candle = not is_bullish(candle_dt)

            if not has_bearish_sig_candle:
                break

            if has_valid_retracement and has_bullish_counterpart and has_bearish_sig_candle:
                poi_derived_entry = sub_low - ((sub_high - sub_low) / 2)
                poi_trade_idx = idx + 1
                take_profit = calculate_profit_price_value(poi_derived_entry, profit_amount)
                stop_loss = calculate_loss_price_value(poi_derived_entry, loss_amount)

                modified_idx = poi_trade_idx + 1
                modified_price_data = price_data[modified_idx:]

                for each in modified_price_data:

                    if each["low"] == take_profit or each["high"] == stop_loss:
                        exit_index = modified_idx
                        modified_candle_data = {
                            "signal_candle": curr,
                            "entry_candle": sub_candle,
                            "exit_candle": each,
                            "trade_index" : poi_trade_idx,
                            "exit_index" : exit_index,
                            "entry_price" : poi_derived_entry,
                            "stop_loss" : stop_loss,
                            "take_profit" : take_profit,
                        }
                        print(modified_candle_data)
                        poi_candles_data.append(modified_candle_data)
                        break

                    modified_idx += 1

                exit_index = -1
                modified_candle_data = {
                            "signal_candle": curr,
                            "entry_candle": sub_candle,
                            "exit_candle": price_data[exit_index],
                            "trade_index" : poi_trade_idx,
                            "exit_index" : exit_index,
                            "entry_price" : poi_derived_entry,
                            "stop_loss" : stop_loss,
                            "take_profit" : take_profit,
                        }
                poi_candles_data.append(modified_candle_data)
                break

        current_count += 1
    print(len(poi_candles_data))
    return poi_candles_data


def trade():
    pass