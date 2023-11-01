import json
from pprint import pprint

import requests


# PRIVATE, DO NOT SHARE!!!
GITHUB_TOKEN = "<insert your GitHub Personal Access Token here>"


GITHUB_HEADERS = {
    "Authorization": f"bearer {GITHUB_TOKEN}",
}


def main():
    REPO_OWNER = "sopel-irc"
    REPO_NAME = "sopel"
    MILESTONE_TARGET = "8.0.0"

    QUERY =  """
    query {
        repository(owner:"sopel-irc", name: "sopel") {
            milestones(first:1, query: "8.0.0") {
                nodes {
                    pullRequests(first:1000) {
                        nodes {
                            title
                            createdAt
                            closedAt
                            number
                            timelineItems(first:10, itemTypes: [MILESTONED_EVENT]) {
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
                            timelineItems(first:10, itemTypes: [MILESTONED_EVENT]) {
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


    JSON_PAYLOAD = f"""
    {{
        "query": "{QUERY}"
    }}
    """

    response = requests.post("https://api.github.com/graphql", data=JSON_PAYLOAD, headers=GITHUB_HEADERS)
    try:
        response.raise_for_status()
    except:
        print(response.content)
        raise

    data = response.json()
    if "errors" in data:
        pprint(data, width=120)
        raise SystemExit

    outfn = "sopel_milestone_data.json"
    with open(outfn, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Query output dumped to {outfn!r}")

if __name__ == "__main__":
    main()
