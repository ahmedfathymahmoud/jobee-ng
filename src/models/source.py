from abc import ABC, abstractmethod

class Source(ABC):
    @abstractmethod
    def fetch_jobs(self):
        pass
