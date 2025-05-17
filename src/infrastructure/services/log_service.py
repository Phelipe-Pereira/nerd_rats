import os
import logging
import glob
from datetime import datetime, timedelta
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
        
        # Evita handlers duplicados
        if not self.logger.handlers:
            # Define o nível de log baseado na configuração
            log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
            self.logger.setLevel(log_level)
            
            # Configura o formato do log
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
            
            # Configura o handler para arquivo
            file_handler = logging.FileHandler(self.current_log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            
            # Configura o handler para console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            
            # Adiciona os handlers
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

            # Limpa logs antigos
            self._cleanup_old_logs()
    
    def _get_current_log_file(self) -> str:
        """Retorna o caminho do arquivo de log do dia atual."""
        today = datetime.now().strftime('%Y-%m-%d')
        return str(self.logs_dir / f'{today}.log')
    
    def _cleanup_old_logs(self) -> None:
        """Remove logs mais antigos que LOG_RETENTION_DAYS."""
        try:
            cutoff_date = datetime.now() - timedelta(days=settings.LOG_RETENTION_DAYS)
            for log_file in glob.glob(str(self.logs_dir / '*.log')):
                # Extrai a data do nome do arquivo
                file_date_str = os.path.basename(log_file).split('.')[0]
                try:
                    file_date = datetime.strptime(file_date_str, '%Y-%m-%d')
                    if file_date < cutoff_date:
                        os.remove(log_file)
                        self.info(f"Log antigo removido: {log_file}")
                except ValueError:
                    continue  # Ignora arquivos com formato de nome inválido
        except Exception as e:
            self.error(f"Erro ao limpar logs antigos: {e}")
    
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