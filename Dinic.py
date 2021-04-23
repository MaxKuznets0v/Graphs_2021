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
        self.first_edge = list()

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

    def dfs(self, v, flow):
        pass

    def dinic(self):
        maxFlow = 0
        # пока сток достижим в остаточной сети
        while self.bfs():
            self.first_edge = [0 for i in range(len(self.cap))]
            flow = self.dfs(self.source, float('Inf'))
            # пока находятся блокирующие пути
            while flow != 0:
                maxFlow += flow
                flow = self.dfs(self.source, float('Inf'))

        return maxFlow
