import inspect


class Inspectable:
    def __init__(self):
        self.property = 42


def introspection_info(obj):
    attributes = list()
    methods = list()
    init_source = None

    for name in dir(obj):
        if callable(getattr(obj, name)):
            methods.append(name)
        else:
            attributes.append(name)

    try:
        init_source = inspect.getsource(obj.__init__)
    except TypeError:
        pass

    return {
        'type': obj.__class__.__name__,
        'attributes': attributes,
        'methods': methods,
        'module': obj.__class__.__module__,
        'init_source': init_source
    }


def test_func():
    return 1


class_info = introspection_info(42)
print(class_info)

class_info = introspection_info(test_func)
print(class_info)

class_info = introspection_info(Inspectable())
print(class_info)

class_info = introspection_info(inspect)
print(class_info)
