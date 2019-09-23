import parser

import os
from collections import Counter
import pickle 
from typing import Dict, List, Tuple, Text



def build_idf(path:Text, output_bin:Text):
  """Builds a dictionary with counters per word."""

  word_counter = Counter()
  def process_one_doc(fl):
    nonlocal word_counter
    def processing_closure(help_counter: Counter, content_counter:Counter):
      doc_word_set = set(help_counter)
      doc_word_set |= content_counter.keys()
      word_counter.update(doc_word_set)
    parser.parse_file(fl, processing_closure)
  for root, dirs, files in os.walk(path, topdown=True):
    for fname in files:
      if fname.endswith('json'):
        process_one_doc(os.path.join(root, fname))
  with open(output_bin, 'wb') as fout:
    pickle.dump(word_counter, fout)


def load_idf(pckl_path:Text) -> Counter:
  with open(pckl_path, 'rb') as inpf:
    return pickle.load(inpf)

if __name__ == '__main__':
  build_idf('../data//', 'idf_data.pckl') 
