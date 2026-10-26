"""Equivalence-partition and boundary tests for calculate_discount."""
import pytest

from app.tasks import calculate_discount


@pytest.mark.parametrize(
    ("price", "is_premium", "expected"),
    [
        pytest.param(100, True, 80, id="TC-01-premium-standard-price"),
        pytest.param(100, False, 100, id="TC-02-regular-standard-price"),
        pytest.param(0, True, 0, id="TC-03-premium-zero-boundary"),
        pytest.param(0, False, 0, id="TC-04-regular-zero-boundary"),
        pytest.param(0.01, True, 0.008, id="TC-05-premium-just-above-zero"),
        pytest.param(0.01, False, 0.01, id="TC-06-regular-just-above-zero"),
        pytest.param(0.005, True, 0.004, id="TC-07-premium-sub-cent-no-rounding"),
        pytest.param(0.005, False, 0.005, id="TC-08-regular-sub-cent-no-rounding"),
    ],
)
def test_valid_price_and_premium_partitions(price, is_premium, expected):
    assert calculate_discount(price, is_premium) == pytest.approx(expected)


@pytest.mark.parametrize(
    "price",
    [
        pytest.param(-0.01, id="TC-09-negative-price"),
        pytest.param(float("nan"), id="TC-10-nan-price"),
        pytest.param(float("inf"), id="TC-11-positive-infinity-price"),
        pytest.param(float("-inf"), id="TC-12-negative-infinity-price"),
    ],
)
def test_invalid_numeric_prices_are_rejected(price):
    with pytest.raises(ValueError):
        calculate_discount(price, True)


@pytest.mark.parametrize(
    "price",
    [
        pytest.param("100", id="TC-13-string-price"),
        pytest.param(True, id="TC-14-boolean-price"),
    ],
)
def test_invalid_price_types_are_rejected(price):
    with pytest.raises(TypeError):
        calculate_discount(price, False)


@pytest.mark.parametrize(
    "is_premium",
    [
        pytest.param(1, id="TC-15-integer-one-flag"),
        pytest.param(0, id="TC-16-integer-zero-flag"),
        pytest.param(None, id="TC-17-none-flag"),
        pytest.param("true", id="TC-18-string-flag"),
    ],
)
def test_non_boolean_premium_flags_are_rejected(is_premium):
    with pytest.raises(TypeError):
        calculate_discount(100, is_premium)
