Kaomoji Database Edit Tool
==========================

Quickly add and categorize kaomojis in a database.

Python lib (ready) and tool (soon…) to edit kaomoji database.

Features:

-  easily add new kaomoji to the database
-  easily add ou remove new keywords

*(readme in the make!)*

Installation
------------

1. Clone this repository and change to it’s directory
2. pip install –requirement requirements.txt
3. Get the emoticons.tsv: wget
   https://raw.githubusercontent.com/cspeterson/splatmoji/master/data/emoticons/emoticons.tsv
   -O emoticons.tsv

Usage
-----

python -m kaomojiedit [options]

python -m kaomojiedit –help # list commands

Commands
--------

add
~~~

::

   Usage: python -m kaomojiedit add [OPTIONS]

     Adds the selected kaomoji to the selected database

   Options:
     -f, --database TEXT  Kaomoji database file name.
     -k, --kaomoji TEXT   Kaomoji; use - to read from STDIN.
     -w, --keywords TEXT  Comma-separated list of keywords to change.
     --help               Show this message and exit.

rm
~~

edit
~~~~

kwadd
~~~~~

kwrm
~~~~

diff
~~~~

User config file:
-----------------

You can have a user configuration file at ``~/.kaomojiedit``. The file
has ``toml`` format. Current options:

``~/.kaomojiedit`` config file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   database_filename = "emoticons.tsv"  # can be a path relative to current
                                        # directory or absolute; ~ is expanded
                                        # to $HOME
                                        # default database file to edit
