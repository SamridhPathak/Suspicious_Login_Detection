import logging
from datetime import datetime
from fastapi import FastAPI, Request
from enum import Enum
from pydantic import BaseModel, Field
import joblib
import numpy as np
from pathlib import Path
import redis
from fastapi.middleware.cors import CORSMiddleware
import os
import pandas as pd

# -------------------------
# Redis Configuration
# -------------------------
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)

LOGIN_WINDOW_SECONDS = 60
MAX_ATTEMPTS_BLOCK = 5

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(title="Suspicious Login Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Suspicious Login Detection API is running",
        "docs": "/docs"
    }

# -------------------------
# Load ML Model
# -------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "suspicious_login_model.pkl"
model = joblib.load(MODEL_PATH)

# -------------------------
# Audit Logger
# -------------------------
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "audit.log"

audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter("%(asctime)s | %(message)s"))

if not audit_logger.handlers:
    audit_logger.addHandler(file_handler)

# -------------------------
# Schemas
# -------------------------
class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Action(str, Enum):
    ALLOW = "ALLOW"
    REQUIRE_OTP = "REQUIRE_OTP"
    BLOCK = "BLOCK"

class LoginRequest(BaseModel):
    login_hour: int = Field(..., ge=0, le=23)
    country: int = Field(..., ge=0)
    device: int = Field(..., ge=0)

class LoginResponse(BaseModel):
    is_suspicious: bool
    risk_level: RiskLevel
    action: Action
    reason: str

# -------------------------
# Reason Generator
# -------------------------
def generate_reasons(request: LoginRequest):
    reasons = []

    if request.login_hour < 7:
        reasons.append("Login at unusual hour")

    if request.device == 1:
        reasons.append("Login from new device")

    if request.country == 1:
        reasons.append("Login from new country")

    return reasons

# -------------------------
# Prediction Endpoint
# -------------------------
@app.post("/predict", response_model=LoginResponse)
def predict_login(request: LoginRequest, http_request: Request):

    # -------------------------
    # 1️⃣ Prepare input (NO sklearn warning)
    # -------------------------
    input_data = pd.DataFrame(
        [[request.login_hour, request.device, request.country]],
        columns=["login_hour", "device", "country"]
    )

    # -------------------------
    # 2️⃣ ML Prediction
    # -------------------------
    proba = model.predict_proba(input_data)[0]
    risk_index = int(np.argmax(proba))

    if risk_index == 0:
        risk_level = RiskLevel.LOW
        action = Action.ALLOW
        is_suspicious = False
    elif risk_index == 1:
        risk_level = RiskLevel.MEDIUM
        action = Action.REQUIRE_OTP
        is_suspicious = True
    else:
        risk_level = RiskLevel.HIGH
        action = Action.REQUIRE_OTP
        is_suspicious = True

    # -------------------------
    # 3️⃣ Rule-based override
    # -------------------------
    if (
        request.login_hour < 7
        and request.device == 1
        and request.country == 1
    ):
        risk_level = RiskLevel.HIGH
        action = Action.REQUIRE_OTP
        is_suspicious = True

    # -------------------------
    # 4️⃣ Redis Brute-Force Protection (FIXED)
    # -------------------------
    client_ip = http_request.client.host
    redis_key = f"login_attempts:{client_ip}"

    try:
        attempt_count = redis_client.incr(redis_key)
        if attempt_count == 1:
            redis_client.expire(redis_key, LOGIN_WINDOW_SECONDS)
    except Exception:
        attempt_count = 1  # Redis fallback

    if attempt_count >= MAX_ATTEMPTS_BLOCK:
        risk_level = RiskLevel.HIGH
        action = Action.BLOCK
        is_suspicious = True

    # -------------------------
    # 5️⃣ Reason
    # -------------------------
    reasons = generate_reasons(request)

    if attempt_count >= MAX_ATTEMPTS_BLOCK:
        reasons.append("Multiple failed login attempts detected")

    reason_text = ", ".join(reasons) if reasons else "Login behavior appears normal"

    # -------------------------
    # 6️⃣ Audit Log
    # -------------------------
    audit_logger.info({
        "timestamp": datetime.utcnow().isoformat(),
        "ip": client_ip,
        "login_hour": request.login_hour,
        "country": request.country,
        "device": request.device,
        "risk_level": risk_level.value,
        "action": action.value,
        "attempts": attempt_count,
        "reason": reason_text
    })

    # -------------------------
    # 7️⃣ Response
    # -------------------------
    return {
        "is_suspicious": is_suspicious,
        "risk_level": risk_level,
        "action": action,
        "reason": reason_text
    }
