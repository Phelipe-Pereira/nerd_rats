import threading
import time
from src.domain.entities.tracking_data import TrackingData
from src.infrastructure.services.mouse_service import MouseService
from src.infrastructure.services.keyboard_service import KeyboardService
from src.infrastructure.persistence.tracking_repository_impl import TrackingRepositoryImpl
from src.infrastructure.config.settings import settings

class TrackEventsUseCase:
    def __init__(self):
        self.mouse_service = MouseService()
        self.keyboard_service = KeyboardService()
        self.repository = TrackingRepositoryImpl()
        self.running = False
        self.email = None

    def _configure_email(self) -> None:
        self.email = settings.read_email()
        if not self.email:
            self.email = input("Digite seu email para configurar o rastreamento: ").strip()
            settings.save_email(self.email)

    def _send_data_periodically(self) -> None:
        while self.running:
            tracking_data = TrackingData(
                email=self.email,
                keys_pressed=self.keyboard_service.key_press_count,
                mouse_distance_cm=self.mouse_service.distance,
                clicks=self.mouse_service.clicks,
                scrolls=self.mouse_service.scrolls
            )

            self.repository.send_tracking_data(tracking_data)

            # Reset counters
            self.keyboard_service.reset_counter()
            self.mouse_service.reset_counters()

            time.sleep(settings.INTERVAL)

    def start(self) -> None:
        self._configure_email()
        
        self.running = True
        self.mouse_service.start()
        self.keyboard_service.start()

        # Inicia thread para envio periódico dos dados
        threading.Thread(
            target=self._send_data_periodically,
            daemon=True
        ).start()

    def stop(self) -> None:
        self.running = False
        self.mouse_service.stop()
        self.keyboard_service.stop() 