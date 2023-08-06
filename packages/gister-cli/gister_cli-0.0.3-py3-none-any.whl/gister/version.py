import platform

__version__ = '0.0.1'

def get_version():
    return (f'gister {__version__} -'
            f' python {platform.python_version()}')
