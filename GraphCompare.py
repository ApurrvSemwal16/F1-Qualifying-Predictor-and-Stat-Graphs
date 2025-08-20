#This file gives Lap time comparison of multiple drivers across Q1, Q2, Q3 session on one track for a particular year.

import pandas as pd
import matplotlib.pyplot as plt

# ================================
# Load datasets
# ================================
races = pd.read_csv("data/races.csv", on_bad_lines="skip")
qualifying = pd.read_csv("data/qualifying.csv")
drivers = pd.read_csv("data/drivers.csv")
constructors = pd.read_csv("data/constructors.csv")
circuits = pd.read_csv("data/circuits.csv")

# ================================
# Merge datasets for analysis
# ================================
qualifying = qualifying.merge(races, on="raceId", how="left", suffixes=("", "_race"))
qualifying = qualifying.merge(drivers, on="driverId", how="left", suffixes=("", "_driver"))
qualifying = qualifying.merge(constructors, on="constructorId", how="left", suffixes=("", "_constructor"))
qualifying = qualifying.merge(circuits, on="circuitId", how="left", suffixes=("", "_circuit"))

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
circuit_data = qualifying[
    (qualifying["name_circuit"].str.contains(user_circuit, case=False, na=False)) &
    (qualifying["year"] == user_year) &
    (qualifying["surname"].isin(user_drivers))
]

if circuit_data.empty:
    print(f"No qualifying data found for {user_circuit} in {user_year} for drivers {user_drivers}.")
    exit()

# ================================
# Time conversion helpers
# ================================
def time_to_seconds(t):
    if pd.isna(t):
        return None
    parts = t.split(":")
    if len(parts) == 2:
        mins, rest = parts
        return float(mins) * 60 + float(rest)
    return None

def seconds_to_time(s):
    if s is None: 
        return None
    mins = int(s // 60)
    secs = s % 60
    return f"{mins}:{secs:06.3f}"

# Convert Q1/Q2/Q3 into seconds
for q in ["q1", "q2", "q3"]:
    circuit_data[q] = circuit_data[q].apply(time_to_seconds)

# ================================
# Build progression data
# ================================
progression_data = {}

for _, row in circuit_data.iterrows():
    driver = row["surname"]
    q1, q2, q3 = row["q1"], row["q2"], row["q3"]
    progression_data[driver] = [q1, q2, q3]

# ================================
# Plot with Annotations
# ================================
plt.figure(figsize=(12, 6))

labels = ["Q1", "Q2", "Q3"]

for driver, times in progression_data.items():
    plt.plot(labels, times, marker="o", label=driver)

    # Add text annotations at each point
    for i, t in enumerate(times):
        if t is not None:
            plt.text(
                labels[i], t, seconds_to_time(t),
                fontsize=9, ha="left", va="bottom"
            )

plt.title(f"Qualifying Progression (Q1→Q2→Q3) at {user_circuit} ({user_year})")
plt.xlabel("Qualifying Sessions")
plt.ylabel("Lap Time (M:SS.mmm)")
plt.legend()
plt.grid(True)

# Format y-axis ticks to lap time format
yticks = plt.gca().get_yticks()
plt.gca().set_yticklabels([seconds_to_time(y) for y in yticks])

plt.show()
