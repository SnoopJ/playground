This script queries the [PyPI JSON API](https://warehouse.pypa.io/api-reference/json.html)
(as well as the [JSON dialect of the 'Simple API'](https://peps.python.org/pep-0691))
to retrieve information about the requirements of each available version of a
package, in particular allowing for querying a specific set of requirements and
a specific range of package versions.

```
$ python3 query_pypi_requirements_by_version.py --help
usage: query_pypi_requirements_by_version.py [-h] [-r REQS] [--pre] [--min MIN] [--max MAX] [--rate-limit RATE_LIMIT] pkg

Query the PyPI JSON APIs for information about a package's requirements across multiple versions

positional arguments:
  pkg                   The name of a package to query

optional arguments:
  -h, --help            show this help message and exit
  -r REQS, --requirement REQS
                        Optional name of a requirement to query across each version. May be given multiple times
  --pre                 If given, show pre-release versions
  --min MIN             If given, minimum package version to consider
  --max MAX             If given, maximum package version to consider
  --rate-limit RATE_LIMIT
                        Maximum number of requests/sec to make to PyPI

$ python3 query_pypi_requirements_by_version.py apache-beam --min 2.30 -r protobuf
apache-beam==2.30.0 - ['protobuf<4,>=3.12.2']
apache-beam==2.31.0 - ['protobuf<4,>=3.12.2']
apache-beam==2.32.0 - ['protobuf<4,>=3.12.2']
apache-beam==2.33.0 - ['protobuf<4,>=3.12.2']
apache-beam==2.34.0 - ['protobuf<4,>=3.12.2']
apache-beam==2.35.0 - ['protobuf<4,>=3.12.2']
apache-beam==2.36.0 - ['protobuf<4,>=3.12.2']
apache-beam==2.37.0 - ['protobuf<4,>=3.12.2']
apache-beam==2.38.0 - ['protobuf<4,>=3.12.2']
apache-beam==2.39.0 - ['protobuf<4,>=3.12.2']
apache-beam==2.40.0 - ['protobuf<4,>=3.12.2']
apache-beam==2.41.0 - ['protobuf<4,>=3.12.2']
apache-beam==2.42.0 - ['protobuf<4,>=3.12.2']
apache-beam==2.43.0 - ['protobuf<3.19.5,>3.12.2']
apache-beam==2.44.0 - ['protobuf<3.19.5,>3.12.2']
apache-beam==2.45.0 - ['protobuf<3.19.5,>3.12.2']
apache-beam==2.46.0 - ['protobuf<3.19.5,>3.12.2']
apache-beam==2.47.0 - ['protobuf<4.23.0,>=3.20.3']
apache-beam==2.48.0 - ['protobuf<4.24.0,>=3.20.3']
apache-beam==2.49.0 - ['protobuf<4.24.0,>=3.20.3']
apache-beam==2.50.0 - ['protobuf<4.24.0,>=3.20.3']
apache-beam==2.51.0 - ['protobuf!=4.0.*,!=4.21.*,!=4.22.0,!=4.23.*,!=4.24.0,!=4.24.1,!=4.24.2,<4.25.0,>=3.20.3']
```
