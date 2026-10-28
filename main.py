"""
Deriv Authenticated WebSocket URL via OTP Endpoint
===================================================
Python implementation of the OTP REST call to get an
authenticated WebSocket URL for Deriv's trading API.

Install:
    pip install requests websocket-client
"""

# ── IMPORTS ─────────────────────────────────────────────────────────────────
from stream_handler import on_open, on_message, on_error, on_close
from exceptions import DerivAuthError
from generate_url_ws import get_authenticated_ws_url
from validate_config import config_validator
import websocket
import logging
import sys
import threading
from queues import chart_queue
from visualize_daemon_worker import background_daemon_worker

# ── LOGGING ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger(__name__)


# ── CONFIG ───────────────────────────────────────────────────────────────────
ACCOUNT_ID  = "DOT91915855"        # e.g. "CR123456"
AUTH_TOKEN  = "pat_71046b871e1994eb15cbf7df1dd3c5346c1cc8ef58b978c7f19f6d6dce493739"  # PAT or JWT token
APP_ID      = "33CkezSldU4aPfT0xJlIS"            # Your Deriv app ID
OTP_URL     = f"https://api.derivws.com/trading/v1/options/accounts/{ACCOUNT_ID}/otp"
TIMEOUT     = 10                       # seconds for REST request
# ─────────────────────────────────────────────────────────────────────────────




# ── WSS CONNECT: Connect and verify the WebSocket URL works ─────────────────────

def verify_ws_connection(ws_url: str) -> None:
    """
    Opens the authenticated WebSocket and prints the first message
    received, then closes. Use this to confirm the URL is valid.
    """
    log.info("Verifying WebSocket connection...")


    try:
        ws_app = websocket.WebSocketApp(
            ws_url,
            on_open    = on_open,
            on_message = on_message,
            on_error   = on_error,
            on_close   = on_close,
        )
        ws_app.run_forever()
    except Exception as e:
        log.error(f"Failed to connect to WebSocket: {e}")
        raise


# ── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    # Validate config before making any network calls
    config_validator(APP_ID, ACCOUNT_ID, AUTH_TOKEN)

    # 🔥 STEP A: Initialize and start your background daemon thread BEFORE network calls.
    # Setting daemon=True ensures that when you close the main script, the thread dies cleanly.
    daemon_thread = threading.Thread(target=background_daemon_worker, args= (chart_queue,),daemon=True)
    daemon_thread.start()
    log.info("[*] Background Daemon Thread initialized and listening for tasks...")

    try:
        ws_url = get_authenticated_ws_url(
            account_id = ACCOUNT_ID,
            auth_token = AUTH_TOKEN,
            app_id     = APP_ID,
        )
        print(f"\nAuthenticated WebSocket URL:\n  {ws_url}\n")

        # Connect to the Deriv websockets for market data, backtesting and live trade executions
        # 🛑 Note: This line blocks the main thread completely. 
        # But because our daemon was started above, it will run concurrently!
        verify_ws_connection(ws_url)

    except DerivAuthError as e:
        log.error(f"Authentication failed:\n  {e}")
        sys.exit(1)

    except KeyboardInterrupt:
        log.info("Interrupted by user.")
        sys.exit(0)