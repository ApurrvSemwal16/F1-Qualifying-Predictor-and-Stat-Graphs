#This file gives you stat graph of multiple driver's race result comparison across the whole season.

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ================================
# Load datasets
# ================================
races = pd.read_csv("data/races.csv", on_bad_lines="skip")
results = pd.read_csv("data/results.csv", on_bad_lines="skip")
drivers = pd.read_csv("data/drivers.csv")
constructors = pd.read_csv("data/constructors.csv")
circuits = pd.read_csv("data/circuits.csv")

# Optional: status lookup (maps statusId -> status text)
status_path = "data/status.csv"
status_df = None
if os.path.exists(status_path):
    try:
        status_df = pd.read_csv(status_path)
    except Exception:
        status_df = None

# ================================
# Merge datasets for analysis
# ================================
results = results.merge(races, on="raceId", how="left", suffixes=("", "_race"))
results = results.merge(drivers, on="driverId", how="left", suffixes=("", "_driver"))
results = results.merge(constructors, on="constructorId", how="left", suffixes=("", "_constructor"))
results = results.merge(circuits, on="circuitId", how="left", suffixes=("", "_circuit"))

# If we have status.csv, bring in readable status
if status_df is not None and "statusId" in results.columns and "statusId" in status_df.columns:
    results = results.merge(status_df[["statusId", "status"]], on="statusId", how="left")
else:
    # Fallback: derive a status-like string from positionText
    # positionText is numeric for classified finishers, or strings like 'R', 'DQ', etc.
    def fallback_status(row):
        pt = str(row.get("positionText", ""))
        if pt.isdigit():
            return "Finished"
        pt_u = pt.upper()
        if "DQ" in pt_u or "DSQ" in pt_u:
            return "DSQ"
        if pt_u in {"R", "RET"}:
            return "DNF"
        if pt_u in {"DNS"}:
            return "DNS"
        # Use whatever is there, or \N means unknown/finished in Ergast
        return "Finished" if pt == "\\N" else pt
    results["status"] = results.apply(fallback_status, axis=1)

# ================================
# User input
# ================================
year = int(input("Enter season year: ").strip())
driver_inputs = input("Enter driver surnames separated by commas: ").split(",")
driver_inputs = [d.strip().lower() for d in driver_inputs]

# ================================
# Filter for the selected season
# ================================
season_data = results[results["year"] == year].copy()
season_data = season_data.sort_values("round")

# Races in order (labels)
race_order = season_data.drop_duplicates("raceId")[["raceId", "name", "round"]].sort_values("round")
race_labels = race_order["name"].tolist()
race_ids = race_order["raceId"].tolist()

plt.figure(figsize=(18, 8))

# For points box
driver_points = {}
# For a consistent bottom row to place DNF/DSQ/DNS labels
max_pos = int(season_data["positionOrder"].max()) if pd.notna(season_data["positionOrder"].max()) else 20
dnf_label_y = max_pos + 0.8  # a bit below worst finishing position (will flip later)

for drv in driver_inputs:
    # filter by surname (case-insensitive)
    ddf = season_data[season_data["surname"].str.lower() == drv].copy()
    if ddf.empty:
        print(f"No data found for {drv} in {year}")
        continue

    # Build a position list aligned to all races in the season
    positions = []
    ann_tags = []  # P#, DNF, DSQ, DNS, etc.

    for rid in race_ids:
        row = ddf[ddf["raceId"] == rid]
        if not row.empty:
            row = row.iloc[0]
            status_txt = str(row.get("status", ""))
            pos_order = row.get("positionOrder", np.nan)

            # Decide classification vs non-classification
            if str(row.get("positionText", "")).isdigit() or status_txt == "Finished" or status_txt == "\\N":
                positions.append(pos_order)
                ann_tags.append(f"P{int(pos_order)}")
            else:
                # Non-classified → mark as NaN so line shows a gap; annotate with status
                positions.append(np.nan)
                st_up = status_txt.upper()
                if "DNF" in st_up or "RET" in st_up:
                    ann_tags.append("DNF")
                elif "DSQ" in st_up or "DQ" in st_up or "DISQUAL" in st_up:
                    ann_tags.append("DSQ")
                elif "DNS" in st_up or "DID NOT START" in st_up:
                    ann_tags.append("DNS")
                else:
                    ann_tags.append(status_txt if status_txt else "N/C")
        else:
            positions.append(np.nan)
            ann_tags.append("N/A")

    # Plot one continuous line (NaNs create gaps rather than multiple separate lines)
    label_name = ddf.iloc[0]["surname"]
    plt.plot(race_labels, positions, marker="o", label=label_name)

    # Annotate each race point
    for i, (pos, tag) in enumerate(zip(positions, ann_tags)):
        if not pd.isna(pos):
            # Valid classified result → annotate on the point
            plt.text(i, pos, tag, fontsize=8, ha="center", va="bottom")
        else:
            # Non-classified → show tag at the bottom line (in red)
            plt.text(i, dnf_label_y, tag, fontsize=8, ha="center", va="top", color="red")

    # Sum points for the season
    driver_points[label_name] = ddf["points"].sum()

# Invert Y so P1 at top
plt.gca().invert_yaxis()

plt.title(f"Season {year} - Race Position Progression")
plt.xlabel("Race")
plt.ylabel("Position")

# Main legend (driver colors)
plt.legend(loc="upper right")

# Secondary legend (points summary)
points_text = "\n".join([f"{drv}: {pts} pts" for drv, pts in driver_points.items()])
plt.gcf().text(
    0.02, 0.70,
    f"Total Points:\n{points_text}",
    fontsize=10,
    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5')
)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
