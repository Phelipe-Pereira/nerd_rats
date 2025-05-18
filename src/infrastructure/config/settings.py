import os
from typing import Optional
from pathlib import Path


class Settings:
    # Configurações mockadas diretamente no código
    POST_URL: str = "https://nerds-rats-hackathon.onrender.com/metrics"
    INTERVAL: int = 15  # segundos
    LOG_LEVEL: str = "INFO"
    LOG_RETENTION_DAYS: int = 30
    
    # Usando AppData no Windows ou /etc no Linux
    CONFIG_PATH: str = os.getenv(
        "CONFIG_PATH",
        str(Path.home() / "AppData" / "Local" / "nerd_rats" / "config.ini") if os.name == "nt"
        else "/etc/nerd_rats.conf"
    )

    @staticmethod
    def _read_config_value(key: str) -> Optional[str]:
        """Método interno para ler um valor do arquivo de configuração."""
        if os.path.exists(Settings.CONFIG_PATH):
            try:
                with open(Settings.CONFIG_PATH, "r") as f:
                    for line in f:
                        if line.startswith(f"{key}="):
                            return line.strip().split("=", 1)[1]
            except Exception as e:
                print(f"Falha ao ler configuração: {e}")
        return None

    @staticmethod
    def read_email() -> Optional[str]:
        """Lê o email do arquivo de configuração."""
        return Settings._read_config_value("email")

    @staticmethod
    def read_github() -> Optional[str]:
        """Lê o usuário do GitHub do arquivo de configuração."""
        return Settings._read_config_value("github")

    @staticmethod
    def save_email(email: str) -> None:
        """Salva o email no arquivo de configuração."""
        Settings._save_config_value("email", email)

    @staticmethod
    def save_github(github: str) -> None:
        """Salva o usuário do GitHub no arquivo de configuração."""
        Settings._save_config_value("github", github)

    @staticmethod
    def _save_config_value(key: str, value: str) -> None:
        """Método interno para salvar um valor no arquivo de configuração."""
        os.makedirs(os.path.dirname(Settings.CONFIG_PATH), exist_ok=True)
        
        # Lê configurações existentes
        config = {}
        if os.path.exists(Settings.CONFIG_PATH):
            try:
                with open(Settings.CONFIG_PATH, "r") as f:
                    for line in f:
                        if "=" in line:
                            k, v = line.strip().split("=", 1)
                            config[k] = v
            except Exception:
                pass

        # Atualiza ou adiciona novo valor
        config[key] = value

        # Salva todas as configurações
        try:
            with open(Settings.CONFIG_PATH, "w") as f:
                for k, v in config.items():
                    f.write(f"{k}={v}\n")
        except Exception as e:
            print(f"Falha ao salvar configuração: {e}")

settings = Settings()
