import json
import signal
import pickle
import hashlib

from typing import Dict

from .sto import 文件系统, zip文件


存储 = {
    'folder': 文件系统,
    'zip': zip文件,
}


协议 = {
    'pickle': [
        pickle.dumps,
        pickle.loads,
        'pkl',
    ],
    'json': [
        lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf8'),
        json.loads,
        'json',
    ],
}


class _mapdict:
    def get(self, key, default=None):
        if key not in self:
            return default
        return self[key]


def disk_cache(protocol='pickle', storage='folder', path=None):
    dump, load, ext = 协议[protocol]
    def q(func):
        nonlocal path
        name = func.__name__
        if path is None:
            path = f'./_rimocache_{name}_{protocol}.{storage}'
        map = 存储[storage](path)
        def 获取名字(*li, **d):
            i = [name, li, d]
            return hashlib.md5(dump(i)).hexdigest()
        def 假func(*li, **d):
            i = [name, li, d]
            md5 = hashlib.md5(dump(i)).hexdigest()
            名字 = f'{md5}.{ext}'
            if 名字 in map:
                i, o = load(map[名字])
                return o
            else:
                o = func(*li, **d)
                s = dump([i, o])
                map[名字] = s
                return o
        假func.获取名字 = 获取名字
        return 假func
    return q
