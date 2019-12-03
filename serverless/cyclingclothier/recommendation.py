import abc
import json
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Recommendation(abc.ABC):
    __metaclass__ = abc.ABCMeta
    TEMP_INCREMENTS = 5
    REC_OVERRIDE = "_override"
    REC_KEY = "recommendations"

    @abc.abstractmethod
    def __init__(self, defaults, temperature):
        """Create recommendation object"""

    @abc.abstractmethod
    def recommend(self, gear, temperature):
        """Get gear recommendation"""


class UnknownGearTypeException(Exception):
    """Thrown when an unknown/unexpected gear type is encountered"""
    pass


class RecommendationOverrideException(Exception):
    """Thrown when the recommendations config section has an override"""


class GearRecommendation():
    def __init__(self, gear: str, rec: str):
        self.type = gear
        self.recommendation = rec

    def __str__(self):
        if self.type == 'undershirt':
            return f"a {self.recommendation} base layer"
        elif self.type == 'pants':
            return f"biking {self.recommendation}"
        elif self.type == 'jersey':
            return f"a {self.recommendation} jersey"
        elif self.type == 'gloves':
            return f"a pair of {self.recommendation} gloves"
        elif self.type == 'boot_covers':
            return 'boot covers'
        elif self.type == 'facemask':
            return 'facemask'
        else:
            raise UnknownGearTypeException(f"Unknown gear type: '{self.type}'")


class DefaultRecommendation(Recommendation):
    DEFAULT_RECOMMENDATIONS_FILE = './defaults.json'

    def __init__(self, defaults: str = DEFAULT_RECOMMENDATIONS_FILE,
                 temperature: float = None):
        self.defaults = json.load(open(defaults, 'r'))
        self.temp = temperature

    def recommend(self, gear: str, temperature: float = None):
        if temperature is None:
            temperature = self.temperature

        self._vet_temp(temperature)
        floor = str(int(temperature // self.TEMP_INCREMENTS))

        # Check if defaults are set for this temperature range
        if floor in self.defaults:
            gear_recs = self.defaults[floor]

            # If so, see if there's an override
            if self.REC_OVERRIDE in gear_recs[self.REC_KEY]:
                raise RecommendationOverrideException(
                                          gear_recs[self.REC_KEY][self.REC_OVERRIDE])
            elif gear in gear_recs[self.REC_KEY]:
                # logger.debug(f"Got recommendation {gear_recs[self.REC_KEY][gear]} for {gear}")
                return GearRecommendation(gear,
                                          gear_recs[self.REC_KEY][gear])
            else:
                raise UnknownGearTypeException("Unknown gear type: '{gear}'")
        else:
            raise KeyError("No defaults specified for the specified temperature")

    def _vet_temp(self, temp):
        if temp:
            if type(temp) is float:
                return temp
            else:
                raise TypeError("temp parameter must be a float")
        else:
            raise TypeError("temp argument must not be None")
