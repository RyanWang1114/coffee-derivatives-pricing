import math
import unittest
from pricing import cost_of_carry, black76_call, black_scholes_call, monte_carlo_call


class PricingTests(unittest.TestCase):
    def test_reference_values(self):
        f = cost_of_carry(1.2, .02, .01, .5)
        self.assertAlmostEqual(f, 1.21813568, places=8)
        self.assertAlmostEqual(black76_call(f, 1.25, .02, .5, .25), .07119, places=5)
        self.assertAlmostEqual(black_scholes_call(1.2, 1.25, .02, .5, .25), .06836, places=5)

    def test_simulation_matches_analytical_price(self):
        f = cost_of_carry(1.2, .02, .01, .5)
        analytical = black76_call(f, 1.25, .02, .5, .25)
        mc = monte_carlo_call(f, 1.25, .02, .5, .25, seed=42)
        self.assertLessEqual(mc.ci95_low, analytical)
        self.assertGreaterEqual(mc.ci95_high, analytical)

    def test_expiry_and_zero_volatility(self):
        self.assertAlmostEqual(black76_call(1.4, 1.25, .02, 0, .25), .15)
        expected = math.exp(-.02 * .5) * .15
        self.assertAlmostEqual(black76_call(1.4, 1.25, .02, .5, 0), expected)
        mc = monte_carlo_call(1.4, 1.25, .02, .5, 0)
        self.assertAlmostEqual(mc.price, expected)
        self.assertAlmostEqual(mc.standard_error, 0)

    def test_bounds_and_sensitivity(self):
        for f in (.8, 1.2, 1.6):
            price = black76_call(f, 1.25, .02, .5, .25)
            self.assertGreaterEqual(price, math.exp(-.02 * .5) * max(f - 1.25, 0))
            self.assertLessEqual(price, math.exp(-.02 * .5) * f)
        self.assertLess(black76_call(1.2, 1.25, .02, .5, .15),
                        black76_call(1.2, 1.25, .02, .5, .35))

    def test_invalid_inputs(self):
        for args in [(0, 1, .02, .5, .25), (1, -1, .02, .5, .25),
                     (1, 1, float('nan'), .5, .25), (1, 1, .02, -.5, .25),
                     (1, 1, .02, .5, -.25)]:
            with self.assertRaises(ValueError):
                black76_call(*args)
        for count in (True, 1, 2.5):
            with self.assertRaises(ValueError):
                monte_carlo_call(1.2, 1.25, .02, .5, .25, simulations=count)


if __name__ == '__main__':
    unittest.main()
