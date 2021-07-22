.. code-block:: python

    >>> lst = list(range(10))
    >>> id(lst)  # id(name) tells us the identity of the named object
    139757282878912
    >>> lst[0] = -1  # changing the object...
    >>> id(lst)      # ...does not change its identity...
    139757282878912
    >>> lst          # ...but DOES change its contents
    [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> val = lst.pop()  # list.pop() changes the list AND returns the item
                         # removed from it...
    >>> val
    9
    >>> id(lst)          # and it does not change the identity of the object
    139757282878912
    >>> lst2 = lst       # we can refer to this object by two different names...
    >>> id(lst2)         # ...but it's still the SAME object
    139757282878912
    >>> lst is lst2      # the usual way to check that these names mean the same exact object
    True
    >>> lst = lst[:-1]   ## this case is tricky; the right-hand side builds a new
                         ## list object (by indexing with a slice), and the `=`
                         ## assigns this _brand-new_ object to the SAME name
    >>> lst
    [-1, 1, 2, 3, 4, 5, 6, 7, 8]
    >>> id(lst)          # because it is a brand-new object, it has a different identity
    139757282877824
    >>> id(lst2)         # the original list object's identity is preserved...
    139757282878912
    >>> lst == lst2      # note: the lists are equivalent...
                         # (because they contain the same sequence of values)
    True
    >>> lst is lst2      # ...but not exactly the same object
    False
    >>> lst[:] = -2      # we can modify the new list object...
    >>> lst
    [-2, -2, -2, -2, -2, -2, -2, -2, -2]
    >>> lst2             # ...without modifying the content of the original one
    [-1, 1, 2, 3, 4, 5, 6, 7, 8]
