class Graph:
    """
    Класс представления сети для нахождения максимального потока
    Поля:
        cap - матрица пропускных способностей (двумерный массив)
        source - номер вершины - источника (int)
        sink - номер вершины - стока (int)
        flow - матрица текущего потока в сети (двумерный массив)
        distances - список расстояний от истока (массив)
        first_edge - список первых неудаленный ребер (массив)
    Вершины нумеруются с нуля
    """
    def __init__(self, capacity, source, sink):
        """
        :param capacity: матрица пропускных способностей
        :param source: индекс вершины - источника
        :param sink: индекс вершины - стока
        """
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
        """
        Поиск в ширину с выделением слоев (distances - расстояния от источника)
        :return: bool - возвращается истина, если сток достижим из источника
        """
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
        """
        Поиск в глубину блокирующего пути
        :param v: вершина из которой строится блокирующий путь
        :param flow: минимальная пропускная способность сети в отсавшемся пути
        :return: величина потока по локирующему пути
        """
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

    def dinic(self, cut):
        """
        Реализация алгоритма Диница
        :param cut: булево значение True - если нужно находить разрез
        :return: величина максимального потока в сети, список ребер минимального разреза
        """
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
            if not cut:
                return maxFlow, None
            cut = list()
            visited = [i for i in range(len(self.distances)) if self.distances[i] != float('Inf')]
            for vert in visited:
                for i in range(len(self.cap)):
                    if self.cap[vert][i] > 0 and self.distances[i] == float('Inf'):
                        cut.append((vert, i))

        return maxFlow, cut


def read_capacity(path):
    """
    Составление матрицы пропускных способностей
    :param path: путь до файла
    :return: двумерный массив - матрица пропускных способностей
    """
    with open(path, 'r') as file:
        graph_info = file.read()
    graph_info = graph_info.split('\n')
    size, edges = map(int, graph_info[0].split(' '))
    capacity = list([[0 for i in range(size)] for i in range(size)])
    for i in range(1, edges + 1):
        edge = graph_info[i].split(' ')
        # здесь float для общности
        capacity[int(edge[0]) - 1][int(edge[1]) - 1] = float(edge[2])
    return capacity
