# Pillar 6: Shadow Monitor

## Research Problem
**Plan Rigidity**: Static plans fail when weather changes.

## Solution Logic
**Autonomous Loop**: A background process that polls Weather APIs.
- IF Rain > 5mm THEN Reroute to Indoor Alternative
- Continuous monitoring until trip date

## Technology
- **Weather API**: OpenWeatherMap / Tomorrow.io
- **Pattern**: Background polling with webhooks
- **Integration**: Real-time itinerary updates

## Workflow
1. User creates itinerary with outdoor activities
2. Shadow Monitor subscribes to weather updates
3. On weather change detection:
   - Evaluate impact (rain, storm, extreme heat)
   - Find indoor alternatives nearby
   - Notify user with reroute options

## Current State
- `c_raining` feature exists in XGBoost model
- Currently hardcoded as `False`
- Real-time API integration pending

## Status: ARCHITECTURE PLANNED (Implementation pending)

## Files
```
pillar_6_shadow_monitor/
└── (pending implementation)
```

## Required Dependencies
```bash
pip install httpx  # For async API calls
```

## Sample Weather Response (Future)
```json
{
  "location": "Sigiriya",
  "forecast": {
    "rain_probability": 0.75,
    "rain_mm": 8.5,
    "recommendation": "REROUTE",
    "alternatives": ["Dambulla Cave Temple", "Sigiriya Museum"]
  }
}
```
