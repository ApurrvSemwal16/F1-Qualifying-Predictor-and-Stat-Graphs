#Don't run this unless you are manually changing the dataset!!!

import pandas as pd
import os
import joblib
from sklearn.preprocessing import LabelEncoder

# Load data
qualifying = pd.read_csv("data/qualifying.csv")
races = pd.read_csv("data/races.csv")
drivers = pd.read_csv("data/drivers.csv")
constructors = pd.read_csv("data/constructors.csv")
results = pd.read_csv("data/results.csv")

# Merge necessary fields to qualifying
df = qualifying.merge(races[['raceId', 'year', 'circuitId']], on='raceId', how='left')
df = df.merge(drivers[['driverId', 'surname']], on='driverId', how='left')
df = df.merge(constructors[['constructorId', 'name']], on='constructorId', how='left')

# Rename for clarity
df.rename(columns={
    'surname': 'driver_name',
    'name': 'constructor_name'
}, inplace=True)

# Keep necessary columns
df = df[['driver_name', 'constructor_name', 'circuitId', 'year', 'position']]

# Drop rows without position
df['position'] = pd.to_numeric(df['position'], errors='coerce')
df.dropna(subset=['position'], inplace=True)

# Label encode
le_driver = LabelEncoder()
le_constructor = LabelEncoder()
le_circuit = LabelEncoder()

df['driver_name'] = le_driver.fit_transform(df['driver_name'])
df['constructor_name'] = le_constructor.fit_transform(df['constructor_name'])
df['circuitId'] = le_circuit.fit_transform(df['circuitId'])

# Save encoders and cleaned dataset
os.makedirs("model", exist_ok=True)
joblib.dump(le_driver, "model/driver_encoder.pkl")
joblib.dump(le_constructor, "model/constructor_encoder.pkl")
joblib.dump(le_circuit, "model/circuit_encoder.pkl")
df.to_csv("model/cleaned_qualifying.csv", index=False)

# Extract only latest driver-constructor pairs from real race data
results = results.merge(races[['raceId', 'year']], on='raceId', how='left')
latest_year = results['year'].max()
latest_results = results[results['year'] == latest_year]
latest_results = latest_results.merge(drivers[['driverId', 'surname']], on='driverId', how='left')
latest_results = latest_results.merge(constructors[['constructorId', 'name']], on='constructorId', how='left')
valid_pairs = latest_results[['surname', 'name']].drop_duplicates()
valid_pairs.columns = ['driver_name', 'constructor_name']
valid_pairs.to_csv("model/valid_pairs.csv", index=False)

print("✅ Cleaned qualifying dataset saved to model/cleaned_qualifying.csv")
print("✅ Valid 2025 driver–constructor pairs saved to model/valid_pairs.csv")
