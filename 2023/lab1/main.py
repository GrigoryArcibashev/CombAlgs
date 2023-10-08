from collections import namedtuple
from typing import Union

END = 32767

Edge = namedtuple('Edge', ['v1', 'v2', 'c'])
DISTANCE: dict[int, int] = dict()
PROJECTION: dict[int, int] = dict()


def read_graph() -> tuple[list[int], int]:
    """
    Считывает матрицу весов из файла

    :return: массив смежности графа и количество вершин
    """
    with open('in.txt', 'r') as file:
        file.readline()  # ненужная информация
        graph = list()
        while True:
            line = list(map(int, file.readline().split()))
            graph += line
            if line[-1] == END:
                break
    return graph, graph[0] - 2


def MIN(V: set[int], F: set[int]) -> Edge:
    """
    Ищет ближайшую к остову вершину

    :param V: множество вершин графа.
    :param F: множество вершин остова.
    :return: ребро, где v1 - искомая вершина в V, v2 - проекция v1 на F.
    """
    vert_V = None
    vert_F = None
    min_dist = float('+inf')
    for v in V.difference(F):
        if DISTANCE[v] < min_dist:
            vert_V = v
            vert_F = PROJECTION[v]
            min_dist = DISTANCE[v]
    return Edge(vert_V, vert_F, min_dist)


def DJP(graph: list[int], count: int) -> set[Edge]:
    """
    Алгоритм ЯПД

    :param graph: граф в виде массива смежности
    :param count: количество вершин
    :return: минимальный остов графа в виде множества ребер остова
    """
    v = 0  # стартовая вершина
    V: set[int] = {i for i in range(count)}  # множество всех вершин
    F: set[int] = {v}  # множество вершин остова T
    T: set[Edge] = set()  # мин остов
    for w in V.difference(F):
        PROJECTION[w] = v
        DISTANCE[w] = get_distance(graph, v, w)
    while len(T) < count - 1:
        edge = MIN(V, F)
        w = edge.v1
        F.add(w)
        T.add(edge)
        for v in V.difference(F):
            distance_to_w = get_distance(graph, w, v)
            if distance_to_w < DISTANCE[v]:
                PROJECTION[v] = w
                DISTANCE[v] = distance_to_w
    return T


def get_distance(graph: list[int], v1: int, v2: int) -> Union[int, float]:
    """
    Возвращает расстояние между вершинами

    :param graph: граф, заданный массивом смежности
    :param v1: первая вершина
    :param v2: вторая вершина
    :return: расстояние между v1 и v2 (float(+inf), если связи между вершинами нет)
    """
    # в графе нумерация вершин начинается с 1, а передаваемые вершины - с 0 !!!
    start = graph[v1] - 1
    end = graph[v1 + 1] - 1
    neighbours = graph[start:end]
    for i in range(len(neighbours)):
        if i % 2 == 0 and neighbours[i] - 1 == v2:
            return neighbours[i + 1]
    return float('+inf')


def make_output(T: set[Edge], count: int) -> None:
    """
    Записывает остов в выходной файл

    :param T: остов в виде множества его ребер
    :param count: количество вершин
    """
    weight = sum((e.c for e in T))
    result = {i: list() for i in range(count)}
    for edge in T:
        v1 = edge.v1
        v2 = edge.v2
        result[v1].append(v2)
        result[v2].append(v1)
    with open('out.txt', 'w') as file:
        for key in range(count):
            file.write(' '.join(
                map(
                    lambda v: str(v + 1),
                    sorted(result[key])
                )
            ) + ' 0\n')
        file.write(str(weight) + '\n')


def main() -> None:
    graph, count = read_graph()
    make_output(DJP(graph, count), count)


if __name__ == '__main__':
    main()
