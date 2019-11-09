import pytest

from cyclingclothier.core import CyclingClothier

VALID_ADDR_OBJ_FILENAME = './tests/valid_addr.yaml'
VALID_CURRENT_FORECAST_OBJ_FILENAME = './tests/valid_current_forecast.yaml'

@pytest.fixture
def set_ds_key_key(monkeypatch):
    monkeypatch.setenv("DARKSKY_API_KEY_KEY", "env:DARKSKY_API_KEY")

@pytest.fixture
def set_ds_key(monkeypatch):
    monkeypatch.setenv("DARKSKY_API_KEY", "alsdkfjwoeijwfojiwe")

@pytest.fixture
def set_function_name(monkeypatch):
    monkeypatch.setenv('FUNCTION_NAME', 'CyclingClothier-pytest')

@pytest.fixture()
def get_valid_addr_obj():
    import yaml
    from ask_sdk_model.services.device_address.address import Address

    addr = yaml.load(open('./tests/valid_addr.yaml'), Loader=yaml.FullLoader)
    return addr


class MockDarkSky:
    @staticmethod
    def get_forecast():
        import yaml
        from darksky.forecast import CurrentlyForecast

        current_forecast = yaml.load(open(VALID_CURRENT_FORECAST_OBJ_FILENAME),
                                     Loader=yaml.FullLoader)
        return current_forecast

@pytest.fixture
def mock_current_forecast(monkeypatch):

    def mock_get_current_forecast(*args, **kwargs):
        return MockDarkSky().get_forecast()

    monkeypatch.setattr(CyclingClothier, "_get_current_forecast", mock_get_current_forecast)

@pytest.mark.usefixtures('set_ds_key', 'set_ds_key_key')
def test_core_constructor_neg():
    not_addr = { "stuff": "things" }

    # Ensure there's some basic input validation
    with pytest.raises(TypeError):
        CyclingClothier(not_addr)

@pytest.mark.usefixtures('set_ds_key', 'set_ds_key_key')
def test_core_constructor(get_valid_addr_obj):
    # Test valid Address object returns CyclingClothier object
    # Bless you https://stackoverflow.com/a/25560086/1183198
    cc = CyclingClothier(get_valid_addr_obj)
    assert isinstance(cc, CyclingClothier)

@pytest.mark.usefixtures('set_ds_key', 'set_ds_key_key',
                         'set_function_name')
def test_get_gear_recommendation(get_valid_addr_obj,
                                 mock_current_forecast):
    cc = CyclingClothier(get_valid_addr_obj)

    expected_response = ("It's 42.0 degrees with clear skies,"
                         "so you should wear a dri-fit base layer, short sleeve jersey,"
                         "and long pants.")
    assert cc.recommend_gear() == expected_response
