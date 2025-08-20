# predict_qualifying.py

import joblib
import pandas as pd

# Load model and encoders
model = joblib.load("model/qualifying_model.pkl")
le_driver = joblib.load("model/driver_encoder.pkl")
le_constructor = joblib.load("model/constructor_encoder.pkl")
le_circuit = joblib.load("model/circuit_encoder.pkl")

# Load current grid (driver/constructor pairs)
grid_df = pd.read_csv("model/valid_pairs.csv")

# -------- Inputs --------
circuitId_raw = int(input("Enter circuit ID (e.g., 14 for Spa): ").strip())
year = int(input("Enter season year (e.g., 2025): ").strip() or "2025")

top_k_raw = input("How many to show? (5 / 10 / all): ").strip().lower()

def parse_topk(s: str, max_len: int) -> int | None:
    if s in ("all", "", "a"):
        return None  # show all
    try:
        k = int(s)
        if k < 1:
            return None
        return min(k, max_len)
    except ValueError:
        return 10  # sensible default

# Encode circuit ID
try:
    circuit_encoded = le_circuit.transform([circuitId_raw])[0]
except Exception:
    print(f"❌ Circuit ID '{circuitId_raw}' not found in training data.")
    print("Available circuit IDs the model knows:", list(le_circuit.classes_))
    raise SystemExit(1)

# -------- Predict --------
predictions = []

for _, row in grid_df.iterrows():
    driver, constructor = row["driver_name"], row["constructor_name"]
    try:
        X = pd.DataFrame([{
            "driver_name": le_driver.transform([driver])[0],
            "constructor_name": le_constructor.transform([constructor])[0],
            "circuitId": circuit_encoded,
            "year": year
        }])
        yhat = model.predict(X)[0]
        predictions.append((driver, constructor, float(yhat)))
    except Exception:
        # skip unseen labels not in encoders
        continue

# Sort best (lowest predicted position first)
predictions.sort(key=lambda x: x[2])

# Determine how many to show
k = parse_topk(top_k_raw, len(predictions))
to_show = predictions if k is None else predictions[:k]

# -------- Output --------
encoded_str = f"(Encoded ID {circuit_encoded})" if isinstance(circuit_encoded, (int, float)) else ""
hdr = f"\n📍 Predicted Qualifying for Circuit ID {circuitId_raw} {encoded_str} — Year {year}"
print(hdr)

for i, (driver, constructor, pos) in enumerate(to_show, start=1):
    rank_str = f"{i}."
    print(f"{rank_str} {driver} ({constructor}) — Position: {pos:.2f}")

# If user chose a small top-k, also show who was next (optional)
if k is not None and len(predictions) > k:
    next_up = predictions[k:min(k+3, len(predictions))]
    if next_up:
        print("\n…Next in order:")
        for i, (driver, constructor, pos) in enumerate(next_up, start=k+1):
            print(f"{i}. {driver} ({constructor}) — Position: {pos:.2f}")
