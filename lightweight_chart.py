from lightweight_charts import Chart
import pandas as pd
import time

from lightweight_charts.abstract import AbstractChart
from patched_charts_snippet import patched_df_datetime_format
from visuals.position_overlay import PositionOverlay
# -----------------------------------------------------------------------------

# from multiprocessing import freeze_support
# Replace the library implementation
AbstractChart._df_datetime_format = patched_df_datetime_format
    # chart.show(block=True)
    # freeze_support()

# --------------------------------------------------------------------------------

def visualize_past_exec(full_data: pd.DataFrame, valid_exec_data: list):
    # 1. Initialize the Window frame
    chart = Chart(toolbox=True)
    
   # 2. Reconstruct your clean, verified DataFrame tracking layout
    df = full_data.copy()
    df.columns = [col.lower() for col in df.columns]
    df = df.rename(columns={'date': 'time'})
    df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Load your historical candles directly into the canvas
    chart.set(df)
    # 3. Layer your past trade positions onto the canvas layout
    # overlay = PositionOverlay(chart)

    # for idx, trade in enumerate(valid_exec_data):
    #     overlay.draw(trade, idx)
    # 4. Auto-scale view constraints onto the data timeline
    # chart.fit()

    

     # 5. 🔥 THE CRITICAL VISUAL FIX:
    # Pop open the chart window. We use show() normally here because 
    # our background daemon worker thread will keep it alive for us!


    chart.show()

    chart.run_script("""
    alert(typeof window.realSeries);
    alert(typeof window.realChart);
    """)

    # chart.run_script(f"""
    # PositionOverlay.init({chart.id});
    # """)

    # overlay = PositionOverlay(chart)

    # overlay.draw(valid_exec_data[0])

    # ........................................................................
    # chart.show()

    # chart.run_script(f"""
    # PositionOverlay.init({chart.id});
    # """)

    # overlay = PositionOverlay(chart)

    # for trade in valid_exec_data:
    #     overlay.draw(trade)

    # chart.fit()
    # ................................................................................
    
    print("[✓] TradingView window initialization triggered.")

    # 6. Keep the background window stream pipe active as long as the window is open
    while chart.is_alive:
        time.sleep(0.2) # Keeps the daemon thread engaged so the chart elements draw
