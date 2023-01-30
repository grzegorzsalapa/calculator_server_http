from .calculations import Calculations


class ResourceNotFoundError(Exception):

    def __init__(self, message):
        self.message = message


class SingletonMeta(type):  # TODO: Ripped off. Need to understand what's going on...

    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Resources(Calculations, metaclass=SingletonMeta):

    def __init__(self):
        Calculations.__init__(self)

        self.available_resources = [(r'/calculations(\/?$)', 'POST', Calculations.add_calculation),
                                    (r'/calculations(\/?$)', 'GET', Calculations.get_all_calculations),
                                    (r'/calculations/(\d+)', 'GET', Calculations.get_calculation_by_id)]
