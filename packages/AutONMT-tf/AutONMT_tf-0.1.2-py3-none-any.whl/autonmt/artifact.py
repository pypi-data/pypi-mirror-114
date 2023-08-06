import os
import shutil
from dataclasses import dataclass
from types import coroutine
from typing import Dict, List

from .corpus import Corpus
from .configs import ConfigError

@dataclass
class Artifact:
    corpus: Corpus
    tag: str
    stage: str
    destination: str

    def get_origin(self):
        return self.corpus.filename_gen.get_filename(self.tag, self.stage)

    def save(self):
        origin = self.get_origin()
        destination_dir, _ = os.path.split(self.destination)
        os.makedirs(destination_dir, exist_ok=True)
        shutil.move(origin, self.destination)

    def load(self):
        origin = self.get_origin()
        shutil.move(self.destination, origin)

def build_simple_artifacts(corpus: Corpus, stage, output_dir, config: Dict) -> List:
    result = []
    for tag_name, output_filename in config.items():
        if not isinstance(output_filename, str):
            return None
        output_filename = os.path.join(output_dir, output_filename)
        result.append(Artifact(corpus, tag_name, stage, output_filename))
    return result

def build_cascading_artifacts(corpus: Corpus, stage, output_dir, config: Dict):
    result = []
    root = config.get('root')
    if root is None:
        return None
    root = str(os.path.join(output_dir, root))
    tags = config.get('tags')
    if tags is None:
        return None
    subtags = config.get('subtags')
    for tag, tag_suffix in tags.items():
        tagged_name = f'{root}.{tag_suffix}'
        if subtags is None:
            result.append(Artifact(corpus, tag, stage, tagged_name))
        else:
            for subtag, subtag_suffix in subtags.items():
                subtagged_name = f'{tagged_name}.{subtag_suffix}'
                complete_tag = f'{tag}.{subtag}'
                result.append(Artifact(corpus, complete_tag, stage, subtagged_name))
    return result

artifact_builders = [build_simple_artifacts, build_cascading_artifacts]
def build_artifacts(corpus: Corpus, stage, output_dir, config):
    for artifact_builder in artifact_builders:
        result = artifact_builder(corpus, stage, output_dir, config)
        if result is not None:
            return result
    raise ConfigError('Invalid artifact configuration: no builder could build the output filename')
