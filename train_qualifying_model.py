# train_qualifying_model.py

import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Load cleaned data
df = pd.read_csv("model/cleaned_qualifying.csv")

# Define features and target
X = df[['driver_name', 'constructor_name', 'circuitId', 'year']]
y = df['position']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"\n📊 Mean Absolute Error on Test Set: {mae:.2f}")

# Save model
joblib.dump(model, "model/qualifying_model.pkl")
print("✅ Model saved to model/qualifying_model.pkl")
