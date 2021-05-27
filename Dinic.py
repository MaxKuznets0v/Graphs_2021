import networkx as nx


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
    def __init__(self, network, source, sink):
        """
        :param network: исходная сеть
        :param source: индекс вершины - источника
        :param sink: индекс вершины - стока
        """
        self.net = network
        self.source = source
        self.sink = sink
        self.flow = nx.DiGraph()
        self.flow.add_nodes_from(self.net.nodes)
        rev = [(list(edge)[1], list(edge)[0], 0) for edge in self.net.edges]
        edges = [(*edge, 0) for edge in self.net.edges]
        self.flow.add_weighted_edges_from(rev + edges)
        self.distances = list()
        self.first_edge = list()

    def bfs(self):
        """
        Поиск в ширину с выделением слоев (distances - расстояния от источника)
        :return: bool - возвращается истина, если сток достижим из источника
        """
        import queue
        q = queue.Queue()
        self.distances = [float('Inf') for i in range(len(self.net))]
        self.distances[self.source] = 0
        q.put(self.source)
        while not q.empty():
            cur = q.get()
            print("BFS vertex:", cur)
            for v in list(self.flow[cur].keys()):
                try:
                    capacity = self.net[cur][v]['weight']
                except KeyError:
                    capacity = 0
                if self.flow[cur][v]['weight'] < capacity and self.distances[v] == float('Inf'):
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
        for i in range(self.first_edge[v], len(self.flow[v])):
            # если вершина находится в следующем слое
            ind = list(self.flow[v].keys())[i]
            if self.distances[ind] == self.distances[v] + 1:
                try:
                    capacity = self.net[v][ind]['weight']
                except KeyError:
                    capacity = 0
                add = self.dfs(ind, min(flow, capacity - self.flow[v][ind]['weight']))
                if add != 0:
                    # пускаем поток по ребру
                    self.flow[v][ind]['weight'] += add
                    self.flow[ind][v]['weight'] -= add
                    return add
            # Если по данному ребру не строится блокирующий путь - исключаем из рассмотрения
            self.first_edge[v] += 1
        return 0

    def dinic(self, cut=True):
        """
        Реализация алгоритма Диница
        :param cut: булево значение (True - если нужно находить разрез)
        :return: величина максимального потока в сети, список ребер минимального разреза
        """
        maxFlow = 0
        # пока сток достижим в остаточной сети
        while self.bfs():
            self.first_edge = [0 for i in range(len(self.net))]
            flow = self.dfs(self.source, float('Inf'))
            # пока находятся блокирующие пути
            while flow != 0:
                maxFlow += flow
                flow = self.dfs(self.source, float('Inf'))
                print(self.first_edge[self.source])
        else:
            # нахождение разреза
            if not cut:
                return maxFlow, None
            cut = list()
            visited = [i for i in range(len(self.distances)) if self.distances[i] != float('Inf')]
            for vert in visited:
                for v in list(self.net[vert].keys()):
                    if self.net[vert][v]['weight'] > 0 and self.distances[v] == float('Inf'):
                        cut.append((vert, v))

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
    network = nx.DiGraph()

    for i in range(1, edges + 1):
        edge = graph_info[i].split(' ')
        network.add_node(int(edge[0]) - 1)
        network.add_node(int(edge[1]) - 1)
        # здесь float для общности
        network.add_edge(int(edge[0]) - 1, int(edge[1]) - 1, weight=float(edge[2]))
    return network
