"""Generate temporary names"""

from collections import defaultdict


class TempNameGenerator:
    _instance = None
    temp_count = 0
    prefix_counts: dict[str, int] = defaultdict(lambda: 0)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def temp_name(self, prefix: str) -> str:
        count = self.prefix_counts[prefix]
        self.prefix_counts[prefix] += 1
        return f"__{prefix}_{count}"
