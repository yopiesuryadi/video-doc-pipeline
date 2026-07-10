"""Shared auth + config for the YouTube publish scripts.

Config lives outside the repo (secrets never get committed):
  ~/.config/youtube-pipeline/client_secret.json   OAuth client (Desktop)
  ~/.config/youtube-pipeline/token.json           saved refresh token (created by yt_auth.py)

Scope: youtube (read+write metadata, captions, thumbnails, and upload once the
project passes YouTube API audit). Personal-use projects stay in "Testing" mode
with the owner as a test user.
"""
import os

CONFIG_DIR = os.path.expanduser("~/.config/youtube-pipeline")
CLIENT_SECRET = os.path.join(CONFIG_DIR, "client_secret.json")
TOKEN = os.path.join(CONFIG_DIR, "token.json")
SCOPES = ["https://www.googleapis.com/auth/youtube"]


def get_service():
    """Return an authorized youtube API client, refreshing the token silently.
    Raises SystemExit with a clear message if auth has not been run yet."""
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    if not os.path.exists(TOKEN):
        raise SystemExit(
            "Not authorized yet. Run:\n"
            "  ~/.config/youtube-pipeline/venv/bin/python yt_auth.py"
        )
    creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN, "w") as f:
                f.write(creds.to_json())
        else:
            raise SystemExit(
                "Token invalid/expired and cannot refresh. Re-run yt_auth.py."
            )
    return build("youtube", "v3", credentials=creds)
