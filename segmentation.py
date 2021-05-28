import numpy as np
import networkx as nx
import math
from PIL import Image
Image.LOAD_TRUNCATED_IMAGES = True
from Dinic import Graph

# параметры
sigma = 50
lambda_ = 30

# ширина, высота и количество пикселей в изображениия
width = 0
height = 0
size = 0


def fill_neighbours_list(neighbours_list):
    neighbours_list.append(0)
    for i in range(1, size + 1):
        if i == 1:  # левый верхний пиксель
            neighbours_list.append([i + 1, i + width])
        elif i == width:  # левый правый пиксель
            neighbours_list.append([i - 1, i + width])
        elif i == size - width + 1:  # левый нижний пиксель
            neighbours_list.append([i - width, i + 1])
        elif i == size:  # правый нижний пиксель
            neighbours_list.append([i - width, i - 1])
        # граничные пиксели
        elif 1 < i < width:  # верхние пиксели
            neighbours_list.append([i - 1, i + 1, i + width])
        elif (i - 1) % width == 0:  # левые пиксели
            neighbours_list.append([i - width, i + 1, i + width])
        elif i % width == 0:  # правые пиксели
            neighbours_list.append([i - width, i - 1, i + width])
        elif size - width + 1 < i < size:  # нижние пиксели
            neighbours_list.append([i - width, i - 1, i + 1])
        # внутренние пиксели
        else:
            neighbours_list.append([i - width, i - 1, i + 1, i + width])

step_histo = 16

def R_obj(p, counts_obj, counts_bkg):
    p_row = p // width - 1 if p % width == 0 else p // width # p_y
    p_col = p - width * p_row - 1 # p_x
    p_int = image[p_col, p_row]

    if counts_obj[p_int//step_histo] + counts_bkg[p_int//step_histo] == 0:
        Pr_obj = 0
    else:
        Pr_obj = counts_obj[p_int//step_histo]/(counts_obj[p_int//step_histo] + counts_bkg[p_int//step_histo])
    if Pr_obj == 0.:
        return 10e+6
    return -math.log(Pr_obj)


def R_bkg(p, counts_obj, counts_bkg):
    p_row = p // width - 1 if p % width == 0 else p // width  # p_y
    p_col = p - width * p_row - 1 # p_x
    p_int = image[p_col, p_row]

    if counts_obj[p_int//step_histo] + counts_bkg[p_int//step_histo] == 0:
        Pr_bkg = 0
    else:
        Pr_bkg = counts_bkg[p_int//step_histo] / (counts_obj[p_int//step_histo] + counts_bkg[p_int//step_histo])
    if Pr_bkg == 0.:
        return 10e+6
    return -math.log(Pr_bkg)


# !!! еще подредачить для 8 соседей
def dist(p, q):
    return 1


def B(p, q):
    p_row = p // width - 1 if p % width == 0 else p // width  # p_y
    p_col = p - width * p_row - 1 # p_x
    p_intensity = image[p_col, p_row]

    q_row = q // width - 1 if q % width == 0 else q // width  # q_y
    q_col = q - width * q_row - 1 # q_x
    q_intensity = image[q_col, q_row]

    if p_intensity <= q_intensity:
        return 1
    return math.exp(-(p_intensity - q_intensity)**2 / 2 * sigma**2) * 1 / dist(p, q)


def fill_adj_matrix(adj_matrix, adj_matrix_size, neighbours, counts_obj, counts_bkg, Obj, Bkg):
    # матрица смежности, S - 1-ая вершина, T - последняя вершина
    max_sum_B = 0
    for i in range(1, adj_matrix_size-1): # начинаем с 1, то есть с 1-ой вершины в изначальном графе
        sum_B = 0
        # зададим веса ребрам, соединяющим пиксель с соседями
        for j in neighbours[i]:
            B_ij = B(i, j)
            adj_matrix.add_edge(i, j, weight=B_ij, capacity=B_ij)
            sum_B += B_ij
        max_sum_B = sum_B if sum_B > max_sum_B else max_sum_B

    K = 1 + max_sum_B

    for i in range(1, adj_matrix_size - 1):
        # зададим веса ребрам, соединяющим с терминальными вершинами
        if i in Obj:
            adj_matrix.add_edge(0, i, weight=K, capacity=K) # ребро с истоком S
            adj_matrix.add_edge(i, adj_matrix_size - 1, weight=0,capacity=0) # ребро со стоком T
        elif i in Bkg:
            adj_matrix.add_edge(0, i, weight=0, capacity=0)
            adj_matrix.add_edge(i, adj_matrix_size - 1, weight=K, capacity=K)
        else:
            adj_matrix.add_edge(0, i, weight=lambda_ * R_bkg(i, counts_obj, counts_bkg), capacity=lambda_ * R_bkg(i, counts_obj, counts_bkg))
            adj_matrix.add_edge(i, adj_matrix_size - 1, weight=lambda_ * R_obj(i, counts_obj, counts_bkg), capacity=lambda_ * R_obj(i, counts_obj, counts_bkg))


# функция вызывается из GUI и передает имя изображения, выбранные пиксели объекта и фона
def segmentation(image_name, obj_pixels, bkg_pixels):
    global image
    global width, height, size
    # try:
    #     im = Image.open('images-320/' + image_name)
    # except FileNotFoundError:
    #     print("Файл не найден")
    im = Image.open('images-320/' + image_name)
    width = im.size[0]
    height = im.size[1]
    size = width * height
    image = im.load()

    # пользователь задает пиксели объекта (O) и фона (B)
    # значения индексов пикселей
    Obj = []
    Bkg = []
    # значения интенсивностей пикселей
    Obj_int = []
    Bkg_int = []

    for pair in obj_pixels: # pair - (x, y)
        Obj.append(pair[1] * width + pair[0] + 1)
        Obj_int.append(image[pair[0], pair[1]])
    for pair in bkg_pixels:
        Bkg.append(pair[1] * width + pair[0] + 1)
        Bkg_int.append(image[pair[0], pair[1]])

    # считаем граф ориентированным, учитываем только 4 соседних пикселя
    # список соседей для каждого пикселя
    neighbours = []
    fill_neighbours_list(neighbours)

    # гистограммы для объекта и для фона
    counts_obj, bins_obj = np.histogram(Obj_int, range(0, 257, step_histo))
    counts_bkg, bins_bkg = np.histogram(Bkg_int, range(0, 257, step_histo))

    adj_matrix_size = width * height + 2
    adj_matrix = nx.DiGraph()
    fill_adj_matrix(adj_matrix, adj_matrix_size, neighbours, counts_obj, counts_bkg, Obj, Bkg)
    # Получаем минимальный разрез с помощью алгоритма Диница поиска максимального потока
    _, reachable = Graph(adj_matrix, 0, adj_matrix_size-1).dinic(cut=True)
    # _, partition = nx.algorithms.flow.minimum_cut(adj_matrix, 0, adj_matrix_size-1)
    # reachable, non_reachable = partition

    # пиксели из множества достижимых вершин обозначим 255, остальные - 0 и выведем ч/б изображение
    image = [([0] * width) for i in range(height)]
    image = np.array(image)

    for v in reachable:
        if v != 0 and v != adj_matrix_size-1:
            v_row = v // width - 1 if v % width == 0 else v // width
            v_col = v - width * v_row - 1
            print(v_col, v_row)
            image[v_row][v_col] = 255

    im = Image.fromarray(image.astype(np.uint8))
    im.show()
    im.save("results/" + image_name)
    del adj_matrix
    del neighbours
    del image
    del Obj, Bkg, Obj_int, Bkg_int
