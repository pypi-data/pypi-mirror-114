from typing import Set

from entitykb.contrib.date import Date
from entitykb.models import CompositeEntity, Pattern


class DateRange(CompositeEntity):
    start: Date
    end: Date

    @classmethod
    def relevant_labels(cls) -> Set[str]:
        return {"DATE"}

    def is_valid(self, text: str):
        return True


def test_construct_pattern():
    pattern = Pattern(
        pipeline="default",
        label="DATE_RANGE",
        key="from DATE_0 until DATE_1",
        composite_fields=("start", "end"),
    )
    assert pattern == Pattern(**pattern.dict())
    assert len({pattern, Pattern(**pattern.dict())}) == 1

    assert pattern.key == "from DATE_0 until DATE_1"
    assert pattern.label == "DATE_RANGE"
    assert pattern.composite_fields == ("start", "end")
