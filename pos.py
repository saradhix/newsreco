import nltk


def get_nouns_and_verbs(sentence):
  pos_result = nltk.pos_tag(nltk.word_tokenize(sentence))
  result = []
  print pos_result
  for t in pos_result:
    if str(t[1]).startswith('NN'):
      result.append(t[0])
    if str(t[1]).startswith('VB'):
      result.append(t[0])
  return result

sentence = "Narendra Modi completes 2 years in the Government"
#sentence = "This is an important letter to be sent to Modi"
result = get_nouns_and_verbs(sentence)
print result
