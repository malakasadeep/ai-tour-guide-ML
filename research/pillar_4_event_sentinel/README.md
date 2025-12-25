# Pillar 4: Event Sentinel

## Research Problem
**Cultural Context Blindness**: Apps ignore local events (Poya days) causing logistical failures.

## Solution Logic
**Constraint Satisfaction**: Checks date against a Lunar Calendar.
- IF Poya AND Activity = Alcohol THEN Block
- IF Vesak AND Location = Temple THEN Expect High Crowd

## Technology
- Rule-based constraint system
- Lunar calendar integration
- Holiday database (2021-2025)

## Key Events
| Event | Impact |
|-------|--------|
| **Poya Days** | No alcohol sales, temples crowded |
| **Vesak** | Major Buddhist festival, nationwide |
| **Poson** | Mihintale pilgrimage |
| **Esala Perahera** | Kandy festival (July/August) |
| **School Holidays** | Family destinations crowded |

## Status: DATA READY (API integration pending)

## Files
```
pillar_4_event_sentinel/
└── data/
    ├── consolidated_holidays.csv   # All holidays 2021-2025
    ├── 2021.csv                    # Year-specific holidays
    ├── 2022.csv
    ├── 2023.csv
    ├── 2024.csv
    └── 2025.csv
```

## Integration Points
- CrowdCast: `is_poya_holiday`, `is_school_holiday` features
- Recommendation: Block/boost based on event context
