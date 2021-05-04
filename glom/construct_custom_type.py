"""
Example showing how to construct instances of a custom type using glom

Based on a question in Freenode #python on 4 May 2021
"""

from glom import glom, Call, Invoke, T


class Person:
    id: str
    name: str
    location: str

    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location


if __name__ == "__main__":
    data = [
        {"id": "1337", "name": "Aineko", "geolocation": "The Ring Imperium"},
        {"id": "-1", "name": "Boris", "geolocation": "The Field Circus"},
        {"id": "42", "name": "Manfred", "geolocation": "Amsterdam"},
    ]

    target = [  # for every datum in the target list...
        Invoke(Person).specs(       # construct an instance of Person...
            id="id",                # with the named keyword args, values given by
            name="name",            # the associated specifications (here, a string indicating the associated key)
            location="geolocation",
        )
    ]

    people = glom(data, target)

    for p in people:
        print(p.id, p.name, p.location)
