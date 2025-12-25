# Travion: AI Agentic Tour Guide for Sri Lanka

## Project Reference Document

> This document serves as a comprehensive reference for the Travion project architecture, implementation status, and future development roadmap.

---

## 1. Executive Summary

**Travion** (Travel Vision Agent) is a proactive, multi-modal travel agent designed to solve the rigidity of traditional tourism apps. Unlike standard recommenders that output static lists, Travion operates as an autonomous agent that can:

- **"See"** - Visual Search (CLIP-based image matching)
- **"Predict"** - CrowdCast (crowd density forecasting)
- **"Adapt"** - Shadow Monitor (real-time weather rerouting)

### Architectural Paradigm
**Neuro-Symbolic AI (Hybrid Architecture)** - Combining the creative reasoning of Large Language Models (LLMs) with the strict logic of rule-based systems (Physics/Calendar constraints).

---

## 2. High-Level Architecture

The system follows a **Microservices "Sidecar" Pattern** to separate application logic from heavy AI computation.

### A. The Orchestrator (Node.js Gateway)
- **Role**: Central Nervous System
- **Responsibilities**:
  - Handle high-concurrency user requests (WebSockets/REST)
  - Manage User Authentication (JWT)
  - Perform initial Geospatial Filtering using MongoDB `$near` operators

### B. The Brain (Python AI Engine)
- **Role**: Intelligence Microservice
- **Responsibilities**:
  - Inference Server: Runs XGBoost, Random Forest, and CLIP models
  - Agent Controller: Executes LangGraph workflows (Think → Act → Validate loops)
  - Vector Search: Manages semantic retrieval from ChromaDB

### C. The Memory (Dual-Database Layer)
- **MongoDB**: Structured data (User Profiles, Trip Itineraries, Logs)
- **ChromaDB**: Unstructured vector embeddings
  - Text Vectors: Split by aspect (`_history`, `_nature`, `_logistics`)
  - Image Vectors: CLIP embeddings for Visual Search

---

## 3. Seven Pillars of Intelligence

| # | Module Name | Research Problem | Solution Logic | Status |
|---|-------------|------------------|----------------|--------|
| 1 | **Specialist Boost Engine** | Cold Start Problem: Average ratings fail for niche users | Max-Match Algorithm with XGBoost | ✅ Deployed |
| 2 | **CrowdCast Engine** | Overtourism: Peak locations at peak times | Spatiotemporal Prediction with Random Forest | ✅ Trained |
| 3 | **Visual Vibe Matcher** | Semantic Gap: Users can't describe visual preferences | Cross-Modal Retrieval with OpenAI CLIP | 🔶 Partial |
| 4 | **Event Sentinel** | Cultural Context Blindness: Apps ignore local events | Constraint Satisfaction with Lunar Calendar | 🔶 Data Ready |
| 5 | **Golden Hour Agent** | Aesthetic Ignorance: Ignoring lighting conditions | Physics Calculation with `astral` library | 📋 Pending |
| 6 | **Shadow Monitor** | Plan Rigidity: Static plans fail when weather changes | Autonomous Loop polling Weather APIs | 📋 Pending |
| 7 | **Storyteller** | Content Accessibility: Guidebooks are boring | Generative Audio with Llama 3 + TTS | 🔶 Pipeline Ready |

---

## 4. Project Structure

