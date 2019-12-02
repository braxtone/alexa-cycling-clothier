import pytest
from cyclingclothier.recommendation import Recommendation, DefaultRecommendation, UnknownGearTypeException

VALID_RECOMMENDATION_FILENAME = './tests/recommendation_valid.json'
INVALID_RECOMMENDATION_FILENAME = './tests/recommendation_invalid.json'

@pytest.fixture
def get_dr_object():
    return DefaultRecommendation(VALID_RECOMMENDATION_FILENAME)

def test_constructor():
    # Test valid recommendations file returns DefaultRecommendation object
    dr = DefaultRecommendation(VALID_RECOMMENDATION_FILENAME)
    assert isinstance(dr, Recommendation)

def test_constructor_neg():
    with pytest.raises(ValueError):
        dr = DefaultRecommendation(INVALID_RECOMMENDATION_FILENAME)
        
def test_individual_recommendations(get_dr_object):
    temperature = 42.0
    with pytest.raises(UnknownGearTypeException):
        get_dr_object.recommend('wetsuit', temperature)
    assert get_dr_object.recommend('undershirt', temperature).recommendation == 'dri-fit'
    assert get_dr_object.recommend('boot_covers', temperature).recommendation == None
    assert get_dr_object.recommend('pants', temperature).recommendation == 'tights'
    assert get_dr_object.recommend('jersey', temperature).recommendation == 'longsleeve'
    assert get_dr_object.recommend('gloves', temperature).recommendation == 'full-finger'
    assert get_dr_object.recommend('facemask', temperature).recommendation == None
