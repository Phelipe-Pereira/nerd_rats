from dataclasses import dataclass
from datetime import datetime


@dataclass
class TrackingData:
    email: str
    keys_pressed: int
    mouse_distance_cm: float
    clicks: int
    scrolls: int

    def to_dict(self) -> dict:
        return {
            "email": self.email,
            "keys_pressed": self.keys_pressed,
            "mouse_distance_cm": round(self.mouse_distance_cm, 2),
            "clicks": self.clicks,
            "scrolls": self.scrolls,
            "timestamp": self.timestamp.isoformat(),
        }
