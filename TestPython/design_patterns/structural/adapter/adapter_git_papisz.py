class Target(object):

    def request(self):
        return "I'm a target"


class Adaptee(object):

    def specific_request(self):
        return "I'm an adaptee"


class ObjectAdapter(Target):

    def __init__(self, adaptee):
        self._adaptee = adaptee

    def request(self):
        return self._adaptee.specific_request()


class ClassAdapter(Target, Adaptee):

    def request(self):
        return self.specific_request()

# usage
if __name__ == "__main__":
    obj_adapt = ObjectAdapter(Adaptee())
    print(obj_adapt.request())

    cls_adapt = ClassAdapter()
    print(cls_adapt.request())