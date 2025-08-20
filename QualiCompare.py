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
user_circuit = input("Enter circuit name (e.g., 'Monza'): ").strip()
user_years = input("Enter years separated by commas (e.g., '2020,2021,2022'): ").split(",")
user_years = [int(y.strip()) for y in user_years]
user_drivers = input("Enter driver surnames separated by commas (e.g., 'Verstappen,Hamilton,Leclerc'): ").split(",")
user_drivers = [d.strip().capitalize() for d in user_drivers]

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

# ================================
# Collect best quali times per driver/year
# ================================
results = []

for year in user_years:
    year_data = qualifying[
        (qualifying["year"] == year) &
        (qualifying["name_circuit"].str.contains(user_circuit, case=False, na=False)) &
        (qualifying["surname"].isin(user_drivers))
    ]

    if year_data.empty:
        print(f"No qualifying data found for {user_circuit} in {year}.")
        continue

    for _, row in year_data.iterrows():
        driver = row["surname"]
        # take best available quali session time (priority Q3 > Q2 > Q1)
        times = [time_to_seconds(row["q3"]), time_to_seconds(row["q2"]), time_to_seconds(row["q1"])]
        best_time = next((t for t in times if t is not None), None)

        if best_time is not None:
            results.append({"Driver": driver, "Year": year, "BestTime": best_time})

# ================================
# Convert results to DataFrame
# ================================
df = pd.DataFrame(results)

if df.empty:
    print("No valid qualifying times found for given input.")
    exit()

# ================================
# Plotting
# ================================
plt.figure(figsize=(12, 6))

for driver in user_drivers:
    driver_data = df[df["Driver"] == driver]
    plt.plot(driver_data["Year"], driver_data["BestTime"], marker="o", label=driver)

    # Annotate with actual lap times
    for _, row in driver_data.iterrows():
        plt.text(
            row["Year"], row["BestTime"] - 0.15,  # slight downward offset
            seconds_to_time(row["BestTime"]),
            fontsize=9, ha="center", va="top"
        )

plt.title(f"Qualifying Comparison at {user_circuit} ({', '.join(map(str, user_years))})")
plt.xlabel("Year")
plt.ylabel("Best Qualifying Time (M:SS.mmm)")
plt.legend()
plt.grid(True)
# Format y-axis to lap time format
yticks = plt.gca().get_yticks()
plt.gca().set_yticklabels([seconds_to_time(y) for y in yticks])
plt.show()
