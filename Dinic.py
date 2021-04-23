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
        if v == self.sink or not flow:
            return flow
        for i in range(self.first_edge[v], len(self.cap)):
            # если вершина находится в следующем слое
            if self.distances[i] == self.distances[v] + 1:
                add = self.dfs(i, min(flow, self.cap[v][i] - self.flow[v][i]))
                if add != 0:
                    # пускаем поток по ребру
                    self.flow[v][i] += add
                    self.flow[i][v] -= add
                    return add
            # Если по данному ребру не строится блокирующий путь - исключаем из рассмотрения
            self.first_edge[v] += 1
        return 0

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
        else:
            # нахождение разреза
            cut = list()
            visited = [i for i in range(len(self.distances)) if self.distances[i] != float('Inf')]
            for vert in visited:
                for i in range(len(self.cap)):
                    if self.cap[vert][i] > 0 and self.distances[i] == float('Inf'):
                        cut.append((vert, i))

        return maxFlow, cut
