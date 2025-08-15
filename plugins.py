
registered_plugins = []

def register_plugin(fn):
    registered_plugins.append(fn)
    print(f"Plugin '{fn.__name__}' registered")

def run_plugins(event, data):
    for fn in registered_plugins:
        fn(event, data)
