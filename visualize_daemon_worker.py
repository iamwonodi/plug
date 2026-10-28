from lightweight_chart import visualize_past_exec
import traceback


def background_daemon_worker(chart_queue):
    """ Runs on your separate daemon thread, isolated from the WebSocket loop """
    print("[*] Background Daemon Thread actively monitoring queue...")
    while True:
        try:
            # The thread stays asleep until data drops into the queue channel
            historical_payload = chart_queue.get()
            
            candles_df = historical_payload["candles"]
            valid_trades = historical_payload["trades"]
            
            print("[Daemon Thread] Launching chart window outside the main stream...")
            visualize_past_exec(candles_df, valid_trades)
            
        except Exception as e:
            # Protects the thread loop from dying if a charting data asset error occurs
            print(f"🔥 [Daemon Thread Error Captured]: {e}")
            traceback.print_exc()
        finally:
            # Guarantees the queue unblocks even if an operation fails
            chart_queue.task_done()
