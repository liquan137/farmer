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

# 示例
# list(dedupe([random.randint(0, 100) for k in range(1000)]))
