from src.infrastructure.persistence.tracking_repository_impl import (
    TrackingRepositoryImpl,
)

from src.infrastructure.persistence.local_cache import LocalCache


class TrackingResender:

    def __init__(self) -> None:
        self.repository = TrackingRepositoryImpl()
        self.cache = LocalCache()

    def retry_pending_data(self) -> None:
        pending_data = self.cache.get_pending_data()
        
        for filepath, data in pending_data:
            if self.repository.send_tracking_data(data):
                self.cache.delete_file(filepath)
