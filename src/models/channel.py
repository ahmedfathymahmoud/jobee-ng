from abc import ABC, abstractmethod

class Channel(ABC):
    @abstractmethod
    def post_job(self, job):
        pass
