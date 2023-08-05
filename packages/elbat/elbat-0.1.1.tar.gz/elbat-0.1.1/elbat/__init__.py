# https://github.com/python-poetry/poetry/pull/2366
# auto load the version from the poetry config
try:
    # Standard Library
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    # Third Party Libraries
    import importlib_metadata


__version__ = importlib_metadata.version(__name__)
