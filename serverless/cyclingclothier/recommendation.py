import abc
import json


class Recommendation(abc.ABC):
    @abc.abstractmethod
    def __init__(self, defaults: str):
        pass

    @abc.abstractmethod
    def undershirt(self):
        pass

    @abc.abstractmethod
    def pants(self):
        pass

    @abc.abstractmethod
    def jersey(self):
        pass

    @abc.abstractmethod
    def gloves(self):
        pass

    @abc.abstractmethod
    def facemask(self):
        pass

    @abc.abstractmethod
    def boot_covers(self):
        pass


class DefaultRecommendation(Recommendation):
    DEFAULT_RECOMMENDATIONS_FILE = './defaults.json'

    def __init__(self, defaults: str = DEFAULT_RECOMMENDATIONS_FILE):
        self.defaults = json.load(
            open(self.DEFAULT_RECOMMENDATIONS_FILE,
                 'r'))
        pass
