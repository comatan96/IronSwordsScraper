import os
from dataclasses import dataclass


@dataclass
class APICredentials:
    id: int
    hash: str


def load_api_credentials() -> APICredentials:
    credentials_file = f'{os.environ["HOME"]}/telegram_credentials'
    credentials = {}
    with open(credentials_file) as cf:
        for line in cf:
            if line.startswith('api_id'):
                credentials['id'] = line.strip().split()[-1]
            if line.startswith('api_hash'):
                credentials['hash'] = line.strip().split()[-1]
    return APICredentials(**credentials)