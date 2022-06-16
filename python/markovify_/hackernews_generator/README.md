## HackerNews n-gram Markov generator

### Using this generator

```
$ python3 -m venv hackernews_generator_venv && source hackernews_generator_venv/bin/activate
$ python3 -m pip install -r requirements.txt
$ python3 scrape_hackernews.py
$ python3 generate_sentences.py <path to .json>
```

### More information

* `generate_sentences.py` is a program that, given a corpus built from scraping
  HackerNews, will use a [Markov Chain](https://en.wikipedia.org/wiki/Markov_chain)
  model to generate sentence, using the excellent library [`markovify`](https://github.com/jsvine/markovify)

* `scrape_hackernews.py` is a program that will scrape HackerNews to build a
  corpus for user with `generate_sentences.py`.


These programs are kind of hard to read in their current form. Sorry about that!
