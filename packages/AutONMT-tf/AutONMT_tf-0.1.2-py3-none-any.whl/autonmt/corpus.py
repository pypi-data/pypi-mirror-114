import dataclasses
from dataclasses import dataclass
import os
import json
from typing import Dict

class FilenameGenerator:
    def __init__(self, workdir) -> None:
        self.workdir = workdir

    def get_filename(self, tag, stage):
        tag_dir = os.path.join(self.workdir, tag)
        os.makedirs(tag_dir, exist_ok=True)
        return os.path.join(tag_dir, stage)

class Tag:
    def __init__(self, id_, filename_gen : FilenameGenerator) -> None:
        self.id = id_
        self.filename_gen = filename_gen
        self.stages = []
        self.filenames = {}

    def get(self, stage):
        assert stage in self.stages, f"Trying to access tag '{self.id}' which is not an output of stage '{stage}'"
        return self.filenames[stage]

    def get_last(self):
        assert self.stages, f"Tag {self.id} has no output yet"
        return self.get(self.stages[-1])

    def add(self, stage):
        assert stage not in self.stages, f"Trying to add an already existing stage to tag {self.id}"
        self.stages.append(stage)
        filename = self.filename_gen.get_filename(self.id, stage)
        self.filenames[stage] = filename
        return filename

    def to_jsonable(self):
        return {
            'stages': self.stages,
            'filenames': self.filenames
        }

    @staticmethod
    def from_jsonable(id_, filename_gen: FilenameGenerator, data):
        result = Tag(id_, filename_gen)
        result.stages = data['stages']
        result.filenames = data['filenames']
        return result

@dataclass
class Corpus:
    filename_gen: FilenameGenerator
    tags: Dict[str, Tag] = dataclasses.field(default_factory=dict)

    def get_tag(self, id_) -> Tag:
        assert id_ in self.tags.keys(), f"Trying to access tag '{id_}' which does not exist"
        return self.tags[id_]

    def get(self, tag, stage):
        return self.get_tag(tag).get(stage)

    def get_last(self, tag):
        return self.get_tag(tag).get_last()

    def add(self, tag, stage):
        if tag not in self.tags.keys():
            self.tags[tag] = Tag(tag, self.filename_gen)
        return self.get_tag(tag).add(stage)

    def to_jsonable(self):
        return {
            id_: tag.to_jsonable() for id_, tag in self.tags.items()
        }

    @staticmethod
    def from_jsonable(filename_gen: FilenameGenerator, data):
        return Corpus(filename_gen, { id_: Tag.from_jsonable(id_, filename_gen, tag_data) for id_, tag_data in data.items() })

@dataclass
class Corpora:
    workdir: str
    content: Dict[str, Corpus] = dataclasses.field(default_factory=dict)

    def new_corpus(self, name):
        assert name not in self.content, 'Trying to create an already existing corpus'
        subdir = os.path.join(self.workdir, name)
        os.makedirs(subdir, exist_ok=True)
        self.content[name] = Corpus(FilenameGenerator(subdir))

    def new_corpus_if_missing(self, name):
        if name not in self.content:
            self.new_corpus(name)

    def to_jsonable(self):
        return {
            'workdir': self.workdir,
            'content': { name: corpus.to_jsonable() for name, corpus in self.content.items() }
        }

    @staticmethod
    def from_jsonable(data):
        content = {}
        workdir = data['workdir']
        for name in data['content']:
            subdir = os.path.join(workdir, name)
            content[name] = Corpus.from_jsonable(FilenameGenerator(subdir), data['content'][name])
        return Corpora(data['workdir'], content)
