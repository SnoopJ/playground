This is a (deliberately pathological!) example of a program that deliberate
fragments its own memory by making a whole bunch of objects and then randomly
deleting some fraction of them. Because of the way CPython keeps track of
memory, the deletion of those objects does not actually save much memory in
the resulting program.

More details are given in the program source, but notice in the program output
(below) that only a small handful of the "arenas" allocated for the program are
freed, which means only a small amount of memory is restored to the OS.

```
$ python3 fragmented_memory_program.py
Running in pid 640638
Building a bunch of dummy lists to create a lot of arenas and consume memory

Resident set size: 206.7 MB

# arenas allocated total           =                  595
# arenas reclaimed                 =                    0
# arenas highwater mark            =                  595
# arenas allocated current         =                  595
595 arenas * 262144 bytes/arena    =          155,975,680
30 unused pools * 4096 bytes       =              122,880

---

Removing 250/1000 lists (~25%) from the list-of-lists

# arenas allocated total           =                  595
# arenas reclaimed                 =                    7
# arenas highwater mark            =                  595
# arenas allocated current         =                  588
588 arenas * 262144 bytes/arena    =          154,140,672
8523 unused pools * 4096 bytes     =           34,910,208

---

Resident set size: 205.1 MB
---
Ratio of off-peak and peak RSS usage: 0.992
Detailed allocator stats written to before.txt and after.txt
```
