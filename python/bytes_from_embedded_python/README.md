This sample shows off a Python interpreter embedded in a C++ program. The C++
program evaluates Python source given as the first argument and attempts to
retrieve bytes (`uint8_t`) from the result.

### Example invocation
```
$ ./main 'b"hello world!"'
Buffer at 0x7f8691216f20
#0      h
#1      e
#2      l
#3      l
#4      o
#5
#6      w
#7      o
#8      r
#9      l
#10     d
#11     !
```
