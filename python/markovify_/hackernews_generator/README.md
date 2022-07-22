## Markov n-gram model

### Usage

```
$ python3 -m venv hn_markov && source hn_markov/bin/activate
$ python3 -m pip install -r requirements.txt
$ python3 scrape_hackernews.py  # and wait for a bit
$ python3 generate_sentences.py <path to .json>
```

### Details

This is a little [Markov chain](https://en.wikipedia.org/wiki/Markov_chain)
sentence generator built on a corpus learned by scraping HackerNews posts for
comments, using the excellent library [`markovify`](https://github.com/jsvine/markovify).
