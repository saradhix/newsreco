import nltk
from nltk.corpus import stopwords
from nltk.stem import *

def preprocess_sentence(sentence):
  #first convert everything to small case
  sentence = sentence.lower()
  #Replace apostrophes
  sentence = sentence.replace("'s","")
  return sentence

stemmer = PorterStemmer()
def get_nouns_and_verbs(sentence):
  sentence = preprocess_sentence(sentence)
  pos_result = nltk.pos_tag(nltk.word_tokenize(sentence))
  nouns = set()
  verbs = set()
  #print pos_result
  for t in pos_result:
    if str(t[0]) in stopwords.words("english"):
      continue
    if str(t[1]).startswith('NN'):
      nouns.add(t[0])
    if str(t[1]).startswith('VB'):
      verbs.add(t[0])
  nouns = [stemmer.stem(noun) for noun in nouns]
  verbs = [stemmer.stem(verb) for verb in verbs]
  return nouns, verbs

def similarity(a, b):
  alist = get_nouns_and_verbs(a)
  blist = get_nouns_and_verbs(b)
  return jaccard_similarity(alist, blist)

def jaccard_similarity(x,y):
  #print "Finding jaccard similarity of "
  #print x
  #print "and"
  #print y
  intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
  union_cardinality = len(set.union(*[set(x), set(y)]))
  #print intersection_cardinality, union_cardinality
  return intersection_cardinality/float(union_cardinality)

def make_bigrams(para):
  text = para.split('.')
  text = [ word.strip() for word in text]
  bigrams = [b for l in text for b in zip(l.split(" ")[:-1], l.split(" ")[1:])]
  return bigrams
def make_trigrams(para):
  text = para.split('.')
  text = [ word.strip() for word in text]
  bigrams = [b for l in text for b in zip(l.split(" ")[:-1], l.split(" ")[1:],
      l.split(" ")[2:])]
  return bigrams
def make_fourgrams(para):
  text = para.split('.')
  text = [ word.strip() for word in text]
  bigrams = [b for l in text for b in zip(l.split(" ")[:-1], l.split(" ")[1:],
      l.split(" ")[2:], l.split(" ")[3:])]
  return bigrams
def make_fivegrams(para):
  text = para.split('.')
  text = [ word.strip() for word in text]
  bigrams = [b for l in text for b in zip(l.split(" ")[:-1], l.split(" ")[1:],
      l.split(" ")[2:], l.split(" ")[3:], l.split(" ")[4:])]
  return bigrams
def make_sixgrams(para):
  text = para.split('.')
  text = [ word.strip() for word in text]
  bigrams = [b for l in text for b in zip(l.split(" ")[:-1], l.split(" ")[1:],
      l.split(" ")[2:], l.split(" ")[3:], l.split(" ")[4:], l.split(" ")[5:])]
  return bigrams
