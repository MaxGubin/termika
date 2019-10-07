import math
import idf_builder
import tokenizer_utils
import parser
import nltk
import heapq
from collections import Counter 
from typing import Dict, List, Tuple, Text, Iterator

def calc_tfidf_similarity(doc1: Counter, doc2: Counter, idf:
    Dict[Text, float]):
  """Calculates similarity between doc1 and doc2 represented as word occurance
  counters. """
  tf1_max = max(doc1.values())
  tf2_max = max(doc2.values())
  total_sum  = 0.0
  for word, tf1 in doc1.items():
    tf2 = doc2[word]
    if tf2 == 0 or word not in idf:
      continue
    tf1_norm = (0.5+0.5*float(tf1)/tf1_max)
    tf2_norm = (0.5+0.5*float(tf2)/tf2_max)
    idf_val = idf[word]
    total_sum += tf1_norm * tf2_norm * (idf_val*idf_val)
  return math.sqrt(total_sum)


def find_similar(s_help_text:Text, path:Text, idf_path:Text,
    max_results_count:int):
  """Finds max_results_count of the closest "Help" fields to s_help_text.""" 
  doc_wc = tokenizer_utils.calculate_word_counts(s_help_text)
  idf_statistics = idf_builder.load_idf(idf_path)
  return heapq.nlargest(max_results_count,
      ((calc_tfidf_similarity(doc_wc, tokenizer_utils.calculate_word_counts(help_text),
        idf_statistics), content_text, help_text) for help_text, content_text 
        in parser.parse_directory(path)))
  

if __name__ == '__main__':
  print(find_similar(
      """Курение разрешается в специально отведенных и оборудованных местах, """
      """отмеченных указательным знаком \"Место для курения\"""",
      '../data//', 'idf_data.pckl', 5))
