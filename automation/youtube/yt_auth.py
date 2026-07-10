#!/usr/bin/env python3
"""One-time OAuth consent. Opens a browser, you approve, refresh token is saved
to ~/.config/youtube-pipeline/token.json. Re-run only if the token is revoked
or expires (Testing-mode tokens lapse after ~7 days until the app is published).
"""
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from yt_common import CLIENT_SECRET, TOKEN, SCOPES


def main():
    if not os.path.exists(CLIENT_SECRET):
        raise SystemExit(f"Missing {CLIENT_SECRET}")
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
    # Loopback flow: opens the browser, catches the redirect on localhost.
    creds = flow.run_local_server(port=0, prompt="consent")
    with open(TOKEN, "w") as f:
        f.write(creds.to_json())
    os.chmod(TOKEN, 0o600)
    print(f"Authorized. Token saved to {TOKEN}")


if __name__ == "__main__":
    main()
