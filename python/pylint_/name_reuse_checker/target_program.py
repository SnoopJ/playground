def munge(x):
    return x+1


def simple_assignment():
    x = 42
    x = -1
    return x


def multiple_assignment():
    a, b = 42
    b = -1
    return x


def multiple_assignment_complex():
    a, (b, c), [d, e] = [1, (2, 3), [4, 5]]
    b, e = (-1, -1)
    return x


if __name__ == "__main__":
    name = 42
    name = munge(name)

    func()
