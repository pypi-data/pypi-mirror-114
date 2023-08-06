from dataclasses import dataclass
from typing import Tuple, Iterable, Type

from entitykb import interfaces


@dataclass
class Pipeline(object):
    name: str = None
    kb: interfaces.IKnowledgeBase = None
    extractor: interfaces.IExtractor = None
    composer: Type[interfaces.IComposer] = None
    filterers: Tuple[Type[interfaces.IFilterer], ...] = tuple

    def __call__(self, text: str, labels: Iterable[str]):
        doc = self.extractor.extract_doc(text=text, labels=labels)
        doc.spans = self.filter_spans(doc)
        return doc

    @property
    def has_composer(self):
        return self.composer is not None

    def filter_spans(self, doc):
        spans = iter(doc.spans)

        if self.has_composer:
            composer = self.make_composer(doc)
            spans = composer.compose(spans)

        for filterer_cls in self.filterers:
            filterer = filterer_cls(doc)
            spans = filterer.filter(spans)

        spans = sorted(spans, key=lambda span: span.offset)

        return tuple(spans)

    def make_composer(self, doc) -> interfaces.IComposer:
        return self.composer(kb=self.kb, pipeline=self.name, doc=doc)
