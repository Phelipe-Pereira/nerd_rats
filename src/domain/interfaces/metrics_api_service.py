from abc import ABC, abstractmethod
from src.domain.dtos.metrics_dto import MetricsDTO

class MetricsApiService(ABC):
    @abstractmethod
    def send_metrics(self, metrics: MetricsDTO) -> bool:
        """
        Envia métricas para a API
        
        Args:
            metrics (MetricsDTO): Dados a serem enviados
            
        Returns:
            bool: True se o envio foi bem sucedido, False caso contrário
        """
        pass 