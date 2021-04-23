class Graph:
    def __init__(self, capacity, source, sink):
        import copy
        self.cap = copy.deepcopy(capacity)
        self.source = source
        self.sink = sink
        self.flow = list()
        for i in range(len(self.cap)):
            self.flow.append([0 for i in range(len(self.cap))])
        self.distances = list()

    def bfs(self):
        import queue
        q = queue.Queue()
        self.distances = [float('Inf') for i in range(len(self.cap))]
        self.distances[self.source] = 0
        q.put(self.source)
        while not q.empty():
            cur = q.get()
            for v in range(len(self.cap[cur])):
                if self.flow[cur][v] < self.cap[cur][v] and self.distances[v] == float('Inf'):
                    # отмечаем достижимые и непосещенные вершины из источника расстоянием до него
                    self.distances[v] = self.distances[cur] + 1
                    q.put(v)
        return self.distances[self.sink] != float('Inf')
