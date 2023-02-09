def gen(n):
    for i in range(n):
        yield i






n = 10
iter = gen(10)


for i in range(n):
    print(next(iter))