```
ai-tour-guide-backend/
│
├── docs/                                    # DOCUMENTATION
│   └── PROJECT_REFERENCE.md                 # This file
│
├── services/                                # PRODUCTION SERVICES
│   │
│   ├── ml-engine/                           # Python AI Engine (The Brain)
│   │   ├── app/
│   │   │   ├── main.py                      # FastAPI application entry
│   │   │   ├── core/
│   │   │   │   ├── config.py                # Pydantic Settings
│   │   │   │   └── lifespan.py              # Startup/shutdown events
│   │   │   ├── api/v1/
│   │   │   │   └── endpoints.py             # REST API endpoints
│   │   │   ├── schemas/
│   │   │   │   ├── requests.py              # Request validation
│   │   │   │   └── responses.py             # Response models
│   │   │   └── services/
│   │   │       ├── ml_services/
│   │   │       │   └── predictor.py         # MLService (core logic)
│   │   │       └── pillars/                 # 7 Pillars (future)
│   │   ├── models/
│   │   │   └── enjoyment_model.json         # XGBoost model (2.1 MB)
│   │   ├── data/
│   │   │   └── locations_metadata.csv       # 80 locations
│   │   ├── requirements.txt
│   │   ├── run.py
│   │   └── README.md
│   │
│   └── gateway/                             # Node.js Gateway (Orchestrator)
│       ├── server.js                        # (pending)
│       └── package.json
│
├── research/                                # RESEARCH & DEVELOPMENT
│   │
│   ├── pillar_1_specialist_boost/           # P1: XGBoost Recommender
│   │   ├── notebooks/
│   │   │   └── model_train.ipynb            # Training with GridSearchCV
│   │   ├── data/
│   │   │   ├── generate_data.py             # Synthetic data generator
│   │   │   └── training_interactions.csv    # 9,000 samples
│   │   ├── models/
│   │   └── README.md
│   │
│   ├── pillar_2_crowdcast/                  # P2: Crowd Prediction
│   │   ├── notebooks/
│   │   │   └── crowdcast_model_training.ipynb
│   │   ├── data/
│   │   │   ├── crowd_data_pipeline.py       # Data scraping pipeline
│   │   │   ├── crowdcast_dataset.csv        # 3.5M samples
│   │   │   ├── google_trends_raw.csv
│   │   │   ├── popular_times_default.json
│   │   │   └── holidays/
│   │   │       ├── 2021-2025.csv            # Year-wise holidays
│   │   │       └── consolidated_holidays.csv
│   │   ├── models/
│   │   │   ├── crowdcast_model.joblib       # Random Forest
│   │   │   ├── crowdcast_model.json
│   │   │   ├── label_encoder.joblib
│   │   │   └── metadata.json
│   │   └── README.md
│   │
│   ├── pillar_3_visual_matcher/             # P3: CLIP Visual Search
│   │   ├── notebooks/
│   │   │   └── knowledge_base_builder.ipynb # ChromaDB setup
│   │   ├── data/
│   │   │   └── sri_lanka_knowledge_base.json
│   │   └── README.md
│   │
│   ├── pillar_4_event_sentinel/             # P4: Poya Calendar
│   │   ├── data/
│   │   │   ├── consolidated_holidays.csv
│   │   │   └── 2021-2025.csv
│   │   └── README.md
│   │
│   ├── pillar_5_golden_hour/                # P5: Sun Position (pending)
│   │   └── README.md
│   │
│   ├── pillar_6_shadow_monitor/             # P6: Weather (pending)
│   │   └── README.md
│   │
│   ├── pillar_7_storyteller/                # P7: LLM + TTS
│   │   ├── notebooks/
│   │   │   └── llm_finetuning_sri_lankan_tour_guide.ipynb
│   │   ├── data/
│   │   │   └── finetune_dataset_metadata.json
│   │   └── README.md
│   │
│   ├── shared/                              # Shared resources
│   │   └── locations_metadata.csv           # Master location list
│   │
│   ├── vector_db/                           # ChromaDB storage
│   │
│   └── README.md                            # Research overview
│
└── .gitignore
```

---

## 5. Implementation Details

### 5.1 Specialist Boost Engine (✅ Implemented)

**Technology**: XGBoost Regressor v2.0.3

**Location**: `services/ml-engine/app/services/ml_services/predictor.py`

**Features (12 inputs)**:
| Feature | Description | Range |
|---------|-------------|-------|
| `u_hist` | User interest in historical sites | 0.0 - 1.0 |
| `u_adv` | User interest in adventure | 0.0 - 1.0 |
| `u_nat` | User interest in nature | 0.0 - 1.0 |
| `u_rel` | User interest in religious sites | 0.0 - 1.0 |
| `l_hist` | Location historical significance | 0.0 - 1.0 |
| `l_adv` | Location adventure level | 0.0 - 1.0 |
| `l_nat` | Location natural beauty | 0.0 - 1.0 |
| `l_rel` | Location religious significance | 0.0 - 1.0 |
| `l_outdoor` | Is outdoor activity | 0 or 1 |
| `l_lat` | Location latitude | GPS |
| `l_lng` | Location longitude | GPS |
| `c_raining` | Current weather condition | 0 or 1 |

