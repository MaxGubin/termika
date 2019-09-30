import pickle


# local modules
from idf_builder import load_idf

from typing import Dict, List, Tuple, Text

def build_vectors(path: Text, idf_path: Text, output_bin: Text):
  """Builds all vectors for all docs."""
  idf_dictionaly = load_idf(idf_path) 

