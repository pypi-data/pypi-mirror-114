import os
import subprocess

from .stage import Stage
from ..corpus import Corpora
from ..configs import ConfigError, GlobalConfig, StageConfig
from ..util import run_and_check_result

class Script(Stage):
    """Stage class implementing script stage"""

    def __init__(self, corpora: Corpora, global_config: GlobalConfig, config: StageConfig) -> None:
        super().__init__(corpora, global_config, config)
        subpath = config.specific['subpath']
        self.script = os.path.join(global_config.scripts.dir, subpath) if global_config.scripts else subpath
        if self.config.input_tags is None:
            raise ConfigError("'input_tags' cannot be omitted for 'script' stages")
        if self.config.output_tags is None:
            raise ConfigError("'output_tags' cannot be omitted for 'script' stages")

    def run(self):
        """Run the stage"""
        for corpus_name in self.config.corpora:
            input_filenames = self.get_input_filenames(corpus_name)
            output_filenames = self.add_output_filenames(corpus_name)
            command = [self.script] + input_filenames + output_filenames
            run_and_check_result(command, stderr = subprocess.PIPE)