**Algorithm**:
1. Candidate generation (Haversine distance filtering)
2. ML ranking (XGBoost predictions)
3. Sort by score (desc) then distance (asc)

**Performance Metrics**:
- **R² Score**: 0.9753 (97.53% variance explained)
- **RMSE**: 0.3272
- **MAE**: 0.2539

**Recommendation Levels**:
```
Score >= 7.5: "HIGHLY RECOMMENDED"
Score >= 6.0: "RECOMMENDED"
Score >= 4.0: "MIGHT ENJOY"
Score < 4.0:  "NOT RECOMMENDED"
```

**Model Hyperparameters** (after GridSearchCV):
```python
{
    "n_estimators": 200,
    "max_depth": 8,
    "learning_rate": 0.05,
    "subsample": 0.9,
    "colsample_bytree": 1.0,
    "gamma": 0,
    "min_child_weight": 3
}
```

### 5.2 Semantic Knowledge Base (✅ Implemented)

**Technology**: ChromaDB v0.5.0 + OpenAI text-embedding-3-small

**Location**: `research/vector_db/`

**Structure**:
- **Collection**: `tourism_knowledge`
- **Documents**: 480 (6 aspects × 80 locations)
- **Embedding Dimension**: 1536

**Aspects per Location**:
| Aspect | Content |
|--------|---------|
| `_history` | Historical background, colonial influences |
| `_adventure` | Activities, safety tips |
| `_nature` | Wildlife, flora, ecosystem |
| `_culture` | Traditions, festivals, cuisine |
| `_logistics` | Price, hours, best time to visit |
| `_vibe` | Atmosphere tags and keywords |

### 5.3 LLM Fine-tuning Pipeline (📋 Ready, Not Trained)

**Notebook**: `research/notebooks/llm_finetuning_sri_lankan_tour_guide.ipynb`

**Model**: Meta-Llama-3.1-8B-Instruct (4-bit quantized)

**Framework**: Unsloth + LoRA (2-5x faster, 80% less memory)

**Dataset**: 343 Alpaca-format examples

**System Prompt**:
```
You are an expert Sri Lankan Tour Guide with warm hospitality...
```

**Export Options**:
- GGUF (for Ollama local deployment)
- HuggingFace Hub
- LoRA adapters only

---

