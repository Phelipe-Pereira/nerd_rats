import requests
from typing import Optional
from src.domain.entities.tracking_data import TrackingData
from src.infrastructure.config.settings import settings
from .local_cache import LocalCache


class TrackingRepositoryImpl:

    def __init__(self) -> None:
        self.cache = LocalCache()

    def send_tracking_data(self, data: TrackingData) -> bool:
        try:
            response = requests.post(settings.POST_URL, json=data.to_dict())
            print(f"Dados enviados: {data.to_dict()}, Status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            self.cache.save_data(data)
            return False
