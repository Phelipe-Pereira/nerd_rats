import requests
from src.domain.dtos.metrics_dto import MetricsDTO
from src.domain.interfaces.metrics_api_service import MetricsApiService
from src.infrastructure.services.log_service import LogService

class MetricsApiServiceImpl(MetricsApiService):
    def __init__(self):
        self.api_url = "https://nerds-rats-hackathon.onrender.com/metrics"
        self.log_service = LogService()

    def send_metrics(self, metrics: MetricsDTO) -> bool:
        try:
            payload = {
                "user_github": metrics.user_github,
                "email": metrics.email,
                "quant_clicks": metrics.quant_clicks,
                "quant_dist": metrics.quant_dist,
                "quant_scrow": metrics.quant_scrow,
                "quant_keys": metrics.quant_keys
            }

            response = requests.post(self.api_url, json=payload)
            
            if response.status_code == 200:
                self.log_service.info(f"Métricas enviadas com sucesso para {metrics.email}")
                return True
            else:
                self.log_service.error(f"Erro ao enviar métricas: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            self.log_service.error(f"Erro ao enviar métricas: {str(e)}")
            return False 