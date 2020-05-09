# Flask Gallery

This is a gallery that holds graphic books in a MongoDB database. The program is meant to be for development and has little security practice.

## Getting Started

Follow these steps to setup your environment.
* Install the prerequisites (down below).
* Download and install [MongoDB] (https://docs.mongodb.com/manual/).
* Copy mongod.conf into your mongodb folder.
* Edit the mongod.conf file. Change the path and dbPath to your own paths.
* run the following command in your terminal.
```
<directory to mongodb>/bin/mongod --config <directory to mongodb>/mongod.conf --fork
```

### Prerequisites

Requires the following libraries.

```
    pip install --upgrade flask
    pip install --upgrade flask-wtf
    pip install --upgrade pymongo
```

## Built With

* [Python 3.8.1](https://www.python.org/downloads/release/python-381/)
* [Flask 1.1.1](https://flask.palletsprojects.com/)
* [Bootstrap 4.4](https://getbootstrap.com/docs/4.4/)
* [MongoDB 4.2](https://docs.mongodb.com/manual/)

## Demo

To start the server, run `python main.py`

![Flask Gallery Showcase](https://i.imgur.com/bpc6zq4.jpg)

## Authors

* **[Kevin Chen](https://github.com/kkchen-dev)**

## License

* **[MIT License](../LICENSE)**

## Acknowledgments

* [Billie Thompson](https://gist.github.com/PurpleBooth) provides [the template]((https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)) for this document.

* [Corey Schafer](https://github.com/CoreyMSchafer) - This project follows [Corey Schafer's guide](https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH) on Flask.