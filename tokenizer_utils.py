import re
import nltk
from collections import Counter
from typing import Dict, List, Tuple, Text, Iterator

ONLY_LETTER_WORDS = re.compile('\w+')

def tokenized_text(text: Text):
  """Returns an iterator over all words in "text" """
  words = nltk.word_tokenize(text)
  return (w.lower().strip() for w in words if ONLY_LETTER_WORDS.match(w))


def calculate_word_counts(text : Text)->Counter:
  """Returns a counter for all words in text."""
  return Counter(tokenized_text(text))

