# filmbuff

[![pipeline status](https://gitlab.com/emerac/filmbuff/badges/master/pipeline.svg)](https://gitlab.com/emerac/filmbuff/-/commits/master)
[![coverage report](https://gitlab.com/emerac/filmbuff/badges/master/coverage.svg)](https://gitlab.com/emerac/filmbuff/-/commits/master)

## About

filmbuff is a database front-end for managing film information. In other words,
it is a graphical user interface (GUI) application used to access and modify
film data contained in a SQLite database.

filmbuff is designed to appear and function in the same manner as a general
spreadsheet editor. This means that much of the same functionality is present
in filmbuff, such as saving and opening sheets, inserting rows, moving and
sorting columns, etc.

Here are a couple of notable features:

* To aid in data entry, filmbuff includes the ability to access an API
(application programming interface - usually used to retrieve information from
a web service) provided by [TMDb](https://www.themoviedb.org/) (The Movie
Database). The [TMDb API](https://www.themoviedb.org/documentation/api) can be
used to search for and retrieve information about films. Obtaining a key from
TMDb is required in order to be able to use this functionality.

* Once you have populated your database with some data, you can export that
data to a tab-separated value (TSV) file. Many other programs (especially
spreadsheet editors) support importing/exporting TSV files. This allows you to
format the data and print it off to create an index for your film collection.
(filmbuff also supports importing TSV files).

## How to Get Started

### Compatibility

This application is designed to run on all major Linux distributions that have
Python 3.8 or higher.

### Installation

You can use `pip` to install this application by running `pip install
filmbuff`.

### Usage

After installing this application, you can run it with the command `filmbuff`.

If you would like to be able to run filmbuff without having to open a terminal,
run the command `filmbuff --create-shortcut` to create a shortcut in the
applications menu. Please note the following about the `--create-shortcut`
option:

* This option will only work for GNOME desktop environments.
* The shortcut will not show up if filmbuff is installed in a virtual
environment.

To learn about how to use this application and the features it provides, please
take a look at the
[help page](https://gitlab.com/emerac/filmbuff/-/blob/master/src/filmbuff/resources/help.md).
This same help page can be viewed while running filmbuff by pressing `F1`.

## Contributing

Please report any bugs to the
[GitLab issue tracker](https://gitlab.com/emerac/filmbuff/-/issues).
See
[CONTRIBUTING](https://gitlab.com/emerac/filmbuff/-/blob/master/CONTRIBUTING.md)
for more details.

## Credits

Big thanks to [TMDb](https://www.themoviedb.org/) for providing the API used
to retrieve metadata.

## License

This program is free software and is licensed under the GNU General
Public License. For the full license text, view the
[LICENSE](https://gitlab.com/emerac/filmbuff/-/blob/master/LICENSE) file.

Copyright © 2021 emerac
