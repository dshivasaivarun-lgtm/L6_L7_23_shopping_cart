"""Small shopping-cart parsers used by the Lab 7 fuzzing exercise."""

ZONES = {
    "1": "North",
    "2": "North",
    "3": "West",
    "4": "West",
    "5": "South",
    "6": "South",
    "7": "East",
    "8": "East",
}


def cart_total(cart):
    """Sum valid ``name:pricexqty`` rows and ignore malformed rows."""
    if not isinstance(cart, str):
        return 0

    total = 0
    for item in cart.split(","):
        name, separator, rest = item.partition(":")
        if not separator or not name.strip():
            continue

        price_text, separator, quantity_text = rest.partition("x")
        if not separator:
            continue
        if len(price_text) > 18 or len(quantity_text) > 18:
            continue
        if not price_text.isascii() or not price_text.isdigit():
            continue
        if not quantity_text.isascii() or not quantity_text.isdigit():
            continue

        price = int(price_text)
        quantity = int(quantity_text)
        if quantity > 0:
            total += price * quantity

    return total


def promo_percent(code):
    """Return the value of an OFF<n> code, or zero if the code is invalid."""
    if not isinstance(code, str):
        return 0

    normalized = code.strip().upper()
    if not normalized.startswith("OFF"):
        return 0

    percentage_text = normalized[3:]
    if len(percentage_text) > 3:
        return 0
    if not percentage_text.isascii() or not percentage_text.isdigit():
        return 0

    percentage = int(percentage_text)
    return percentage if percentage <= 100 else 0


def delivery_zone(pincode):
    """Map a six-digit pincode to its zone, or return Unknown if invalid."""
    if not isinstance(pincode, str):
        return "Unknown"

    normalized = pincode.strip()
    if len(normalized) != 6 or not normalized.isascii() or not normalized.isdigit():
        return "Unknown"

    return ZONES.get(normalized[0], "Unknown")


def main():
    print("==== Running cart_total ====")
    user_input = input("Enter cart as name:pricexqty CSV (e.g. pen:10x2,book:250x1): ")
    result = cart_total(user_input)
    print("Cart Total:", result)

    print("\n==== Running promo_percent ====")
    user_input = input("Enter a promo code (e.g. OFF20): ")
    result = promo_percent(user_input)
    print("Discount Percent:", result)

    print("\n==== Running delivery_zone ====")
    user_input = input("Enter a 6 digit pincode (e.g. 560085): ")
    result = delivery_zone(user_input)
    print("Delivery Zone:", result)


if __name__ == "__main__":
    main()
