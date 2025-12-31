import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report

# -------------------------
# Paths
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "login_data_augmented.csv"
MODEL_PATH = BASE_DIR / "ml" / "suspicious_login_model.pkl"

# -------------------------
# Load dataset
# -------------------------
df = pd.read_csv(DATA_PATH)

# Expected columns:
# login_hour, device, country, label

X = df[["login_hour", "device", "country"]]
y = df["label"]

# -------------------------
# Train / Test split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# -------------------------
# Base model
# -------------------------
base_model = RandomForestClassifier(
    n_estimators=150,
    max_depth=10,
    random_state=42
)

# -------------------------
# Calibrated model
# -------------------------
calibrated_model = CalibratedClassifierCV(
    base_model,
    method="isotonic",   # best for RandomForest
    cv=3
)

# -------------------------
# Train
# -------------------------
calibrated_model.fit(X_train, y_train)

# -------------------------
# Evaluation
# -------------------------
y_pred = calibrated_model.predict(X_test)
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# -------------------------
# Save model
# -------------------------
joblib.dump(calibrated_model, MODEL_PATH)

print(f"\n✅ Model trained & saved at: {MODEL_PATH}")