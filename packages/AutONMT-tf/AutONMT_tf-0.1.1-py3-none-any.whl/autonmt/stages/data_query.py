import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
import shutil
from enum import Enum, auto

from ..corpus import Corpora
from ..configs import ConfigError, GlobalConfig, StageConfig
from .stage import Stage

class DataTransferUnit(ABC):
    """Interface for the transfer of a data file"""
    
    @abstractmethod
    def transfer(self, origin, destination):
        """Function responsible for the actual data transfer"""

class SimpleDataTransferUnit(DataTransferUnit):
    """DataTransferUnit implementation which simply copy files"""
    def transfer(self, origin, destination):
        shutil.copyfile(origin, destination)

class TruncatingDataTransferUnit(DataTransferUnit):
    """DataTransferUnit implementation which truncates files to a maximum length"""
    def __init__(self, max_entries) -> None:
        self.max_entries = max_entries

    def transfer(self, origin, destination):
        with open(origin, 'r') as input_file, open(destination, 'w') as output_file:
            for i, line in enumerate(input_file):
                if i == self.max_entries:
                    return
                output_file.write(line)

class DataTransferMethod(Enum):
    SIMPLE = auto()
    TRUNCATING = auto()

class DataTransferUnitDependencyInjector:
    defaults = {
        DataTransferMethod.SIMPLE: SimpleDataTransferUnit,
        DataTransferMethod.TRUNCATING: TruncatingDataTransferUnit
    }
    transfer_unit_classes = {
        DataTransferMethod.SIMPLE: SimpleDataTransferUnit,
        DataTransferMethod.TRUNCATING: TruncatingDataTransferUnit
    }

    @classmethod
    def get(cls, method: DataTransferMethod, *args, **kwargs):
        return cls.transfer_unit_classes[method](*args, **kwargs)

    @classmethod
    def inject(cls, method: DataTransferMethod, underlying):
        cls.transfer_unit_classes[method] = underlying

    @classmethod
    def back_to_defaults(cls):
        cls.transfer_unit_classes = cls.defaults

@dataclass
class LanguagePair:
    src: str
    tgt: str

    def __str__(self):
        return f'{self.src}-{self.tgt}'

    def reversed(self):
        return LanguagePair(self.tgt, self.src)

class MissingDataError(Exception):
    def __init__(self, message, corpus, pair, missing_filename) -> None:
        self.message = message
        self.corpus = corpus
        self.pair = pair
        self.missing_filename = missing_filename
        super().__init__(message)

def is_valid_file(path):
    return os.path.isfile(path)

class DataQuery(Stage):
    """Stage class implementing data query stage"""
    def __init__(self, corpora: Corpora, global_config: GlobalConfig, config: StageConfig, path_checker = is_valid_file) -> None:
        super().__init__(corpora, global_config, config)
        if self.config.input_tags is not None:
            raise ConfigError("'input_tags' makes no sense for 'data_query' stage")
        self.path_checker = path_checker

    def fetch(self, corpus: str):
        subpath = self.config.specific['subpaths'][corpus]
        path = os.path.join(self.config.specific.get('search_root', ''), subpath)
        filenames = []
        query = self.config.specific['query']
        for src in query['src_lgs']:
            for tgt in query['tgt_lgs']:
                pair = LanguagePair(src, tgt)
                input_src = f'{path}.{pair}.{src}'
                input_tgt = f'{path}.{pair}.{tgt}'
                try_reversed = 'try_reversed_lg_pairs' in query.get('options', [])
                if not self.path_checker(input_src):
                    if try_reversed:
                        input_src = f'{path}.{pair.reversed()}.{src}'
                        if not self.path_checker(input_src):
                            raise MissingDataError(f"No source data available for corpus '{corpus}' and pair '{pair}'", corpus, pair, input_src)
                    else:
                        raise MissingDataError(f"No source data available for corpus '{corpus}' and pair '{pair}'", corpus, pair, input_src)
                if not self.path_checker(input_tgt):
                    if try_reversed:
                        input_tgt = f'{path}.{pair.reversed()}.{tgt}'
                        if not self.path_checker(input_tgt):
                            raise MissingDataError(f"No target data available for corpus '{corpus}' and pair '{pair}'", corpus, pair, input_tgt)
                    else:
                        raise MissingDataError(f"No target data available for corpus '{corpus}' and pair '{pair}'", corpus, pair, input_tgt)
                filenames.extend([input_src, input_tgt])
        return filenames

    def run(self):
        """Run the stage"""
        max_entries = self.config.specific['query'].get('max_entries')
        if max_entries is not None:
            transfer_unit = DataTransferUnitDependencyInjector.get(DataTransferMethod.TRUNCATING, int(max_entries))
        else:
            transfer_unit = DataTransferUnitDependencyInjector.get(DataTransferMethod.SIMPLE)

        for corpus_name in self.config.corpora:
            self.corpora.new_corpus_if_missing(corpus_name)
            input_filenames = self.fetch(corpus_name)
            output_paths = self.add_output_filenames(corpus_name)
            for input_filename, output_path in zip(input_filenames, output_paths):
                transfer_unit.transfer(input_filename, output_path)
