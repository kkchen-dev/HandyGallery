# Crawler Set

This is a set of crawlers that grab images from the Internet. They are only for personal use.

## Getting Started

* Copy your headers into headers_unenc.json and headers.json.
* Set the host in headers.json to *the supported website*.
* In data.json, set the site_string to https://{*the supported website*}/s/

You can use any of the following, but beware of some of the prerequisites.

```
python ex_reader_neo.py
python ex_crawler.py
python ex_crawlerdb.py
python read_db.py
```

If you face any problem, try altering the json files and the preceding python files.

### Prerequisites

Requires the following libraries.

```
    pip install --upgrade requests
```

## Built With

* [Python 3.8.1](https://www.python.org/downloads/release/python-381/)

## Demo

## Authors

* **[Kevin Chen](https://github.com/kkchen-dev)**

## License

* **[MIT License](../LICENSE)**

## Acknowledgments

* [Billie Thompson](https://gist.github.com/PurpleBooth) provides [the template]((https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)) for this document.