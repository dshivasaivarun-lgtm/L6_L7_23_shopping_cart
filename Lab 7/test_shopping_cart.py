"""Property-based tests for the shopping cart input parsers."""

from hypothesis import given, strategies as st

from shopping_cart import cart_total, delivery_zone, promo_percent


@given(st.text() | st.none())
def test_cart_total_arbitrary_input_never_crashes(value):
    result = cart_total(value)
    assert isinstance(result, int)
    assert result >= 0


@given(st.text() | st.none())
def test_promo_percent_arbitrary_input_never_crashes(value):
    result = promo_percent(value)
    assert isinstance(result, int)
    assert 0 <= result <= 100


@given(st.text() | st.none())
def test_delivery_zone_arbitrary_input_never_crashes(value):
    assert delivery_zone(value) in {"North", "West", "South", "East", "Unknown"}


@given(
    st.lists(
        st.tuples(
            st.text(min_size=1, max_size=10).filter(lambda name: ":" not in name and "," not in name),
            st.integers(min_value=0, max_value=1_000_000),
            st.integers(min_value=1, max_value=1000),
        ),
        min_size=1,
        max_size=10,
    )
)
def test_cart_total_sums_well_formed_items(items):
    cart = ",".join(f"{name}:{price}x{quantity}" for name, price, quantity in items)
    assert cart_total(cart) == sum(price * quantity for _, price, quantity in items)


@given(st.integers(min_value=0, max_value=100))
def test_promo_percent_parses_valid_codes(percent):
    assert promo_percent(f"OFF{percent}") == percent


@given(st.integers(min_value=1, max_value=8), st.text(alphabet="0123456789", min_size=5, max_size=5))
def test_delivery_zone_maps_six_digit_pincodes(first_digit, suffix):
    expected = {
        1: "North", 2: "North", 3: "West", 4: "West",
        5: "South", 6: "South", 7: "East", 8: "East",
    }[first_digit]
    assert delivery_zone(f"{first_digit}{suffix}") == expected


def test_cart_total_ignores_malformed_rows_and_keeps_valid_rows():
    assert cart_total("pen:10x2,broken,book:250x1,coin:nope") == 270


def test_cart_total_ignores_invalid_numbers_and_oversized_fields():
    assert cart_total("bad:-10x1,bad:1.5x2,bad:2x0,bad:1x2x3,bad:9999999999999999999x1") == 0


def test_invalid_promo_code_returns_zero():
    assert promo_percent("SAVE20") == 0
    assert promo_percent("OFF101") == 0
    assert promo_percent("OFF" + "9" * 5000) == 0


def test_invalid_pincode_returns_unknown():
    assert delivery_zone("") == "Unknown"
    assert delivery_zone("960085") == "Unknown"
