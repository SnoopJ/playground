from functools import partial


def transform(datum, a, b):
    return datum*a + b

try:
    result = transform(a=1, b=2)
    print(f"Result of transform(a=1, b=2) is {result}")
except TypeError as exc:
    print("Calling transform(a=1, b=2) failed!")

# transform_ab is a new function, ROUGHLY equivalent to:
#     def transform_ab(datum):
#         return transform(datum, 1, 2)
transform_ab = partial(transform, a=1, b=2)

result = transform_ab(42)
print(f"Result of transform_ab(42) is {result}")
