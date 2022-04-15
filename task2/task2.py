from collections import namedtuple
from enum import Enum

Parts = namedtuple('Parts', ['white_part', 'black_part'])


class Colors(Enum):
    COLORLESS = -1
    WHITE = 0
    BLACK = 1


class ColoredVertex:
    def __init__(self, name: int, color=Colors.COLORLESS):
        self.name = name
        self.color = color

    def __str__(self):
        return f'{self.name} - {self.color}'


def read_input() -> dict[int, list[ColoredVertex]]:
    """
    Читает файл с входными данными.
    Возвращает граф в виде списков смежностей.
    """
    graph = dict()
    with open('in.txt', 'r') as file:
        N = int(file.readline())
        vertexes = generate_vertexes(N)
        for i in range(1, N + 1):
            graph[i] = list(
                    map(
                            lambda name: vertexes[name],
                            map(int, file.readline().split()[:-1])))
    return graph


def generate_vertexes(count: int) -> dict[int, ColoredVertex]:
    """
    Создает указанное количество вершин без цвета
    и возвращает их в виде словаря:
    <имя вершины: int> -> <вершина: ColoredVertex>
    """
    result = dict()
    for name in range(1, count + 1):
        result[name] = ColoredVertex(name)
    return result


def is_graph_bipartite(
        graph: dict[int, list[ColoredVertex]],
        vertex: ColoredVertex,
        color: Colors) -> bool:
    """
    Проверяет двудольность графа,
    раскрашивая его в два цвета
    """
    vertex.color = color
    opposite_color = Colors.WHITE if color == Colors.BLACK else Colors.BLACK
    for neighbour in graph[vertex.name]:
        if neighbour.color == Colors.COLORLESS:
            is_graph_bipartite(graph, neighbour, opposite_color)
        elif neighbour.color == color:
            return False
    return True


def graph_into_two_parts(graph: dict[int, list[ColoredVertex]]) -> Parts:
    """
    Разделяет граф на две доли по цветам
    Возвращает эти доли в виде кортежа
    """
    white_part = set()
    black_part = set()
    for neighbours in graph.values():
        for neighbour in neighbours:
            if neighbour.color == Colors.WHITE:
                white_part.add(neighbour.name)
            else:
                black_part.add(neighbour.name)
    return Parts(sorted(white_part), sorted(black_part))


def write_result(result: bool, parts: Parts = None) -> None:
    """Записывает результат работы программы в выходной файл"""
    with open('out.txt', 'w') as file:
        if not result:
            file.write('N\n')
        else:
            file.write('Y\n')
            if parts is not None:
                sorted_parts = sorted(parts)
                file.write(' '.join(map(str, sorted_parts[0])) + ' 0\n')
                file.write(' '.join(map(str, sorted_parts[1])) + '\n')


def main() -> None:
    graph = read_input()
    if len(graph.keys()) == 0:
        write_result(True)
    elif is_graph_bipartite(graph, graph[1][0], Colors.WHITE):
        write_result(True, graph_into_two_parts(graph))
    else:
        write_result(False)


if __name__ == '__main__':
    main()
