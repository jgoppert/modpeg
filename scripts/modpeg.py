#!/usr/bin/env python

import argparse
import dev_path
from modpeg import modelica_parser

description = """
PEG based modelica compiler
"""
arg_parser = argparse.ArgumentParser(description)
arg_parser.add_argument('src')

args = arg_parser.parse_args()

with open(args.src) as src_file:
    print modelica_parser.parse(file.read(src_file))
