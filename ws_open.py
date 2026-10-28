import json

# ── CONFIG ──────────────────────────────────────────────────────────────────
symbol      = "BOOM600"               # Boom 600 symbol on Deriv
granularity = 180                       # 60 seconds = 1 minute candle; 180 seconds = 3 minute candle.
history_count = 1_500                  # How many past candles to load on start

contract_id = ""

# ────────────────────────────────────────────────────────────────────────────

def ws_open(ws):

    #` Get available symbols
    def get_symbols():
            ws.send(json.dumps({
                "active_symbols": "brief",
                "req_id": 1
            }))

    # Get historical data and stream latest price data via subscribe
    def subscribe_and_get_past_data():
        ws.send(json.dumps({
                "ticks_history": symbol,
                "adjust_start_time": 1,
                "end": "latest",
                "count": history_count,
                "style": "candles",
                "granularity": granularity,
                "subscribe": 1,          # keep streaming new candles
            }))
        
    # Get price proposal
    def get_price_proposal():
        ws.send(json.dumps({
        "proposal": 1,
        "amount": 10,
        "basis": "stake",
        "contract_type": "MULTDOWN",
        "currency": "USD",
        "duration_unit": "s",
        "multiplier": 10,
        "underlying_symbol": "1HZ100V",
        "subscribe": 1,
        "req_id": 5
        }))

    # Buy the contract (when ready)
    # Use proposal ID from previous response
    def buy_contract():
        ws.send(json.dumps({
        "buy": "PROPOSAL_ID_HERE",
        "price": 100,
        "req_id": 6
        }))

    # Monitor contract status
    def monitor_contract_status():
        ws.send(json.dumps({
        "proposal_open_contract": 1,
        "contract_id": contract_id,
        "subscribe": 1,
        "req_id": 7
        }))

    print("Getting symbols")
    get_symbols()
    print("Got symbols")
    print("Subcription Request Made")
    subscribe_and_get_past_data()
    print("Subscription Request Completed")


        