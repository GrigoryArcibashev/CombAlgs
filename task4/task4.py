from collections import namedtuple

NO_PATH = '32767'

Edge = namedtuple('Edge', ['v1', 'v2', 'c'])
DISTANCE: dict[int, int] = dict()
PROJECTION: dict[int, int] = dict()


def read_graph() -> list[list[int]]:
    """
    Считывает матрицу весов из файла

    :return: список списков - представление графа в виде матрицы весов
    """
    with open('in.txt', 'r') as file:
        N = int(file.readline())
        graph = list()
        func = lambda x: int(x) if x != NO_PATH else float('+inf')
        for i in range(N):
            line = list(map(func, file.readline().split()))
            graph.append(line)
    return graph


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
    for vert in V.difference(F):
        if DISTANCE[vert] < min_dist:
            vert_V = vert
            vert_F = PROJECTION[vert]
            min_dist = DISTANCE[vert]
    return Edge(vert_V, vert_F, min_dist)


def DJP(graph: list[list[int]]) -> set[Edge]:
    """
    Алгоритм ЯПД

    :param graph: граф в виде матрицы весов.
    :return: минимальный остов графа в виде множества ребер остова
    """
    v = 0  # стартовая вершина
    vertex_count = len(graph)
    V: set[int] = {i for i in range(vertex_count)}
    F: set[int] = {v}
    T: set[Edge] = set()
    for w in V.difference(F):
        PROJECTION[w] = v
        DISTANCE[w] = graph[w][v]
    while len(T) < vertex_count - 1:
        edge = MIN(V, F)
        w = edge.v1
        F.add(w)
        T.add(edge)
        for v in V.difference(F):
            if graph[v][w] < DISTANCE[v]:
                PROJECTION[v] = w
                DISTANCE[v] = graph[v][w]
    return T


def make_output(skeleton: set[Edge]) -> None:
    """
    Записывает остов в выходной файл
    
    :param skeleton: остов в виде множества его ребер
    """
    T = skeleton
    raw_output: list[list[str]] = [list() for _ in range(len(T) + 1)]
    for edge in T:
        raw_output[edge.v1].append(str(edge.v2 + 1))
        raw_output[edge.v2].append(str(edge.v1 + 1))
    with open('out.txt', 'w') as file:
        for line in raw_output:
            wr_line = ' '.join(sorted(line)) + ' 0\n'
            file.write(wr_line)
        file.write(str(sum((e.c for e in T))) + '\n')


def main() -> None:
    make_output(DJP(read_graph()))


if __name__ == '__main__':
    main()
