N = int(input())
numbers = input().split()
mult = int(numbers[0])
for i in range(1, N):
    mult &= int(numbers[i])
ones_count = format(mult, 'b').count('1')
print(2 ** ones_count)
