import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

data = pd.read_csv("data/clean_qualifying.csv")

from sklearn.preprocessing import LabelEncoder

le_driver = LabelEncoder()
le_constructor = LabelEncoder()
le_circuit = LabelEncoder()

data['driver_name'] = le_driver.fit_transform(data['driver_name'])
data['constructor_name'] = le_constructor.fit_transform(data['constructor_name'])
data['circuitId'] = le_circuit.fit_transform(data['circuitId'])

X = data[['driver_name', 'constructor_name', 'circuitId', 'year']]
y = data['position'].astype(int)
y = y.apply(lambda x: x if x <= 10 else 11)  # 1–10 stay, rest become 11

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\n🎯 Accuracy:", accuracy_score(y_test, y_pred))
print("\n📊 Classification Report:\n", classification_report(y_test, y_pred))

joblib.dump(model, "model/qualifying_model.pkl")
joblib.dump(le_driver, "model/driver_encoder.pkl")
joblib.dump(le_constructor, "model/constructor_encoder.pkl")
joblib.dump(le_circuit, "model/circuit_encoder.pkl")
