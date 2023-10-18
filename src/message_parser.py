import re
from datetime import datetime
from collections import deque
from typing import List

from alert_type import AlertType
from alert import Alert, Area
from notification_patterns import NotificationPatterns


class AlertParser:
    def __init__(self, alert_type: AlertType) -> None:
        self.type = alert_type

    def parse(self, message: str) -> Alert | None:
        lines = deque(message.split('\n'))
        alert_attrs = {}
        areas: List[Area] = []
        while lines:
            line = lines.popleft().strip()
            if match := NotificationPatterns.notification_header.match(line):
                if date := self._get_datetime_from_header(match):
                    alert_attrs['date'] = date
                    alert_attrs['type'] = self.type
            if 'date' in alert_attrs:
                if match := NotificationPatterns.notification_area.match(line):
                    areas.append(self._get_area(match, lines))
                elif line.startswith('**היכנסו'):
                    alert_attrs['instructions'] = line.strip('**')
        if alert_attrs:
            alerts = []
            for area in areas:
                for city in area.cities:
                    alerts.append(Alert(**alert_attrs, area=area.name, city=city))
            return alerts
            # return Alert(**alert_attrs)
        return None

    def _get_datetime_from_header(self, header: re.Match) -> datetime:
        alert_type, date, time = header.groups()
        if self.type != alert_type:
            return None
        return datetime(*map(int, date.split('/')[::-1]), *map(int, time.split(':')))

    def _get_area(self, area: re.Match, text_cont: deque) -> Area:
        area_name = area.group(1)
        cities = []
        while city := text_cont.popleft():
            if not city.strip():
                break
            city = NotificationPatterns.city.match(city).group(1)
            cities.extend([c for c in city.split(', ')])
        return Area(area_name, cities)
