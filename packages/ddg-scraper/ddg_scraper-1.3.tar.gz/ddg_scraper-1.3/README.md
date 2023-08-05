
# Asynchronous and Synchronous DuckDuckGo Search Engine Scraper

Scrapes the [duckduckgo](https://duck.com) search engine.

# Asynchronous Example
```py
from ddg_scraper import asearch
import asyncio


async def main():
    results = await asearch("Python")
    async for result in results:
        ...

asyncio.run(main())
```

# Synchronous Example
```py
from ddg_scraper import search


results = search("Python")
for result in results:
    ...
```

In both examples, `result` is [`ddg_scraper.Result`](ddg_scraper/_dataclasses.py)

# Attributes and Methods of [`ddg_scraper.Result`](ddg_scraper/_dataclasses.py)

Attributes

- `title`
- `description`
- `url`
- `icon_url`

Methods

- `as_dict()`
    - Converts the dataclass to a `dict` object and returns it.

# How To Install

- **Using pip:** `pip install ddg-scraper`
- **Manual:**
  - Clone the folder somewhere
  - CD to the location
  - Install the packages listed in [`requirements.txt`](/requirements.txt) (`pip install -r requirements.txt`)
  - Copy the folder, [ddg_scraper](/ddg_scraper) where you want to use it.
