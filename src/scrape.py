from datetime import datetime, timezone
from collections import defaultdict

from telethon import TelegramClient
from bidi.algorithm import get_display

from telegram_api import load_api_credentials
from message_parser import AlertParser
from alert_type import AlertType
from alert import Area

import polars as pd

class PikudHaorefScraper:
    _channel_name = 'פיקוד העורף'

    def __init__(self, alert_type=AlertType.MISSILES) -> None:
        self._api = load_api_credentials()
        self.client = TelegramClient('anon', self._api.id, self._api.hash)
        self.client.start()
        self.alert_parser = AlertParser(alert_type=alert_type)
        self.alerts = defaultdict(list)

    @property
    async def channel(self):
        if hasattr(self, '_channel'):
            return self._channel
        await self.client.connect()
        async for dialog in self.client.iter_dialogs():
            if dialog.is_channel and dialog.name == self._channel_name:
                self._channel = dialog
                return dialog

    async def extract_red_alert(self, start_date=datetime(2023, 10, 8, tzinfo=timezone.utc)):
        await self.client.connect()
        async for message in self.client.iter_messages(await self.channel):
            if message.date >= start_date:
                if alerts := self.alert_parser.parse(message.text):
                    for alert in alerts:
                        for feature, value in alert.items():
                            self.alerts[feature].append(value)
            else:
                break
        pd.from_dict(self.alerts).write_csv('data.csv')


if __name__ == '__main__':
    scraper = PikudHaorefScraper()
    scraper.client.loop.run_until_complete(scraper.extract_red_alert())