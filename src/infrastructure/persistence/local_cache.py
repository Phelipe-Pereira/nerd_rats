import json
import os
from datetime import datetime
from typing import List, Dict
from src.domain.entities.tracking_data import TrackingData

class LocalCache:
    def __init__(self, cache_dir: str = None):
        self.cache_dir = cache_dir or os.path.join(os.getenv('APPDATA'), 'nerd_rats', 'cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        
    def save_data(self, data: TrackingData) -> None:
        """Salva os dados em um arquivo local quando falha o envio ao servidor."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"tracking_data_{timestamp}.json"
        filepath = os.path.join(self.cache_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data.to_dict(), f, indent=2)
            
    def get_pending_data(self) -> List[Dict]:
        """Recupera todos os dados pendentes de envio."""
        pending_data = []
        
        for filename in os.listdir(self.cache_dir):
            if filename.startswith("tracking_data_"):
                filepath = os.path.join(self.cache_dir, filename)
                with open(filepath, 'r') as f:
                    pending_data.append((filepath, json.load(f)))
                    
        return pending_data
        
    def delete_file(self, filepath: str) -> None:
        """Remove um arquivo de cache após envio bem-sucedido."""
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Erro ao deletar arquivo de cache {filepath}: {e}") 
 