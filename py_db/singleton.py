import threading


class SingletonMeta(type):
    """
    A metaclass that implements the Singleton design pattern.

    Classes using SingletonMeta as their metaclass will only have one instance.
    Subsequent instantiations will return the same instance.

    Attributes:
        _instances (dict): A dictionary mapping classes to their singleton instances.

    Methods:
        __call__(cls, *args, **kwargs): Returns the singleton instance of the class.
    """

    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):

        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(SingletonMeta, cls).__call__(
                    *args, **kwargs
                )
        return cls._instances[cls]
