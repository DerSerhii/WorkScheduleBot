"""
The module credentials:
Contains credentials to authenticate/authorize access to the Google API.

Requires an OAuth2 token for your Google service account in the form of a JSON key file.
This file must be named `service_account.json` and locate in the current package.
"""

import json
from pathlib import Path

from aiogoogle.auth.creds import ServiceAccountCreds


BASE_DIR = Path(__file__).resolve().parent

SERVICE_ACCOUNT_KEY = json.load(open(f'{BASE_DIR}/service_account.json'))

CREDS = ServiceAccountCreds(
    scopes=[
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
    ],
    **SERVICE_ACCOUNT_KEY
)
