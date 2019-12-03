import os
from darksky.api import DarkSky
from darksky.types import languages, units, weather
from geopy.geocoders import Nominatim
from geopy.location import Location
from ask_sdk_model.services.device_address.address import Address
from .recommendation import Recommendation, RecommendationOverrideException

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CyclingClothier:
    UNDERSHIRT = 'undershirt'
    PANTS = 'pants'
    BOOT_COVERS = 'boot_covers'
    JERSEY = 'jersey'
    GLOVES = 'gloves'
    FACEMASK = 'facemask'

    GEAR = [UNDERSHIRT, PANTS,
            JERSEY, GLOVES,
            BOOT_COVERS, FACEMASK]

    def __init__(self, addr: Address,
                 defaults: Recommendation,
                 log_level=logging.INFO):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logger.level)
        if type(addr) is Address:
            self.addr = addr
        else:
            raise TypeError(f"addr parameter must be of type Address, got {type(addr)}")
        self.darksky_api_key = None
        self.ds = DarkSky(self.__get_darksky_api_key())
        self.defaults = defaults

    def __get_darksky_api_key(self):
        self.logger.info("Retrieving DarkSky API key")
        if self.darksky_api_key is not None:
            self.logger.info("Already got DarkSky API key, returning cached key")
            return self.darksky_api_key

        ds_key_key = os.environ['DARKSKY_API_KEY_KEY']
        ds_key_key_locator, ds_key_key_value = ds_key_key.split(':')

        if ds_key_key_locator == 'env':
            self.logger.info("Getting DarkSky API key from environment variable")
            # Get DarkSky API key from environment variable for local testing
            env_var = ds_key_key.split(':')[1]
            if env_var in os.environ and os.environ[env_var]:
                self.darksky_api_key = os.environ[env_var]
                self.logger.info(f"Successfully got API key from env variable {env_var}")
            else:
                raise NameError(f"Unable to retrieve DarkSky API key from env variable {env_var}")
            return self.darksky_api_key

        elif ds_key_key_locator == 'sm':
            self.logger.info("Getting DarkSky API key from Secrets Manager")
            # TODO: Get key from Secrets Manager
            return ds_key_key.split(':')[1]
        else:
            raise AttributeError(
                    f"Unknown DarkSky key prefix: {ds_key_key_locator}")

    def __get_addr_string(self, addr: Address):
        self.logger.info("Retrieving base address string from object")
        # Hardcoding the order of the keys in case the dict changes order at some point
        keys = ['address_line1',
                'address_line2',
                'address_line3',
                'city',
                'country_code',
                'district_or_county',
                'postal_code',
                'state_or_region']

        addr = addr.to_dict()
        address_str = ""
        for key in keys:
            if key in addr and addr[key] is not None:
                address_str += f"{addr[key]} "

        return address_str

    def __get_location(self, addr: str):
        self.logger.info("Getting geo coordinates for address")
        geolocator = Nominatim(user_agent=os.environ['FUNCTION_NAME'])
        self.logger.debug(f"Looking up lat long for {addr}")

        # TODO Get better error handling here
        # Something like a custom CantGetAddrLatLongException that is caught by
        # the recommend_gear method and returns and error voice prompt
        try:
            location = geolocator.geocode(addr)
        except Exception as e:
            self.logger.error(f"Unable to retrieve coordinates for address: {e}")
            raise Exception(e)

        return location

    def _get_current_forecast(self, location: Location):
        self.logger.info("Getting forecast from location")
        forecast = self.ds.get_forecast(
                location.latitude, location.longitude,
                extend=False,
                lang=languages.ENGLISH,
                units=units.AUTO,
                exclude=[weather.MINUTELY, weather.ALERTS])

        return forecast.currently

    def get_all_recommendations(self, temperature: float):
        logger.debug(f"Getting recommendations for temp: {temperature}")
        recommendations = []
        for gear in self.GEAR:
            recommendations.append(
                self.defaults.recommend(gear, temperature))

        return dict(zip(self.GEAR, recommendations))

    def recommend_gear(self, addr: Address = None):
        self.logger.info("Getting gear recommendations based on address")
        addr = self.addr if addr is None else addr
        addr_str = self.__get_addr_string(addr)
        location = self.__get_location(addr_str)
        current = self._get_current_forecast(location)
        rec_boilerplate = f"It's {current.temperature} degrees and {current.summary}. "
        try:
            recs = self.get_all_recommendations(current.temperature)
            # Filter out things without recommendations
            recs = dict(filter(lambda e: e[1].recommendation is not None, recs.items()))
            # Turn the list of objects in to a list of string-ified recommendations
            rec_vals = [str(e) for e in recs.values()]
            # https://www.youtube.com/watch?v=P_i1xk07o4g
            recommendations = 'So you should wear: '
            recommendations += ', '.join(rec_vals[:-1]) + ', and ' + rec_vals[-1]
        except RecommendationOverrideException as e:
            self.logger.info("Encountered an override for temp: {current.temperature}")
            recommendations = str(e)

        # TODO Google Sheets data for default weather-based recommendations
        # Return list of recommended clothing options

        return (rec_boilerplate + recommendations)
