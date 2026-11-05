"""Line coverage tests for the shopping cart application."""

import pytest

from shopping_cart import cart_discount, item_total, shipping_fee


@pytest.mark.parametrize(
    ("category", "price", "qty", "expected"),
    [
        ("food", 100, 2, 210),
        ("electronics", 100, 1, 118),
        ("clothing", 100, 1, 112),
        ("food", 100, 9, 945),
        ("food", 100, 10, 945),
        ("food", 100, 11, 1039),
    ],
)
def test_item_totals_for_categories_and_bulk_boundaries(category, price, qty, expected):
    assert item_total(category, price, qty) == expected


@pytest.mark.parametrize(
    ("category", "price", "qty", "message"),
    [
        ("toys", 10, 1, "unknown category"),
        ("food", -1, 1, "invalid price or quantity"),
        ("food", 1, 0, "invalid price or quantity"),
        ("food", 1, -1, "invalid price or quantity"),
    ],
)
def test_item_total_rejects_invalid_inputs(category, price, qty, message):
    with pytest.raises(ValueError, match=message):
        item_total(category, price, qty)


@pytest.mark.parametrize(
    ("cart_value", "prime", "coupon", "expected"),
    [
        (1999, False, "", 0),
        (2000, False, "", 200),
        (4999, False, "", 200),
        (5000, False, "", 500),
        (6000, False, "", 500),
        (1999, True, "", 100),
        (2000, True, "", 300),
        (5000, True, "", 600),
        (999, False, "FLAT10", 0),
        (1000, False, "FLAT10", 100),
        (2500, False, "FLAT10", 450),
        (2500, True, "FLAT10", 550),
        (6000, True, "FLAT10", 1200),
        (6000, False, "INVALID", 500),
    ],
)
def test_cart_discount_rules(cart_value, prime, coupon, expected):
    assert cart_discount(cart_value, prime, coupon) == expected


@pytest.mark.parametrize(
    ("cart_value", "prime", "express", "expected"),
    [
        (499, True, False, 0),
        (499, False, False, 40),
        (500, False, False, 0),
        (501, False, False, 0),
        (499, False, True, 140),
        (500, False, True, 100),
        (499, True, True, 50),
        (500, True, True, 50),
    ],
)
def test_shipping_fee_rules(cart_value, prime, express, expected):
    assert shipping_fee(cart_value, prime, express) == expected


