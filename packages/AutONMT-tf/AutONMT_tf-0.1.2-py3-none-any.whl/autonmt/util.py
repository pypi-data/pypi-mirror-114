import subprocess

import yaml

class YamlLoadError(Exception):
    """Exception class for errors happening during the loading of a yaml file"""
    def __init__(self, message, filename, underlying = None):
        self.message = message
        self.filename = filename
        self.underlying = underlying
        super().__init__(message)

def load_yaml(filename):
    try:
        with open(filename, 'r') as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as e:
        raise YamlLoadError(f'Invalid YAML file {filename}', filename, e)
    except FileNotFoundError as e:
        raise YamlLoadError(f'File {filename} not found', filename, e)
            
class SubprocessError(Exception):
    def __init__(self, message, result = None):
        self.message = message
        self.result = result
        super().__init__(message)

class SubprocessRunner:
    def run_and_check_result(self, *args, **kwargs):
        try:
            result = subprocess.run(*args, **kwargs)
        except TypeError:
            raise SubprocessError(f'Invalid type for command {args[0]}', )
        if result.returncode != 0:
            raise SubprocessError(f'Subprocess returned {result.returncode}', result)
        return result

class SubprocessRunnerDependencyInjector:
    underlying = SubprocessRunner()
    @classmethod
    def run_and_check_result(cls, *args, **kwargs):
        return cls.underlying.run_and_check_result(*args, **kwargs)

    @classmethod
    def override(cls, underlying):
        cls.underlying = underlying

def run_and_check_result(*args, **kwargs):
    return SubprocessRunnerDependencyInjector.run_and_check_result(*args, **kwargs)
    