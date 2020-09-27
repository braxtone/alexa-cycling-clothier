import pytest

from cyclingclothier.core import CyclingClothier
from cyclingclothier.recommendation import DefaultRecommendation

ADDR_OBJ_VALID = './tests/addr_valid.yaml'
FORECAST_CURRENT_VALID_OBJ = './tests/forecast_current_valid.yaml'
FORECAST_28_VALID_OBJ = './tests/forecast_28_valid.yaml'
FORECAST_61_VALID_OBJ = './tests/forecast_61_valid.yaml'
RECOMMENDATIONS_VALID = './tests/recommendation_valid.json'
RECOMMENDATIONS_INVALID = './tests/recommendation_invalid.json'
SECRETS_MANAGER_VALID = './tests/sm_response_valid.yaml'


@pytest.fixture
def set_env_ds_key_key(monkeypatch):
    monkeypatch.setenv('DARKSKY_API_KEY_KEY', 'env:DARKSKY_API_KEY')

@pytest.fixture
def set_sm_ds_key_key(monkeypatch):
    monkeypatch.setenv('DARKSKY_API_KEY_KEY', 'sm:dev/CyclingClothier/DarkSkyAPIKey')

@pytest.fixture
def set_ds_key(monkeypatch):
    monkeypatch.setenv('DARKSKY_API_KEY', 'alsdkfjwoeijwfojiwe')

@pytest.fixture
def set_function_name(monkeypatch):
    monkeypatch.setenv('FUNCTION_NAME', 'CyclingClothier-pytest')

@pytest.fixture
def get_invalid_recs_filename():
    return RECOMMENDATIONS_INVALID

@pytest.fixture
def get_valid_recs_filename():
    return RECOMMENDATIONS_VALID

@pytest.fixture
def get_default_recs_obj(get_valid_recs_filename):
    return DefaultRecommendation(get_valid_recs_filename)

@pytest.fixture()
def get_valid_addr_obj():
    import yaml
    from ask_sdk_model.services.device_address.address import Address

    addr = yaml.load(open(ADDR_OBJ_VALID), Loader=yaml.FullLoader)
    return addr


class MockDarkSky:
    @staticmethod
    def get_current_forecast():
        import yaml
        from darksky.forecast import CurrentlyForecast

        current_forecast = yaml.load(open(FORECAST_CURRENT_VALID_OBJ),
                                     Loader=yaml.FullLoader)
        return current_forecast

    @staticmethod
    def get_61_forecast():
        import yaml
        from darksky.forecast import CurrentlyForecast

        forecast = yaml.load(open(FORECAST_61_VALID_OBJ),
                                     Loader=yaml.FullLoader)
        return forecast

    @staticmethod
    def get_28_forecast():
        import yaml
        from darksky.forecast import CurrentlyForecast

        forecast = yaml.load(open(FORECAST_28_VALID_OBJ),
                                     Loader=yaml.FullLoader)
        return forecast


class MockSecretsManager:
    @staticmethod
    def get_secret_value():
        import yaml
        from botocore.client import SecretsManager

        secret_value = yaml.load(open(SECRETS_MANAGER_VALID),
                                 Loader=yaml.FullLoader)

@pytest.fixture
def mock_valid_secret(monkeypatch):
    def mock_get_valid_secret(*args, **kwargs):
        return MockSecretsManager().get_secret_value()

    from botocore.client import SecretsManager  # noqa: F401
    monkeypatch.setattr(SecretsManager, 'get_secret_value', mock_get_valid_secret)

@pytest.fixture
def mock_current_forecast(monkeypatch):

    def mock_get_current_forecast(*args, **kwargs):
        return MockDarkSky().get_current_forecast()

    monkeypatch.setattr(CyclingClothier, '_get_current_forecast', mock_get_current_forecast)

@pytest.fixture
def mock_61_degree_forecast(monkeypatch):

    def mock_get_61_forecast(*args, **kwargs):
        return MockDarkSky().get_61_forecast()

    monkeypatch.setattr(CyclingClothier, '_get_current_forecast', mock_get_61_forecast)

@pytest.fixture
def mock_28_degree_forecast(monkeypatch):

    def mock_get_28_forecast(*args, **kwargs):
        return MockDarkSky().get_28_forecast()

    monkeypatch.setattr(CyclingClothier, '_get_current_forecast', mock_get_28_forecast)

@pytest.mark.usefixtures('set_ds_key', 'set_env_ds_key_key')
def test_core_constructor_neg():
    not_addr = { "stuff": "things" }

    # Ensure there's some basic input validation
    with pytest.raises(TypeError):
        CyclingClothier(not_addr)

@pytest.mark.usefixtures('set_ds_key', 'set_env_ds_key_key')
def test_core_constructor(get_valid_addr_obj,
                          get_default_recs_obj):
    # Test valid Address object returns CyclingClothier object
    # Bless you https://stackoverflow.com/a/25560086/1183198
    cc = CyclingClothier(get_valid_addr_obj, get_default_recs_obj)
    assert isinstance(cc, CyclingClothier)

@pytest.mark.usefixtures('set_ds_key', 'set_env_ds_key_key',
                         'set_function_name')
def test_default_gear_recommendation(get_valid_addr_obj,
                                 mock_current_forecast,
                                 get_default_recs_obj):
    cc = CyclingClothier(get_valid_addr_obj, get_default_recs_obj)

    expected_response = ("It's 42.0 degrees and Clear. "
                         "So you should wear: a dri-fit base layer, "
                         "biking tights, a longsleeve jersey, and a pair of full-finger gloves.")
    assert cc.recommend_gear() == expected_response

@pytest.mark.usefixtures('set_ds_key', 'set_env_ds_key_key',
                         'set_function_name')
def test_default_gear_recommendation(get_valid_addr_obj,
                                 mock_61_degree_forecast,
                                 get_default_recs_obj):
    cc = CyclingClothier(get_valid_addr_obj, get_default_recs_obj)

    expected_response = ("It's 61.0 degrees and Clear. "
                            "So you should wear: biking shorts, a shortsleeve "
                            "jersey, and a pair of fingerless gloves.")
    assert cc.recommend_gear() == expected_response

@pytest.mark.usefixtures('set_ds_key', 'set_sm_ds_key_key',
                         'set_function_name')
def test_sm_gear_recommendation(get_valid_addr_obj,
                                 mock_61_degree_forecast,
                                 mock_valid_secret,
                                 get_default_recs_obj):
    cc = CyclingClothier(get_valid_addr_obj, get_default_recs_obj)

    expected_response = ("It's 61.0 degrees and Clear. "
                            "So you should wear: biking shorts, a shortsleeve "
                            "jersey, and a pair of fingerless gloves.")
    assert cc.recommend_gear() == expected_response

# TODO Add test for 28 degrees (says to ride the bus)
@pytest.mark.usefixtures('set_ds_key', 'set_env_ds_key_key',
                         'set_function_name')
def test_default_gear_recommendation(get_valid_addr_obj,
                                 mock_28_degree_forecast,
                                 get_default_recs_obj):
    cc = CyclingClothier(get_valid_addr_obj, get_default_recs_obj)

    expected_response = ("It's 28.0 degrees and Clear. "
                            "Brrrr, ride the bus")
    assert cc.recommend_gear() == expected_response
