# New implementation goes here

class ModuleContext:
    def __init__(self):
        self.data = {}

    def set_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key)


def import_and_render_module(module_name, context):
    module = __import__(module_name)
    module_instance = module.Module(context)
    module_instance.render()
