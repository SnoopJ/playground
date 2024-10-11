class RealClass:
    def __init__(self, data=0):
        self.data = data

    def func(self):
        print(f"Inside real func method:\n\t{self = },\n\t{self.data = }")

    def some_stateful_activity(self):
        self.data += 1
        print(f"Performing some stateful activity, {self.data = }")


def main():
    instance = RealClass()
    for _ in range(3):
        instance.func()
        instance.some_stateful_activity()


if __name__ == "__main__":
    main()
