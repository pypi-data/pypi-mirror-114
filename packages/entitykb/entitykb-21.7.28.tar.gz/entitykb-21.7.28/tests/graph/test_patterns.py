from entitykb.graph.patterns import PatternIndex
from entitykb.models import Pattern


def test_pattern_index(root):
    index = PatternIndex(root=root)

    p1 = Pattern(
        pipeline="default",
        label="TEST",
        key="a b",
        composite_fields=["one", "two"],
    )
    index.save(p1)

    p2 = Pattern(
        pipeline="default",
        label="MORE",
        key="a c",
        composite_fields=["one", "tre"],
    )
    index.save(p2)

    index.reindex()

    assert index.is_prefix("default", "TEST", "a")
    assert index.is_prefix("default", "TEST", "a b")
    assert not index.is_prefix("default", "TEST", "a c")

    assert index.is_prefix("default", "MORE", "a")
    assert not index.is_prefix("default", "MORE", "a b")
    assert index.is_prefix("default", "MORE", "a c")

    assert index.get("default", "TEST", "a b") == [p1]
    assert index.get("default", "MORE", "a c") == [p2]
    assert index.get("default", "MORE", "a b") == []

    assert index.labels_by_pipeline == {}
    assert index.get_labels("default") == {"TEST", "MORE"}
    assert len(index.labels_by_pipeline) == 1
    assert index.get_labels("def") == set()
    assert len(index.labels_by_pipeline) == 2
