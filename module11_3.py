import inspect

class Inspectable:
    def __init__(self):
        self.property = 42

def introspection_info(obj):
    return {
        'type' : obj.__class__.__name__,
        'methods' : dir(obj),
        'module' : obj.__class__.__module__,
        'init_source' : inspect.getsource(obj.__init__)
    }

class_info = introspection_info(Inspectable())
print(class_info)
