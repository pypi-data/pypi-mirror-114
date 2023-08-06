from pathlib import Path
import os
import coh2_stats.cache.__cache_root_path as cache_root_path

class Coh2IO:
    cache_root_path = os.path.dirname(cache_root_path.__file__)

    @staticmethod
    def set_root_path(path):
        Coh2IO.cache_root_path = path
        Path(path).mkdir(parents=True, exist_ok=True)

    def __init__(self, parent_path, postfix = "pickle", cache_root_path = "") -> None:
        if not cache_root_path:
            cache_root_path = Coh2IO.cache_root_path

        self.parent_path = os.path.join(cache_root_path, parent_path)
        self.postfix = postfix
        self.make_dir()

    def make_dir(self):
        Path(self.parent_path).mkdir(parents=True, exist_ok=True)

    def read_str(self, filename):
        file_path = os.path.join(self.parent_path, f'{filename}.{self.postfix}')
        with open(file_path, 'r') as f:
            data = f.read()
        return data

    def read_binary(self, filename):
        file_path = os.path.join(self.parent_path, f'{filename}.{self.postfix}')
        if not os.path.exists(file_path):
            return None

        with open(file_path, 'rb') as f:
            data = f.read()
        return data

    def write_binary(self, data, filename):
        file_path = os.path.join(self.parent_path, f'{filename}.{self.postfix}')
        print(file_path)
        with open(file_path, 'wb') as f:
            f.write(data)

    def write_str(self, data, filename):
        file_path = os.path.join(self.parent_path, f'{filename}.{self.postfix}')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(data)