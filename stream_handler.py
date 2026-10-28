"""
Deriv Boom 600 - 1 Minute Candle Data Fetcher
==============================================
Uses Deriv's WebSocket API to stream live 1-minute OHLC candles.

Setup:
  pip install websocket-client pandas

Get your API token:
  1. Log in to app.deriv.com
  2. Go to Account Settings > API Token
  3. Create a token with "Read" and "Trade" scopes
"""

import json
import pandas as pd
# from lightweight_chart import visualize_past_exec
import ws_message as wm


from engine import  poi_setup_detector
from ws_open import ws_open

from queues import chart_queue

# ── CONFIG ──────────────────────────────────────────────────────────────────
symbol      = "BOOM600"               # Boom 600 symbol on Deriv
granularity = 180                       # 60 seconds = 1 minute candle; 180 seconds = 3 minute candle.
history_count = 10_000                  # How many past candles to load on start

contract_id = ""
active_symbols = []
# ────────────────────────────────────────────────────────────────────────────

# Stores completed 3-minute candles
candles = pd.DataFrame(columns=["date", "open", "high", "low", "close"])

# Tracks the candle currently forming (not yet closed)
live_candle = {}


def on_open(ws):
    """Called when WebSocket connects — authorize first."""
    print("[+] Connected to Deriv API") 

    #` Get available symbols
    ws_open(ws)


def on_message(ws, message):
    global candles, live_candle, active_symbols

    data = json.loads(message)
    msg_type = data.get("msg_type")
    # print(msg_type)

    # ── Step 1: Handle active symbols reponse data fed to us by Deriv Websockets ──
    if msg_type == "active_symbols":
        active_symbols = wm.active_symbols_event(data)

    # ── Step 2: Handle historical candle batch (arrives once on subscribe) ──
    elif msg_type == "candles":
        candles = wm.candles_event(data)

        # Implementing magic strategy on historical candle data
        poi_candles_data = poi_setup_detector(candles.to_dict('records'))

        # Pass data over to the queue so the daemon thread renders it
        chart_queue.put({
            "candles": candles,
            "trades": poi_candles_data
        })


        # Visualizing the implemented strategy
        # visualize_past_exec(candles, poi_candles_data)


    # ── Step 3: Handle live candle updates (streams every tick) ──
    elif msg_type == "ohlc":
        candles, live_candle = wm.ohlc_event(data, candles, live_candle)

    elif msg_type == "error":
        print(f"[!] API Error: {data['error']['message']}")


def on_error(ws, error):
    print(f"[!] WebSocket Error: {error}")


def on_close(ws, close_status_code, close_msg):
    print("[x] Connection closed")




