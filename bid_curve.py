from battery_arbitrage_model import optimise_window
import numpy as np
import pandas as pd

initial_soc = 50
horizon = 3

future_prices = np.array([80.0, 60.0])
price_sweep = np.arange(-100, 201, 1)
results = []

for p in price_sweep:
    price_window = np.concatenate(([p], future_prices))
    result = optimise_window(price_window, initial_soc)
    results.append({
        "First_period_price": p,
        "Charge": result["charge"],
        "Discharge": result["discharge"]})

sweep_df = pd.DataFrame(results)
import matplotlib.pyplot as plt
sweep_df["Net_Power"] = (
    sweep_df["Discharge"] - sweep_df["Charge"])
sweep_df = sweep_df.sort_values("First_period_price")
plt.figure(figsize=(10, 6))

plt.step(
    sweep_df["Net_Power"],
    sweep_df["First_period_price"],
    where="mid")

plt.ylabel("Electricity Price ($/MWh)")
plt.xlabel("Net Power (MW)")
plt.title("Battery Bid Curve")

plt.grid(True)
plt.tight_layout()
plt.show()