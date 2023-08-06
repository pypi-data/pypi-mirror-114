
from abc import abstractmethod

class ISerialization:
    @abstractmethod
    def save(self):
        return

    @abstractmethod
    def load(self, path):
        return

from coh2_stats.query.coh2_io import Coh2IO 
import pickle
class PickleSerialization(ISerialization):
    def __init__(self, folder_name, savefile) -> None:
        super().__init__()
        self.io = Coh2IO(folder_name)
        self.savefile = savefile

    def save(self):
        data = pickle.dumps(self.__dict__)
        self.io.write_binary(data, self.savefile)
        
    def load(self):
        data = self.io.read_binary(self.savefile)
        if data != None:
            tmp_dict = pickle.loads(data)
            self.__dict__.update(tmp_dict)
            return self
        else:
            return None


