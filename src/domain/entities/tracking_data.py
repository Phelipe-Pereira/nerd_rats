from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TrackingData:
    email: str
    keys_pressed: int
    mouse_distance_cm: float
    clicks: int
    scrolls: int
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "keys_pressed": self.keys_pressed,
            "mouse_distance_cm": round(self.mouse_distance_cm, 2),
            "clicks": self.clicks,
            "scrolls": self.scrolls,
            "timestamp": self.timestamp.isoformat()
        }