## 6. API Reference

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model_loaded": true,
  "locations_loaded": 80
}
```

#### 2. Predict Enjoyment Score
```http
POST /predict
Content-Type: application/json
```

**Request**:
```json
{
  "user_profile": {
    "u_hist": 0.9,
    "u_adv": 0.4,
    "u_nat": 0.6,
    "u_rel": 0.2
  },
  "location_name": "Sigiriya Rock Fortress"
}
```

**Response**:
```json
{
  "location_name": "Sigiriya Rock Fortress",
  "predicted_score": 8.75,
  "recommendation_level": "HIGHLY RECOMMENDED",
  "location_attributes": {
    "l_hist": 1.0,
    "l_adv": 0.7,
    "l_nat": 0.8,
    "l_rel": 0.1,
    "l_outdoor": 0.9,
    "l_lat": 7.957,
    "l_lng": 80.7603
  }
}
```

#### 3. Get Recommendations
```http
POST /recommend
Content-Type: application/json
```

**Request (by location)**:
```json
{
  "user_profile": {
    "u_hist": 0.9,
    "u_adv": 0.4,
    "u_nat": 0.6,
    "u_rel": 0.2
  },
  "target_location": "Colombo",
  "max_distance_km": 50.0,
  "top_n": 5
}
```

**Request (by GPS)**:
```json
{
  "user_profile": {
    "u_hist": 0.9,
    "u_adv": 0.4,
    "u_nat": 0.6,
    "u_rel": 0.2
  },
  "current_lat": 6.9271,
  "current_lng": 79.8612,
  "max_distance_km": 30.0,
  "top_n": 5
}
```

**Response**:
```json
{
  "search_origin": {
    "type": "location",
    "name": "Colombo",
    "lat": 6.9271,
    "lng": 79.8612
  },
  "total_candidates": 15,
  "recommendations": [
    {
      "rank": 1,
      "location_name": "Galle Fort",
      "predicted_score": 8.75,
      "recommendation_level": "HIGHLY RECOMMENDED",
      "distance_km": 12.5,
      "latitude": 6.0329,
      "longitude": 80.2168,
      "highlights": {
        "historical": 0.9,
        "adventure": 0.2,
        "nature": 0.6,
        "religious": 0.3,
        "outdoor": 0.5
      }
    }
  ],
  "max_distance_km": 50.0,
  "user_profile": {...}
}
```

---

## 7. Technology Stack

### Backend Core
| Component | Version | Purpose |
|-----------|---------|---------|
| FastAPI | 0.109.0 | REST API framework |
| Uvicorn | 0.27.0 | ASGI server |
| Python | 3.10+ | Runtime |
| Pydantic | 2.5.3 | Data validation |

### Machine Learning
| Component | Version | Purpose |
|-----------|---------|---------|
| XGBoost | 2.0.3 | Enjoyment prediction |
| Pandas | 2.2.0 | Data manipulation |
| NumPy | 1.26.3 | Numerical computation |
| scikit-learn | 1.4.0 | Model evaluation |

### Semantic Search
| Component | Version | Purpose |
|-----------|---------|---------|
| ChromaDB | 0.5.0 | Vector database |
| OpenAI API | Latest | Embeddings (text-embedding-3-small) |

### LLM (Planned)
| Component | Purpose |
|-----------|---------|
| Llama 3.1 8B | Base model |
| Unsloth | Fast fine-tuning |
| LoRA/PEFT | Parameter-efficient training |
| LangGraph | Agent orchestration |

---

## 8. Data Assets

### 8.1 Locations Database
**File**: `services/ml-engine/data/locations_metadata.csv`

**Coverage**: 80 major Sri Lankan attractions across all regions:
- Sigiriya/Dambulla Hub (7 locations)
- Kandy Hub (9 locations)
- Nuwara Eliya Hub (8 locations)
- Ella Hub (7 locations)
- Galle/South Coast (10 locations)
- Ancient Cities (7 locations)
- East Coast (9 locations)
- Colombo & West (9 locations)
- North/Jaffna (7 locations)

### 8.2 Knowledge Base
**File**: `research/data/raw/sri_lanka_knowledge_base.json`

**Structure per location**:
```json
{
  "name": "Sigiriya Rock Fortress",
  "type": "Historical Site",
  "descriptions": {...},
  "history": "...",
  "adventure": "...",
  "nature": "...",
  "culture": "...",
  "logistics": {...},
  "vibe_tags": ["ancient", "majestic", "UNESCO"]
}
```

### 8.3 Training Data
**Generator**: `research/data/raw/generate_data.py`

**Specifications**:
- 600 simulated users × 15 interactions = 9,000 records
- 6 user archetypes:
  - Backpacker: [0.2, 0.9, 0.7, 0.3]
  - Historian: [0.9, 0.2, 0.4, 0.4]
  - Luxury_Relax: [0.1, 0.1, 0.4, 0.9]
  - Nature_Lover: [0.2, 0.6, 0.9, 0.5]
  - Family_Vacation: [0.4, 0.3, 0.5, 0.7]
  - Digital_Nomad: [0.1, 0.5, 0.5, 0.8]

---

## 9. Agentic Workflow Example

**Scenario**: User uploads a photo of a "Misty Mountain" and asks to visit next Full Moon.

```
1. PERCEPTION (Visual Matcher)
   └── CLIP converts image to vector → ChromaDB search
   └── Result: Identifies "Riverston Gap" (94% Match)

2. CONTEXTUALIZATION (Event Sentinel)
   └── Checks "Next Full Moon" date
   └── Result: "Poson Poya" - No Alcohol Sales constraint

3. PREDICTION (CrowdCast)
   └── Queries Crowd Model for "Riverston" on "Poson Poya"
   └── Result: High Traffic (85%) at 10:00 AM

4. OPTIMIZATION (Reasoning Loop)
   └── Agent (Llama 3) analyzes: "Crowd high at 10 AM"
   └── Golden Hour Agent checks sunset: 6:15 PM
   └── Decision: Schedule for 4:30 PM (lower crowd + sunset)

