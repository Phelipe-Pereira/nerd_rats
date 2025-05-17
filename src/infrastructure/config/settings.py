import os
from typing import Optional
from pathlib import Path


class Settings:
    POST_URL: str = os.getenv("TRACKING_POST_URL", "http://localhost:5000/track")
    INTERVAL: int = int(os.getenv("TRACKING_INTERVAL", "15"))  # segundos
    
    # Usando AppData no Windows ou /etc no Linux
    CONFIG_PATH: str = os.getenv(
        "CONFIG_PATH",
        str(Path.home() / "AppData" / "Local" / "nerd_rats" / "config.ini") if os.name == "nt"
        else "/etc/nerd_rats.conf"
    )

    @staticmethod
    def read_email() -> Optional[str]:
        if os.path.exists(Settings.CONFIG_PATH):
            try:
                with open(Settings.CONFIG_PATH, "r") as f:
                    for line in f:
                        if line.startswith("email="):
                            return line.strip().split("=", 1)[1]
            except Exception as e:
                print(f"Falha ao ler configuração: {e}")
        return None

    @staticmethod
    def save_email(email: str) -> None:
        try:
            os.makedirs(os.path.dirname(Settings.CONFIG_PATH), exist_ok=True)
            # Lê configuração existente
            config = {}
            if os.path.exists(Settings.CONFIG_PATH):
                with open(Settings.CONFIG_PATH, "r") as f:
                    for line in f:
                        if "=" in line:
                            key, value = line.strip().split("=", 1)
                            config[key] = value
            
            # Atualiza email
            config["email"] = email

            # Salva todas as configurações
            with open(Settings.CONFIG_PATH, "w") as f:
                for key, value in config.items():
                    f.write(f"{key}={value}\n")
        except Exception as e:
            print(f"Falha ao salvar configuração: {e}")

    @staticmethod
    def read_github() -> Optional[str]:
        if os.path.exists(Settings.CONFIG_PATH):
            try:
                with open(Settings.CONFIG_PATH, "r") as f:
                    for line in f:
                        if line.startswith("github="):
                            return line.strip().split("=", 1)[1]
            except Exception as e:
                print(f"Falha ao ler configuração: {e}")
        return None

    @staticmethod
    def save_github(github: str) -> None:
        try:
            os.makedirs(os.path.dirname(Settings.CONFIG_PATH), exist_ok=True)
            # Lê configuração existente
            config = {}
            if os.path.exists(Settings.CONFIG_PATH):
                with open(Settings.CONFIG_PATH, "r") as f:
                    for line in f:
                        if "=" in line:
                            key, value = line.strip().split("=", 1)
                            config[key] = value
            
            # Atualiza github
            config["github"] = github

            # Salva todas as configurações
            with open(Settings.CONFIG_PATH, "w") as f:
                for key, value in config.items():
                    f.write(f"{key}={value}\n")
        except Exception as e:
            print(f"Falha ao salvar configuração: {e}")


settings = Settings()
