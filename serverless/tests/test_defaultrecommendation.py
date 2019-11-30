import pytest
from cyclingclothier.recommendation import Recommendation, DefaultRecommendation

VALID_RECOMMENDATION_FILENAME = './tests/valid_recommendation.json'
INVALID_RECOMMENDATION_FILENAME = './tests/invalid_recommendation.json'

# @pytest.fixture
# def set_ds_key_key(monkeypatch):
#     monkeypatch.setenv("DARKSKY_API_KEY_KEY", "env:DARKSKY_API_KEY")
# 
# @pytest.fixture
# def set_ds_key(monkeypatch):
#     monkeypatch.setenv("DARKSKY_API_KEY", "alsdkfjwoeijwfojiwe")
# 
# @pytest.fixture
# def set_function_name(monkeypatch):
#     monkeypatch.setenv('FUNCTION_NAME', 'CyclingClothier-pytest')
# 
# @pytest.fixture()
# def get_valid_addr_obj():
#     import yaml
#     from ask_sdk_model.services.device_address.address import Address
# 
#     addr = yaml.load(open(VALID_ADDR_OBJ_FILENAME), Loader=yaml.FullLoader)
#     return addr
# 
# 
# class MockDarkSky:
#     @staticmethod
#     def get_forecast():
#         import yaml
#         from darksky.forecast import CurrentlyForecast
# 
#         current_forecast = yaml.load(open(VALID_CURRENT_FORECAST_OBJ_FILENAME),
#                                      Loader=yaml.FullLoader)
#         return current_forecast
# 
# @pytest.fixture
# def mock_current_forecast(monkeypatch):
# 
#     def mock_get_current_forecast(*args, **kwargs):
#         return MockDarkSky().get_forecast()
# 
#     monkeypatch.setattr(CyclingClothier, "_get_current_forecast", mock_get_current_forecast)

# @pytest.mark.usefixtures('set_ds_key', 'set_ds_key_key')
# def test_core_constructor_neg():
#     # Ensure there's some basic input validation
#     with pytest.raises(TypeError):
#         CyclingClothier(not_addr)

def test_constructor():
    # Test valid recommendations file returns DefaultRecommendation object
    dr = DefaultRecommendation(VALID_RECOMMENDATION_FILENAME)
    assert isinstance(dr, Recommendation)

def test_constructor_neg():
    with pytest.raises(ValueError):
        dr = DefaultRecommendation(INVALID_RECOMMENDATION_FILENAME)
        
# @pytest.mark.usefixtures('set_ds_key', 'set_ds_key_key',
#                          'set_function_name')
# def test_default_gear_recommendation(get_valid_addr_obj,
#                                  mock_current_forecast):
#     # TODO: Mock calls for address to location translation
#     cc = CyclingClothier(get_valid_addr_obj)
# 
#     expected_response = ("It's 42.0 degrees and Clear, "
#                          "so you should wear biking tights, a dri-fit base layer, "
#                          "longsleeve jersey, full-finger gloves.")
#     assert cc.recommend_gear() == expected_response
