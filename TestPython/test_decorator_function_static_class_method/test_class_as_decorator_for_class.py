from functools import wraps

__author__ = 'R.Azh'


class ClassDecorator:
    _decorator_classes = {}   # _decorator_classes_of_decorated_functions as {"decorated_function" : decorator_class}

    def decoration(self, decorator_class):
        def decorator(decorated_class):
            self._decorate(decorated_class, decorator_class, self._decorate_func)
            return decorated_class
        return decorator

    def _decorate(self, decorated_class, decorator_class, decorate_func):
        for name, obj in vars(decorated_class).items():
            if not name.startswith("_"):
                if callable(obj):
                    function_full_path = "{}.{}".format(obj.__module__, obj.__qualname__)
                    self._decorator_classes[function_full_path] = decorator_class
                    setattr(decorated_class, name, decorate_func(obj))

    # calling decorated function after decorator function
    # def _decorate_func(self, func):
    #     @wraps(func)
    #     def decorator(*args, **kwargs):
    #         if not func.__name__.startswith("_"):
    #             function_full_path = "{}.{}".format(func.__module__, func.__qualname__)
    #             decorator_class = self._decorator_classes[function_full_path]
    #             decorator_instance = decorator_class(args[0])       # args[0] is current decorated class instance (self)
    #             if hasattr(decorator_instance, func.__name__):      # set func in decorator class as decorator to the same name func in decorated class
    #                 decorator_function = getattr(decorator_instance, func.__name__)
    #                 decorator_function(*args[1:])    # calling decorator function
    #         return func(*args, **kwargs)             # calling decorated function
    #     return decorator

    # calling decorated function before decorator function
    def _decorate_func(self, func):
        @wraps(func)
        def decorator(*args, **kwargs):
            decorator_function = None   #
            if not func.__name__.startswith("_"):
                function_full_path = "{}.{}".format(func.__module__, func.__qualname__)
                decorator_class = self._decorator_classes[function_full_path]
                decorator_instance = decorator_class(args[0])       # args[0] is current decorated class instance (self)
                if hasattr(decorator_instance, func.__name__):      # set func in decorator class as decorator to the same name func in decorated class
                    decorator_function = getattr(decorator_instance, func.__name__)
                    func(*args, **kwargs)   #
            return decorator_function(*args[1:])    #
        return decorator


class Foo:
    instance = None

    def __init__(self, instance):
        self.instance = instance

    def a(self, *args):
        print("in decorator:", *args)

    def b(self, *args):
        print("in decorator:", *args)


decorator = ClassDecorator()


@decorator.decoration(Foo)
class Bar:
    def a(self, arg1):
        print(arg1)

    def b(self, arg2):
        print(arg2)


bar = Bar()
bar.a("hi")
bar.b("by")