from abc import ABC, abstractmethod
from os import PathLike
import os
from typing import List, Union

from ..artifact import build_artifacts
from ..corpus import Corpora
from ..configs import GlobalConfig, StageConfig

class Stage(ABC):
    def __init__(self, corpora: Corpora, global_config: GlobalConfig, config: StageConfig) -> None:
        self.corpora = corpora
        self.global_config = global_config
        self.config = config

    def get_input_filenames(self, corpus: str):
        """Return the input filenames corresponding to the input tags"""
        corpus = self.corpora.content[corpus]
        return [corpus.get_last(input_tag) for input_tag in self.config.input_tags]

    def add_output_filenames(self, corpus: str):
        """Return the input filenames corresponding to the input tags after adding them to the corpus"""
        corpus = self.corpora.content[corpus]
        return [corpus.add(output_tag, self.config.name) for output_tag in self.config.output_tags]

    def save_artifacts(self):
        dest_dir = self.config.artifacts_config.dir
        dest_dir = self.global_config.dirs.get(dest_dir, dest_dir)
        os.makedirs(dest_dir, exist_ok=True)
        artifacts = []
        for corpus_name, corpus_artifacts in self.config.artifacts_config.items.items():
            corpus = self.corpora.content[corpus_name]
            artifacts.extend(build_artifacts(corpus, self.config.name, dest_dir, corpus_artifacts))
        for artifact in artifacts:
            artifact.save()

    def run_and_save(self):
        self.run()
        if self.config.artifacts_config is not None:
            self.save_artifacts()

    @abstractmethod
    def run(self):
        """Run the stage"""
        