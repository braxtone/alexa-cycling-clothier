import os
import json
from darksky.api import DarkSky, DarkSkyAsync
from darksky.types import languages, units, weather


class CyclingClothier:
    DEFAULT_RECOMMENDATIONS_FILE = './defaults.json'

    def __init__(self):
        darksky_api_key = self.__get_darksky_api_key()
        self.ds = DarkSky(darksky_api_key)

        self.defaults = json.load(
                            open(self.DEFAULT_RECOMMENDATIONS_FILE,
                                 'r'))

    def __get_darksky_api_key(self):
        ds_key_key = os.environ['DARKSKY_API_KEY_KEY']
        ds_key_key_locator, ds_key_key_value = ds_key_key.split(':')

        # TODO: Implement retrieving API key from SecretsManager
        if ds_key_key_locator == 'env:':
            # Get DarkSky API key from environment variable for local testing
            return ds_key_key.split(':')[1]
        elif ds_key_key_locator == 'sm':
            # TODO: Get key from Secrets Manager
            return ds_key_key.split(':')[1]
        else:
            raise AttributeError(
                    f"Unknown DarkSky key prefix: {ds_key_key_locator}")
