# in a build of Python with Py_DEBUG enabled (--with-pydebug=yes during
# configuration), defining the __ltrace__ (note: one l!) name enables some
# debug prints, notably a print for every push/pop from the stack and for each
# bytecode instruction
__ltrace__ = True


def main():
    x = 40
    x += 1
    x += 1
    return x


# quirk: we need to enter a new call frame for the definition of __ltrace__
# to actually take effect
main()


### Running this program in a CPython 3.9.15 built with --with-pydebug=yes produces:

# $ ~/repos/cpython/python lltrace.py
# 0: 100, 1
# push 40
# 2: 125, 0
# pop 40
# 4: 124, 0
# push 40
# 6: 100, 2
# push 1
# 8: 55
# pop 1
# 10: 125, 0
# pop 41
# 12: 124, 0
# push 41
# 14: 100, 2
# push 1
# 16: 55
# pop 1
# 18: 125, 0
# pop 42
# 20: 124, 0
# push 42
# 22: 83
# pop 42
# ext_pop <function main at 0x7f83fc979370>
# push 42
# 16: 1
# pop 42
# 18: 100, 3
# push None
# 20: 83
# pop None
