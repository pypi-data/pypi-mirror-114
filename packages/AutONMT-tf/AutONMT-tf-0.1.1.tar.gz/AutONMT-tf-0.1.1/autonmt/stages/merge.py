from contextlib import ExitStack

from ..configs import ConfigError
from .stage import Stage

class Merge(Stage):
    """Stage class implementing merge stage"""

    def run(self):
        """Run the stage"""
        output_corpus_name = self.config.specific['output_corpus_name']
        if not output_corpus_name in self.corpora.content:
            self.corpora.new_corpus_if_missing(output_corpus_name)
        output_paths = self.add_output_filenames(output_corpus_name)
        with ExitStack() as stack:
            output_files = [stack.enter_context(open(fname, 'w')) for fname in output_paths]
            for corpus_name in self.config.corpora:
                input_filenames = self.get_input_filenames(corpus_name)
                print(f'Input filenames: {input_filenames}')
                if len(input_filenames) != len(output_paths):
                    raise ConfigError(f'Merge stage must have same number of input_tags than output_tags ({len(input_filenames)} != {len(output_paths)})')
                input_files = [stack.enter_context(open(fname, 'r')) for fname in input_filenames]
                for input_file, output_file in zip(input_files, output_files):
                    for line in input_file:
                        output_file.write(line)
