from abc import ABC, abstractmethod

class Detector(ABC):
    @abstractmethod
    def predict(self, image):
        pass
