#!/usr/bin/env python3
import json
import xml.sax as sax
from collections import Counter
from typing import Dict, List, Tuple, Text, Iterator
import os


def extract_html_fragment_text(fragment:Text) -> Text:
  """Converts HTML to text."""
  class XMLTextExtractor(sax.handler.ContentHandler):
    def __init__(self):
      self.buffer = ''
    def characters(self, chars):
      self.buffer += chars
  handler = XMLTextExtractor()
  sax.parseString(fragment, handler=handler)
  return handler.buffer


def parse_file(flpath: Text):
  """Iterates over one fle and returns "Help" and "Content" fields for every
  question."""
  with open(flpath) as f:
    parsed = json.load(f)
    for q in parsed['Questions']:
      process_field = lambda field_name: extract_html_fragment_text(
          '<div>'+q[field_name]+'</div>').strip()
      yield process_field('Help'), process_field('Content')


def parse_files(filepaths: Iterator[Text]):
  """Iterate all fields inside all filepaths."""
  for flpath in filepaths:
    for i,v in parse_file(flpath):
      yield i,v


def parse_directory(path: Text):
  """Iterate all fields inside a directory.""" 
  for root, dirs, files in os.walk(path, topdown=True):
    for i,v in parse_files(os.path.join(root, fl) for fl in files if fl.endswith('json')):
       yield i,v


if __name__ == '__main__':
  for i,v in parse_directory('../data/'):
    print (i,'+',v)

