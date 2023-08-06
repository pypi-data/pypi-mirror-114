from __future__ import annotations

from itertools import chain
from typing import Tuple, List, Set, Type, Optional

from pydantic import BaseModel, Field

from . import Registry, Span, Entity


class CompositeEntity(Entity):
    subspans: List[Span] = Field(default_factory=list)

    @classmethod
    def relevant_labels(cls) -> Set[str]:
        return set()

    @classmethod
    def get_subclass(cls, label: str) -> Type["CompositeEntity"]:
        registry = Registry.instance()
        return registry.identify_class(CompositeEntity, {"label": label})

    def subspan_offsets(self) -> Set[int]:
        return set(chain(*[subspan.offsets for subspan in self.subspans]))


class Pattern(BaseModel):
    pipeline: str
    label: str
    key: str
    composite_fields: Tuple[Optional[str], ...]

    def __hash__(self):
        return hash(self.as_tuple())

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        values = ", ".join(map(str, self.as_tuple()))
        return f"Pattern({values})"

    def as_tuple(self):
        return self.pipeline, self.label, self.key, self.composite_fields
