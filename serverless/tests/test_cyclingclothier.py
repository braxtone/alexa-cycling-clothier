import pytest
from cyclingclothier.core import CyclingClothier

def test_core_constructor(monkeypatch):
    not_addr = { "stuff": "things" }
    monkeypatch.setenv("DARKSKY_API_KEY_KEY", "env:DARKSKY_API_KEY")
    monkeypatch.setenv("DARKSKY_API_KEY", "alsdkfjwoeijwfojiwe")

    # Ensure there's some basic input validation
    with pytest.raises(TypeError):
        CyclingClothier(not_addr)

