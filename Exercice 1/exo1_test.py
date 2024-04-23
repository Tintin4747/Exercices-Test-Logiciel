import pytest


@pytest.fixture(scope="function")
def fixture_open_close():
    # Setup
    file = open("file.txt", "r")
    # Retour des informations sur le fichier
    yield file
    # Teardown
    file.close()


@pytest.fixture(scope="function")
def content(fixture_open_close):
    return fixture_open_close.read()


def test_content(content):
    assert content == "Hello world"


def test_file_is_opened(fixture_open_close):
    assert fixture_open_close.closed is False
