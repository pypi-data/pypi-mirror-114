[![pipeline status](https://gitlab.com/mehdidou99/autONMT/badges/main/pipeline.svg)](https://gitlab.com/mehdidou99/autONMT/-/commits/main)

[![coverage report](https://gitlab.com/mehdidou99/autONMT/badges/main/coverage.svg)](https://mehdidou99.gitlab.io/autONMT/main/)

# AutONMT-tf

AutONMT-tf is a configuration tool designed to simplify the creation of complete OpenNMT-tf pipelines (data loading, preprocessing, training, inference...). It can also be used for other tasks not related to OpenNMT-tf, but there are no built-in modules for other NMT frameworks.

It is still at an early development stage, neither stability nor backward-compatibilty are guaranteed.

## Requirements

AutONMT-tf requires :

- Python 3.7 or above
- OpenNMT-tf 2.20 or above

## Installation

### Using pip

It is the recommanded (and simplest) installation method :

```bash
pip install --upgrade pip
pip install AutONMT-tf
```

### From source

You can also install AutONMT-tf directly from source :

```bash
git clone https://gitlab.com/mehdidou99/AutONMT-tf.git
cd AutONMT-tf
pip install --upgrade pip
pip install AutONMT-tf
```

## Usage

### Quickstart

Once installed, you can try to run a simple Transformer model pipeline with some preprocessing :

```bash
git clone https://gitlab.com/mehdidou99/AutONMT-tf.git
cd AutONMT-tf
# Download datasets
autonmt_cli -v --config examples/pipelines/simple_transformer.yml --pipeline train
```

### Pipeline examples

Some examples are available in [examples/pipelines/](examples/pipelines/):

- simple_encoder.yml: A very simple example showcasing base functionalities of AutONMT-tf
- fren_triple_encoder.yml: A more complex example showcasing the future functionalities of AutONMT-tf, which will allow it to have the flexibility needed for more complex models and pipelines.

### Command line

AutONMT-tf is used through the `autonmt_cli` command line interface.

- Simplest usage : `autonmt_cli --config path/to/pipeline/config/file.yml --pipeline name_of_the_pipeline_to_run`
- Key options :
    - `--until step` : stops the execution after step *step*
    - `--use_cache` : resumes execution using cache instead of launching the pipeline from the beginning

### Pipeline elements

Each pipeline configuration file is made of the following elements:

- Global configuration
- Pipelines made of pipeline blocks
- Modules

The [simple_transformer](examples/pipelines/simple_transformer.yml) example illustrates all of those elements.

#### Global configuration

The global configuration defines the elements that are used by all the pipelines defined in the file :

- Experiment name
- Custom directories
- Model configuration
- Scripts directory
- Cache directory

#### Pipelines

Pipelines are the core element of AutONMT-tf. A pipeline is a list of pipeline blocks which each define a specific step of the process : block is applied to a list of **corpora**; it receives input through **input tags** and outputs **output tags**. See [Tags](#tags) to learn more.

AutONMT-tf currently provides the following block types:

- data_query: Loads data : it is usually the first block of a pipeline, and creates the corpora that are later used by the subsequent blocks.
- merging: Used to merge data from several datasets into one new dataset, usually used to merge data for training.
- vocab_building: Builds a vocabulary using the 'onmt-build-vocab' command from OpenNMT-tf.
- splitting: Splits input data into several parts, the intended use is to split train data into train, test and validation sets.
- training: Trains the model using the 'onmt-main' command from OpenNMT-tf.
- script: Executes custom scripts, usually used for experiment-dependent features such as preprocessing, tokenization, score computation...

#### Modules

Modules are currently simply configuration modules allowing blocks to delegate their specific configuration to said module. Their use should be extended in future versions, allowing complete blocks to be defined as modules and allowing external module files in order to allow blocks to be reused in different experiments.

#### Tags

Tags are a core element of AutONMT-tf: they allow pipelines to manipulate data through tags instead of real files, making the pipeline definition much more natural.

The link between abstract tags and underlying real files is handled automatically by AutONMT-tf. For *script* blocks, the paths to the real files are passed to the script as follows :

```bash
script_name input_tag_1_path ... input_tag_N_path output_tag_1_path ... output_tag_M_path
```

Scripts can thus process data without the script writer needing to know the paths to the real data files.

#### Artifacts

Some of the generated files are needed by the user, either to be inspected (e.g training data) or to be used in other pipelines. For example, a tokenizer can be trained with the training data, the output of the training being then needed to tokenize test data. Users can retrieve such files through artifacts, by defining correspondancies between Corpora/Tag pairs and custom filenames to which they want to save their files. See [simple_transformer](examples/pipelines/simpletransformer.yml) for a concrete example.
