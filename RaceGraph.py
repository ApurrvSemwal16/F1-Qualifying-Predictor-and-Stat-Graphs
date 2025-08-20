# This file gives you stat graph of multiple driver's starting position to finishing position in a particular race.

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
# User inputs
# ================================
user_circuit = input("Enter circuit name (e.g., 'Silverstone'): ").strip()
user_year = int(input("Enter year (e.g., 2023): ").strip())
user_drivers = input("Enter driver surnames separated by commas (e.g., 'Verstappen,Leclerc,Hamilton'): ").split(",")
user_drivers = [d.strip().capitalize() for d in user_drivers]

# ================================
# Filter data
# ================================
circuit_data = results[
    (results["name_circuit"].str.contains(user_circuit, case=False, na=False)) &
    (results["year"] == user_year) &
    (results["surname"].isin(user_drivers))
]

if circuit_data.empty:
    print(f"No race results found for {user_circuit} in {user_year} for drivers {user_drivers}.")
    exit()

# ================================
# Build progression data
# ================================
progression_data = {}

for _, row in circuit_data.iterrows():
    driver = row["surname"]
    grid = row["grid"]
    finish = row["positionOrder"]  # final classification
    progression_data[driver] = [grid, finish]

# ================================
# Plot Race Position Progression
# ================================
plt.figure(figsize=(10, 6))

labels = ["Grid Start", "Race Finish"]

for driver, positions in progression_data.items():
    plt.plot(labels, positions, marker="o", label=driver)

    # Add text labels on points
    for i, pos in enumerate(positions):
        plt.text(labels[i], pos, str(pos), fontsize=9, ha="left", va="bottom")

plt.title(f"Race Progression (Grid → Finish) at {user_circuit} ({user_year})")
plt.xlabel("Race Stages")
plt.ylabel("Position (lower is better)")
plt.legend()
plt.grid(True)

# Invert y-axis so P1 is at the top
plt.gca().invert_yaxis()

plt.show()
