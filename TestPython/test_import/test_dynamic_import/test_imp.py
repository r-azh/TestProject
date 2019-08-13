__author__ = 'R.Azh'


print('###### imp is deprecated use importlib instead ######')

import imp


def dynamic_importer(name, class_name):
    """
    Dynamically imports modules / classes
    """
    try:
        fp, pathname, description = imp.find_module(name)
    except ImportError:
        print("unable to locate module: " + name)
        return (None, None)

    try:
        example_package = imp.load_module(name, fp, pathname, description)
    except Exception as e:
        print(e)

    try:
        myclass = imp.load_module("%s.%s" % (name, class_name), fp, pathname, description)
        print(myclass)
    except Exception as e:
        print(e)

    return example_package, myclass


if __name__ == "__main__":
    module, modClass = dynamic_importer("decimal", "Context")

    module, modClass = dynamic_importer('foo', "Foo")
