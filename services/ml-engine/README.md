# Tourism Recommendation Engine - ML Service

Production-grade FastAPI backend for tourism recommendations powered by XGBoost machine learning.

## 🏗️ Project Structure

```
services/ml-engine/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Pydantic settings
│   │   └── lifespan.py         # Startup/shutdown events
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints.py    # API routes
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── requests.py         # Request models
│   │   └── responses.py        # Response models
│   └── services/
│       ├── __init__.py
│       └── ml_service.py       # ML logic & Haversine
├── models/
│   └── enjoyment_model.json    # XGBoost model
├── data/
│   └── locations_metadata.csv  # Location data
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Features

- **Predict Enjoyment Score**: Get ML prediction for any location based on user profile
- **Smart Recommendations**: Hybrid filtering (distance + ML ranking) for top N nearby locations
- **Haversine Distance**: Accurate geospatial calculations for location proximity
- **Dependency Injection**: Clean architecture with FastAPI dependencies
- **Type Safety**: Full Python 3.10+ type hints with Pydantic v2
- **Production Ready**: Environment-based config, error handling, logging

## 📋 Prerequisites

- Python 3.10+
- pip or poetry

## ⚙️ Installation

### 1. Clone and Navigate

```bash
cd services/ml-engine
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
```

### 5. Prepare Data Files

Ensure these files exist:
- `models/enjoyment_model.json` - Trained XGBoost model
- `data/locations_metadata.csv` - Location metadata

CSV should have columns:
```
Location_Name, l_hist, l_adv, l_nat, l_rel, l_price, l_outdoor, l_lat, l_lng
```

## 🏃 Running the Application

### Development Mode

```bash
# From ml-engine directory
python -m app.main

# Or with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
# Set environment
export ENVIRONMENT=production
export DEBUG=false

# Run with production workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📡 API Endpoints

### Health Check
```http
GET /api/v1/health
```

### Predict Score
```http
POST /api/v1/predict
Content-Type: application/json

{
  "user_profile": {
    "u_hist": 0.9,
    "u_adv": 0.4,
    "u_nat": 0.6,
    "u_rel": 0.2,
    "u_bud": 0.3
  },
  "location_name": "Sigiriya Rock Fortress"
}
```

### Get Recommendations (by location)
```http
POST /api/v1/recommend
Content-Type: application/json

{
  "user_profile": {
    "u_hist": 0.9,
    "u_adv": 0.4,
    "u_nat": 0.6,
    "u_rel": 0.2,
    "u_bud": 0.3
  },
  "target_location": "Colombo",
  "max_distance_km": 50.0,
  "top_n": 5
}
```

### Get Recommendations (by GPS)
```http
POST /api/v1/recommend
Content-Type: application/json

{
  "user_profile": {
    "u_hist": 0.9,
    "u_adv": 0.4,
    "u_nat": 0.6,
    "u_rel": 0.2,
    "u_bud": 0.3
  },
  "current_lat": 6.9271,
  "current_lng": 79.8612,
  "max_distance_km": 30.0,
  "top_n": 5
}
```

## 📚 API Documentation

Interactive API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest httpx

# Run tests (when implemented)
pytest tests/
```

## 🔧 Configuration

Environment variables (`.env`):

```env
# Application
APP_NAME=Tourism Recommendation Engine
APP_VERSION=1.0.0
ENVIRONMENT=development

# API
API_V1_PREFIX=/api/v1
DEBUG=true

# Model Paths
MODEL_PATH=models/enjoyment_model.json
LOCATIONS_DATA_PATH=data/locations_metadata.csv

# Recommendation Settings
MAX_DISTANCE_KM=50.0
TOP_N_RECOMMENDATIONS=5

# Server
HOST=0.0.0.0
PORT=8000

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

## 🏗️ Architecture

### Hybrid Filtering Algorithm

1. **Candidate Generation**: Filter locations by Haversine distance
2. **ML Ranking**: Predict enjoyment score for each candidate
3. **Sorting**: Rank by score (descending), distance (ascending) as tiebreaker

### Dependency Injection

```python
from app.core.lifespan import get_ml_service
from app.services.ml_services import MLService

@router.post("/predict")
async def predict(
    request: PredictRequest,
    ml_service: Annotated[MLService, Depends(get_ml_service)]
):
    # Use ml_service...
```

### Lifespan Events

- **Startup**: Load XGBoost model and CSV data once
- **Shutdown**: Clean up resources (automatic for XGBoost/pandas)

## 📊 ML Model

- **Algorithm**: XGBoost Regressor
- **Target**: Enjoyment score (0-10)
- **Features**:
  - User preferences: u_hist, u_adv, u_nat, u_rel, u_bud
  - Location attributes: l_hist, l_adv, l_nat, l_rel, l_price, l_outdoor, l_lat, l_lng
  - Context: c_raining

## 🚢 Deployment

### Docker (recommended)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
docker build -t tourism-ml-engine .
docker run -p 8000:8000 --env-file .env tourism-ml-engine
```

## 📝 License

Proprietary - All Rights Reserved

## 👨‍💻 Author

Senior Backend Engineer & MLOps Architect
