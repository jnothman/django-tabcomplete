import sys
if 'IPython' in sys.modules:
    from .interactive import activate
    activate()

__all__ = []

__version__ = '0.1a'
