import pytest

from mobile.pages.api_demos_home import TextFieldsScreen


@pytest.mark.mobile
@pytest.mark.regression
def test_text_input_accepts_and_retains_value(home_screen):
    home_screen.open_category("Views").open_item("Controls").open_item("1. Light Theme")

    screen = TextFieldsScreen(home_screen.driver)
    screen.enter_text("Appium automation")
    assert screen.entered_text() == "Appium automation"


@pytest.mark.mobile
@pytest.mark.regression
def test_checkbox_toggles_state(home_screen):
    home_screen.open_category("Views").open_item("Controls").open_item("1. Light Theme")

    screen = TextFieldsScreen(home_screen.driver)
    initial = screen.checkbox_is_checked()
    screen.toggle_checkbox()
    assert screen.checkbox_is_checked() is not initial, "Checkbox state did not change"


@pytest.mark.mobile
@pytest.mark.regression
def test_long_press_opens_context_menu(home_screen):
    """Views > Context Menu exposes a long-press target that raises a menu."""
    from appium.webdriver.common.appiumby import AppiumBy

    screen = home_screen.open_category("Views").open_item("Context Menu")
    target = (AppiumBy.ANDROID_UIAUTOMATOR,
              'new UiSelector().textContains("long-press")')

    screen.long_press(target)
    assert screen.is_visible(
        (AppiumBy.ID, "android:id/title"), timeout=10
    ), "Long press did not raise the context menu"


@pytest.mark.mobile
@pytest.mark.regression
def test_swipe_gesture_scrolls_the_list(home_screen):
    before = home_screen.category_labels()
    home_screen.swipe(direction="up", percent=0.8)
    after = home_screen.category_labels()
    assert before != after, "Swipe did not change the visible rows"


@pytest.mark.mobile
@pytest.mark.regression
def test_rotation_preserves_the_current_screen(home_screen):
    screen = home_screen.open_views()
    assert screen.is_loaded()

    screen.rotate("LANDSCAPE")
    assert screen.is_loaded(), "Screen lost its state after rotating to landscape"

    screen.rotate("PORTRAIT")
    assert screen.is_loaded()


@pytest.mark.mobile
@pytest.mark.negative
def test_unknown_item_is_not_present(home_screen):
    screen = home_screen.open_views()
    assert not screen.has_item("This Item Does Not Exist")
