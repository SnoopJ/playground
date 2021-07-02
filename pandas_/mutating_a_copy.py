import pandas as pd

df = pd.DataFrame(
    {
        "ID": [1000, 1001, 1005, 1337, 1578],
        "first_name": ["Jason", "Molly", "Tina", "Jake", "Amy"],
        "last_name": ["Miller", "Jacobson", "Ali", "Milner", "Cooze"],
        "age": [42, 52, 36, 24, 73],
        "preTestScore": [4, 24, 31, 2, 3],
        "postTestScore": [25, 94, 57, 62, 70],
    }
)

print("Original DataFrame (df):\n------------------")
print(df)

id_copy = df["ID"]
id_view = df.loc[:, "ID"]

id_copy[:] = -1
print("Mutating copy")
print("copy:\n----")
print(id_copy)
print("view:\n----")
print(id_view)
print("df:\n----")
print(df)
