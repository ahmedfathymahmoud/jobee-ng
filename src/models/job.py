from abc import ABC, abstractmethod

class Job(ABC):
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return f"Job(id={self.id})"
