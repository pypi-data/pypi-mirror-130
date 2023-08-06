import zipfile
from pathlib import Path
from typing import Mapping


# str -> bytes
class 文件系统:
    def __init__(self, path):
        self.path = Path(path)
        if self.path.is_file():
            raise Exception('你不对劲')
        self.path.mkdir(parents=True, exist_ok=True)
        self.dirs = set()

    def __contains__(self, k):
        return (self.path/k[:2]/(k[2:]+'_')).is_file()

    def __getitem__(self, k):
        with open(self.path/k[:2]/(k[2:]+'_'), 'rb') as f:
            return f.read()

    def __setitem__(self, k, v):
        if k[:2] not in self.dirs:
            (self.path/k[:2]).mkdir(exist_ok=True)
            self.dirs.add(k[:2])
        with open(self.path/k[:2]/(k[2:]+'_'), 'wb') as f:
            f.write(v)

# str -> bytes
class zip文件:
    def __init__(self, path):
        self.z = _zz(path, mode='a')

    def __contains__(self, x):
        try:
            self.z.getinfo(x)
            return True
        except KeyError:
            return False

    def __getitem__(self, k):
        return self.z.read(k)

    def __setitem__(self, k, v):
        self.z.writestr(k, v)


class _zz(zipfile.ZipFile):
    def __del__(self):
        s = signal.signal(signal.SIGINT, lambda *li:print('不行，那里不行！'))
        print('zip关闭中，请不要ctrl-c。')
        super().__del__()
        print('关好啦。')
