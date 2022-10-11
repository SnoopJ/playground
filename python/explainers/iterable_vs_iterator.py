# this object is 'iterable,' meaning we can call iter() on it to get an 'iterator' object
lst = [1,2,3,4,5]
print(f"{lst = }")

# these objects are distinct 'iterators' over the list
it1 = iter(lst)
it2 = iter(lst)
print(f"{it1 is it2 = }")

# the iterators can be advanced separately; in this case, they hold state about "where" in the list they are
print(f"{next(it1) = }")  # 1
print(f"{next(it1) = }")  # 2
print(f"{next(it2) = }")  # 1
print(f"{next(it1) = }")  # 3


# iterators are themselves iterable, calling iter() on them returns the same object
print(f"{iter(it1) is it1 = }")


# an iterable object can be used directly in a loop. Python calls iter() for us to make
# the iterator that will be advanced for each iteration of the loop
for item in lst:
    print(item)
