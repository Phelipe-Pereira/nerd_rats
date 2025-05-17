import requests
from typing import Optional
from src.domain.entities.tracking_data import TrackingData
from src.infrastructure.config.settings import settings
from src.infrastructure.services.log_service import LogService
from .local_cache import LocalCache


class TrackingRepositoryImpl:

    def __init__(self) -> None:
        self.cache = LocalCache()
        self.log_service = LogService()

    def send_tracking_data(self, data: TrackingData) -> bool:
        try:
            response = requests.post(settings.POST_URL, json=data.to_dict())
            self.log_service.info(f"Dados enviados: {data.to_dict()}, Status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            self.cache.save_data(data)
            self.log_service.error(f"Erro ao enviar dados: {str(e)}")
            return False