5. EXECUTION (Response)
   └── Generate Itinerary
   └── Append "Storyteller" button for Riverston legend

6. RESILIENCE (Shadow Monitor)
   └── Subscribe itinerary to Weather Watcher queue
   └── Active monitoring until trip date
```

---

## 10. Configuration

### Environment Variables
```env
# Application
APP_NAME=Tourism Recommendation Engine
APP_VERSION=1.0.0
ENVIRONMENT=development

# API
API_V1_PREFIX=/api/v1
DEBUG=true

# Model Paths
XGBOOST_MODEL_PATH=models/enjoyment_model.json
LOCATIONS_DATA_PATH=data/locations_metadata.csv

# Recommendations
MAX_DISTANCE_KM=50.0
TOP_N_RECOMMENDATIONS=5

# Server
HOST=0.0.0.0
PORT=8000

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

---

## 11. Running the Application

### Development
```bash
cd services/ml-engine

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run with auto-reload
python run.py
# OR
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
export ENVIRONMENT=production
export DEBUG=false

uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker
```bash
docker build -t tourism-ml-engine .
docker run -p 8000:8000 --env-file .env tourism-ml-engine
```

### API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 12. Research Novelty

### Multi-Objective Dynamic Optimization

Standard apps optimize for **Relevance** (User Likes).

Travion simultaneously optimizes for:
1. **Relevance** - Specialist Boost Engine
2. **Comfort** - CrowdCast Engine
3. **Aesthetics** - Golden Hour Agent
4. **Resilience** - Shadow Monitor

This approach contributes to the field of **Smart Tourism** by introducing real-time, context-aware, multi-dimensional recommendation optimization.

---

## 13. Future Development Roadmap

### Phase 1: Core Infrastructure (Current)
- [x] XGBoost recommendation model
- [x] FastAPI backend with 3 endpoints
- [x] ChromaDB semantic knowledge base
- [x] Training pipeline with GridSearchCV
- [ ] Unit tests and integration tests

### Phase 2: Weather & Calendar Integration
- [ ] Shadow Monitor: Weather API integration
- [ ] Event Sentinel: Poya calendar database
- [ ] Real-time `c_raining` feature updates

### Phase 3: Visual & Crowd Intelligence
- [ ] Visual Vibe Matcher: CLIP model integration
- [ ] Location image dataset collection
- [ ] CrowdCast: Historical crowd data collection
- [ ] Google Trends API integration

### Phase 4: LLM & Audio
- [ ] Complete Llama 3.1 fine-tuning
- [ ] Storyteller TTS integration
- [ ] LangGraph agent orchestration

### Phase 5: Production & Scale
- [ ] Node.js gateway implementation
- [ ] MongoDB user profile persistence
- [ ] Authentication (JWT)
- [ ] Mobile app (React Native)
- [ ] A/B testing framework

---

## 14. Key Files Quick Reference

| Purpose | File Path |
|---------|-----------|
| FastAPI Entry | `services/ml-engine/app/main.py` |
| ML Predictor | `services/ml-engine/app/services/ml_services/predictor.py` |
| API Endpoints | `services/ml-engine/app/api/v1/endpoints.py` |
| Request Schemas | `services/ml-engine/app/schemas/requests.py` |
| Response Schemas | `services/ml-engine/app/schemas/responses.py` |
| Config | `services/ml-engine/app/core/config.py` |
| XGBoost Model | `services/ml-engine/models/enjoyment_model.json` |
| Locations CSV | `services/ml-engine/data/locations_metadata.csv` |
| Model Training | `research/notebooks/model_train.ipynb` |
| Knowledge Base Builder | `research/notebooks/knowledge_base_builder.ipynb` |
| LLM Fine-tuning | `research/notebooks/llm_finetuning_sri_lankan_tour_guide.ipynb` |
| Knowledge Base JSON | `research/data/raw/sri_lanka_knowledge_base.json` |
| Data Generator | `research/data/raw/generate_data.py` |

---

## 15. Contact & Resources

- **Project**: Travion - AI Agentic Tour Guide for Sri Lanka
- **Institution**: SLIIT (Sri Lanka Institute of Information Technology)
- **Type**: Research Project

---

*Last Updated: December 2024*
