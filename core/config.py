from importlib.machinery import SourceFileLoader

# Load config.cfg file as a python file
try:
    cfg = SourceFileLoader('cfg', 'config.cfg').load_module()
except Exception as e:
    print("Failed to load config.cfg file!")
    raise e
