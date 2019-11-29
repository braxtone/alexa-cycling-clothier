import os
import json
from darksky.api import DarkSky
from darksky.types import languages, units, weather
from geopy.geocoders import Nominatim
from geopy.location import Location
from ask_sdk_model.services.device_address.address import Address

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class CyclingClothier:
    DEFAULT_RECOMMENDATIONS_FILE = './defaults.json'

    def __init__(self, addr: Address,
                 log_level=logging.INFO,
                 defaults: str = DEFAULT_RECOMMENDATIONS_FILE):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logger.level)
        if type(addr) is Address:
            self.addr = addr
        else:
            raise TypeError(f"addr parameter must be of type Address, got {type(addr)}")

        self.darksky_api_key = None

        self.ds = DarkSky(self.__get_darksky_api_key())
        self.defaults = json.load(
                            open(self.DEFAULT_RECOMMENDATIONS_FILE,
                                 'r'))

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

        try:
            location = geolocator.geocode(addr)
        except Exception as e:
            self.logger.error(f"Unable to retrieve coordinates for address: {e}")

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

    def recommend_gear(self, addr: Address = None):
        self.logger.info("Getting gear recommendations based on address")
        addr = self.addr if addr is None else addr
        addr_str = self.__get_addr_string(addr)
        location = self.__get_location(addr_str)
        current = self._get_current_forecast(location)
        # Get local JSON or Google Sheets data for default weather-based
        # recommendations
        # Return list of recommended clothing options

        return (f"It's {current.temperature} degrees and {current.summary}, "
                "so you should wear a dri-fit base layer, short sleeve jersey, "
                "and long pants.")
