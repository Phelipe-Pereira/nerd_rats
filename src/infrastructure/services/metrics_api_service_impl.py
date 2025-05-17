import requests
from src.domain.dtos.metrics_dto import MetricsDTO
from src.domain.interfaces.metrics_api_service import MetricsApiService
from src.infrastructure.services.log_service import LogService
from src.infrastructure.config.settings import settings

class MetricsApiServiceImpl(MetricsApiService):
    def __init__(self):
        self.api_url = settings.POST_URL
        self.log_service = LogService()

    def _validate_metrics(self, metrics: MetricsDTO) -> bool:
        """Valida se todos os campos obrigatórios estão preenchidos."""
        required_fields = {
            'user_github': metrics.user_github,
            'email': metrics.email,
            'quant_clicks': metrics.quant_clicks,
            'quant_dist': metrics.quant_dist,
            'quant_scrow': metrics.quant_scrow,
            'quant_keys': metrics.quant_keys
        }
        
        for field, value in required_fields.items():
            if value is None:
                self.log_service.error(f"Campo obrigatório ausente: {field}")
                return False
            # Validação específica por tipo de campo
            if field in ['user_github', 'email']:
                if not str(value).strip():
                    self.log_service.error(f"Campo {field} não pode estar vazio")
                    return False
            elif isinstance(value, (int, float)):
                if value < 0:
                    self.log_service.error(f"Campo {field} não pode ser negativo")
                    return False
        return True

    def send_metrics(self, metrics: MetricsDTO) -> bool:
        try:
            if not self._validate_metrics(metrics):
                return False

            # Garantindo que todos os campos estejam presentes e com os tipos corretos
            payload = {
                "user_github": str(metrics.user_github).strip(),
                "email": str(metrics.email).strip(),
                "quant_clicks": max(0, int(metrics.quant_clicks)),  # Garante valor mínimo 0
                "quant_dist": max(0.0, round(float(metrics.quant_dist), 2)),  # Garante valor mínimo 0
                "quant_scrow": max(0, int(metrics.quant_scrow)),  # Garante valor mínimo 0
                "quant_keys": max(0, int(metrics.quant_keys))  # Garante valor mínimo 0
            }

            # Validação adicional do payload completo
            if not all(key in payload for key in ["user_github", "email", "quant_clicks", "quant_dist", "quant_scrow", "quant_keys"]):
                self.log_service.error(f"Payload incompleto: {payload}")
                return False

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            self.log_service.info(f"Enviando métricas para {self.api_url}")
            self.log_service.debug(f"Payload: {payload}")
            
            response = requests.post(self.api_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                self.log_service.info(f"Métricas enviadas com sucesso para {metrics.email}")
                return True
            else:
                self.log_service.error(f"Erro ao enviar métricas: {response.status_code} - {response.text}")
                self.log_service.debug(f"Payload que falhou: {payload}")
                return False

        except Exception as e:
            self.log_service.error(f"Erro ao enviar métricas: {str(e)}")
            return False 