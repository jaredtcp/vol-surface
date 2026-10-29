import numpy as np
from fontTools.ttLib.beyond64k import upper_tables
from scipy.stats import norm
from scipy.optimize import brentq

def d1_d2(S, K, T, r, q, sigma):
    d1 = (np.log(S / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2

def bs_price(S, K, T, r, q, sigma, option_type):
    d1, d2 = d1_d2(S, K, T, r, q, sigma)
    if option_type == "call":
        call_price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        return call_price
    elif option_type == "put":
        put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
        return put_price
    else:
        raise ValueError("option_type must be 'call' or 'put'")

def bs_delta(S, K, T, r, q, sigma, option_type):
    d1, _ = d1_d2(S, K, T, r, q, sigma)
    if option_type == "call":
        call_delta = np.exp(-q * T) * norm.cdf(d1)
        return call_delta
    elif option_type == "put":
        put_delta = - np.exp(-q * T) * norm.cdf(-d1)
        return put_delta
    else:
        raise ValueError("option_type must be 'call' or 'put'")

def bs_vega(S, K, T, r, q, sigma):
    d1, _ = d1_d2(S, K, T, r, q, sigma)
    vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)
    return vega

def price_gap(sigma, S, K, T, r, q, option_type, market_price):
    return bs_price(S, K, T, r, q, sigma, option_type) - market_price

def price_bounds(S, K, T, r, q, option_type):
    if option_type == 'call':
        lower = max(S * np.exp(-q * T) - K * np.exp(-r * T), 0)
        upper = S * np.exp(-q * T)
        return lower, upper
    elif option_type == 'put':
        lower = max(K * np.exp(-r * T) - S * np.exp(-q * T), 0)
        upper = K * np.exp(-r * T)
        return lower, upper
    else:
        raise ValueError("option_type must be 'call' or 'put'")

def implied_vol(S, K, T, r, q, option_type, market_price):
    lower, upper = price_bounds(S, K, T, r, q, option_type)
    if market_price <= lower or market_price >= upper:
        return np.nan
    else:
        vol = brentq(price_gap, 1e-6, 5, args=(S, K, T, r, q, option_type, market_price))
        return vol


if __name__ == "__main__":
    p = bs_price(100, 100, 1, 0.05, 0, 0.2, "call")
    print(implied_vol(100, 100, 1, 0.05, 0, "call", p))
    print(implied_vol(100, 100, 1,0.05, 0, "call", 0.0))
