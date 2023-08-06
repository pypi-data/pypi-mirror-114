from datetime import date
from typing import Any, Optional

from entitykb import Entity


def get_date(year, month, day):
    try:
        return date(year, month, day or 1)
    except ValueError:
        pass


def get_name(*, year: int = None, month: int = None, day: int = None, **_):
    if year:
        if month and 1 <= month <= 12:
            if day is not None:
                if get_date(year, month, day):
                    return f"{year:0>4}-{month:0>2}-{day:0>2}"
            else:
                return f"{year:0>4}-{month:0>2}"
        else:
            return f"{year:0>4}"


class Date(Entity):
    year: int = None
    month: int = None
    day: int = None
    text: str = None

    def __init__(self, **data: Any):
        name = get_name(**data)
        data.setdefault("name", name)
        super().__init__(**data)

    def is_valid(self, _: str):
        return self.name is not None

    @property
    def as_date(self) -> Optional[date]:
        return get_date(self.year, self.month, self.day)
