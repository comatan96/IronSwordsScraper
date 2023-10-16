from dataclasses import dataclass
from datetime import datetime
from typing import List

from alert_type import AlertType


@dataclass
class Area:
    name: str
    cities: List[str]


@dataclass
class Alert:
    type: AlertType
    area: str
    city: str
    date: datetime
    instructions: str

    def items(self):
        for key in self.__dataclass_fields__:
            yield key, getattr(self, key)