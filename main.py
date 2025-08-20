import pandas as pd

# Load datasets
qualifying = pd.read_csv("data/qualifying.csv")
races = pd.read_csv("data/races.csv")
drivers = pd.read_csv("data/drivers.csv")
constructors = pd.read_csv("data/constructors.csv")

# Merge races (to get year, circuitId)
qualifying = qualifying.merge(races[['raceId', 'year', 'circuitId']], on='raceId', how='left')
print("✅ After merging races:", qualifying.columns.tolist())

# Merge drivers (get full name)
drivers['driver_name'] = drivers['forename'] + " " + drivers['surname']
qualifying = qualifying.merge(drivers[['driverId', 'driver_name']], on='driverId', how='left')
print("✅ After merging drivers:", qualifying.columns.tolist())

# Merge constructors
qualifying = qualifying.merge(constructors[['constructorId', 'name']], on='constructorId', how='left')
print("✅ After merging constructors:", qualifying.columns.tolist())

# Rename constructor column
qualifying.rename(columns={'name': 'constructor_name'}, inplace=True)
print("✅ After renaming constructor name:", qualifying.columns.tolist())

# Drop rows without position
qualifying = qualifying.dropna(subset=['position'])

# Keep only relevant columns
qualifying_data = qualifying[['driver_name', 'constructor_name', 'circuitId', 'year', 'position']]

# Final output
print("\n✅ Final Cleaned Qualifying Data:\n")
print(qualifying_data.head(10))
qualifying_data.to_csv("data/clean_qualifying.csv", index=False)
