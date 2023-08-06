import os
from dataclasses import dataclass
import shutil
import json

from .corpus import Corpora

@dataclass
class CacheInfo:
    last_stage: str
    corpora: Corpora

    def to_jsonable(self):
        return {
            'last_stage': self.last_stage,
            'corpora': self.corpora.to_jsonable()
        }

    @staticmethod
    def from_jsonable(data):
        return CacheInfo(data['last_stage'], Corpora.from_jsonable(data['corpora']))

class CacheInfoFile:
    def __init__(self, cachedir) -> None:
        self.filename = os.path.join(cachedir, 'cache_info')
    
    def save(self, info: CacheInfo) -> None:
        with open(self.filename, 'w') as cacheinfo_file:
            json.dump(info.to_jsonable(), cacheinfo_file)

    def load(self) -> CacheInfo:
        with open(self.filename, 'r') as cacheinfo_file:
            return CacheInfo.from_jsonable(json.load(cacheinfo_file))

class PipelineCache:
    def __init__(self, workdir, cachedir, exp: str, pipeline: str) -> None:
        self.workdir = workdir
        self.cachedir = os.path.join(cachedir, exp, pipeline)
        self.cachecontentdir = os.path.join(self.cachedir, 'cache_content')
        self.cacheinfo_file = CacheInfoFile(self.cachedir)
        # self.exp = exp
        # self.pipeline = pipeline

    def save(self, cacheinfo: CacheInfo):
        os.makedirs(self.cachedir, exist_ok=True)
        self.cacheinfo_file.save(cacheinfo)
        shutil.rmtree(self.cachecontentdir, ignore_errors=True)
        shutil.copytree(self.workdir, self.cachecontentdir)


    def load(self):
        cacheinfo = self.cacheinfo_file.load()
        shutil.rmtree(self.workdir, ignore_errors=True)
        shutil.copytree(self.cachecontentdir, self.workdir)
        return cacheinfo

