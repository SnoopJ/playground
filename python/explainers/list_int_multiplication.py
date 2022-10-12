lst = [1,2,3]

# multiplying a list (or tuple, etc.) by an int is a syntax trick to get N
# repetitions of the contents. The idea here is that e.g. `[1,2] + [1,2]`
# gives `[1,2,1,2]`, and `[1,2]*2` is the "same idea"
#
# lol = list of list
lol = [lst]*3
print(f"lol = [lst]*3 = {lol}")

print("trying to change the first element of the first list...")
lol[0][0] = -1

print(f"{lol = }")  # uh oh! our list contains the SAME list 3 times


print("\n---\n")

lst2 = [1,2,3]

# this does what we wanted: it makes three COPIES of the list
lol2 = [lst2.copy() for _ in range(3)]
print(f"lol2 = [lst2.copy() for _ in range(3)] = {lol2}")

print("trying to change the first element of the first list...")
lol2[0][0] = -1

print(f"{lol2 = }")  # hooray, no surprises
