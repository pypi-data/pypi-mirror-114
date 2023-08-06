from collections import Counter
from itertools import chain
from typing import Iterator, List, Set

from entitykb import Span, interfaces, CompositeEntity, Pattern
from . import DedupeByLabelOffset


class DefaultComposer(interfaces.IComposer):
    def compose(self, spans: Iterator[Span]) -> Iterator[Span]:
        labels = self.graph.get_pattern_labels(self.pipeline)
        if not labels:
            return spans

        original_spans = list(spans)

        full_spans = self.dedupe_sort_spans(original_spans)
        composite_spans = []

        for label in labels:
            klass = CompositeEntity.get_subclass(label)
            relevant_labels = klass.relevant_labels()
            label_spans = self.keep_spans(relevant_labels, spans=full_spans)
            composite_spans += self.get_composites(label, spans=label_spans)

        composite_offsets = set()
        for comp_span in composite_spans:
            for subspan in getattr(comp_span.entity, "subspans", []):
                composite_offsets.update(
                    range(subspan.offset, subspan.last_offset + 1)
                )

        keep_spans = []
        for original_span in full_spans:
            if not composite_offsets.issuperset(original_span.offsets):
                keep_spans.append(original_span)

        if composite_spans:
            return chain(*(keep_spans, composite_spans))
        else:
            return iter(original_spans)

    def get_composites(self, comp_label: str, spans: List[Span]) -> List[Span]:
        composite_spans = []
        for offset, span in enumerate(spans):
            patterns = self.find_patterns(comp_label, spans, offset)
            for pattern in patterns:
                data, subspans = self.data_from_subspans(
                    offset, pattern, spans
                )

                token_0 = subspans[0].offset
                token_n = subspans[-1].last_offset
                tokens = self.doc.tokens[token_0 : token_n + 1]
                text = self.kb.tokenizer.detokenize(tokens)

                # create composite entity
                composite = CompositeEntity.create(
                    **data, label=comp_label, name=text, subspans=subspans
                )

                # create new span if composite entity is valid
                if composite.is_valid(text):
                    span = Span(entity=composite, text=text, tokens=tokens)
                    composite_spans.append(span)

        # keep unique composite spans
        composite_spans = self.filter_composite_spans(composite_spans)

        return composite_spans

    @classmethod
    def data_from_subspans(cls, first_span_offset, pattern, spans):
        # identify fields using offsets, attaching subspans
        data = {}
        subspans = []
        subspan_keys = set()
        span_offsets = set()

        for field_offset, field in enumerate(pattern.composite_fields):
            if field is not None:
                span_offset = first_span_offset + field_offset
                span_offsets.add(span_offset)
                subspan = spans[span_offset]
                data[field] = subspan.entity
                subspans.append(subspan)
                subspan_keys.add(subspan.entity_key)

        # add subspans for spans with same entity keys
        # e.g. acronyms such as Comma-Separated Values (CSV)
        for check_offset in range(first_span_offset, max(span_offsets)):
            if check_offset not in span_offsets:
                subspan = spans[check_offset]
                if subspan.entity_key in subspan_keys:
                    subspans.append(subspan)

        # sort subspans by offset
        subspans = sorted(subspans, key=lambda ss: ss.offset)

        return data, subspans

    def find_patterns(
        self, comp_label: str, spans: List[Span], offset: int
    ) -> List[Pattern]:
        ok = True

        last_offset = offset
        keys_by_last_offset = {}

        while ok and last_offset < len(spans):
            last_offset += 1
            subspans = spans[offset:last_offset]
            key = self.create_pattern_key(subspans)
            ok = self.graph.is_pattern_prefix(self.pipeline, comp_label, key)
            if ok:
                keys_by_last_offset[last_offset] = key

        patterns = []
        while last_offset > offset:
            key = keys_by_last_offset.get(last_offset)
            if key:
                patterns = self.graph.get_patterns(
                    self.pipeline, comp_label, key
                )
                if patterns:
                    break
            last_offset -= 1

        return patterns

    def get_token(self, token_offset: int):
        return self.doc.tokens[token_offset].token

    def create_pattern_key(self, spans: Iterator[Span]) -> str:
        spans = list(spans)
        last_span_offset = None
        pattern: List[str] = []
        keys_by_labels = {}

        for span in spans:
            if last_span_offset is not None:
                token_offset = last_span_offset + 1

                while token_offset < span.offset:
                    token = self.get_token(token_offset=token_offset)
                    pattern.append(token)
                    token_offset += 1

            keys_map = keys_by_labels.setdefault(span.label, {})
            index = keys_map.setdefault(span.entity_key, len(keys_map))
            pattern_key = f"{span.label}_{index}"

            pattern.append(pattern_key)
            last_span_offset = span.last_offset

        return " ".join(pattern)

    @classmethod
    def keep_spans(cls, labels: Set[str], spans: Iterator[Span]) -> List[Span]:
        """ Keep unique spans for a given set of labels, sort by offset. """
        spans = filter(lambda sp: sp.label in labels, spans)
        spans = cls.dedupe_sort_spans(spans)
        return spans

    @classmethod
    def dedupe_sort_spans(cls, spans: Iterator[Span]) -> List[Span]:
        spans = DedupeByLabelOffset(None).filter(spans)
        spans = sorted(spans, key=lambda sp: sp.offset)
        return spans

    # noinspection PyUnresolvedReferences
    @classmethod
    def filter_composite_spans(cls, composite_spans: List[Span]) -> List[Span]:
        composite_spans = cls.remove_fully_overlapped(composite_spans)

        # do counts for each token
        offset_counts = Counter()
        for span in composite_spans:
            for subspan in span.entity.subspans:
                offset_counts[subspan.offset] += 1

        keep_composite_spans = []

        for span in composite_spans:
            for subspan in span.entity.subspans:
                if offset_counts[subspan.offset] == 1:
                    keep_composite_spans.append(span)
                    break

        return keep_composite_spans

    @classmethod
    def remove_fully_overlapped(cls, composite_spans):
        # sort by longest first (start offset second)
        composite_spans = sorted(
            composite_spans, key=lambda s: (-len(s.tokens), s.offset)
        )

        # remove composites whose subspans are a complete subset of another
        seen_offsets = []
        keep_composites = []
        for span in composite_spans:
            is_ok = True
            subspan_offsets = span.entity.subspan_offsets()
            for seen_set in seen_offsets:
                if subspan_offsets.issubset(seen_set):
                    is_ok = False
                    break

            if is_ok:
                keep_composites.append(span)
                seen_offsets.append(subspan_offsets)

        return keep_composites


class TokComposer(DefaultComposer):
    """ Replace tokens with constant 'tok'. """

    def get_token(self, token_offset: int):
        return "tok"
