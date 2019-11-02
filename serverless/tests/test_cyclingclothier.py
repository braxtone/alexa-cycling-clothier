import pytest

from cyclingclothier.core import CyclingClothier

@pytest.fixture
def set_ds_key_key(monkeypatch):
    monkeypatch.setenv("DARKSKY_API_KEY_KEY", "env:DARKSKY_API_KEY")

@pytest.fixture
def set_ds_key(monkeypatch):
    monkeypatch.setenv("DARKSKY_API_KEY", "alsdkfjwoeijwfojiwe")

@pytest.mark.usefixtures('set_ds_key', 'set_ds_key_key')
def test_core_constructor_neg():
    not_addr = { "stuff": "things" }

    # Ensure there's some basic input validation
    with pytest.raises(TypeError):
        CyclingClothier(not_addr)


@pytest.mark.usefixtures('set_ds_key', 'set_ds_key_key', 'set_ds_key')
def test_core_constructor():
    # A proper input parameter shouldn't raise an exception
    import yaml
    from ask_sdk_model.services.device_address.address import Address

    addr = yaml.load(open('./tests/valid_addr.yaml'), Loader=yaml.FullLoader)
    cc = CyclingClothier(addr)
    assert isinstance(cc, CyclingClothier)

