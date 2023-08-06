import os
import random
import sys
from typing import List, Tuple
from dataclasses import dataclass

from .stage import Stage

class DataSplitError(Exception):
    pass

@dataclass
class Data:
    name: str
    lines: List[str]

    @staticmethod
    def from_name(name):
        with open(name) as input_file:
            return Data(name, [line for line in input_file])

def build_splitted_dataset(data: List[Data], set_name_modifier, indices: List[int]):
    for entry in data:
        with open(set_name_modifier(entry.name), 'w') as f:
            for i in indices:
                f.write(entry.lines[i])

def split_data(seed: int, sets: List[Tuple], data: List[Data], remain):
    if not data:
        raise DataSplitError('Empty data')
    content_length = len(data[0].lines)
    if not all(len(entry.lines) == content_length for entry in data):
        raise DataSplitError('Inconsistent file number in input files')

    indices = list(range(content_length))
    if seed != 0:
        random.seed(seed)
        random.shuffle(indices)

    from_idx = 0
    for set_name, set_size in sets:
        to_idx = from_idx + set_size
        if to_idx > content_length:
            raise DataSplitError(f'Not enough data entries to fill all sets : got {content_length}, needed {sum(set_size for _, set_size in sets)}')
        build_splitted_dataset(data,set_name,indices[from_idx:to_idx])
        from_idx = to_idx

    if from_idx < len(indices):
        build_splitted_dataset(data,remain,indices[from_idx:])

def get_name_modificator(subtag, stage):
    def subtag_name_modificator(name):
        head, _ = os.path.split(name)
        head = str(head).rstrip('/')
        new_head = f'{head}.{subtag}'
        return str(os.path.join(new_head, stage))
    return subtag_name_modificator

class Split(Stage):
    """Stage class implementing script stage"""

    # def build_output_tags(self):
    #     """Build output tags from subtags and input tags """
    #     return [f'{input_tag}/{subtag}'
    #                 for subtag in ()
    #                 for input_tag in self.config.input_tags]

    def run(self):
        """Run the stage"""
        subtags = [subtag for subtag in self.config.specific['parts']]
        subtags.append(self.config.specific['remain'])
        self.config.output_tags = [f'{input_tag}.{subtag}'
                                for subtag in subtags
                                for input_tag in self.config.input_tags
                            ]
        for corpus_name in self.config.corpora:
            input_filenames = self.get_input_filenames(corpus_name)
            self.add_output_filenames(corpus_name)
            seed = self.config.specific.get('seed', 0)
            seed = int(seed)
            sets = [(get_name_modificator(set_name, self.config.name), int(set_size)) for set_name, set_size in self.config.specific['parts'].items()]
            data = [Data.from_name(input_filename) for input_filename in input_filenames]
            remain = get_name_modificator(self.config.specific['remain'], self.config.name)
            split_data(seed, sets, data, remain)

