import abc
import json


class Recommendation(abc.ABC):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, defaults: str,
                 temp: float = None):
        """Create recommendation object"""
        self.temp = temp

    @property
    @abc.abstractmethod
    def undershirt(self, temperature: float):
        """Get undershirt recommendation"""

    @abc.abstractmethod
    def pants(self, temperature: float):
        """Get pants recommendation"""

    @abc.abstractmethod
    def jersey(self, temperature: float):
        """Get jersey recommendation"""

    @abc.abstractmethod
    def gloves(self, temperature: float):
        """Get gloves recommendation"""

    @abc.abstractmethod
    def facemask(self, temperature: float):
        """Get facemask recommendation"""

    @abc.abstractmethod
    def boot_covers(self, temperature: float):
        """Get boot cover recommendation"""


class DefaultRecommendation(Recommendation):
    DEFAULT_RECOMMENDATIONS_FILE = './defaults.json'

    def __init__(self, defaults: str = DEFAULT_RECOMMENDATIONS_FILE,
                 temp: float = None):
        self.defaults = json.load(open(defaults, 'r'))

        self.temp = temp if temp else None

    def vet_temp(temp):
        if temp:
            if type(temp) is float:
                return temp
            else:
                raise TypeError("temp parameter must be a float")
        else:
            raise TypeError("temp argument must not be None")

    def undershirt(self, temperature: float):
        self.vet_temp(temperature)

    def pants(self, temperature: float):
        pass

    def jersey(self, temperature: float):
        pass

    def gloves(self, temperature: float):
        pass

    def facemask(self, temperature: float):
        pass

    def boot_covers(self, temperature: float):
        pass
