# 🔐 Suspicious Login Detection System

A full-stack security system that simulates and detects suspicious login attempts using **machine learning**, **rule-based security logic**, and **real-time rate limiting**, presented through a **modern React UI**.

---

## 📌 Project Overview

This project analyzes login attempts based on:
- Login time
- Device familiarity
- Country familiarity

Each login attempt is classified into one of three risk levels:
- 🟢 **LOW** – Safe login
- 🟡 **MEDIUM** – Requires OTP verification
- 🔴 **HIGH** – Potential attack (blocked after multiple attempts)

The objective is to **simulate real-world authentication systems** used by banks, SaaS platforms, and enterprise applications.

---

## 🧠 Key Features

- Machine-learning-based risk classification
- Three-level risk model: **LOW / MEDIUM / HIGH**
- Rule-based security overrides for critical patterns
- Redis-backed brute-force attack detection
- Clean FastAPI backend architecture
- React-based frontend with risk-aware UI
- Frontend input validation and defensive UX
- Audit logging for traceability and analysis

---

## 🛠️ Technologies & Tools Used

### Frontend
- React.js
- JavaScript (ES6)
- HTML5
- CSS3 (custom dark theme)
- Fetch API
- Client-side input validation

### Backend
- FastAPI
- Python 3
- Pydantic (data validation)
- Uvicorn (ASGI server)
- CORS Middleware

### Machine Learning
- scikit-learn
- RandomForestClassifier (multi-class)
- Synthetic dataset generation
- Feature engineering
- Model persistence using Joblib

### Data & Storage
- CSV dataset (generated login behavior)
- Redis (Docker-based) for rate limiting
- File-based audit logging

### Development & Infrastructure
- Docker (Redis container)
- Python virtual environment (venv)
- Git & GitHub
- VS Code

---

## 🔐 Security Rules

- Unusual hour + new device + new country → **HIGH risk**
- More than 5 rapid attempts → **BLOCK**
- Confidence scores are intentionally **not exposed** to prevent model probing

---

## 🔄 Project Workflow (Brief)

1. **Dataset Generation**
   - Generated synthetic login data using realistic constraints
   - Labeled data into LOW, MEDIUM, and HIGH risk classes

2. **Model Training**
   - Trained a multi-class Random Forest classifier
   - Evaluated and saved the trained model using Joblib

3. **Backend Integration**
   - Loaded ML model into FastAPI
   - Added rule-based overrides for security-critical cases
   - Implemented Redis-based rate limiting
   - Logged all decisions for audit purposes

4. **Frontend Development**
   - Built a React-based UI for login simulation
   - Implemented risk-based visual indicators
   - Added strict input validation
   - Displayed backend decisions clearly to users

5. **Testing & Validation**
   - Verified LOW, MEDIUM, HIGH, and BLOCK scenarios
   - Tested boundary conditions and invalid inputs

---

## 📸 Screenshots

### 🟢 LOW Risk – Normal Login
<img width="1905" height="993" alt="01_low_risk_normal_login" src="https://github.com/user-attachments/assets/08f6b63e-7def-4b8d-9391-05bb9af41744" />

### 🟡 MEDIUM Risk – New Device & Country
<img width="1904" height="1000" alt="02_medium_risk_new_device_country" src="https://github.com/user-attachments/assets/bd0bea49-6867-459b-a2fd-f2a0c40ca61d" />

### 🟡 MEDIUM Risk – Unusual Hour
<img width="1910" height="992" alt="03_medium_risk_unusual_hour" src="https://github.com/user-attachments/assets/671fe7cf-8cb6-4b76-954a-90b63827a1c0" />


### 🔴 HIGH Risk – Critical Pattern
<img width="1910" height="996" alt="04_high_risk_critical_pattern" src="https://github.com/user-attachments/assets/5d2e9b7d-c798-4263-a288-c99515c6caec" />


### 🚫 BLOCKED – Brute Force Detected
<img width="1906" height="991" alt="05_blocked_after_multiple_attempts" src="https://github.com/user-attachments/assets/e85928bc-54bf-43e7-b67a-6606671e4cb2" />


### ⚠️ Input Validation Alert
<img width="1906" height="1004" alt="06_input_validation_alert" src="https://github.com/user-attachments/assets/2ef605a6-636a-4487-8060-1c54abadb394" />

---

## 📈 Future Enhancements

1. OTP verification workflow
2. User-specific behavioral profiling
3. Admin dashboard for audit logs
4. Cloud deployment (AWS / Azure)
5. JWT-based authentication

---

## ⭐ Final Note

This project demonstrates real-world security thinking, combining machine learning, backend engineering, and frontend UX in a practical and scalable way.
