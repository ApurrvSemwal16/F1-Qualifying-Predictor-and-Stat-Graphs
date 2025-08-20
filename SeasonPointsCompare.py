# SeasonPointsCompare.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ================================
# Load datasets (from data/)
# ================================
races = pd.read_csv("data/races.csv", on_bad_lines="skip")
results = pd.read_csv("data/results.csv", on_bad_lines="skip")
drivers = pd.read_csv("data/drivers.csv")

# ================================
# Merge results with races & drivers
# ================================
merged = (
    results.merge(races, on="raceId", how="left", suffixes=("", "_race"))
           .merge(drivers, on="driverId", how="left", suffixes=("", "_driver"))
)

# ================================
# User inputs
# ================================
year = int(input("Enter season year (e.g., 2022): ").strip())
driver_inputs_raw = input(
    "Enter drivers (surname, code, or full name) separated by commas\n"
    "e.g., Verstappen,HAM,Charles Leclerc: "
).split(",")
driver_inputs = [d.strip().lower() for d in driver_inputs_raw if d.strip()]

# ================================
# Filter to chosen season
# ================================
season = merged[merged["year"] == year].copy()
if season.empty:
    print(f"No races found for season {year}.")
    raise SystemExit

# Keep only needed columns to avoid confusion
season = season[
    ["raceId", "round", "name", "driverId", "forename", "surname", "code", "points"]
].rename(columns={"name": "raceName"})

# ================================
# Resolve driver selection (surname OR code OR full name)
# ================================
season["driverLabel"] = (season["forename"] + " " + season["surname"]).str.strip()
season["key_surname"] = season["surname"].str.lower()
season["key_code"] = season["code"].astype(str).str.lower()
season["key_full"] = season["driverLabel"].str.lower()

# Which rows match any of the typed tokens?
mask = False
for token in driver_inputs:
    mask = mask | (season["key_surname"] == token) | (season["key_code"] == token) | (season["key_full"] == token)

selected = season[mask].copy()

if selected.empty:
    print("No matching drivers for the given inputs in that season.")
    raise SystemExit

# Standardize the plotted driver name (Surname or Full Name if duplicate surnames)
name_counts = selected["surname"].value_counts()
def display_name(row):
    # If two drivers share a surname (rare in a season), show full name to avoid ambiguity
    if name_counts.get(row["surname"], 0) > 1:
        return row["driverLabel"]
    return row["surname"]
selected["plotName"] = selected.apply(display_name, axis=1)

# ================================
# Build race order & cumulative points per driver
# ================================
race_order = (
    season[["raceId", "round", "raceName"]]
    .drop_duplicates("raceId")
    .sort_values("round")
)
race_ids = race_order["raceId"].tolist()
race_labels = race_order["raceName"].tolist()

# Sum points per driver per race (some datasets may have sprint etc.; this sums all points for that raceId)
points_tbl = (
    selected.groupby(["plotName", "raceId"], as_index=False)["points"]
    .sum()
)

# Reindex per driver across all season races, fill missing with 0, then cumulative sum
lines = {}
final_points = {}

for drv, grp in points_tbl.groupby("plotName"):
    # Align with all raceIds in the season
    s = grp.set_index("raceId")["points"].reindex(race_ids).fillna(0.0)
    cum = s.cumsum()  # cumulative points across the season
    lines[drv] = cum.values
    final_points[drv] = float(cum.values[-1]) if len(cum.values) else 0.0

# ================================
# Plot cumulative points progression
# ================================
plt.figure(figsize=(18, 8))

for drv, y in lines.items():
    plt.plot(race_labels, y, marker="o", label=drv)
    # Annotate last point with final points
    if len(y) > 0:
        plt.text(len(race_labels)-1, y[-1], f"{y[-1]:.0f}", fontsize=9, ha="left", va="center")

plt.title(f"Season {year} — Cumulative Points Progression")
plt.xlabel("Race")
plt.ylabel("Cumulative Points")
plt.xticks(rotation=45, ha="right")
plt.grid(True, linestyle="--", alpha=0.6)

# Standard legend (driver colors) outside the plot on the right
plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0.)

# Side box with final points, aligned neatly
points_lines = [f"{drv}: {pts:.0f} pts" for drv, pts in sorted(final_points.items(), key=lambda x: -x[1])]
points_text = "Final Points:\n" + "\n".join(points_lines)

plt.gcf().text(
    0.015, 0.70,
    points_text,
    fontsize=10,
    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5')
)

plt.tight_layout()
plt.show()
