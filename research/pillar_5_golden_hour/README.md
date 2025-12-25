# Pillar 5: Golden Hour Agent

## Research Problem
**Aesthetic Ignorance**: Recommenders ignore lighting conditions for photography.

## Solution Logic
**Physics Calculation**: Uses `astral` library to calculate sun elevation. Auto-schedules scenic spots during Golden Hour (-4° to 6° elevation).

## Technology
- **Library**: astral (Python)
- **Calculation**: Sun position based on GPS coordinates and datetime
- **Output**: Optimal visit windows for photography

## Golden Hour Definition
| Phase | Sun Elevation | Description |
|-------|---------------|-------------|
| Blue Hour | -6° to -4° | Deep blue sky, calm atmosphere |
| Golden Hour | -4° to 6° | Warm, soft light ideal for photos |
| Harsh Light | > 20° | Avoid for photography |

## Use Cases
- Sigiriya sunrise (5:30 AM - 6:30 AM)
- Galle Fort sunset (5:45 PM - 6:15 PM)
- Nine Arches Bridge golden light

## Status: NOT IMPLEMENTED

## Files
```
pillar_5_golden_hour/
└── (pending implementation)
```

## Required Dependencies
```bash
pip install astral
```

## Sample Code (Future)
```python
from astral import LocationInfo
from astral.sun import sun

location = LocationInfo("Sigiriya", "Sri Lanka", "Asia/Colombo", 7.957, 80.760)
s = sun(location.observer, date=datetime.date.today())
print(f"Sunrise: {s['sunrise']}")
print(f"Golden Hour: {s['sunrise']} - {s['sunrise'] + timedelta(hours=1)}")
```
