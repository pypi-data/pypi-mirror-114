#!/usr/bin/env python3

import argparse
import logging
import sys

from autonmt import run_pipeline, load_yaml, YamlLoadError

def main():
    parser = argparse.ArgumentParser(description='Run custom OpenNMT-tf pipeline')
    parser.add_argument('--config', type=str, help='filename of the pipeline config file')
    parser.add_argument('--pipeline', type = str, help = 'name of the pipeline to run')
    parser.add_argument('--until', type = str, default= None, help = 'last stage to execute')
    parser.add_argument('--verbose', '-v', action='store_true')
    parser.add_argument('--use_cache', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    try:
        config = load_yaml(args.config)
    except YamlLoadError:
        logging.error(f'Invalid YAML format in {args.config}')
        sys.exit(1)
    run_pipeline(args.pipeline, config, args.until, args.use_cache)

if __name__ == '__main__':
    main()
