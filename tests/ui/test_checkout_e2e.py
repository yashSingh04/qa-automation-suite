import pytest


@pytest.mark.ui
@pytest.mark.e2e
def test_full_purchase_journey(inventory_page):
    """Login -> add two items -> cart -> checkout -> totals -> confirmation."""
    products = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    for product in products:
        inventory_page.add_to_cart(product)
    assert inventory_page.cart_count() == len(products)

    cart = inventory_page.go_to_cart()
    assert cart.is_loaded()
    assert cart.item_count() == len(products)
    assert sorted(cart.item_names()) == sorted(products)

    checkout = cart.checkout()
    checkout.fill_details("Yash", "Singh", "122001")

    # Tax should be a positive amount and the total must reconcile exactly.
    assert checkout.tax > 0
    assert round(checkout.subtotal + checkout.tax, 2) == checkout.total

    checkout.finish()
    assert checkout.is_order_complete()
    assert "thank you for your order" in checkout.confirmation_text.lower()


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize(
    "first,last,postcode,expected",
    [
        ("", "Singh", "122001", "First Name is required"),
        ("Yash", "", "122001", "Last Name is required"),
        ("Yash", "Singh", "", "Postal Code is required"),
    ],
    ids=["no-first-name", "no-last-name", "no-postcode"],
)
def test_checkout_rejects_incomplete_details(inventory_page, first, last, postcode, expected):
    inventory_page.add_to_cart("Sauce Labs Backpack")
    checkout = inventory_page.go_to_cart().checkout()
    checkout.fill_details(first, last, postcode)
    assert checkout.has_error()
    assert expected in checkout.error_message
