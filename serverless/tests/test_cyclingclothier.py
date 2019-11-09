import pytest

from cyclingclothier.core import CyclingClothier

VALID_ADDR_OBJ_FILENAME = './tests/valid_addr.yaml'

@pytest.fixture
def set_ds_key_key(monkeypatch):
    monkeypatch.setenv("DARKSKY_API_KEY_KEY", "env:DARKSKY_API_KEY")

@pytest.fixture
def set_ds_key(monkeypatch):
    monkeypatch.setenv("DARKSKY_API_KEY", "alsdkfjwoeijwfojiwe")

@pytest.fixture()
def get_valid_addr_obj():
    # A proper input parameter shouldn't raise an exception
    import yaml
    from ask_sdk_model.services.device_address.address import Address

    addr = yaml.load(open('./tests/valid_addr.yaml'), Loader=yaml.FullLoader)
    return addr

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
