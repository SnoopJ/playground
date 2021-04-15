from pathlib import Path
from collections import Counter
import random


words = Path("english-words/words.txt").read_text().splitlines()  # a dictionary I have a local copy of

corpus = random.sample(words, k=25)  # let's pick 25 random words to be a corpus
target_words = random.sample(corpus, k=5)  # and 5 of those will be our "target" words

sentence = ' '.join(random.choices(corpus, k=30))  # and build a sentence out of 100 of *those* words (repeats guaranteed)

print("Sentence:\n---")
print(sentence)
print("---")

print("Target words:\n---")
print(target_words)
print("---")

cnts = Counter(word for word in sentence.split())
print("Counts:\n---")
print(cnts)
print("---")

target_cnts = {w: cnts.get(w, 0) for w in target_words}
print("Target counts:\n---")
print(target_cnts)
