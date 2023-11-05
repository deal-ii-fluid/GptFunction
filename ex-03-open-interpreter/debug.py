def fibonacci(n):
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]

    sequence = [0, 1]

    for i in range(2, n):
        next_val = sequence[i - 1] + sequence[i - 2]
        sequence.append(next_val)

    return sequence

integer_input = int(input("请输入一个整数："))
print(fibonacci(10))
print(integer_input)
print("hello")

