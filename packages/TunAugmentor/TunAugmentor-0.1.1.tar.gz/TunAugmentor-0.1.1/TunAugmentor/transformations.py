from abc import ABC,abstractmethod
from typing import List
import numpy
class BasicTransform(ABC):
    def check_images(self,images):
        for im in images:
            if not(isinstance(im,numpy.ndarray)):
                raise TypeError
    @abstractmethod
    def transform(self,images):
        pass

class DummyTransformation(BasicTransform):
    def transform(self,images: List[numpy.ndarray]):
        self.check_images(images)
        return images