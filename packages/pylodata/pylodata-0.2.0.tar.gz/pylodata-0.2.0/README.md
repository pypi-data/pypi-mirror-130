# Data Samples and Data Handling Routines for Pylogeny Packages

## Installation

```
$ git clone https://github.com/pylogeny/data
$ pip install -e data
```

## Usage

```
>>> from pylodata import data_path, patterns, wordlist
>>> from lingpy import Wordlist
>>> patterns, characters = wordlist.get_multistate_patterns(Wordlist(data_path("wichmannmixezoquean.tsv")))
```

