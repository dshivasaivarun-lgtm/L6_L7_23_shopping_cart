"""Branch coverage tests for the shopping cart application."""

import pytest

from shopping_cart import cart_discount, item_total, shipping_fee


@pytest.mark.parametrize(
    ("category", "price", "qty", "expected"),
    [
        ("food", 100, 1, 105),
        ("electronics", 100, 9, 1062),
        ("clothing", 100, 10, 1008),
        ("food", 100, 11, 1039),
    ],
)
def test_item_total_valid_paths_and_bulk_decision(category, price, qty, expected):
    assert item_total(category, price, qty) == expected


@pytest.mark.parametrize(
    ("category", "price", "qty", "message"),
    [
        ("unknown", 1, 1, "unknown category"),
        ("food", -1, 1, "invalid price or quantity"),
        ("food", 1, 0, "invalid price or quantity"),
        ("food", 1, -1, "invalid price or quantity"),
    ],
)
def test_item_total_validation_branches(category, price, qty, message):
    with pytest.raises(ValueError, match=message):
        item_total(category, price, qty)


@pytest.mark.parametrize(
    ("value", "prime", "coupon", "expected"),
    [
        (1999, False, "", 0),
        (2000, False, "", 200),
        (5000, False, "", 500),
        (1000, True, "", 100),
        (1000, False, "FLAT10", 100),
        (999, False, "FLAT10", 0),
        (1000, False, "OTHER", 0),
        (1000, True, "FLAT10", 200),
        (2000, True, "FLAT10", 500),
        (5000, True, "FLAT10", 1100),
    ],
)
def test_cart_discount_decision_outcomes(value, prime, coupon, expected):
    assert cart_discount(value, prime, coupon) == expected


@pytest.mark.parametrize(
    ("value", "prime", "express", "expected"),
    [
        (499, True, False, 0),
        (499, False, False, 40),
        (500, False, False, 0),
        (501, False, False, 0),
        (499, False, True, 140),
        (500, False, True, 100),
        (499, True, True, 50),
    ],
)
def test_shipping_decision_outcomes(value, prime, express, expected):
    assert shipping_fee(value, prime, express) == expected

