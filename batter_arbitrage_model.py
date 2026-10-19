import gurobipy as gp
from gurobipy import GRB
import numpy as np
import math
import matplotlib.pyplot as plt

capacity = 100.0
min_soc = 20.0
max_soc = 80.0
usable_capacity = max_soc - min_soc
max_rate = 25.0
eta_c = math.sqrt(0.90)
eta_d = math.sqrt(0.90)
np.random.seed(42)
prices = np.random.uniform(20, 150, 24)

horizon = 3
T = len(prices)

def optimise_window(price_window, initial_soc):

    H = len(price_window)

    model = gp.Model("rolling_battery")
    model.Params.OutputFlag = 0

    # Decision variables
    C = model.addVars(
        H, lb=0, ub=max_rate, name="Charge"
    )

    D = model.addVars(
        H, lb=0, ub=max_rate, name="Discharge"
    )

    SOC = model.addVars(
        H + 1, lb=20, ub=80, name="SOC"
    )

    model.addConstr(SOC[0] == initial_soc)

    # SOC dynamics
    for t in range(H):
        model.addConstr(
            SOC[t+1] == SOC[t]
            + eta_c * C[t]
            - D[t] / eta_d
        )

    # Objective
    objective = gp.quicksum(
        price_window[t] * (D[t] - C[t])
        for t in range(H)
    )

    model.setObjective(objective, GRB.MAXIMIZE)

    model.optimize()

    if model.status == GRB.OPTIMAL:

        return {
            "charge": C[0].X,
            "discharge": D[0].X,
            "predicted_soc": SOC[1].X,
            "profit": model.ObjVal
        }

    else:
        raise RuntimeError("Optimisation failed")
    
current_soc = 30.0

results = []

for t in range(T):

    # Define the future window
    end = min(t + horizon, T)

    price_window = prices[t:end]

    # Optimise future window
    result = optimise_window(
        price_window,
        current_soc
    )

    # Implement ONLY the first decision
    charge = result["charge"]
    discharge = result["discharge"]

    # Realised profit for this hour
    realised_profit = prices[t] * (
        discharge - charge
    )

    # Update actual SOC
    next_soc = (
        current_soc
        + eta_c * charge
        - discharge / eta_d
    )

    # Save results
    results.append({
        "hour": t,
        "price": prices[t],
        "soc_start": current_soc,
        "charge": charge,
        "discharge": discharge,
        "soc_end": next_soc,
        "profit": realised_profit
    })

    # Move to next hour
    current_soc = next_soc

cumulative_profit = sum(r["profit"] for r in results)
total_charge = sum(r["charge"] for r in results)
total_discharge = sum(r["discharge"] for r in results)
total_throughput = total_charge + total_discharge
equivalent_full_cycles = (total_throughput/ (2 * usable_capacity))
if equivalent_full_cycles > 0:
    profit_per_cycle = (cumulative_profit/ equivalent_full_cycles)
else:
    profit_per_cycle = 0.0

energy_stored = total_charge * eta_c

energy_required_for_discharge = total_discharge / eta_d
if energy_required_for_discharge > 0:
    round_trip_efficiency = (total_discharge/ energy_required_for_discharge)
else:
    round_trip_efficiency = 0.0

event_threshold = 1e-6
charge_events = sum(
    1
    for r in results
    if r["charge"] > event_threshold
)
discharge_events = sum(
    1
    for r in results
    if r["discharge"] > event_threshold
)

print("\n" + "=" * 50)
print("BATTERY PERFORMANCE SUMMARY")
print("=" * 50)
print(f"Cumulative profit:       ${cumulative_profit:,.2f}")
print(f"Total charge:            {total_charge:,.2f} MWh")
print(f"Total discharge:         {total_discharge:,.2f} MWh")
print(f"Total throughput:        {total_throughput:,.2f} MWh")
print(f"Equivalent full cycles:  {equivalent_full_cycles:,.2f}")
print(f"Profit per cycle:        ${profit_per_cycle:,.2f}")
print(f"Round-trip efficiency:    "f"{round_trip_efficiency * 100:.2f}%")
print(f"Charge events:           {charge_events}")
print(f"Discharge events:        {discharge_events}")
print("=" * 50)

import matplotlib.pyplot as plt

hours = [r["hour"] for r in results]
prices_plot = [r["price"] for r in results]
charge = [r["charge"] for r in results]
discharge = [r["discharge"] for r in results]

plt.style.use("dark_background")
plt.figure(figsize=(10, 8))

plt.subplot(2, 1, 1)

plt.plot(hours, prices_plot, label="Price ($/MWh)")
plt.bar(hours, charge, alpha=0.5, label="Charge (MW)")
plt.bar(hours, [-d for d in discharge], alpha=0.5, label="Discharge (MW)")

plt.axhline(0, linewidth=0.8)
plt.xlabel("Hour")
plt.ylabel("Price / Power")
plt.title("Battery Charging and Discharging")
plt.legend()
plt.grid(True)

plt.subplot(2, 1, 2)

soc = [results[0]["soc_start"]] + [r["soc_end"] for r in results]
soc_hours = range(len(soc))

plt.plot(soc_hours, soc)

plt.axhline(100, linestyle="--", linewidth=0.8)
plt.axhline(0, linestyle="--", linewidth=0.8)

plt.xlabel("Hour")
plt.ylabel("SOC (MWh)")
plt.title("Battery State of Charge")
plt.ylim(0, 105)
plt.grid(True)
plt.tight_layout()
plt.show()