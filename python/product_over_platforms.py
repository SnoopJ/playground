"""
Based on a question in #python on Freenode on 3 June 2020
"""
import itertools
from pprint import pprint

supported_platforms = {
        'operating_systems': ['rhel7', 'ubuntu18', 'ubuntu16'],
        'databases': ['postgres9.5', 'mssql2016', 'mssql2017', 'oracle12'],
        'file_storage': ['s3', 'azure', 'nfs', 'cifs'],
        'auth_methods': ['oidc', 'oidc_google', 'saml', 'ldap']
}

def platforms(spec):
    valproduct = itertools.product(*spec.values())  # cartesian product of all values
    for vals in valproduct:
        yield {k:v for k,v in zip(spec.keys(), vals)}


if __name__ == "__main__":
    results = list(platforms(supported_platforms))
    print(f"Number of results: {len(results)}")
    print(f"Number of expected results: {3*4*4*4}")
    print("First 6 results:")
    pprint(results[:6])


