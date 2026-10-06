"""Educational European-call pricing with continuously compounded annual rates.

Prices and strikes use dollars per pound; maturity is measured in years.
"""
from dataclasses import dataclass
from math import erf, exp, isfinite, log, sqrt
import numpy as np


def _positive(name, value):
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")


def _finite(name, value):
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")


def _inputs(price, strike, rate, maturity, volatility):
    _positive("price", price)
    _positive("strike", strike)
    _finite("rate", rate)
    for name, value in [("maturity", maturity), ("volatility", volatility)]:
        _finite(name, value)
        if value < 0:
            raise ValueError(f"{name} must be nonnegative")


def _cdf(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


def cost_of_carry(spot, rate, storage_rate, maturity, convenience_yield=0.0):
    """Simplified forward/futures benchmark with proportional storage costs.

    Assumes deterministic rates, no delivery frictions, and equivalence of
    forwards and futures under these assumptions. Storage is an annual rate.
    """
    _positive("spot", spot)
    for name, value in [("rate", rate), ("storage_rate", storage_rate),
                        ("convenience_yield", convenience_yield)]:
        _finite(name, value)
    _finite("maturity", maturity)
    if maturity < 0:
        raise ValueError("maturity must be nonnegative")
    return spot * exp((rate + storage_rate - convenience_yield) * maturity)


def black76_call(futures, strike, rate, maturity, volatility):
    """Black's model for a European call on futures."""
    _inputs(futures, strike, rate, maturity, volatility)
    discount = exp(-rate * maturity)
    if maturity == 0 or volatility == 0:
        return discount * max(futures - strike, 0.0)
    width = volatility * sqrt(maturity)
    d1 = log(futures / strike) / width + width / 2
    d2 = d1 - width
    return discount * (futures * _cdf(d1) - strike * _cdf(d2))


def black_scholes_call(spot, strike, rate, maturity, volatility):
    """European spot call with no dividends or commodity storage adjustment.

    This is a separate model example, not the coffee futures-option benchmark.
    """
    _inputs(spot, strike, rate, maturity, volatility)
    return black76_call(spot * exp(rate * maturity), strike, rate,
                        maturity, volatility)


@dataclass(frozen=True)
class MonteCarloResult:
    price: float
    standard_error: float
    ci95_low: float
    ci95_high: float
    simulations: int


def monte_carlo_call(futures, strike, rate, maturity, volatility,
                     simulations=100_000, seed=42):
    """Risk-neutral terminal simulation matching Black's futures model.

    The 95% interval uses a normal approximation to the sample-mean sampling
    distribution; it measures numerical uncertainty, not model uncertainty.
    """
    _inputs(futures, strike, rate, maturity, volatility)
    if isinstance(simulations, bool) or not isinstance(simulations, int) or simulations < 2:
        raise ValueError("simulations must be an integer of at least 2")
    rng = np.random.default_rng(seed)
    terminal = futures * np.exp(-0.5 * volatility**2 * maturity
                                + volatility * sqrt(maturity)
                                * rng.standard_normal(simulations))
    discounted = exp(-rate * maturity) * np.maximum(terminal - strike, 0)
    price = float(discounted.mean())
    se = float(discounted.std(ddof=1) / sqrt(simulations))
    return MonteCarloResult(price, se, price - 1.96 * se,
                           price + 1.96 * se, simulations)
