from cffiwhat._cffiwhat_c import lib  # import the compiled library


def main():
    print("hello from python")

    lib.cffihello()


if __name__ == '__main__':
    main()
