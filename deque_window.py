from collections import deque
from io import StringIO

txt = StringIO("""
’Twas brillig, and the slithy toves
      Did gyre and gimble in the wabe:
All mimsy were the borogoves,
      And the mome raths outgrabe.

three identical lines
three identical lines
three identical lines

“Beware the Jabberwock, my son!
      The jaws that bite, the claws that catch!
Beware the Jubjub bird, and shun
      The frumious Bandersnatch!” 
""".strip())

d = deque(maxlen=3)  # create a deque that can hold 3 values maximum
for line in txt.readlines():
    d.append(line)  # put the current line into the deque, pushing out an old one if we have 3
    print(d)
    if len(d) == 3 and (d[0] == d[1] == d[2]):  # if the last three lines are identical, print a special message
        print("\t\tO frabjous day!")


