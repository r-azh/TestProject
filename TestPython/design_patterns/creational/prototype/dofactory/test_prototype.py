__author__ = 'R.Azh'

# Specify the kind of objects to create using a prototypical instance, and create new objects by copying this prototype.
# Prototype pattern in which new objects are created by copying pre-existing objects (prototypes) of the same class.


# Prototype : declares an interface for cloning itself
class ColorPrototype:
    def clone(self):
        pass


# ConcretePrototype : implements an operation for cloning itself
class Color(ColorPrototype):
    _red = None
    _green = None
    _blue = None

    def __init__(self, red, green, blue):
        self._red = red
        self._green = green
        self._blue = blue

    def clone(self):
        print("Cloning color RGB: {}, {}, {}".format(self._red, self._green, self._blue))
        import copy
        return copy.copy(self)


# Client : creates a new object by asking a prototype to clone itself
class ColorManager:
    _colors = {}

    # def __iter__(self):
    #     return self

    def __getitem__(self, item):
        return self._colors[item]

    def __setitem__(self, key, value):
        self._colors[key] = value


colorMger = ColorManager()
colorMger['red'] = Color(255, 0, 0)
colorMger['green'] = Color(0, 255, 0)
colorMger['blue'] = Color(0, 0, 255)

colorMger['angry'] = Color(255, 54, 0)
colorMger['peace'] = Color(128, 211, 128)
colorMger['flame'] = Color(211, 34, 20)

color1 = colorMger["red"].clone()
color2 = colorMger["peace"].clone()
color3 = colorMger["flame"].clone()