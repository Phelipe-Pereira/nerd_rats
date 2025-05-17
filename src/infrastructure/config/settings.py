import os
from typing import Optional

class Settings:
    POST_URL: str = os.getenv('TRACKING_POST_URL', 'http://localhost:5000/track')
    INTERVAL: int = int(os.getenv('TRACKING_INTERVAL', '15'))  # segundos
    CONFIG_PATH: str = os.getenv('CONFIG_PATH', '/etc/nerd_rats.conf')

    @staticmethod
    def read_email() -> Optional[str]:
        if os.path.exists(Settings.CONFIG_PATH):
            try:
                with open(Settings.CONFIG_PATH, 'r') as f:
                    for line in f:
                        if line.startswith('email='):
                            return line.strip().split('=', 1)[1]
            except Exception as e:
                print(f"Falha ao ler configuração: {e}")
        return None

    @staticmethod
    def save_email(email: str) -> None:
        try:
            os.makedirs(os.path.dirname(Settings.CONFIG_PATH), exist_ok=True)
            with open(Settings.CONFIG_PATH, 'w') as f:
                f.write(f"email={email}\n")
        except Exception as e:
            print(f"Falha ao salvar configuração: {e}")

settings = Settings() 