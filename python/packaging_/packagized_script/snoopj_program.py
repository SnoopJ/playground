import appdirs


# NOTE:we define this in a function so we can also call it from a generated
# entrypoint when this package has been installed
def main():
    print("Hello from the sample script")
    print(f"{appdirs.user_data_dir() = }")


if __name__ == "__main__":
    main()
