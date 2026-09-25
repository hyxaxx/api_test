import pytest
import requests

@pytest.fixture
def session():
    s = requests.Session()
    yield s
    s.close()