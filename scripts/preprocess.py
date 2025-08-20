import pandas as pd

# Load CSVs from data folder
qualifying = pd.read_csv('data/qualifying.csv')
results = pd.read_csv('data/results.csv')
races = pd.read_csv('data/races.csv')
drivers = pd.read_csv('data/drivers.csv')
constructors = pd.read_csv('data/constructors.csv')
circuits = pd.read_csv('data/circuits.csv')
driver_standings = pd.read_csv('data/driver_standings.csv')
constructor_standings = pd.read_csv('data/constructor_standings.csv')

# Create driver name
drivers['driver_name'] = drivers['forename'] + ' ' + drivers['surname']

# ---------------------------
# PROCESS QUALIFYING DATASET
# ---------------------------
qdf = qualifying.merge(races[['raceId', 'year', 'round', 'circuitId']], on='raceId', how='left')
qdf = qdf.merge(drivers[['driverId', 'driver_name']], on='driverId', how='left')
qdf = qdf.merge(constructors[['constructorId', 'name']], on='constructorId', how='left')
qdf = qdf.rename(columns={'name': 'team'})
qdf = qdf.merge(circuits[['circuitId', 'name']], on='circuitId', how='left')
qdf = qdf.rename(columns={'name': 'circuit'})

# Merge driver standings
qdf = qdf.merge(driver_standings[['raceId', 'driverId', 'points']], on=['raceId', 'driverId'], how='left')
qdf = qdf.rename(columns={'points': 'driver_points'})

qualifying_df = qdf(columns={'points': 'driver_points'})

# Merge constructor standings
qdf = qdf.merge(constructor_standings[['raceId', 'constructorId', 'points']], on=['raceId', 'constructorId'], how='left')
qdf = qdf.rename(columns={'points': 'team_points'})

# Keep best qualifying time
qdf['qualifying_time'] = qdf[['q1', 'q2', 'q3']].bfill(axis=1).iloc[:, 0]

# Drop rows with missing important values
qdf = qdf.dropna(subset=['position', 'qualifying_time', 'driver_points', 'team_points'])

# Keep only top 10
qdf = qdf[qdf['position'] <= 10]

# Final cleaned qualifying data
qdf_final = qdf[['year', 'round', 'driver_name', 'team', 'circuit', 'driver_points', 'team_points', 'position']]
qdf_final.to_csv('data/cleaned_qualifying.csv', index=False)

print("✅ cleaned_qualifying.csv saved!")

# ------------------------
# PROCESS RACE RESULT DATASET
# ------------------------
rdf = results.merge(races[['raceId', 'year', 'round', 'circuitId']], on='raceId', how='left')
rdf = rdf.merge(drivers[['driverId', 'driver_name']], on='driverId', how='left')
rdf = rdf.merge(constructors[['constructorId', 'name']], on='constructorId', how='left')
rdf = rdf.rename(columns={'name': 'team'})
rdf = rdf.merge(circuits[['circuitId', 'name']], on='circuitId', how='left')
rdf = rdf.rename(columns={'name': 'circuit'})

rdf = rdf.merge(driver_standings[['raceId', 'driverId', 'points']], on=['raceId', 'driverId'], how='left')
rdf = rdf.rename(columns={'points': 'driver_points'})

rdf = rdf.merge(constructor_standings[['raceId', 'constructorId', 'points']], on=['raceId', 'constructorId'], how='left')
rdf = rdf.rename(columns={'points': 'team_points'})

rdf = rdf.dropna(subset=['positionOrder', 'driver_points', 'team_points'])
rdf = rdf[rdf['positionOrder'] <= 10]

rdf_final = rdf[['year', 'round', 'driver_name', 'team', 'circuit', 'driver_points', 'team_points', 'positionOrder']]
rdf_final = rdf_final.rename(columns={'positionOrder': 'position'})
rdf_final.to_csv('data/cleaned_race.csv', index=False)

print("cleaned_race.csv saved!")
