import json
import math
import os
import string
from pprint import pprint

import requests


try:
    GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
except LookupError as exc:
    raise ValueError("Set the environment variable GITHUB_TOKEN to your personal access token")


GITHUB_HEADERS = {
    "Authorization": f"bearer {GITHUB_TOKEN}",
}


def main():
    # this is a bunch of computation for paginating the results to stay within the
    # limits of the GitHub GraphQL 
    MAX_NODES_PER_QUERY = 500_000
    N_MAX_ITEMS_PER_MILESTONE = 2*1000  # factor of 2 for issues + PRs
    N_MAX_TIMELINE_PER_ITEM = 100
    N_MAX_NODES_PER_MILESTONE = N_MAX_ITEMS_PER_MILESTONE * N_MAX_TIMELINE_PER_ITEM

    N_MILESTONES_PER_QUERY = int(max(MAX_NODES_PER_QUERY // N_MAX_NODES_PER_MILESTONE, 1))

    N_MILESTONES = 100
    N_CHUNKS = math.ceil(N_MILESTONES / N_MILESTONES_PER_QUERY)

    # NOTE: the below query assumes there are no more than 1000 pull requests/issues in a milestone,
    # and also that there are no more than 100 timeline events on any given PR/issue
    QUERY_TEMPLATE = string.Template(
        """
        query {
            repository(owner:"sopel-irc", name: "sopel") {
                milestones(first: $CHUNKSIZE, $MAYBE_OFFSET orderBy: {field: CREATED_AT, direction: DESC}) {
                    pageInfo {
                        startCursor
                        endCursor
                    }
                    nodes {
                        number
                        title
                        pullRequests(first:1000) {
                            nodes {
                                title
                                number
                                createdAt
                                closedAt
                                timelineItems(first:100, itemTypes: [MILESTONED_EVENT]) {
                                    nodes {
                                        ... on MilestonedEvent {
                                            milestoneTitle
                                            createdAt
                                        }
                                    }
                                }
                            }
                        }
                        issues(first:1000) {
                            nodes {
                                title
                                createdAt
                                closedAt
                                number
                                timelineItems(first:100, itemTypes: [MILESTONED_EVENT]) {
                                    nodes {
                                        ... on MilestonedEvent {
                                            milestoneTitle
                                            createdAt
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        """.replace("\n", "").replace('"', r'\"')
    )

    milestone_nodes = []
    cursor = ""

    for chunknum in range(1, N_CHUNKS+1):
        offset = rf'after: \"{cursor}\", ' if cursor else ""
        query = QUERY_TEMPLATE.substitute(CHUNKSIZE=N_MILESTONES_PER_QUERY, MAYBE_OFFSET=offset)

        JSON_PAYLOAD = f"""
        {{
            "query": "{query}"
        }}
        """

        response = requests.post("https://api.github.com/graphql", data=JSON_PAYLOAD, headers=GITHUB_HEADERS)
        try:
            response.raise_for_status()
        except:
            print(response.content)
            raise

        response_data = response.json()
        if "errors" in response_data:
            pprint(response_data, width=120)
            raise SystemExit

        milestones = response_data["data"]["repository"]["milestones"]
        if not milestones["nodes"]:
            # response is empty, all done
            break
        milestone_nodes += milestones["nodes"]
        print(f"Added data for milestones: {[ms['title'] for ms in milestones['nodes']]}")

        cursor = milestones["pageInfo"]["endCursor"]

    outfn = "sopel_milestone_data.json"
    with open(outfn, "w") as f:
        json.dump(milestone_nodes, f, indent=4)

    print(f"Query output dumped to {outfn!r}")

if __name__ == "__main__":
    main()
