import collections
import enum

InputData = collections.namedtuple(
        'InputData',
        ['maze', 'row_count', 'column_count', 'start', 'target'])
Point = collections.namedtuple('Point', ['x', 'y'])


class State(enum.Enum):
    EMPTY = 0
    WALL = 1


class LinkedList:
    """Односвязный список"""

    def __init__(self, value, previous=None):
        """
        value: object- значение данного элемента списка
        previous: LinkedList - предыдущий элемент списка
        """
        self.value = value
        self.previous = previous


def get_tuple_of_int_from(string: str) -> tuple:
    """Переводит строку из чисел в кортеж из чисел"""
    return tuple(map(int, string.strip().split()))


def get_line_as_states(line: tuple) -> tuple:
    """Переводит кортеж чисел из 0/1 в кортеж из State.EMPTY/State.WALL"""
    return tuple(map(lambda n: State.EMPTY if n == 0 else State.WALL, line))


def get_input_data() -> InputData:
    """
    Возвращает все входные данные (количество строк в лабиринте,
    количество столбцов в лабиринте, лабиринт, координаты источника и цели)
    как именованный кортеж
    """
    maze = list()
    with open('in.txt', 'r') as input_file:
        row_count = int(input_file.readline())  # N
        column_count = int(input_file.readline())  # M
        for _ in range(row_count):
            maze.append(
                    get_line_as_states(
                            get_tuple_of_int_from(input_file.readline())))
        point = get_tuple_of_int_from(input_file.readline())
        start = Point(point[0] - 1, point[1] - 1)
        point = get_tuple_of_int_from(input_file.readline())
        target = Point(point[0] - 1, point[1] - 1)
    return InputData(maze, row_count, column_count, start, target)


def is_in_boundaries(row_count: int, column_count: int, point: Point) -> bool:
    """Возвращает True если точка находится в лабиринте, иначе False"""
    return (0 <= point.x < row_count) and (0 <= point.y < column_count)


def is_point_empty(maze: list, point: Point) -> bool:
    """Возвращает True если точка пуста, иначе False"""
    return maze[point.x][point.y] == State.EMPTY


def are_start_and_target_correct(inp_data: InputData) -> bool:
    """
    Возвращает True, если стартовая и целевая точки из ввода
    находятся в лабиринте они пусты, иначе False
    """
    for point in (inp_data.start, inp_data.target):
        if not (is_in_boundaries(
                inp_data.row_count, inp_data.column_count, point)
                and is_point_empty(inp_data.maze, point)):
            return False
    return True


def get_neighbours(row_count: int, column_count: int, point: Point) -> list:
    """Возвращает всех соседей точки"""
    result = list()
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        neighbour = Point(point.x + dx, point.y + dy)
        if is_in_boundaries(row_count, column_count, neighbour):
            result.append(neighbour)
    return result


def get_empty_neighbours(
        maze: list,
        row_count: int,
        column_count: int,
        point: Point) -> list:
    """Возвращает всех пустых соседей точки"""
    result = list()
    for neighbour in get_neighbours(row_count, column_count, point):
        if is_point_empty(maze, neighbour):
            result.append(neighbour)
    return result


def get_adjacency_list(inp_data: InputData) -> dict:
    """Возвращает список смежностей для всех пустых точек лабиринта"""
    adjacency_list = dict()
    for row in range(inp_data.row_count):
        for column in range(inp_data.column_count):
            point = Point(row, column)
            if is_point_empty(inp_data.maze, point):
                adjacency_list[point] = get_empty_neighbours(
                        inp_data.maze,
                        inp_data.row_count,
                        inp_data.column_count,
                        point)
    return adjacency_list


def find_path(inp_data: InputData) -> (list, None):
    """Ищет путь между указанными в вводе точками"""
    if not are_start_and_target_correct(inp_data):
        return None
    adjacency_list = get_adjacency_list(inp_data)
    queue = collections.deque()
    queue.append(LinkedList(inp_data.start))
    visited_points = set()
    visited_points.add(inp_data.start)
    while len(queue) != 0:
        path = queue.popleft()  # instance of LinkedList class
        point = path.value
        if point == inp_data.target:
            return expand_path_to_list(path)
        for next_point in adjacency_list[point]:
            if next_point not in visited_points:
                visited_points.add(next_point)
                queue.append(LinkedList(next_point, path))


def expand_path_to_list(path: LinkedList) -> list:
    """Разворачивает путь как связный список в обычный список"""
    result = collections.deque()
    while path is not None:
        result.appendleft(path.value)
        path = path.previous
    return list(result)


def write_result(path: (LinkedList, None)) -> None:
    """Записывает результат работы программы в файл out.txt"""
    with open('out.txt', 'w') as file:
        if path is None:
            file.write('N\n')
        else:
            file.write('Y\n')
            for point in path:
                file.write(f'{point.x + 1} {point.y + 1}\n')


if __name__ == '__main__':
    write_result(find_path(get_input_data()))
