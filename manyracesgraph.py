#This file gives you the stat graph of multiple driver's race finishing position across multiple years on 1 track.

import pandas as pd
import matplotlib.pyplot as plt

# ================================
# Load datasets
# ================================
races = pd.read_csv("data/races.csv", on_bad_lines="skip")
results = pd.read_csv("data/results.csv")
drivers = pd.read_csv("data/drivers.csv")
constructors = pd.read_csv("data/constructors.csv")
circuits = pd.read_csv("data/circuits.csv")

# ================================
# Merge datasets
# ================================
results = results.merge(races, on="raceId", how="left", suffixes=("", "_race"))
results = results.merge(drivers, on="driverId", how="left", suffixes=("", "_driver"))
results = results.merge(constructors, on="constructorId", how="left", suffixes=("", "_constructor"))
results = results.merge(circuits, on="circuitId", how="left", suffixes=("", "_circuit"))

# ================================
# User input
# ================================
circuit_name = input("Enter circuit name (e.g. Monza, Silverstone): ").strip().lower()
years = input("Enter years separated by commas (e.g. 2019,2020,2021): ").split(",")
years = [int(y.strip()) for y in years]

drivers_input = input("Enter driver names separated by commas (e.g. Lewis Hamilton, Max Verstappen): ").split(",")
drivers_input = [d.strip().lower() for d in drivers_input]

# --- Filter data ---
filtered = results[
    (results["name_circuit"].str.lower().str.contains(circuit_name)) &
    (results["year"].isin(years))
]

if filtered.empty:
    print("No data found for that circuit/year combination.")
    exit()

# --- Create driver label ---
filtered["driverLabel"] = filtered["surname"]

# --- Keep only selected drivers ---
filtered = filtered[filtered["driverLabel"].str.lower().isin(drivers_input)]

if filtered.empty:
    print("No matching drivers found for that circuit/year combination.")
    exit()

# ================================
# Plot
# ================================
plt.figure(figsize=(10, 6))

for driver in filtered["driverLabel"].unique():
    driver_data = filtered[filtered["driverLabel"] == driver].sort_values("year")

    plt.plot(
        driver_data["year"],
        driver_data["positionOrder"],
        marker="o",
        label=driver
    )

    # Annotate each point with position
    for x, y in zip(driver_data["year"], driver_data["positionOrder"]):
        plt.text(x, y, str(y), fontsize=9, ha="center", va="bottom")

# Invert Y axis (lower position = better result)
plt.gca().invert_yaxis()
plt.xlabel("Year")
plt.ylabel("Finishing Position")
plt.title(f"Driver Performance at {circuit_name.title()} Across Years")

# Move legend outside on the right
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left", borderaxespad=0.)

plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
