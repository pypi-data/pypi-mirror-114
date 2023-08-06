import os
import shutil
import logging
import sys

from .pipeline_cache import CacheInfo, PipelineCache
from .corpus import Corpora
from .configs import GlobalConfig, StageConfig
from .stages import DataQuery, Script, BuildVocab, Merge, Split, Train
from .util import SubprocessError

stages = {
    'data_query': DataQuery,
    'script': Script,
    'vocab_building': BuildVocab,
    'merging': Merge,
    'splitting': Split,
    'training': Train
}

class InvalidRunRequest(Exception):
    pass

def crop_stage_list(pipeline_name, stage_list, last_stage, until):
    beginning = 0
    if last_stage is not None:
        try:
            beginning = stage_list.index(last_stage) + 1
        except ValueError:
            raise InvalidRunRequest(f"Stage '{last_stage}' does not exist in pipeline '{pipeline_name}'")
    end = len(stage_list) - 1
    if until is not None:
        try:
            end = stage_list.index(until)
        except ValueError:
            raise InvalidRunRequest(f"Stage '{until}' does not exist in pipeline '{pipeline_name}'")
    if end < beginning:
        raise InvalidRunRequest(f"Stage '{until}' precedes stage '{stage_list[beginning]}' in pipeline '{pipeline_name}'")
    return stage_list[beginning:end+1]

def run_pipeline(pipeline_name, config, until = None, use_cache = False):
    workdir = f'/tmp/autonmt/{pipeline_name}'
    shutil.rmtree(workdir, ignore_errors=True)
    os.makedirs(workdir)
    global_config = GlobalConfig.from_raw(config)
    modules = config['modules']
    pipeline_config = config['pipelines'][pipeline_name]
    if use_cache:
        pipeline_cache = PipelineCache(workdir, global_config.cache.dir, global_config.exp, pipeline_name)
        cache_info = pipeline_cache.load()
        last_stage = cache_info.last_stage
        corpora = cache_info.corpora
    else:
        last_stage = None
        corpora = Corpora(workdir)
    to_run = crop_stage_list(pipeline_name, pipeline_config['stages'], last_stage, until)
    logging.info(f"Running pipeline '{pipeline_name}'. Stages: {to_run}")
    if global_config.cache is not None:
        pipeline_cache = PipelineCache(workdir, global_config.cache.dir, global_config.exp, pipeline_name)
    for i, stage_name in enumerate(to_run):
        logging.info(f"{i+1}) {stage_name}")
        stage_raw_config = pipeline_config[stage_name]
        stage_class = stages[stage_raw_config['type']]
        stage_config = StageConfig.from_raw(stage_raw_config, stage_name)
        stage_config.expand(modules)
        stage = stage_class(corpora, global_config, stage_config)
        try:
            stage.run_and_save()
        except SubprocessError as e:
            logging.error(f"[Stage '{stage_name}'] {e.message}")
            if e.result is not None and e.result.stderr is not None:
                    logging.error(f"[Stage '{stage_name}'] STDERR:\n{e.result.stderr.decode('utf-8')}")

            sys.exit(1)

        pipeline_cache.save(CacheInfo(stage_name, corpora))
