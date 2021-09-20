
value = 42

def f(x):
   return x**2

mystring = f"You can use f-strings to embed a value (like {value}) in a string. You can even call a function: {f(7)}"

print(mystring)
