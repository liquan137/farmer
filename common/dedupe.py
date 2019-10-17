class Dedupe:
    def __init__(self):
        self.data = None

    def dedupe(self, items, key=None):
        seen = set()
        for item in items:
            val = item if key is None else key(item)
            if val not in seen:
                yield item
                seen.add(val)

