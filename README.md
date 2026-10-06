# Coffee derivatives pricing

An educational Python case study comparing cost-of-carry pricing, Black's
European futures-option model, and Monte Carlo valuation. The central question
is: **Can a risk-neutral simulation reproduce the analytical call price under
the same assumptions?** A supporting report connects pricing to a hypothetical
coffee-linked structured note and risk management.

## Context and contribution

This project began with a Citi Markets Quantitative Analysis job simulation on
Forage. It is an educational exercise, not employment at Citi or a live trading
system. The supplied coffee inputs are illustrative rather than current market
observations. Course instructions, model answers, and resource images are not
redistributed here.

The original working folder contained pricing scripts and written scenario
analyses. This portfolio version was refactored and documented with OpenAI Codex
assistance: reusable functions, explicit model distinctions, Monte Carlo
uncertainty, sensitivity output, and validation tests were added. These additions
should not be represented as independently authored work. The owner should
review and be able to explain the code before sharing it professionally.

## Models

| Model | Question answered | Main assumption |
|---|---|---|
| Cost of carry | What is the simplified futures benchmark? | Constant proportional carrying costs |
| Black (1976) | What is the European futures-call premium? | Lognormal futures price under risk-neutral pricing |
| Monte Carlo | Does simulated discounted payoff agree with Black? | Same underlying, maturity and volatility as Black |
| Standard Black-Scholes | What is the no-dividend spot-call premium? | No commodity storage adjustment |

Cost of carry uses `F = S exp((r + storage - convenience_yield) T)`.
The simulation uses `F_T = F exp(-0.5 sigma^2 T + sigma sqrt(T) Z)`
and averages `exp(-r T) max(F_T - K, 0)`.

## Run

Requires Python 3.10 or later and NumPy. From this repository's root:

```shell
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install dependencies and run:

```shell
python -m pip install -r requirements.txt
python compare_models.py
python -m unittest discover -s tests -v
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe` in place of
`python` in the commands above. This avoids changing execution policy.

## Example inputs and analytical results

Spot: $1.20/lb; strike: $1.25/lb; annual rate: 2%; annual storage: 1%;
convenience yield: 0%; maturity: 0.5 years; annual volatility: 25%.

| Output | USD per pound |
|---|---:|
| Futures benchmark | 1.21813568 |
| Black futures-call premium | approximately 0.07119 |
| Standard spot-call premium | approximately 0.06836 |

`compare_models.py` prints the simulation estimate, its approximate 95%
confidence interval, and volatility sensitivity. It uses 100,000 independent
terminal draws and seed 42. The spot-call price is shown as a different model,
not as an interchangeable answer. Contract values require multiplication by
the appropriate contract quantity.

## Validation and limitations

Tests cover reference values, Monte Carlo agreement with the analytical price,
expiry and zero-volatility limits, pricing bounds, volatility sensitivity, and
invalid inputs. The fixed-seed confidence-interval check is a reproducible
diagnostic; a 95% interval does not cover the target for every possible seed.

Constant rates and volatility, lognormal dynamics, proportional storage costs,
and European exercise simplify real commodity markets. The example does not
calibrate market data, model jumps, account for bid-ask spreads or transaction
costs, or implement early exercise. Forward/futures equivalence assumes
deterministic rates. Numerical confidence intervals exclude model and parameter
uncertainty. Risk-neutral outcomes are pricing distributions, not real-world
price forecasts. The structured note discussion is qualitative; this code does
not value issuer default risk or optimize note terms.

## Files

- `pricing.py`: reusable pricing functions and Monte Carlo result type.
- `compare_models.py`: reproducible example and sensitivity comparison.
- `tests/test_pricing.py`: numerical and input validation.
- `docs/structured_note_analysis.md`: proposed payoff, valuation considerations,
  and risk discussion.
- `docs/risk_management.md`: scenario responses from the original report.
- `docs/results.txt`: output captured during validation.

## Possible extensions

Add market calibration with attributable data, put pricing and parity checks,
Greeks, a convergence plot across simulation sizes, or an explicit valuation
budget for the structured note. These are future work, not implemented features.
