import json
import requests
from exceptions import DerivAuthError

import logging

# Initialize a standard logger object
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


timeout = 10


def get_authenticated_ws_url(
    account_id: str,
    auth_token: str,
    app_id: str,
    timeout: int = timeout,
) -> str:
    """
    Makes a POST request to Deriv's OTP endpoint and returns
    the authenticated WebSocket URL.

    Args:
        account_id : Your Deriv account ID (e.g. "CR123456")
        auth_token : Bearer token (PAT or JWT)
        app_id     : Your Deriv app ID
        timeout    : Request timeout in seconds

    Returns:
        Authenticated WebSocket URL string

    Raises:
        DerivAuthError : On any auth, network, or response error
    """
    url = f"https://api.derivws.com/trading/v1/options/accounts/{account_id}/otp"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Deriv-App-ID":  app_id,
        "Content-Type":  "application/json",
    }

    log.info("Requesting OTP from Deriv API...")
    log.info(f"  Endpoint : {url}")

    try:
        response = requests.post(url, headers=headers, timeout=timeout)

    except requests.exceptions.ConnectionError as e:
        raise DerivAuthError(
            f"Could not connect to Deriv API. Check your internet connection.\n  Detail: {e}"
        )
    except requests.exceptions.Timeout:
        raise DerivAuthError(
            f"Request timed out after {timeout}s. Deriv API may be slow or unreachable."
        )
    except requests.exceptions.RequestException as e:
        raise DerivAuthError(f"Unexpected network error: {e}")

    # ── HTTP status check ────────────────────────────────────────────────────
    log.info(f"  HTTP status : {response.status_code}")

    if response.status_code == 401:
        raise DerivAuthError(
            "Unauthorized (401). Your AUTH_TOKEN is invalid or expired. "
            "Generate a fresh PAT from app.deriv.com → Account Settings → API Token."
        )
    if response.status_code == 403:
        raise DerivAuthError(
            "Forbidden (403). Your token does not have permission for this account. "
            "Check that the token belongs to the correct account ID."
        )
    if response.status_code == 404:
        raise DerivAuthError(
            f"Not Found (404). Account ID '{account_id}' may be incorrect, "
            "or this endpoint is not available for your account type."
        )
    if response.status_code == 429:
        raise DerivAuthError(
            "Too Many Requests (429). You've hit the rate limit. Wait a moment and retry."
        )
    if not response.ok:
        raise DerivAuthError(
            f"Unexpected HTTP error {response.status_code}: {response.text[:300]}"
        )

    # ── Parse JSON ───────────────────────────────────────────────────────────
    try:
        result = response.json()
    except ValueError:
        raise DerivAuthError(
            f"Response was not valid JSON. Raw response:\n{response.text[:300]}"
        )

    # ── Validate response structure ──────────────────────────────────────────
    if "error" in result:
        err = result["error"]
        code    = err.get("code", "UNKNOWN")
        message = err.get("message", "No message provided")
        raise DerivAuthError(f"Deriv API error [{code}]: {message}")

    if "data" not in result:
        raise DerivAuthError(
            f"Unexpected response structure — 'data' key missing.\n"
            f"Full response: {json.dumps(result, indent=2)[:500]}"
        )

    ws_url = result.get("data", {}).get("url")

    if not ws_url:
        raise DerivAuthError(
            f"'url' not found in response data.\n"
            f"data field: {json.dumps(result['data'], indent=2)}"
        )

    if not ws_url.startswith("wss://"):
        raise DerivAuthError(
            f"Returned URL does not look like a WebSocket URL: {ws_url}"
        )

    log.info("Authenticated WebSocket URL obtained successfully.")
    log.info(f"  WS URL: {ws_url}")
    return ws_url
