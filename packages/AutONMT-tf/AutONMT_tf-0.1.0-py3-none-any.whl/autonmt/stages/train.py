import os

from .stage import Stage
from ..corpus import Corpora
from ..configs import ConfigError, GlobalConfig, StageConfig
from ..util import run_and_check_result

class Train(Stage):
    """Stage class implementing build_vocab stage"""

    def __init__(self, corpora: Corpora, global_config: GlobalConfig, config: StageConfig) -> None:
        super().__init__(corpora, global_config, config)
        if self.config.corpora is not None:
            raise ConfigError("'corpora' is invalid for 'training' stages")
        if self.config.input_tags is not None:
            raise ConfigError("'input_tags' is invalid for 'training' stages")
        if self.config.output_tags is not None:
            raise ConfigError("'output_tags' is invalid for 'training' stages")

    def run(self):
        """Run the stage"""
        outputdir = self.global_config.dirs[self.config.specific['output_dir']]
        os.makedirs(outputdir, exist_ok=True)
        current_env = os.environ.copy()
        current_env['CUDA_VISIBLE_DEVICES'] = 0
        base_command = ['onmt-main']
        model_spec = self.global_config.model.to_model_spec()
        model_config = ['--config', self.global_config.model.config]
        command_suffix = '--auto_config train'.split(' ')
        options = ['--with_eval'] if 'eval' in self.config.specific.get('options', []) else []
        with open(f'{outputdir}/train.log', 'wb') as log_file:
            run_and_check_result(base_command + model_spec + model_config + command_suffix + options, stdout=log_file, stderr=log_file)
        