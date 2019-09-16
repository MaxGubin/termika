#!/usr/bin/env python3
import json
import xml.sax as sax
from collections import Counter
from typing import Dict, List, Tuple, Text
import re
import nltk
# nltk initialization.
nltk.download('punkt')

ONLY_LETTER_WORDS = re.compile('\w+')

def extract_html_fragment_text(fragment:Text) -> Text:
  """."""
  class XMLTextExtractor(sax.handler.ContentHandler):
    def __init__(self):
      self.buffer = ''
    def characters(self, chars):
      self.buffer += chars
  handler = XMLTextExtractor()
  sax.parseString(fragment, handler=handler)
  return handler.buffer

def calculate_word_counts(text : Text)->Counter:
  words = nltk.word_tokenize(text)
  return Counter((w.lower() for w in words if ONLY_LETTER_WORDS.match(w)))

def parse_file(flpath: Text):
  """."""
  with open(flpath) as f:
    parsed = json.load(f)
    for q in parsed['Questions']:
      print(
          calculate_word_counts(extract_html_fragment_text('<div>'+q['Help']+'</div>')))
      break


if __name__ == '__main__':
  parse_file('../data/1001/instruction.json')

