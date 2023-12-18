def predicate_a():
    ...


def predicate_b():
    ...


if predicate_a():
    print(
        "imagine "
        "many "
        "lines "
        "of "
        "code "
        "here "
    )
elif predicate_b():
    print(
        "imagine "
        "many "
        "lines "
        "of "
        "code "
        "here "
    )
else:
    print(
        "imagine "
        "many "
        "lines "
        "of "
        "code "
        "here "
    )


if predicate_a():
    z = -1


if (
    predicate_a() and
    predicate_b()
    ):
    z = 1


if True: 1
elif predicate_a(): 2
else: 3
