import mylib

text = 'this is a  very big line line. This is next line in this paragraph to make 4 grams'
se = mylib.make_bigrams(text)
print se
se = mylib.make_trigrams(text)
print se
se = mylib.make_fourgrams(text)
print se
