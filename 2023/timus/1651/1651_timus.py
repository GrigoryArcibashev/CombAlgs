def next_nums(n):
    """
    :param n: int : количество вершин в списке
    :return: генератор, возвращающий вершины из stdin
    """
    k = 0
    while k < n:
        inp = list(map(int, input().strip().split()))
        k += len(inp)
        for num in inp:
            yield num


def build_chain(n):
    """
    :param n: int : количество вершин в списке
    :return: список вершин (list[int]) и оптимальная цепочка (dict[int])
    """
    gen = next_nums(n)
    prev_num = 0

    nums = list()
    dist = {prev_num: 0}
    prevs = {}
    pos = {}

    for i in range(1, n + 1):
        num = next(gen)
        nums.append(num)
        if num not in dist or dist[prev_num] + 1 <= dist[num]:
            prevs[i] = i - 1
            dist[num] = dist[prev_num] + 1
            pos[num] = i
        else:
            prevs[i] = prevs[pos[num]]
        prev_num = num
    return nums, prevs


def print_result(nums, prevs):
    """
    :param nums: list[int] : список вершин
    :param prevs: dict[int] : оптимальная цепочка
    :return:
    """
    result = list()
    i = len(nums)
    while i > 0:
        result.append(nums[i - 1])
        i = prevs[i]
    print(*reversed(result))


def main():
    print_result(*build_chain(int(input())))


if __name__ == '__main__':
    main()
