# mediawiki-history-dumps-scraper

This is the **pip** module of "Mediawiki history dumps scraper", refer to the [main branch](https://github.com/euberdeveloper/mediawiki-history-dumps-scraper) to see in general the projects' purpose.

## What does the module do?

This pip module allows you to get (also selectively), through a **scraper**, the available content in [Mediawiki history dumps](https://dumps.wikimedia.org/other/mediawiki_history/readme.html). You can check wich versions are available, which language, which datasets, the download links, the size...

## How was it made?

This module was written in **Python 3.9** and uses `requests` and regexps to **scrape** the content from the [Download site](https://dumps.wikimedia.org/other/mediawiki_history/). The package manager is **poetry**, because it is far better than just pip and because it has a command to directly publish it to pypi. It is also linted with **pylint**.

## How to use it?

### Installation

With *pip*:

```bash
pip install mhdscraper
```

With *pipenv*:

```bash
pipenv install mhdscraper
```

With *poetry*:

```bash
poetry add mhdscraper
```

### Examples

An example (you can add print of a variable to see the response).

```python
import mhdscraper

from datetime import date

# Returns the root url of the datasets site
wiki_url = print(mhdscraper.WIKI_URL)

# Returns a list of versions, returning the version name and its url
versions = mhdscraper.fetch_versions()
# Returns a list of datasets, returning the dataset name, its url and 
# including all the available wikies (name and url)
versions_with_langs = mhdscraper.fetch_versions(wikies=True)

# Returns a list containing all the wikies of the latest version, 
# returning name and url
wikies = mhdscraper.fetch_wikies('latest')
# Returns a list containing the wikies ending with 'wiki' of the 
# latest version, returning name and url
wikies_ending_with_wiki = mhdscraper.fetch_wikies('latest', wikitype='wiki')
# Returns a list containing the wikies starting with 'it' of the latest version, 
# returning name, url and the list of available dumps
wikies_with_dumps = mhdscraper.fetch_wikies('latest', lang='it', dumps=True)

# Returns a list containing all the dumps of 'itwiki' of the latest version, 
# reurning many pieces of information such as filename, start and end date 
# of the content, size in bytes, url to download it...
dumps = mhdscraper.fetch_dumps('latest', 'itwiki')
# Returna a listo containing all the dumps of 'itwiki' of the latest version,
# whose content is between 2004-01-01 and 2005-02-01
dumps_selected = mhdscraper.fetch_dumps('latest', 'itwiki', start=date(2004, 1, 1), end=date(2005, 2, 1))
```

The result of:

```python
import mhdscraper
from datetime import date

result = mhdscraper.fetch_wikies('latest', lang='it', wikitype='wiki', dumps=True, start=date(2010, 1, 1), end=date(2012, 12, 31))
```

Would be (as of July 2021):

```json
[
    {
        "dumps": [
            {
                "bytes": "691419132",
                "filename": "2021-06.itwiki.2010.tsv.bz2",
                "from": "2010-01-01",
                "lastUpdate": "2021-07-03T10:38:00",
                "time": "2010",
                "to": "2010-12-31",
                "url": "https://dumps.wikimedia.org/other/mediawiki_history/2021-06/itwiki/2021-06.itwiki.2010.tsv.bz2"
            },
            {
                "bytes": "706208269",
                "filename": "2021-06.itwiki.2011.tsv.bz2",
                "from": "2011-01-01",
                "lastUpdate": "2021-07-03T10:57:00",
                "time": "2011",
                "to": "2011-12-31",
                "url": "https://dumps.wikimedia.org/other/mediawiki_history/2021-06/itwiki/2021-06.itwiki.2011.tsv.bz2"
            },
            {
                "bytes": "747376403",
                "filename": "2021-06.itwiki.2012.tsv.bz2",
                "from": "2012-01-01",
                "lastUpdate": "2021-07-03T10:11:00",
                "time": "2012",
                "to": "2012-12-31",
                "url": "https://dumps.wikimedia.org/other/mediawiki_history/2021-06/itwiki/2021-06.itwiki.2012.tsv.bz2"
            }
        ],
        "url": "https://dumps.wikimedia.org/other/mediawiki_history/2021-06/itwiki",
        "wiki": "itwiki"
    }
]
```

## API

### `WIKI_URL`

It is a constant containing the url of the root of the datasets site

### `fetch_latest_version(*, wikies, lang, wikitype, dumps, start, end)`

Fetches the last version of the mediawiki history dumps.

The version is the year-month of the release of the dumps

Keyword parameters:
* __wikies__ (_bool, default=False)_: If for each returned version the wikies will be fetched
* __lang__ _(str, default=None)_: If the wikies argument is True, the language of the wikies to return (a wiki name starts with the language).
* __wikitype__ _(str, default=None)_: If the wikies argument is True, the wiki type of the wikies to return (a wiki name ends with the wiki type).
* __dumps__ _(bool, default=false)_: If for each returned wiki the wikies will be fetched
* __start__ _(date, default=None)_: If the wikies and dumps arguments are True, retrieve only the dumps newer than this date
* __end__ _(date, default=None)_: If the wikies and dumps arguments are True, retrieve only the dumps older than this date

Returns a dict with:
*  `version` _(str)_ for the version year-month
*  `url` _(str)_ for the url of that version. 
*  `wikies` will contain the fetched wikies if the argument was set to True.  
If no version is found, `None` is returned.

### `fetch_versions(*, wikies, lang, wikitype, dumps, start, end)`

Fetch the versions of the mediawiki history dumps

The versions are the year-month of the release of the dumps

Keyword parameters:
* __wikies__ (_bool, default=False)_: If for each returned version the wikies will be fetched
* __lang__ _(str, default=None)_: If the wikies argument is True, the language of the wikies to return (a wiki name starts with the language).
* __wikitype__ _(str, default=None)_: If the wikies argument is True, the wiki type of the wikies to return (a wiki name ends with the wiki type).
* __dumps__ _(bool, default=false)_: If for each returned wiki the wikies will be fetched
* __start__ _(date, default=None)_: If the wikies and dumps arguments are True, retrieve only the dumps newer than this date
* __end__ _(date, default=None)_: If the wikies and dumps arguments are True, retrieve only the dumps older than this date

Returns a list of dicts with:
* `version` _(str)_ for the version year-month
* `url` _(str)_ for the url of that version. 
* `wikies` will contain the fetched wikies if the argument was set to True (see *fetch_wikies* to see the result).

### `fetch_wikies(version, /, *, lang, wikitype, dumps, start, end)`

Fetch the wikies of a version of the mediawiki history dumps

Parameters:
* version _(str)_: The version whose wikies will be returned. If "latest" is passed, the latest version is retrieved.

Keyword parameters:
* lang _(str, default=None)_: The language of the wikies to return (a wiki name starts with the language).
* wikitype _(str, default=None)_: The wiki type of the wikies to return (a wiki name ends with the wiki type).
* dumps _(bool, default=false)_: If for each returned wiki the dumps will be fetched
* start _(date, default=None)_: If the dumps argument is True, retrieve only the dumps newer than this date
* end _(date, default=None)_: If the dumps argument is True, retrieve only the dumps older than this date

Returns a list of dicts with:
* `wiki` _(str)_ for the wiki name
* `url` _(str)_ for the url of that wiki. 
In addition, if the `dumps` argument is True, a `dumps` (list) field contain the fetched dumps (see *fetch_dumps* to see the reuslt).

### `fetch_dumps(version, wiki, /, *, start, end)`

Fetch the dumps of a wiki of the mediawiki history dumps

Parameters:
* version _(str)_: The version of the wiki
* wiki _(str)_: The wiki whose dumps will be returned

Keyword parameters:
* start _(date, default=None)_: Retrieve only the dumps newer than this date
* end _(date, default=None)_: Retrieve only the dumps older than this date

Returns a list of dicts with:
* `filename` _(str)_ for dump file name
* `time` _(str)_ for the time of the data (`'all-time'`, year or year-month
* `lastUpdate` _(datetime)_ for the last update date
* `bytes` _(int)_ for the size in bytes of the file
* `from` _(date)_ for the start date of the data
* `to` _(date)_ for the end date of the data
* `url` _(str)_ the url of the file
