from collections import defaultdict
import numpy as np
import pandas as pd
import conllu


class POSCorpus(object):
  """Corpus for analyzing POS flexibility. After creation, corpus.sentences should consist of
  a list of sentences, each with a list of words. Example structure:
  [
    [
      {'char': "I", 'pos': "PRON"},
      {'char': "love", 'pos': "VERB"},
      {'char': "cats", 'pos': "NOUN"},
    ]
  ]
  """
  def __init__(self):
    pass

  @classmethod
  def create_from_ud(cls, data_file_list):
    """Initialize corpus from a path to a file in conllu format"""
    corpus = POSCorpus()
    corpus.sentences = []

    for data_file_path in data_file_list:
      with open(data_file_path, "r", encoding="utf-8") as data_file:
        data = data_file.read()
        data = conllu.parse(data)

      for token_list in data:
        sentence = []
        for token in token_list:
          pos = token['upostag']
          word = token['form']
          for char in word:
            sentence.append({'char': char, 'pos': pos})
        if len(sentence) > 0:
          corpus.sentences.append(sentence)

    return corpus
  

  def get_nv_stats(self):
    pos_counts = defaultdict(list)
    for sentence in self.sentences:
      for token in sentence:
        char = token['char']
        pos = token['pos']
        pos_counts[char].append(pos)

    count_df = []
    for char, pos_tags in pos_counts.items():
      noun_count = len([pos for pos in pos_tags if pos == 'NOUN'])
      verb_count = len([pos for pos in pos_tags if pos == 'VERB'])
      count_df.append({'char': char, 'noun_count': noun_count, 'verb_count': verb_count})
    count_df = pd.DataFrame(count_df)

    count_df['total_count'] = count_df[['noun_count', 'verb_count']].sum(axis=1)
    count_df = count_df[count_df.total_count > 0]
    count_df['noun_ratio'] = count_df.noun_count / count_df.total_count
    return count_df
