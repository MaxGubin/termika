import parser
import tokenizer_utils

import os
from collections import Counter
import pickle 
from typing import Dict, List, Tuple, Text
import nltk
import math

# nltk initialization.
nltk.download('punkt')

class IdfStatisticsBuilder(object):
  def __init__(self):
    self.total_count = 0
    self.counter = Counter()

  def update(self, word_iterable):
    self.total_count += 1
    self.counter.update(word_iterable)

  def finalize_idf(self):
    if self.counter == 0:
      return {}
    return {k:-math.log(float(v)/self.total_count) for k, v in self.counter.items()}


def build_idf(path:Text, output_bin:Text):
  """Builds a dictionary with counters per word."""
  idf_builder = IdfStatisticsBuilder()
  for help_text, content_text in parser.parse_directory(path):
    doc_word_set = set(tokenizer_utils.tokenized_text(help_text))
    doc_word_set |= set(tokenizer_utils.tokenized_text(content_text))
    idf_builder.update(doc_word_set)
  idf_statistics = idf_builder.finalize_idf() 
  print(idf_statistics)
  with open(output_bin, 'wb') as fout:
    pickle.dump(idf_statistics, fout)


def load_idf(pckl_path:Text) -> Counter:
  with open(pckl_path, 'rb') as inpf:
    return pickle.load(inpf)

if __name__ == '__main__':
  build_idf('../data//', 'idf_data.pckl') 
