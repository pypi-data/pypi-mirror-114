try:
    from .Event import Event
except ImportError:
    from Event import Event
from inspect import getmembers


class StaticHandler:
    def __init__(self):
        """
        Oberklasse von der abgeleitet werden kann.
        Die Attribute der Unterklassen werden zu Events.
        Näheres zur Notation in der Dokumentation.
        """
        self.__add_attrs_for_instance()
        pass

    def __add_attrs_for_instance(self):
        """ Durchsucht die Attribute, die den Unterklassen gegeben werden und macht daraus Events. """
        for i in getmembers(self):
            if i[0] == "__annotations__":
                self.__add_attribute(list(i[1].keys()))
            elif (i[1] is None or type(i[1]) == Event) and ((i[0].startswith("__") and i[0].endswith("__")) is False):
                self.__add_attribute(i[0])
        pass

    def __add_attribute(self, attrs):
        """ Fuegt Attribute hinzu. Nimmt entweder eine Liste oder einen einzelnen String. """
        if type(attrs) == list:
            for attr in attrs:
                self.__add_attribute(attr)
            return None

        object.__setattr__(self, attrs, Event())
        pass

    def __setattr__(self, key, value):
        return None

    def __delattr__(self, item):
        return None
    pass
