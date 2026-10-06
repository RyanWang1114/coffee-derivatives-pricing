"""Run from the repository root: python compare_models.py."""
from pricing import (cost_of_carry, black76_call, black_scholes_call,
                     monte_carlo_call)


def main():
    spot, strike, rate, storage, maturity, volatility = 1.20, 1.25, 0.02, 0.01, 0.5, 0.25
    futures = cost_of_carry(spot, rate, storage, maturity)
    analytical = black76_call(futures, strike, rate, maturity, volatility)
    mc = monte_carlo_call(futures, strike, rate, maturity, volatility)
    print("Illustrative coffee example; all prices are USD per pound.")
    print(f"Cost-of-carry futures benchmark: {futures:.8f}")
    print(f"Black futures call:             {analytical:.8f}")
    print(f"Monte Carlo futures call:       {mc.price:.8f}")
    print(f"Monte Carlo standard error:     {mc.standard_error:.8f}")
    print(f"Approximate 95% interval:       [{mc.ci95_low:.8f}, {mc.ci95_high:.8f}]")
    print(f"Analytical price in interval:   {mc.ci95_low <= analytical <= mc.ci95_high}")
    print(f"Spot call (different model):    {black_scholes_call(spot, strike, rate, maturity, volatility):.8f}")
    print("\nVolatility sensitivity (Black futures call):")
    for vol in (0.15, 0.25, 0.35):
        print(f"  {vol:.0%}: {black76_call(futures, strike, rate, maturity, vol):.8f}")


if __name__ == "__main__":
    main()
