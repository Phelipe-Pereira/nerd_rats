import json
import os
from datetime import datetime
from typing import List, Dict, Tuple
from src.domain.entities.tracking_data import TrackingData
from src.infrastructure.services.log_service import LogService


class LocalCache:
    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or os.path.join(
            os.getenv("APPDATA"), "nerd_rats", "cache"
        )
        os.makedirs(self.cache_dir, exist_ok=True)
        self.log_service = LogService()
        self.log_service.info(f"Cache inicializado em: {self.cache_dir}")

    def save_data(self, data: TrackingData) -> None:
        """Salva os dados em um arquivo local quando falha o envio ao servidor."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"tracking_data_{timestamp}.json"
        filepath = os.path.join(self.cache_dir, filename)

        try:
            with open(filepath, "w") as f:
                json.dump(data.to_dict(), f, indent=2)
            self.log_service.info(f"Dados salvos com sucesso em: {filepath}")
        except Exception as e:
            self.log_service.error(f"Erro ao salvar dados no cache: {e}")

    def get_pending_data(self) -> List[Tuple[str, Dict]]:
        pending_data = []
        self.log_service.info(f"Buscando dados pendentes em: {self.cache_dir}")

        try:
            for filename in os.listdir(self.cache_dir):
                if filename.startswith("tracking_data_"):
                    filepath = os.path.join(self.cache_dir, filename)
                    with open(filepath, "r") as f:
                        data = json.load(f)
                        pending_data.append((filepath, data))
                        self.log_service.info(f"Arquivo carregado: {filepath}")
            
            self.log_service.info(f"Total de {len(pending_data)} arquivos pendentes encontrados")
            return pending_data
        except Exception as e:
            self.log_service.error(f"Erro ao carregar dados pendentes: {e}")
            return []

    def delete_file(self, filepath: str) -> None:
        """Remove um arquivo de cache após envio bem-sucedido."""
        try:
            os.remove(filepath)
            self.log_service.info(f"Arquivo removido com sucesso: {filepath}")
        except Exception as e:
            self.log_service.error(f"Erro ao deletar arquivo de cache {filepath}: {e}")
