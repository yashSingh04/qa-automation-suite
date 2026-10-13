import pytest

from mobile.pages.api_demos_home import ApiDemosHome


@pytest.mark.mobile
@pytest.mark.smoke
def test_app_launches_to_home_screen(home_screen):
    assert home_screen.is_loaded()
    assert home_screen.current_activity.endswith("ApiDemos")


@pytest.mark.mobile
@pytest.mark.smoke
def test_home_screen_lists_expected_categories(home_screen):
    labels = home_screen.category_labels()
    assert labels, "Category list came back empty"
    # The first screenful should start with the alphabetically-first categories.
    assert labels[0] == "Accessibility"
    for expected in ["Accessibility", "Animation", "App", "Content"]:
        assert expected in labels


@pytest.mark.mobile
@pytest.mark.regression
@pytest.mark.parametrize(
    "category",
    ["Accessibility", "Animation", "App", "Content", "Graphics", "Views"],
)
def test_each_category_opens_a_populated_screen(home_screen, category):
    screen = home_screen.open_category(category)
    assert screen.is_loaded(), f"{category} did not open a list screen"
    assert screen.item_labels(), f"{category} opened but contained no items"


@pytest.mark.mobile
@pytest.mark.regression
def test_back_navigation_returns_to_home(home_screen):
    screen = home_screen.open_views()
    assert screen.is_loaded()

    screen.back()
    assert ApiDemosHome(screen.driver).is_loaded(), "Back did not return to the home list"


@pytest.mark.mobile
@pytest.mark.regression
def test_scrolling_reveals_offscreen_categories(home_screen):
    """'Views' sits below the fold on most screen sizes and needs a scroll."""
    element = home_screen.scroll_to_text("Views")
    assert element.is_displayed()
