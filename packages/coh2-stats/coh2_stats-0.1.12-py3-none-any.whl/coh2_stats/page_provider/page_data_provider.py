from coh2_stats.query.coh2_io import Coh2IO
from abc import abstractmethod
from coh2_stats.utils.logger import Logger
import pickle

class Serialization:
    def __init__(self, cache_folder_str = "temp") -> None:
        self.io = Coh2IO(cache_folder_str)

class PageDataProvider:
    def __init__(self, cache_folder_str = "temp") -> None:
        self.io = Coh2IO(cache_folder_str)
        self.pages = []

    def get_pages(self):
        return self.pages

    def save(self):
        data = pickle.dumps(self)
        self.io.write_binary(data, self.get_savefile_string())
        Logger(f"{self} has been saved")

    def load_locally(self):
        try:
            data = self.io.read_binary(self.get_savefile_string())
            obj = pickle.loads(data)
            self.pages = obj.pages
            Logger(f"successfully loaded {self}")
        except:
            Logger(f"unsuccessfully loaded {self}, trying internet...")
            self.load_from_internet()

    def load_from_internet(self):
        self.download()
        self.save()

    def load(self, use_internet = True):
        if use_internet:
            self.load_from_internet()
        else:
            self.load_locally()

    def download(self):
        self.pages = self._download_from_internet()
        Logger(f"successfully downloaded {self}")

    @abstractmethod
    def _download_from_internet(self):
        return

    @abstractmethod
    def get_savefile_string(self):
        return