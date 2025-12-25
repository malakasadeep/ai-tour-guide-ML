# Pillar 1: Specialist Boost Engine

## Research Problem
**The Cold Start Problem**: Average ratings fail for niche users (e.g., History buffs).

## Solution Logic
**Max-Match Algorithm**: Boosts score if one specific interest strongly aligns, ignoring low scores in other categories.

## Technology
- **Model**: XGBoost Regressor
- **Performance**: R² = 0.9753, RMSE = 0.3272

## Features (12 inputs)
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

## Status: IMPLEMENTED

## Files
```
pillar_1_specialist_boost/
├── notebooks/
│   └── model_train.ipynb       # Training notebook with GridSearchCV
├── data/
│   ├── generate_data.py        # Synthetic data generator
│   └── training_interactions.csv  # 9,000 training samples
└── models/
    └── (exported to services/ml-engine/models/)
```

## Deployed Location
`services/ml-engine/models/enjoyment_model.json`
