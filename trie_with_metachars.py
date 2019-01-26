"""
  Prefix tree (trie) that supports searching with wildcards ?, *

  Based on code courtesy of StackOverflow user Lin Ma https://codereview.stackexchange.com/q/142878
  Heavily adapted for a question in #python on freenode
"""
import time
import random
import string

TREESIZE = 100_000

# Set if you wish to observe the search process
# This slows everything down by a lot, so I recommend changing TREESIZE too
DEBUGSEARCH = False


class TrieNode:
    def __init__(self, c=""):
        self.children = {}
        self.isEnd = False
        self.c = c

    def randomwalk(self, maxdepth=10):
        """ Retrieve some random nodes, going no deeper than `depth` """
        if (
            maxdepth == 0
            or len(self.children) == 0  # can't go any further
            or (self.c and random.random() < 0.1)
        ):  # don't wish to go any further
            return self.c

        # choose a random child and keep walking
        return self.c + random.choice(list(self.children.values())).randomwalk(
            maxdepth - 1
        )

    def insert(self, keystr):
        node = self
        for c in keystr:
            if c in node.children:
                node = node.children[c]
            else:
                node.children[c], node = [TrieNode(c)] * 2

    def search(self, searchstr, history="<root>"):
        """ Perform a depth-first search """
        if searchstr in ("", "*"):
            # if the search string is either a wildcard or the empty string, we are a trivial match
            return ""

        state = history + self.c
        if DEBUGSEARCH:
            print(f"in ({state}), searchstr = {searchstr}")

        if searchstr[0] == "?":
            for (ch, node) in self.children.items():
                res = node.search(searchstr[1:], state)
                if res or res == "":
                    return ch + res
        elif searchstr[0] == "*":
            for (ch, node) in self.children.items():
                res = node.search(searchstr[1:], state) or node.search(searchstr, state)
                if res or res == "":
                    return ch + res
        else:  # nothing special about the search key
            if searchstr[0] in self.children:
                node = self.children[searchstr[0]]
                res = node.search(searchstr[1:], state)
                if res or res == "":
                    return searchstr[0] + res

        # if we made it all the way down here, no luck, return False
        return False


def randomstring(N):
    """ Generate a random string of length N """
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(N)
    )


if __name__ == "__main__":
    root = TrieNode()
    print(f"Generating a random tree of {TREESIZE} elements")
    start = time.time()
    for _ in range(TREESIZE):
        randstr = randomstring(9)
        root.insert(randstr)
    end = time.time()
    print(f"Tree generation took {end-start:.2e} s\n")

    searches = []
    # select at random strings matching some of those nodes and randomly pepper in *, ?
    for _ in range(10):
        node = root.randomwalk(10)
        # randomly swap in other characters
        node = "".join(
            c
            if random.random() < 0.05
            else random.choice(string.ascii_letters + string.digits)
            for c in node
        )
        # randomly pepper in wildcards
        node = "".join(
            random.choice("?*") if random.random() < 0.25 else c for c in node
        )
        searches.append(node)

    # explicitly insert a few known elements, too
    for s in ("foo1bar2baz", "lorem ipsum dolor sit amet", "Hey, I'm walking here!"):
        root.insert(s)

    searches += [
        "",  # included only for pretty printing below to separate random and fixed searches
        "foo*",
        "Lorem ips?m",
        "*do?or",
        "foo*bar",
        "H*walk*",
        "*walk*",  # note that a leading * is extremely expensive compared to even a single prefix character! In the worst case, this becomes almost a linear search!
        "In the beginning...",  # microoptimization possibility (for search): store trie height on root node, at expense of insert() ?
        "a?*",
    ]

    pad = max(len(s) for s in searches) + 10
    for searchstr in searches:
        if len(searchstr) == 0:
            continue
        start = time.time()
        result = root.search(searchstr)
        end = time.time()

        print(
            f'{searchstr:<{pad}} in tree: {result and "YES" or "NO "} (search took {end-start:.2e} s)'
        )
