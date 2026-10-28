

stake = 10
profit = 10.3
multiplier = 100

max_allowed_sl = 9
actual_profit = 10.22
commission = 0.08


def calculate_change_in_price(entry, profit_or_loss):

    # change_in_balance = stake * multiplier * price_change / entry
    change_in_balance = profit_or_loss
    price_change = (change_in_balance * entry) / (stake * multiplier)
    return price_change

def calculate_profit_price_value(entry_price, profit_amount):

    price_change = calculate_change_in_price(entry_price, profit_amount)
    return entry_price - price_change

def calculate_loss_price_value(entry_price, loss_amount):

    price_change = calculate_change_in_price(entry_price, loss_amount)
    return entry_price + price_change