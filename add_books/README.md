# Add book

This program adds the data in the books folder to the Mongodb of Flask gallery.

## Getting Started

Prepare the books using the following data format.

* Create a folder named `METADATA <Title>` under the books folder, except the titles starting with f"METADATA TEMPLATE", which are reserved.
    * These will work:
        * METADATA Animals
        * METADATA Cars
        * METADATA Paints
    * These won't work:
        * METADATA Template
        * METADATA TEMPLATE ABC
        * METADATAAnimals
* Put your jpg files under the f"METADATA {Title}" folder. Named `1.jpg`, `2.jpg`, `3.jpg`, etc.
* Copy the `metadata.json` file from `books/METADATA Template`
* Edit the `<>` parts in `METADATA <Title>/metadata.json`.
* Do `python add_books/run`.


### Prerequisites

Requires the following library.

```
    pip install --upgrade pymongo
```

## Built With

* [Python 3.8.1](https://www.python.org/downloads/release/python-381/)
* [MongoDB 4.2](https://docs.mongodb.com/manual/)

## Demo

To start the server, run `python run.py`

## Authors

* **[Kevin Chen](https://github.com/kkchen-dev)**

## License

* **[MIT License](../LICENSE)**

## Acknowledgments

* [Billie Thompson](https://gist.github.com/PurpleBooth) provides [the template]((https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)) for this document.