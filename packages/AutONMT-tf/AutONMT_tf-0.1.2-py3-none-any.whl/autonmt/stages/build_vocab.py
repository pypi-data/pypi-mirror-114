import os

from .stage import Stage
from ..corpus import Corpora
from ..configs import ConfigError, GlobalConfig, StageConfig
from ..util import run_and_check_result

class BuildVocab(Stage):
    """Stage class implementing build_vocab stage"""

    def __init__(self, corpora: Corpora, global_config: GlobalConfig, config: StageConfig) -> None:
        super().__init__(corpora, global_config, config)
        if self.config.input_tags is None:
            raise ConfigError("'input_tags' cannot be omitted for 'build_vocab' stages")
        if self.config.output_tags is None:
            raise ConfigError("'output_tags' cannot be omitted for 'build_vocab' stages")
        if len(self.config.output_tags) > 1:
            print(self.config.output_tags)
            raise ConfigError("The 'build_vocab' stage cannot have more than one element in 'output_tags'")

    def run(self):
        """Run the stage"""
        base_command = ['onmt-build-vocab']
        size_config = ['--size', str(self.config.specific['size'])]
        for corpus_name in self.config.corpora:
            (output_filename,) = self.add_output_filenames(corpus_name)
            output_config = ['--save_vocab', output_filename]
            input_filenames = self.get_input_filenames(corpus_name)
            command = base_command + output_config + size_config + input_filenames
            run_and_check_result(command)