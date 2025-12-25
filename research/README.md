# Travion Research & Development

This folder contains all research notebooks, training data, and experimental models for the 7 Pillars of Intelligence.

## Folder Structure

```
research/
├── pillar_1_specialist_boost/    # XGBoost Recommendation Engine
│   ├── notebooks/                # Training notebooks
│   ├── data/                     # Training data & generators
│   └── models/                   # Trained models
│
├── pillar_2_crowdcast/           # Crowd Prediction Engine
│   ├── notebooks/                # Model training
│   ├── data/                     # Datasets & pipelines
│   │   └── holidays/             # Sri Lankan holiday calendars
│   └── models/                   # Random Forest models
│
├── pillar_3_visual_matcher/      # CLIP Visual Search
│   ├── notebooks/                # ChromaDB setup
│   └── data/                     # Knowledge base
│
├── pillar_4_event_sentinel/      # Poya Calendar & Events
│   └── data/                     # Holiday databases
│
├── pillar_5_golden_hour/         # Sun Position Agent
│   └── (pending)
│
├── pillar_6_shadow_monitor/      # Weather Adaptation
│   └── (pending)
│
├── pillar_7_storyteller/         # LLM + TTS
│   ├── notebooks/                # Fine-tuning setup
│   └── data/                     # Training data
│
├── shared/                       # Shared resources
│   └── locations_metadata.csv    # 80 Sri Lankan locations
│
└── vector_db/                    # ChromaDB persistent storage
```

## Implementation Status

| Pillar | Name | Status |
|--------|------|--------|
| 1 | Specialist Boost | ✅ Deployed |
| 2 | CrowdCast | ✅ Trained |
| 3 | Visual Matcher | 🔶 Partial |
| 4 | Event Sentinel | 🔶 Data Ready |
| 5 | Golden Hour | ❌ Pending |
| 6 | Shadow Monitor | ❌ Pending |
| 7 | Storyteller | 🔶 Pipeline Ready |
