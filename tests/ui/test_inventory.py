import pytest


@pytest.mark.ui
@pytest.mark.smoke
def test_inventory_lists_all_products(inventory_page):
    assert inventory_page.item_count() == 6


@pytest.mark.ui
@pytest.mark.regression
def test_add_and_remove_updates_cart_badge(inventory_page):
    assert inventory_page.cart_count() == 0
    inventory_page.add_to_cart("Sauce Labs Backpack")
    assert inventory_page.cart_count() == 1
    inventory_page.add_to_cart("Sauce Labs Bike Light")
    assert inventory_page.cart_count() == 2
    inventory_page.remove_from_cart("Sauce Labs Backpack")
    assert inventory_page.cart_count() == 1


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    "sort_value,key,reverse",
    [
        ("lohi", "price", False),
        ("hilo", "price", True),
        ("az", "name", False),
        ("za", "name", True),
    ],
    ids=["price-asc", "price-desc", "name-asc", "name-desc"],
)
def test_sorting_orders_products_correctly(inventory_page, sort_value, key, reverse):
    inventory_page.sort_by(sort_value)
    actual = inventory_page.prices() if key == "price" else inventory_page.product_names()
    assert actual == sorted(actual, reverse=reverse), f"{sort_value} sort is not applied"
