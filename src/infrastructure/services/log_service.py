import os
import logging
from datetime import datetime
from pathlib import Path
from src.infrastructure.config.settings import settings

class LogService:
    def __init__(self):
        # Configura o diretório de logs
        self.logs_dir = Path(__file__).parent.parent / 'logs'
        self.logs_dir.mkdir(exist_ok=True)
        
        # Configura o arquivo de log atual
        self.current_log_file = self._get_current_log_file()
        
        # Configura o logger
        self.logger = logging.getLogger('nerd_rats')
        self.logger.setLevel(logging.INFO)
        
        # Configura o formato do log
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
        
        # Configura o handler para arquivo
        file_handler = logging.FileHandler(self.current_log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def _get_current_log_file(self) -> str:
        """Retorna o caminho do arquivo de log do dia atual."""
        today = datetime.now().strftime('%Y-%m-%d')
        return str(self.logs_dir / f'{today}.log')
    
    def info(self, message: str) -> None:
        """Registra uma mensagem de informação."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Registra uma mensagem de aviso."""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Registra uma mensagem de erro."""
        self.logger.error(message)
    
    def debug(self, message: str) -> None:
        """Registra uma mensagem de debug."""
        self.logger.debug(message) 