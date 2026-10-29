import numpy as np
import pytest
from src.pricing import bs_price, implied_vol, bs_delta, bs_vega


@pytest.mark.parametrize("S, K, T, r, q, sigma",
                         [(100, 100, 1, 0.05, 0.02, 0.2),
                          (100, 80, 0.5, 0.03, 0.0, 0.3)])


def test_put_call_parity(S, K, T, r, q, sigma):
    call = bs_price(S, K, T, r, q, sigma, 'call')
    put = bs_price(S, K, T, r, q, sigma, 'put')
    rhs = S * np.exp(-q * T) - K * np.exp(-r * T)
    assert abs(call - put - rhs) < 1e-10

@pytest.mark.parametrize("sigma", [0.1, 0.2, 0.5])
@pytest.mark.parametrize("K", [80, 100, 120])
@pytest.mark.parametrize("option_type", ["call", "put"])


def test_iv_round_trip(sigma, K, option_type):
    S = 100
    T = 0.5
    r = 0.04
    q = 0.01
    price = bs_price(S, K, T, r, q, sigma, option_type)
    recovered = implied_vol(S, K, T, r, q, option_type, price)
    assert abs(recovered - sigma) < 1e-6

@pytest.mark.parametrize("option_type", ["call", "put"])
@pytest.mark.parametrize("K", [80, 100, 120])

def test_delta_matches_slope(option_type, K):
    S = 100
    T = 0.5
    r = 0.04
    q = 0.01
    sigma = 0.2
    h = 0.01
    up = bs_price(S + h, K , T, r, q, sigma, option_type)
    down = bs_price(S - h, K , T, r, q, sigma, option_type)
    slope = (up - down) / (2 * h)
    analytic =  bs_delta(S, K, T, r, q, sigma, option_type)
    assert abs(slope - analytic) < 1e-4

@pytest.mark.parametrize("K", [80, 100,120])

def test_vega_matches_slope(K):
    S = 100
    T = 0.5
    r = 0.04
    q = 0.01
    sigma = 0.2
    h = 0.0001
    up = bs_price(S, K, T, r, q, sigma + h, 'call')
    down = bs_price(S, K, T, r, q, sigma - h, 'call')
    slope = (up - down) / (2 * h)
    analytic = bs_vega(S, K, T, r, q, sigma)
    assert abs(slope - analytic) < 1e-4