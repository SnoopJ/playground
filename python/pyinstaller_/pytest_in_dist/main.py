def add(x, y):
    return x + y


def sub(x, y):
    # this should return x - y but it's broken
    return -1


if __name__ == "__main__":
    print(f"{add(1, 1) = }")
    print(f"{sub(1, 1) = }")
