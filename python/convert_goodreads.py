"""
A small utility program I wrote to make a dump of my data exported from GoodReads
"""
import csv
import json
import textwrap
from pathlib import Path


HERE = Path(__file__).parent.resolve()
LIBRARY_FILE = HERE.joinpath("www", "goodreads_library_export.csv")


def main():
    with open(LIBRARY_FILE, 'r') as f:
        reader = csv.DictReader(f)
        books = list(reader)

    for book in books:
        title = book["Title"]
        author = book["Author"]
        rating = book["My Rating"]
        review = book["My Review"]
        if rating != '0':
            print(title)
            print(author)
            print(f"My Rating: {rating}/5.0")
            print("-"*24)
            if not review:
                print("<no review>")
            else:
                print(*textwrap.wrap(review), sep='\n')
            print()

if __name__ == "__main__":
    main()
