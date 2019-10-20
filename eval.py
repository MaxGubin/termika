
from typing import Dict, List, Tuple, Text, Iterator
from __future__ import division

def calculate_recall(test_paragraph_question:List[Tuple[Text, Text]],
    tfidf_system, ,max_at:int):
  position_counters = [0]*max_at
  total_count = 0
  for paragraph, question in test_paragraph_question:
    # Get results from the system:
    results = tfidf_system(paragraph, max_at)
    total_count += 1
    if not results:
      continue
    # Just in case, re-sort in decreasing order of scores.
    results.sort(key=lambda x: x[1], reverse=True)
    # Find the position of correct result.
    for index, find_question, score in enumerate(results):
      if question == find_question:
        # increase all recalls starting from this position:
        for i in range(index, max_at):
          position_counters[i] += 1
        break
    return [] if not total_count else [pc/total_count for pc in
        position_counters]



