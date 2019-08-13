__author__ = 'R.Azh'


class C:
    a = None

    def __init__(self):
        self.a = 'x'


c = C()

print(str(c.a))
print()

print(id(c.a))
