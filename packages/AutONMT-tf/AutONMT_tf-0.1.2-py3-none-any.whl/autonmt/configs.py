from dataclasses import dataclass
from typing import Dict

class ConfigError(RuntimeError):
    """Exception class for pipeline configuration errors"""

class ModelConfig:
    def __init__(self, model_file, model_type, config) -> None:
        if model_file is not None and model_type is not None:
            raise ConfigError("The model configuration must either have 'file' or 'type' argument, found both")
        elif model_file is None and model_type is None:
            raise ConfigError("The model configuration must either have 'file' or 'type' argument, found none")
        elif model_file is not None:
            self.file = model_file
            self.type = None
        else: # model_type is not None
            self.type = model_type
            self.file = None
        self.config = config

    def to_model_spec(self):
        if self.file is not None:
            return ['--model', self.file]
        else: # model_type is not None
            return ['--model_type', self.type]

    @staticmethod
    def from_raw(raw_config):
        return ModelConfig(raw_config.get('file'), raw_config.get('type'), raw_config['config'])

class ScriptsConfig:
    def __init__(self, dir) -> None:
        self.dir = dir

    @staticmethod
    def from_raw(raw_config):
        if raw_config is None:
            return None
        return ScriptsConfig(raw_config['dir'])

class CacheConfig:
    def __init__(self, dir) -> None:
        self.dir = dir

    @staticmethod
    def from_raw(raw_config):
        if raw_config is None:
            return None
        return CacheConfig(raw_config['dir'])

class GlobalConfig:
    def __init__(self, exp, dirs, model: ModelConfig, scripts, cache) -> None:
        self.exp = exp
        self.dirs = dirs
        self.model = model
        self.scripts = scripts
        self.cache = cache

    @staticmethod
    def from_raw(raw_config):
        return GlobalConfig(raw_config['exp'], raw_config.get('dirs'), ModelConfig.from_raw(raw_config['model']), ScriptsConfig.from_raw(raw_config.get('scripts')), CacheConfig.from_raw(raw_config.get('cache')))
        
@dataclass
class ArtifactsConfig:
    dir: str
    items: Dict[str, Dict]

    @staticmethod
    def from_raw(raw_config):
        if raw_config is None:
            return None
        return ArtifactsConfig(raw_config['dir'], raw_config['items'])

class StageConfig:
    def __init__(self, name, type_, specific, corpora, input_tags, output_tags, artifacts_config: ArtifactsConfig) -> None:
        self.name = name
        self.type = type_
        self.specific = specific
        self.corpora = corpora
        self.input_tags = input_tags
        self.output_tags = output_tags
        self.artifacts_config = artifacts_config

    def expand(self, modules):
        if self.specific is not None:
            if isinstance(self.specific, str):
                self.specific = modules[f'{self.type}_{self.specific}']

    @staticmethod
    def from_raw(raw_config, name):
        return StageConfig(
            name,
            raw_config['type'],
            raw_config.get('config'),
            raw_config.get('corpora'),
            raw_config.get('input_tags'),
            raw_config.get('output_tags'),
            ArtifactsConfig.from_raw(raw_config.get('artifacts'))
        )


# class LoadAndPreprocessConfig:
#     def __init__(self, raw) -> None:
#         expname = raw['name']
#         self.outputdatadir = raw['data']['output_dir'].rstrip('/')
#         self.outputdatadir = f'{self.outputdatadir}/{expname}'
#         self.preprocdir = f'/tmp/{expname}'
#         self.src_lgs = raw['data']['src_lgs']
#         self.tgt_lgs = raw['data']['tgt_lgs']
#         self.corpora = raw['data']['corpora']
#         self.datadir = raw['data']['dir'].rstrip('/')
#         self.on_missing_data = raw['data'].get('on_missing_data', [])
#         self.max_entries_per_corpus = int(raw['data']['max_entries_per_corpus'])
#         self.preprocessing_steps = raw['preprocessing']['steps']

#         class StepConfig:
#             def __init__(this, step_raw) -> None:
#                 this.corpora = step_raw['corpora']
#                 this.script = step_raw['script']
#         self.step_config = { step: StepConfig(raw[f'preprocessing_{step}']) for step in raw['preprocessing']['steps'] }
#         self.scriptsdir = raw['preprocessing']['scripts_dir']
#         self.final_files = raw['preprocessing']['final_files']

# class TokenizeConfig:
#     def __init__(self, raw) -> None:
#         self.final_files = raw['preprocessing']['final_files']
#         expname = raw['name']
#         self.outputdatadir = raw['data']['output_dir'].rstrip('/')
#         self.outputdatadir = f'{self.outputdatadir}/{expname}'

# class BuildVocabConfig:
#     def __init__(self, raw) -> None:
#         expname = raw['name']
#         self.outputdatadir = raw['data']['output_dir'].rstrip('/')
#         self.outputdatadir = f'{self.outputdatadir}/{expname}'
#         class VocabConfig:
#             def __init__(this, vocab_raw) -> None:
#                 this.output = vocab_raw['save_to']
#                 this.files = vocab_raw['files']
#         self.vocabs = { vocab: VocabConfig(vocab_raw) for vocab, vocab_raw in raw['vocab'].items() }

# class SplitConfig:
#     def __init__(self, raw) -> None:
#         self.files = raw['splitting']['files']
#         self.parts = raw['splitting']['parts']
#         self.remain = raw['splitting']['remain']
#         self.seed = int(raw['splitting']['seed'])
#         expname = raw['name']
#         self.outputdatadir = raw['data']['output_dir'].rstrip('/')
#         self.outputdatadir = f'{self.outputdatadir}/{expname}'

# class TrainConfig:
#     def __init__(self, raw) -> None:
#         expname = raw['name']
#         self.outputdir = raw['train']['output_dir'].rstrip('/')
#         self.outputdir = f'{self.outputdir}/{expname}'
#         model_file = raw['model'].get('file')
#         if model_file is not None:
#             self.model_file = model_file
#             self.custom_model = True
#         else:
#             self.model_type = raw['model']['type']
#             self.custom_model = False
#         self.model_config_file = raw['model']['config']
#         self.options = raw['train']['options']

# class ConfigFactory:
#     configs = {
#         'load': LoadAndPreprocessConfig,
#         'tokenize': TokenizeConfig,
#         'build_vocab': BuildVocabConfig,
#         'split': SplitConfig,
#         'train': TrainConfig
#     }

#     def __init__(self, raw) -> None:
#         self.raw = raw

#     def build_for(self, step):
#         if step not in ConfigFactory.configs.keys():
#             raise NotImplementedError(f'Factory cannot build config for step {step}')
#         try:
#             result = ConfigFactory.configs[step](self.raw)
#         except KeyError as err:
#             logging.warning(f'Missing config element: {err}')
#             return None
#         return result
