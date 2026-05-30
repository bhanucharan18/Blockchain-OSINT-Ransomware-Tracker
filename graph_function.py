import networkx as nx


class BlockchainTracker:
    def __init__(self, trail, source, target):
        self.trail = trail
        self.source = source
        self.target = target
        self.G = nx.DiGraph()
        self.path = []
        self.hops = 0
        self.build()
        self.trace()

    def build(self):
        for src, dsts in self.trail.items():
            for dst, amt in dsts:
                self.G.add_edge(src, dst, amount=amt)

    def trace(self):
        try:
            self.path = nx.shortest_path(self.G, self.source, self.target)
            self.hops = len(self.path) - 1
        except:
            self.path = []

    def metrics(self):
        return {
            "path": self.path,
            "hops": self.hops,
            "last_traced":
                self.path[-2] if len(self.path) > 1 else self.source
        }