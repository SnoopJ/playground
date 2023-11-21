from tensorflow.python.autograph.pyct import inspect_utils

from libapp import Widget, outer


if __name__ == "__main__":
    for obj in [Widget, Widget.__init__, Widget.__repr__, outer]:
        print(f"Source for object: {obj}")
        src = inspect_utils.getimmediatesource(obj)
        print(src)
        print("\n---")

    print("all good :)")
