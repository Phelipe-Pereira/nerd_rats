from dataclasses import dataclass

@dataclass
class MetricsDTO:
    user_github: str
    email: str
    quant_clicks: int
    quant_dist: float
    quant_scrow: int
    quant_keys: int 