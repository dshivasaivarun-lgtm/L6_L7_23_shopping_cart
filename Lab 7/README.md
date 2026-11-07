# L6_L7_23_shopping_cart — Shopping Cart

Lab 7: Fuzz Testing

## Files

| File | Description |
|------|-------------|
| `shopping_cart.py` | Buggy code to test and fix |
| `test_shopping_cart.py` | Fuzz test file to complete using Hypothesis |

Refer to the lab handout for instructions.

## Fuzz test behavior

Install the test dependencies and run the suite from this directory:

```powershell
python -m pip install pytest hypothesis
python -m pytest -q
```

The parsers keep valid-input behavior and handle malformed input without raising:

- `cart_total` adds valid `name:pricexqty` rows and ignores malformed rows; non-string input returns `0`.
- `promo_percent` accepts case-insensitive `OFF0` through `OFF100`; other input returns `0`.
- `delivery_zone` accepts six-digit pincodes beginning with `1` through `8`; other input returns `Unknown`.
