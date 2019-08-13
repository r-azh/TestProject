__author__ = 'R.Azh'

import inspect
import pkgutil


def import_all_subclasses_of(module_to_scan, baseclass, scope):
    """
    :param module_to_scan: Module to scan.
    :param baseclass: A base class to check.
    :param scope: globals(), locals() or a dict-like object.
    """
    path = module_to_scan.__path__
    for mod in pkgutil.iter_modules(path):
        module = mod[0].find_module(mod[1]).load_module(mod[1])

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, baseclass) and name != baseclass.__name__:
                scope[name] = obj


print('###### usage for sqlalchemy model subclasses #######')
# from app import models
# from sqlalchemy.ext.declarative import declarative_base
#
# Model = declarative_base(name='Model')
#
# def init_db():
#     import_all_subclasses_of(models, Model, locals())
#     Model.metadata.create_all(bind=engine)