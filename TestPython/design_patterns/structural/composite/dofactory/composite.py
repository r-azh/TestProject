
# Compose objects into tree structures to represent part-whole hierarchies.
# Composite lets clients treat individual objects and compositions of objects uniformly.


# Component: declares the interface for objects in the composition.
# implements default behavior for the interface common to all classes, as appropriate.
# declares an interface for accessing and managing its child components.
# (optional) defines an interface for accessing a component's parent in the recursive structure,
# and implements it if that's appropriate.
class DrawingElement:
    _name = None

    def __init__(self, name):
        self._name = name

    def add(self, d):
        raise NotImplementedError

    def remove(self, d):
        raise NotImplementedError

    def display(self, indent):
        raise NotImplementedError


# Leaf: represents leaf objects in the composition. A leaf has no children.
# defines behavior for primitive objects in the composition.
class PrimitiveElement(DrawingElement):
    def __init__(self, name):
        super().__init__(name)

    def add(self, d):
        print("Cannot add to a PrimitiveElement")

    def remove(self, d):
        print("Cannot remove from a PrimitiveElement")

    def display(self, indent):
        print("{}{}".format('_'*indent, self._name))


# Composite: defines behavior for components having children.
# stores child components.
# implements child-related operations in the Component interface.
class CompositeElement(DrawingElement):
    elements = None

    def __init__(self, name):
        super().__init__(name)
        self.elements = []

    def add(self, d):
        self.elements.append(d)

    def remove(self, d):
        self.elements.remove(d)

    def display(self, indent):
        print((self._name).rjust(indent, "-"))
        for element in self.elements:
            element.display(indent + 2)


# Client: manipulates objects in the composition through the Component interface.

root = CompositeElement('Picture')
root.add(PrimitiveElement('Red Line'))
root.add(PrimitiveElement('Blue Circle'))
root.add(PrimitiveElement('Green Box'))

comp = CompositeElement('Two Circles')
comp.add(PrimitiveElement('Black Circle'))
comp.add(PrimitiveElement('White Circle'))
root.add(comp)

pe = PrimitiveElement('Yellow Line')
root.add(pe)
root.remove(pe)

root.display(2)


