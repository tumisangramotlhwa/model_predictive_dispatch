# Battery Energy Storage Optimisation & Electricity Market Bidding

An optimisation and market simulation project exploring **battery energy storage system (BESS) arbitrage, rolling-horizon dispatch, and strategic bidding in electricity markets**. Using Python, CVXPY, Gurobi, and NEMPY, the project models battery operation under physical constraints, optimises charging and discharging decisions, and investigates the economic value of stored energy in the Australian National Electricity Market (NEM).

## Key Results

| Metric | Result |
|---|---:|
| Battery energy capacity | 100 MWh |
| Maximum charge/discharge power | 25 MW |
| State-of-charge operating range | 20–80% |
| Round-trip efficiency | 90% |
| Synthetic 24-hour arbitrage profit | **$11.1k** |
| Rolling-dispatch profit per equivalent cycle | **$3.24k** |
| Equivalent full cycles | 3.42 |
| Simulated energy throughput | 410.6 MWh |

*Results are simulation outputs under the specified price and market assumptions, not forecasts of real-world battery revenue.*

## Project Overview

### 1. Battery Arbitrage Optimisation

Formulated a linear programming (LP) model to optimise the charging and discharging schedule of a 100 MWh battery against a synthetic 24-hour electricity price series.

The optimisation model was implemented using **CVXPY** and solved with **Gurobi**, subject to battery operating constraints.

**Key features:**
- Maximises arbitrage revenue by charging during lower-price intervals and discharging during higher-price intervals.
- Enforces a 20–80% state-of-charge (SOC) operating range.
- Limits charging and discharging power to 25 MW.
- Incorporates 90% round-trip efficiency.
- Produces an optimal dispatch schedule and calculates the resulting simulated profit.

**Result:** Achieved approximately **$11,100 in simulated profit** over the 24-hour price series.

### 2. Rolling-Horizon Dispatch in the Australian NEM

Extended the optimisation framework to an *n*-hour rolling-window dispatch strategy integrated with **NEMPY** for single-interval Australian Energy Market Operator (AEMO) regional market clearing.

The rolling-window approach evaluates battery dispatch decisions over a moving horizon, providing a framework for studying how operational decisions interact with electricity market outcomes.

**Key features:**
- Implements rolling-window battery dispatch optimisation.
- Integrates with NEMPY to simulate regional electricity market clearing.
- Evaluates battery charging and discharging under market-based dispatch conditions.
- Tracks profitability, equivalent full cycles, and energy throughput.

**Results:**
- **$3.24k profit per equivalent cycle**
- **3.42 equivalent full cycles**
- **410.6 MWh simulated energy throughput**

### 3. Shadow Pricing, Energy Valuation & Strategic Bidding

Investigated the marginal economic value of stored energy using **dual variables (shadow prices)** and marginal energy values derived from the optimisation framework.

The analysis connects battery dispatch decisions with electricity market bidding by examining the opportunity cost of charging, discharging, and retaining stored energy.

**Key features:**
- Analyses dual variables associated with optimisation constraints.
- Quantifies the marginal value and opportunity cost of stored energy.
- Constructs price–quantity bid curves for battery charging and discharging.
- Investigates the relationship between battery operating constraints and optimal bidding behaviour.
- Explores price-taking versus price-setting behaviour in a competitive electricity market.

## Methodology

The project follows three main stages:

1. **Optimisation:** Formulate a constrained LP to determine economically optimal battery dispatch.
2. **Market simulation:** Apply rolling-horizon dispatch and integrate with NEMPY for regional market clearing.
3. **Economic analysis:** Evaluate simulated profitability, energy throughput, marginal energy values, and price–quantity bidding behaviour.

## Technology Stack

| Technology | Application |
|---|---|
| Python | Core modelling, optimisation workflows, and analysis |
| CVXPY | Mathematical optimisation modelling |
| Gurobi | Linear programming solver |
| NEMPY | Electricity market simulation and regional market clearing |
| AEMO market framework | Australian electricity market context |

## Getting Started

### Prerequisites

The project uses Python and the optimisation and market simulation tools listed above.

You will need:
- Python
- CVXPY
- Gurobi and a valid solver licence
- NEMPY
- Any additional packages required by the project scripts

### Installation

Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>