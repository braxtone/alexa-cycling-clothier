import pytest
from cyclingclothier.recommendation import Recommendation, DefaultRecommendation

VALID_RECOMMENDATION_FILENAME = './tests/valid_recommendation.json'
INVALID_RECOMMENDATION_FILENAME = './tests/invalid_recommendation.json'

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
    assert get_dr_object.recommend('undershirt', temperature) == 'dri-fit'
    assert get_dr_object.recommend('boot_covers', temperature) == None
    assert get_dr_object.recommend('pants', temperature) == 'tights'
    assert get_dr_object.recommend('jersey', temperature) == 'longsleeve'
    assert get_dr_object.recommend('gloves', temperature) == 'full-finger'
    assert get_dr_object.recommend('facemask', temperature) == None
