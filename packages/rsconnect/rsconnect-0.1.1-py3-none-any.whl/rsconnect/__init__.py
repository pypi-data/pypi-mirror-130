"""
A simple meta-package to install packages for working with RStudio Connect
"""

try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata

__version__ = metadata.version("rsconnect")

