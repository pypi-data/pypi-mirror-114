import csv
import pathlib

from entitykb import KB, CompositeEntity, Pattern
from .cli import cli


@cli.register_reader("patterns")
def patterns_reader(file_obj, kb: KB):
    label = pathlib.Path(file_obj.name).stem.upper()
    assert label, f"Invalid Label: {label}"

    klass = CompositeEntity.get_subclass(label=label)
    assert klass, f"No Class for Label: {label}"

    relevant_labels = klass.relevant_labels()
    reader = csv.DictReader(file_obj, dialect="excel-tab")
    pipelines = [pl for pl in kb.pipelines.values() if pl.has_composer]

    for row in reader:
        text = row.pop("text")
        row_invert = dict((v, k) for k, v in row.items() if v)

        for pipeline in pipelines:
            copy = row_invert.copy()
            doc = pipeline.extractor.extract_doc(text=text, labels=[label])
            composer = pipeline.make_composer(doc=doc)
            keep_spans = composer.keep_spans(relevant_labels, doc.spans)
            fields = tuple((copy.pop(sp.text, None) for sp in keep_spans))
            if len(copy) == 0:
                key = composer.create_pattern_key(keep_spans)
                yield Pattern(
                    pipeline=pipeline.name,
                    label=label,
                    key=key,
                    composite_fields=fields,
                )
