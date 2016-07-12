import mylib
from nltk.stem import *

sentence = "UAE head coach Mahdi Ali has shortlisted 23 players to carry the country's hope in the crucial tie. The delegation of the UAE senior football national team heads for Qatar en route to Saudi Arabia ahead of their 2018 FIFA World Cup Qualifier scheduled for October 10 to be held in Jeddah. The Whites will gather at the Al Bustan Rotan Hotel in Dubai at 6pm on Wednesday and fly to Doha on Thursday to launch a 12-day training camp before they leave to Jeddah on October 6. UAE head coach Mahdi Ali has shortlisted 23 players to carry the country's hope in the crucial tie. Al Ahli players will reunite with the squad on October 1, due to their ACL commitment with the club. Al Ahli play Al Hilal in the semifinals of the 2015 AFC Champions League"

(nouns, verbs) = mylib.get_nouns_and_verbs(sentence)
print nouns
print verbs

