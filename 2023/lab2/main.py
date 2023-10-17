from collections import deque
from enum import Enum

INF_POS = float('+inf')


def read_input(path: str) -> tuple[int, list[list[int]], int, int]:
    with open(path, 'r') as file:
        N = int(file.readline())
        capacities = list()
        for _ in range(N):
            capacities.append(list(map(int, file.readline().split(' '))))
        s = int(file.readline())
        t = int(file.readline())
    return N, capacities, s, t


def write_output(path: str, flow_network: list[list[int]], max_flow_value: int) -> None:
    with open(path, 'w') as file:
        for line in flow_network:
            file.write(' '.join(map(str, line)) + '\n')
        file.write(str(max_flow_value) + '\n')


class MarkingMethod(Enum):
    FORWARD = +1  # помечивание с помощью ПРЯМОГО ребра
    BACKWARD = -1  # помечивание с помощью ОБРАТНОГО ребра


class FordFulkerson:
    def __init__(self, N: int, capacities: list[list[int]], s: int, t: int) -> None:
        self._N = N
        self._capacities = capacities
        self._s = s
        self._t = t
        self._flow_network = [[0] * N for _ in range(N)]
        self._max_flow_value = 0

        self._main()

    @property
    def flow_network(self) -> list[list[int]]:
        return self._flow_network

    @property
    def max_flow_value(self) -> int:
        return self._max_flow_value

    def _main(self) -> None:
        while True:
            delta, prev, method = self._mark()
            if delta[self._t] == INF_POS:
                break  # нет дополняющей цепи => построили максимальный поток
            self._max_flow_value += delta[self._t]
            w = self._t
            while w != self._s:
                v = prev[w]
                if method[w] == MarkingMethod.FORWARD:
                    self._flow_network[v][w] += delta[self._t]
                else:
                    self._flow_network[w][v] -= delta[self._t]
                w = v

    def _mark(self) -> tuple[dict[int, int], dict[int, int], dict[int, MarkingMethod]]:
        V = set(range(self._N))
        delta = {v: INF_POS for v in range(self._N)}
        prev = {v: None for v in range(self._N)}
        method = {v: None for v in range(self._N)}
        que = deque()
        que.append(self._s)

        while delta[self._t] == INF_POS and len(que):
            v = que.popleft()
            for w in V.difference({self._s}):
                if delta[w] != INF_POS:
                    continue
                if self._flow_network[v][w] < self._capacities[v][w]:  # c - f > 0
                    delta[w] = min(delta[v], self._capacities[v][w] - self._flow_network[v][w])
                    que.append(w)
                    prev[w] = v
                    method[w] = MarkingMethod.FORWARD
                if self._flow_network[w][v] > 0:  # f > 0
                    delta[w] = min(delta[v], self._flow_network[w][v])
                    que.append(w)
                    prev[w] = v
                    method[w] = MarkingMethod.BACKWARD
        return delta, prev, method


def main():
    N, capacities, s, t = read_input('in.txt')
    ford_fulkerson = FordFulkerson(N, capacities, s - 1, t - 1)
    write_output('out.txt', ford_fulkerson.flow_network, ford_fulkerson.max_flow_value)


if __name__ == '__main__':
    main()
