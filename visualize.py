import plotly.graph_objects as go
import pandas as pd
import webbrowser # Built-in Python helper to open files without freezing
import os

def visualize_past_exec(full_data: pd.DataFrame, valid_exec_data: list):
    # 1. Past Forex Data (Simulating your logic's history)
    df = full_data

    # Calculate a dynamic min and max price based on your last 100 candles
    last_100_candles = df.tail(100)
    padding = (last_100_candles['high'].max() - last_100_candles['low'].min()) * 0.1        


    # 3. Create the Base Candlestick Chart
    fig = go.Figure(data=[go.Candlestick(
        x=df['date'],
        open=df['open'], high=df['high'],
        low=df['low'], close=df['close'],
        name="Market Data"
    )])

    # 4. Add the Target/Risk zones as toggleable Legend Group Traces
    for idx, trade in enumerate(valid_exec_data):
        trade_id = f"Trade #{idx + 1}" # Generates 'Trade #1', 'Trade #2'

        # Your detected trade parameters (From your backend logic)
        trade_index = trade["trade_index"]            # Index where trade triggered ('2026-06-17')
        exit_index = trade["exit_index"]             # Index where trade ended ('2026-06-19')
        entry_price = trade["entry_price"]
        stop_loss = trade["stop_loss"]
        take_profit = trade["take_profit"]

        x0_date = df['date'].iloc[trade_index]
        x1_date = df['date'].iloc[exit_index]

         # Coordinates to construct the translucent polygon boxes
        # Left-Top -> Right-Top -> Right-Bottom -> Left-Bottom -> Close Shape
        tp_x = [x0_date, x1_date, x1_date, x0_date, x0_date]
        tp_y = [take_profit, take_profit, entry_price, entry_price, take_profit]
        
        sl_x = [x0_date, x1_date, x1_date, x0_date, x0_date]
        sl_y = [entry_price, entry_price, stop_loss, stop_loss, entry_price]

        # 🟢 Take Profit Box Trace (Visible by default, but toggleable)
        fig.add_trace(go.Scatter(
            x=tp_x, y=tp_y, fill="toself",
            fillcolor="rgba(0, 255, 0, 0.12)",
            line=dict(color="green", width=1),
            name=f"{trade_id} Zones",
            legendgroup=trade_id, # Links both boxes to the same toggle switch
            showlegend=True,      # Only show one name in the legend list
            hoverinfo="skip"
        ))

        # 🔴 Stop Loss Box Trace (Linked to the same toggle group switch)
        fig.add_trace(go.Scatter(
            x=sl_x, y=sl_y, fill="toself",
            fillcolor="rgba(255, 0, 0, 0.12)",
            line=dict(color="red", width=1),
            name=f"{trade_id} Risk",
            legendgroup=trade_id,
            showlegend=False,     # Hidden from legend so it hides/shows via the parent group
            hoverinfo="skip"
        ))

        # 🔵 Clean Entry Label Marker Annotation
        fig.add_annotation(
            x=x0_date, y=entry_price,
            text=f"🛒 Entry #{idx + 1}",
            showarrow=True, arrowhead=1, arrowcolor="cyan",
            ax=-30, ay=-25,
            font=dict(color="white", size=10),
            bgcolor="rgba(0, 0, 255, 0.7)"
        )


    # 6. Clean up Chart Styling (Dark Theme & Hide Range Slider)
    fig.update_layout(
        title="Vanilla Python Interactive Trade Analysis Visualizer",
        template="plotly_dark",
        xaxis_rangeslider_visible=False, # Hides the messy bottom slider
        yaxis=dict(
        title="Price", 
        side="right",
        range=[last_100_candles['low'].min() - padding, last_100_candles['high'].max() + padding]
    ),
        xaxis=dict(title="Timeframe (UTC)"),
        legend=dict(
            orientation="h", # Places the interactive legend switches horizontally across the top
            yanchor="bottom", y=1.02,
            xanchor="right", x=1
        )
    )

    # This opens your default web browser automatically with the interactive chart
    # fig.show()


      # 🛑 FIXED: Avoid using fig.show() as it blocks the thread
    # Save the interactive chart as an HTML file in your project folder instantly
    output_filename = "historical_analysis.html"
    fig.write_html(output_filename, auto_open=False)
    
    # Open the browser independently via a background system execution call
    # This prevents the main execution pipeline from locking up
    webbrowser.open('file://' + os.path.realpath(output_filename))
    print("[✓] Clean toggleable chart exported successfully.")
