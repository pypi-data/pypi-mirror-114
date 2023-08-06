from typing import Set, List
from pathlib import Path

from dawg import CompletionDAWG

from entitykb import create_index, Pattern

SEP = "\1"
LBL = "\2"


class PatternIndex(object):
    def __init__(self, root: Path):
        self.dawg_path = root / "patterns.dawg"
        self.cache = create_index(str(root / "patterns"))
        self.dawg: CompletionDAWG = self._load_dawg()
        self.labels_by_pipeline = {}

    def __len__(self) -> int:
        return len(self.cache)

    def __contains__(self, pattern: Pattern) -> bool:
        return self.cache.__contains__(pattern.key)

    def __getitem__(self, key) -> List[Pattern]:
        patterns = self.cache.get(key)
        return [Pattern(**p) for p in patterns or []]

    def save(self, pattern: Pattern):
        full_key = SEP.join((pattern.pipeline, pattern.label, pattern.key))
        current = self.cache.setdefault(full_key, [])
        current = set([Pattern(**d) for d in current])
        current.add(pattern)
        self.cache[full_key] = current

    def reload(self):
        self.dawg = self._load_dawg()
        self.labels_by_pipeline = {}

    def reindex(self):
        self.dawg = self._create_dawg()
        self.dawg.save(self.dawg_path)
        self.labels_by_pipeline = {}

    def clear(self):
        self.cache.clear()
        self.reindex()
        self.labels_by_pipeline = {}

    def is_prefix(self, pipeline, label, prefix):
        full_prefix = SEP.join((pipeline, label, prefix))
        return self.dawg.has_keys_with_prefix(full_prefix)

    def get(self, pipeline, label, key) -> List[Pattern]:
        full_key = SEP.join((pipeline, label, key))
        return self[full_key]

    def get_labels(self, pipeline: str) -> Set[str]:
        labels = self.labels_by_pipeline.setdefault(pipeline, None)
        if labels is None:
            labels = set()
            for key in self.dawg.iterkeys(SEP.join((pipeline, ""))):
                labels.add(key.split(SEP)[1])
        return labels

    # private methods

    def _load_dawg(self):
        if self.dawg_path.is_file():
            return CompletionDAWG().load(str(self.dawg_path))
        return CompletionDAWG([])

    def _create_dawg(self) -> CompletionDAWG:
        return CompletionDAWG(self.cache.keys())
