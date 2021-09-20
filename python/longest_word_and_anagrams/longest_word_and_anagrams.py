"""
Based on a question posed on Freenode on Feb 14, 2019

Given a set of valid words and a list of input words, select the longest words
in the input such that at least one anagram of these words appears in the valid
set, and output these words and their anagrams

A word and its anagrams are all made from the same collection of letters,
so that e.g. both 'coat' and 'taco' become the `Counter` object: 
    `{'a': 1, 'o': 1, 'c': 1, 't':1}`

Therefore, if we created a `set` of `Counter` objects for all lists in the
valid set, we would have an O(1) lookup structure for words-and-their-anagrams.
Howevre, the `Counter` implementation from `collections` is not hashable, but
we can pretty easily write a subclass that has the properties we seek.

So, our solution is to create this set, and then do a membership test of the
tuples produced by the input against this set.
"""
import json
from collections import Counter, defaultdict
import random
import time

def wordbag(word):
    bag = sorted(tuple(Counter(word).items()), key=lambda t: t[0])
    return tuple(bag)

def random_anagrammable(Nsamples, wbags, Nanagrams=1, Lmax=None):
    """
    Randomly sample words from a dictionary which also have an anagram in the dictionary.

    Parameters
    ----------
    Nsamples : int
        Number of words to sample
    wbags : mapping
        Structure mapping `wordbag(word)` to a set of all anagrams of that word.
    Nanagrams : int, optional
        Number of anagrams a word must have to be suitable. Defaults to 1.
    Lmax : int, optional
        Maximum length of word to sample.
    """
    candidates = [w for ws in wbags.values() 
                    for w in ws 
                    if (Lmax is None or len(w) <= Lmax) and len(ws) > 1]
    return random.sample(candidates, Nsamples)

if __name__ == "__main__":
    MAXLEN = None  # the maximum length of anagrammable candidates
    NWORDS = (10, 20, 40,
              100, 200, 400,
              1000, 2000, 4000,
              10000, 20000, 40000)
    times = []

    print("Initializing wordbag set...")
    with open('words.json', 'r') as f:
        words = json.load(f).keys()
        wbags = defaultdict(set)
        for w in words:
            wbags[wordbag(w)] |= {w}
    print("Wordbag set complete!")

    for N in NWORDS:
        # testwords = ["taco", "coat", "adobe", "abode"]
        # this solution works for words without any anagrams, but that's boring!
        # so let's sample some random 
        print(f"Creating a list of {N} word candidates")
        testwords = random_anagrammable(N, wbags, Lmax=MAXLEN)
        print("Done finding candidates!")

        start = time.time()
        leaders = None
        L = 0
        for w in testwords:
            wl = len(w)
            if w and wl < L: 
                # skip empty strings and input shorter than the current leader
                continue  
            
            wb = wordbag(w)
            if wb in wbags.keys():
                if wl == L:  # tie, track this word too
                    leaders.append((w, wb))
                else:  # must have `wl > L`, so `w` is the new leader
                    leaders = [(w, wb)]
                    L = wl

        if not any(w[0] for w in leaders):  # no non-empty strings, which means fall-through
            print("None of the input words appear in the valid set!")
            exit()
        else:
            for (word, wb) in leaders:
                anagrams = (',\n'.join(wbags[wb] - {word}) or "None found!")
                print(f"Word: {word}")
                print(f"Anagrams:\n{anagrams}")
        dt = time.time() - start
        times.append(dt)
        print(f"Search for NWORDS={N} took {dt:.3e} sec")
    
    print(f"\nN=\n{N}")
    print(f"times=\n{times}")
