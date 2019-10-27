
from __future__ import division

import parser
import tfidf
from typing import Dict, List, Tuple, Text, Iterator, Any

def calculate_recall(test_paragraph_question:List[Tuple[Text, Text]],
    tfidf_system:Any, max_at:int):
  position_counters = [0]*max_at
  total_count = 0
  for paragraph, question in test_paragraph_question:
    # Get results from the system:
    results = tfidf_system(paragraph, max_at)
    total_count += 1
    if not results:
      continue
    # Just in case, re-sort in decreasing order of scores.
    results.sort(key=lambda x: x[0], reverse=True)
    # Find the position of correct result.
    for index, find_question_score in enumerate(results):
      if question == find_question_score[1]:
        # increase all recalls starting from this position:
        for i in range(index, max_at):
          position_counters[i] += 1
        break
    return [] if not total_count else [pc/total_count for pc in
        position_counters]

def eval_on_files(test_document_path: Text,train_document_path:Text,
    idf_path:Text, max_recall_at:int):
  eval_data = [(help_text, context_text) for  help_text, context_text in
      parser.parse_directory(test_document_path)]
  def tf_idf_system(s_help_text:Text, max_count: int):
    return tfidf.find_similar(s_help_text, train_document_path, idf_path,
        max_count)
  for (at_k, recall) in enumerate(calculate_recall(eval_data, tf_idf_system,
      max_recall_at)):
    print("@", at_k, " recall ", recall)

if __name__ == '__main__':
  eval_on_files('../test_data/', '../data/', 'idf_data.pckl', 5)
