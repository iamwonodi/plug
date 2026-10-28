def check_engulfing(curr, prev, check_wicks=False):
    """
    Checks if the current candle engulfs the previous candle.
    Supports both traditional body engulfing and full range (wick) engulfing.
    """
    # 1. Define the boundaries based on user preference
    if check_wicks:
        curr_top, curr_bot = curr["high"], curr["low"]
        prev_top, prev_bot = prev["high"], prev["low"]
    else:
        curr_top = max(curr["open"], curr["close"])
        curr_bot = min(curr["open"], curr["close"])
        prev_top = max(prev["open"], prev["close"])
        prev_bot = min(prev["open"], prev["close"])

    # 2. Check if an engulfing structure exists
    is_engulfing = (curr_top > prev_top) and (curr_bot < prev_bot)
    
    if not is_engulfing:
        return None  # No engulfing pattern detected

    # 3. Determine the direction based on current candle's close
    is_bullish = curr["close"] > curr["open"]
    
    return "Bullish" if is_bullish else "Bearish"

def is_bullish(curr):
    # Determine bullish candle based on current candle's close and open
    is_bullish = curr["close"] > curr["open"]
    return is_bullish