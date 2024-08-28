import inspect


class Inspectable:
    def __init__(self):
        self.property = 42


def introspection_info(obj):
    init_source = None

    try:
        init_source = inspect.getsource(obj.__init__)
    except TypeError:
        pass

    return {
        'type': obj.__class__.__name__,
        'methods': dir(obj),
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
