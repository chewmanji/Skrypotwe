from functools import cache

def make_generator(fun: callable):
    def generator():
        i = 1
        while True:
            yield fun(i)
            i += 1

    return generator


def fibonacci_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def fibonacci_recursive(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def make_generator_mem(fun: callable):
    @cache
    def mem_fun():
        return fun.__name__

    return make_generator(mem_fun())


# gen1 = make_generator(fibonacci_iterative)()
# gen2 = make_generator(lambda x: x * 3)()
# gen3 = make_generator(lambda x: x**2 + x * 4)()
# for _ in range(10):
#     print("gen1", next(gen1))

# for _ in range(5):
#     print("gen2", next(gen2))

# for _ in range(10):
#     print("gen3", next(gen3))

gen = make_generator(fibonacci_recursive)()

for _ in range(30):
    print(next(gen))

gen = make_generator(fibonacci_recursive)()

for _ in range(30):
    print(next(gen))

dicta = globals()
print(dicta["fibbonacci_recursive"])
