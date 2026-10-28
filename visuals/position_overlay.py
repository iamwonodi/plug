import json

class PositionOverlay:

    def __init__(self, chart):
        self.chart = chart

    def draw(self, trade):


        payload = {

            "entry_time": int(
                trade["entry_candle"]["date"].timestamp()
            ),

            "exit_time": int(
                trade["exit_candle"]["date"].timestamp()
            ),

            "entry_price": trade["entry_price"],

            "take_profit": trade["take_profit"],

            "stop_loss": trade["stop_loss"],

            "side": "sell"

        }


        self.chart.run_script(f"""
            window.PositionManager.add({json.dumps(payload)});
        """)
# class PositionOverlay:

#     def __init__(self, chart):
#         self.chart = chart

#     def draw(self, trade, trade_id):
        
#         trade_id += 1
#         entry_time = trade["entry_candle"]["date"].strftime('%Y-%m-%d %H:%M:%S')
#         exit_time = trade["exit_candle"]["date"].strftime('%Y-%m-%d %H:%M:%S')
#         # entry_index = trade["trade_index"]
#         # exit_index = trade["exit_index"]

#         entry = trade["entry_price"]
#         tp = trade["take_profit"]
#         sl = trade["stop_loss"]

#         # Entry marker
#         self.chart.marker(
#             time=entry_time,
#             position="below",
#             shape="arrow_down",
#             color="#00ff55",
#             text=f"SELL #{trade_id}"
#         )

#         # Exit marker
#         self.chart.marker(
#             time=exit_time,
#             position="above",
#             shape="circle",
#             color="#ffffff",
#             text=f"EXIT #{trade_id}"
#         )

#         # TP
#         self.chart.horizontal_line(
#             tp,
#             color="green",
#             style="dashed",
#             text=f"TP {trade_id}"
#         )

#         # SL
#         self.chart.horizontal_line(
#             sl,
#             color="red",
#             style="dashed",
#             text=f"SL {trade_id}"
#         )

#         # Entry
#         self.chart.horizontal_line(
#             entry,
#             color="white",
#             style="solid",
#             text=f"ENTRY {trade_id}"
#         )