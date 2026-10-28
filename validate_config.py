import logging
import sys

# ── LOGGING ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger(__name__)

def config_validator(app_id, account_id, auth_token):
     # Validate config before making any network calls
    missing = [
        name for name, val in {
            "ACCOUNT_ID": account_id,
            "AUTH_TOKEN": auth_token,
            "APP_ID":     app_id,
        }.items()
        if val.startswith("YOUR_")
    ]
    if missing:
        log.error(
            "Please fill in the following config values before running:\n"
            + "\n".join(f"  - {m}" for m in missing)
        )
        sys.exit(1)
