import os
import json
from darksky.api import DarkSky
from darksky.types import languages, units, weather
from geopy.geocoders import Nominatim
from geopy.location import Location
from ask_sdk_model.services.device_address.address import Address
import logging


class CyclingClothier:
    DEFAULT_RECOMMENDATIONS_FILE = './defaults.json'

    def __init__(self, addr: Address,
                 logger):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logger.level)

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
        address = ""
        for key in keys:
            if key in addr and addr[key] is not None:
                address += f"{addr[key]} "

        return address

    def __get_location(self, addr: Address):
        self.logger.info("Getting geo coordinates for address")
        geolocator = Nominatim(user_agent=os.environ['FUNCTION_NAME'])
        lookup_address = self.__get_addr_string(addr)
        self.logger.debug(f"Looking up lat long for {lookup_address}")

        try:
            location = geolocator.geocode(lookup_address)
        except Exception as e:
            self.logger.error(f"Unable to retrieve coordinates for address: {e}")

        return location

    def __get_current_forecast(self, location: Location):
        self.logger.info("Getting forecast from location")
        forecast = self.ds.get_forecast(
                location.latitude, location.longitude,
                extend=False,
                lang=languages.ENGLISH,
                units=units.AUTO,
                exclude=[weather.MINUTELY, weather.ALERTS])

        return forecast.currently

    def recommend_gear(self, addr: Address):
        self.logger.info("Getting gear recommendations based on address")
        location = self.__get_location(addr)
        current = self.__get_current_forecast(location)
        # Get local JSON or Google Sheets data for default weather-based
        # recommendations
        # Return list of recommended clothing options

        return (f"It's {current.temperature} degrees with clear skies,"
                "so you should wear a dri-fit base layer, short sleeve jersey,"
                "and long pants.")
