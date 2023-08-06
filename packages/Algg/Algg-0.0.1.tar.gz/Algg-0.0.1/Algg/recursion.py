def get_fib(num):
    """ 求出长度为 num 的 fib 数列 """
    fib_list = []
    for i in range(num):
        if len(fib_list) < 2:
            fib_list.append(1)
            continue
        fib_list.append(fib_list[-1] + fib_list[-2])
    return fib_list


def fib_recur(n):
    """ 求出 fib 数列的第 n 个数 """
    fib_ls = []
    for i in range(n):
        if len(fib_ls) < 2:
            fib_ls.append(1)
            continue
        fib_ls.append(fib_ls[-1] + fib_ls[-2])
    # print(fib_ls)
    return fib_ls[n - 1]


def hanoi(n, a, b, c):
    """ 汉诺塔简单实现 """
    if n > 0:
        hanoi(n - 1, a, c, b)
        print('moving from %s to %s' % (a, c))
        hanoi(n - 1, b, a, c)
