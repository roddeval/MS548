# https://data-flair.training/blogs/python-chatbot-project/

# author: Roderick DeValcourt
# project: Assignment: Build A Chatbot
# this handles some nltk/nlp tokenization and returns it as json

import json
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import nltk

class ConvertTextToJson:
    def __init__(self):
      self.patterns = []

    def go(self, text):

      tokenized_words = word_tokenize(text)
      for words in tokenized_words:
          tagged_words = nltk.pos_tag(tokenized_words)

      for w in tagged_words:
          if w[1] == 'JJ':
              self.patterns.append(w[0])
          if w[1] == 'NN':
              self.patterns.append(w[0])
          if w[1] == 'IN':
              self.patterns.append(w[0])
          if w[1] == 'RB':
              self.patterns.append(w[0])
          if w[1] == 'NNP':
              self.patterns.append(w[0])
          if w[1] == 'VBN':
              self.patterns.append(w[0])

      jsonText = json.dumps(self.patterns)
      return jsonText
