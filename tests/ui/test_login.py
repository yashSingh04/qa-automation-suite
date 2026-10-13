import pytest

from utils.config import Config


@pytest.mark.ui
@pytest.mark.smoke
def test_valid_login_lands_on_inventory(login_page):
    inventory = login_page.login(Config.STANDARD_USER, Config.PASSWORD)
    assert inventory.is_loaded()
    assert inventory.title == "Products"


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("ghost_user", "secret_sauce", "Username and password do not match"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("", "", "Username is required"),
    ],
    ids=["bad-password", "unknown-user", "no-username", "no-password", "both-empty"],
)
def test_invalid_login_shows_expected_error(login_page, username, password, expected):
    login_page.login(username, password)
    assert login_page.has_error(), "Expected an error banner but none appeared"
    assert expected in login_page.error_message


@pytest.mark.ui
@pytest.mark.negative
def test_locked_out_user_is_rejected(login_page):
    login_page.login(Config.LOCKED_USER, Config.PASSWORD)
    assert login_page.has_error()
    assert "locked out" in login_page.error_message.lower()
