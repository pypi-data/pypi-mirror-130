#!/usr/bin/env python3

import os
import random
import time

import click
import toml

# from kaomojitool.kaomoji import KaomojiDBKaomojiExists
# from kaomojitool.kaomoji import KaomojiDBKaomojiDoesntExist
from .kaomoji import Kaomoji
from .kaomoji import KaomojiDB

from .kaomoji import KaomojiDBKaomojiExists
from .kaomoji import KaomojiDBKaomojiDoesntExist

class KaomojiToolNoDatabase(Exception):
    description="Kaomoji edit tool couldn't open database"
    def __init__(self, *args, **kwargs):
        super().__init__(self.description, *args, **kwargs)

DEFAULT_CONFIG = {
    'database_filename': './emoticons.tsv',
}

USER_CONFIG_FILENAME = os.path.expanduser("~/.kaomojitool")
USER_CONFIG: dict

CONFIG = DEFAULT_CONFIG  # initialize it with defaults

USER_CONFIG = dict()

class KaomojiTool:

    def __init__(self, database_filename, config_filename, *args, **kwargs):

        if os.path.isfile(USER_CONFIG_FILENAME):
            USER_CONFIG =\
                self._get_user_config_file(filename=USER_CONFIG_FILENAME)
            CONFIG.update(USER_CONFIG)

        self.config = self._update_config(config_filename=config_filename,
                                          database_filename=database_filename)

        self.database = self._open_database()

    def _get_user_config_file(self, filename):

        config_file = os.path.expanduser(filename)

        if os.path.isfile(config_file):
            return toml.load(config_file)

        return DEFAULT_CONFIG

    def _open_database(self):

        database_filename = self.config['database_filename']
        # HERE: also check if it is valid
        if os.path.isfile(database_filename):
            return KaomojiDB(filename=database_filename)
        else:
            raise KaomojiToolNoDatabase

        return None

    def backup_database(self):

        database = self.database
        timestamp = time.time()
        backup_filename = "{filename}.{timestamp}.bkp".\
            format(filename=database.filename, timestamp=timestamp)
        backup = KaomojiDB(filename=database.filename)
        backup.write(filename=backup_filename)

    def _update_config(self, database_filename=None, config_filename=None,
                       config=CONFIG,
                       user_config_filename=USER_CONFIG_FILENAME):
        """Updates config with priority:
        1. user command-line entry.
        2. user default config file.
        3. default config.
        """

        self.config = config

        if config_filename and os.path.isfile(config_filename):
            self.user_config =\
                self._get_user_config_file(filename=user_config_filename)
            self.config.update(self.user_config)

        if database_filename:
            self.config.update({'database_filename': database_filename})

        return self.config

keywords_add_option = click.option(
    "-a", "--add", "keywords_add",
    default=None,
    multiple=True,
    #prompt="Keywords to add, comma-separated",  # this should go inside function
    type=str,
    help = "Comma-separated or option-separated list of keywords to add.")

keywords_remove_option = click.option(
    "-x", "--rm", "keywords_remove",
    default=None,
    multiple=True,
    #prompt="Keywords to remove, comma-separated",  # this should go inside function
    type=str,
    help="Comma-separated or option-separated list of keywords to remove.")

database_filename_option = click.option(
    "-f", "--database", "database_filename",
    default=CONFIG['database_filename'],
    type=str,
    help="Kaomoji database file name.")

kaomoji_code_option = click.option(
    "-k", "--kaomoji", "kaomoji_code",
    default=None,
    #prompt="Kaomoji",
    type=str,
    help="Kaomoji; use - to read from STDIN.")

keywords_option = click.option(
    "-w", "--keywords", "keywords",
    default=None,
    #prompt="Keywords, comma-separated",
    type=str,
    help="Comma-separated list of keywords to change.")

config_filename_option = click.option(
    "-c", "--config", "config_filename",
    default=None,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="Kaomoji database file name.")

other_database_filename_option = click.option(
    "-o", "--other-database", "other_database_filename",
    default=None,
    type=str,
    help="Kaomoji database file name to compare with the default.")

diff_type_option = click.option(
    "-t", "--diff-type", "diff_type",
    default="additional",
    #prompt="Keywords, comma-separated",
    type=click.Choice(["additional", "difference", "exclusive",
                       "intersection"], case_sensitive=False),
    help="Comma-separated list of keywords to change.")

query_string_option = click.option(
    "-q", "--query", "query_string",
    default="",
    type=str,
    help="String to query keywords.")

@click.group()
def cli():
    """Toolchain to edit kaomoji database files.

    Contribute at:

    https://github.com/iacchus/kaomoji-database-edit-tool/
    """
    pass

###############################################################################
# add                                                                         #
###############################################################################
@cli.command()
@database_filename_option
@kaomoji_code_option
@keywords_option
@config_filename_option
def add(database_filename, kaomoji_code, keywords, config_filename):
    """Adds the selected kaomoji to the selected database"""

    kaomojitool = KaomojiTool(database_filename=database_filename,
                              config_filename=config_filename)

    print("Backing up the database '{}'...".\
          format(kaomojitool.database.filename))
    kaomojitool.backup_database()

    kaomoji_add_list: list = list()

    if kaomoji_code:
        new_kaomoji = Kaomoji(code=kaomoji_code, keywords=keywords)
        kaomoji_add_list.append(new_kaomoji)
    else:  # read from stdin
        stdin = click.get_text_stream('stdin')

        for line in stdin.readlines():
            new_kaomoji = Kaomoji(line_entry=line)
            kaomoji_add_list.append(new_kaomoji)

    for kaomoji in kaomoji_add_list:

        db_kaomoji = kaomojitool.database.get_kaomoji(kaomoji)  # reference or None

        if db_kaomoji and kaomoji.keywords:
            print("Kaomoji already exists! Updating keywords..")
            db_kaomoji.add_keywords(keywords)
        elif not db_kaomoji:
            print("New kaomoji! Adding...")
            db_kaomoji = kaomojitool.database.add_kaomoji(kaomoji)  # returns reference

        print("kaomoji:", db_kaomoji.code)
        print("keywords:", db_kaomoji.keywords)

    print("Writing db", kaomojitool.database.filename)
    kaomojitool.database.write()


###############################################################################
# edit                                                                        #
###############################################################################
@cli.command()
@database_filename_option
@kaomoji_code_option
@keywords_add_option
@keywords_remove_option
@config_filename_option
def edit(database_filename, kaomoji_code, keywords_add, keywords_remove,
         config_filename):
    """Edits the selected kaomoji to the selected database, adding or removing
    keywords.
    """

    kaomojitool = KaomojiTool(database_filename=database_filename,
                              config_filename=config_filename)

    keywords_to_add = ",".join(keywords_add)  # adding will have preemptiness
    keywords_to_remove = ",".join(keywords_remove)

    print("Keywords to remove:", keywords_to_remove)

    edit_kaomoji = kaomojitool.database.get_kaomoji(by_entity=kaomoji_code)

    if not edit_kaomoji:
        print("New kaomoji! Adding it do database...")
        kaomoji_to_add = Kaomoji(code=kaomoji_code)
        edit_kaomoji = kaomojitool.database.add_kaomoji(kaomoji_to_add)
    else:
        print("Kaomoji already exists! Editing keywords int it...")

    if keywords_to_remove:
        edit_kaomoji.remove_keywords(keywords=keywords_to_remove)
    if keywords_to_add:
        edit_kaomoji.add_keywords(keywords=keywords_to_add)

    print("Backing up the database...")
    kaomojitool.backup_database(db=kaomojitool.database)

    print("Editing...")
    print("kaomoji:", edit_kaomoji.code)
    print("keywords:", edit_kaomoji.keywords)
    kaomojitool.database.update_kaomoji(edit_kaomoji)

    print("Writing db", kaomojitool.database.filename)
    kaomojitool.database.write()


###############################################################################
# rm                                                                          #
###############################################################################
@cli.command()
@database_filename_option
@kaomoji_code_option
@config_filename_option
def rm(database_filename, kaomoji_code, config_filename):
    """Removes the selected kaomoji from the selected database"""

    kaomojitool = KaomojiTool(database_filename=database_filename,
                              config_filename=config_filename)

    if kaomoji_code:
        kaomoji_to_remove = Kaomoji(code=kaomoji_code)

    if kaomojitool.database.kaomoji_exists(kaomoji_to_remove):
        print("Backing up the database...")
        kaomojitool.backup_database(db=kaomojitool.database)

        print("Removing...")
        print("kaomoji:", kaomoji_to_remove.code)
        print("keywords:", kaomoji_to_remove.keywords)
        kaomojitool.database.remove_kaomoji(kaomoji_to_remove)
    else:
        raise kaomojitool.databaseKaomojiDoesntExist

    print("Writing db", kaomojitool.database.filename)
    kaomojitool.database.write()


###############################################################################
# kwadd                                                                       #
###############################################################################
@cli.command()
@database_filename_option
@kaomoji_code_option
@config_filename_option
@keywords_option
def kwadd(database_filename, kaomoji_code, keywords, config_filename):
    """Add keywords to the selected kaomoji."""

    kaomojitool = KaomojiTool(database_filename=database_filename,
                              config_filename=config_filename)

    if not kaomojitool.database.get_kaomoji(by_entity=kaomoji_code):
        print("New kaomoji! Adding it do database...")
        new_kaomoji = Kaomoji(code=kaomoji_code, keywords=keywords)
        kaomojitool.database.add_kaomoji(kaomoji=new_kaomoji)
    else:
        print("Kaomoji already exists! Removing keywords from it...")

    #edit_kaomoji = kaomojitool.database.get_kaomoji_by_code(code=kaomoji_code)
    edit_kaomoji = kaomojitool.database.get_kaomoji(by_entity=kaomoji_code)
    edit_kaomoji.add_keywords(keywords=keywords)

    print("Backing up the database...")
    kaomojitool.backup_database(db=kaomojitool.database)

    print("Removing keywords...")
    print("kaomoji:", edit_kaomoji.code)
    print("keywords:", edit_kaomoji.keywords)
    kaomojitool.database.update_kaomoji(edit_kaomoji)

    print("Writing db", kaomojitool.database.filename)
    kaomojitool.database.write()


###############################################################################
# kwrm                                                                        #
###############################################################################
@cli.command()
@database_filename_option
@kaomoji_code_option
@config_filename_option
@keywords_option
def kwrm(database_filename, kaomoji_code, keywords, config_filename):
    """Remove keywords to the selected kaomoji."""

    kaomojitool = KaomojiTool(database_filename=database_filename,
                              config_filename=config_filename)

    if not kaomojitool.database.get_kaomoji(by_entity=kaomoji_code):
        print("New kaomoji! Adding it do database...")
        new_kaomoji = Kaomoji(code=kaomoji_code, keywords=keywords)
        kaomojitool.database.add_kaomoji(kaomoji=new_kaomoji)
    else:
        print("Kaomoji already exists! Adding keywords to it...")

    edit_kaomoji = kaomojitool.database.get_kaomoji(by_entity=kaomoji_code)
    edit_kaomoji.remove_keywords(keywords=keywords)

    print("Backing up the database...")
    kaomojitool.backup_database()

    print("Removing keywords...")
    print("kaomoji:", edit_kaomoji.code)
    print("keywords:", edit_kaomoji.keywords)
    kaomojitool.database.update_kaomoji(edit_kaomoji)

    print("Writing db", kaomojitool.database.filename)
    kaomojitool.database.write()


###############################################################################
# diff                                                                        #
###############################################################################
@cli.command()
@database_filename_option
@other_database_filename_option
@diff_type_option
@config_filename_option
def diff(database_filename, other_database_filename, diff_type,
         config_filename):
    """Compare two databases and logs the difference between them."""

    kaomojitool = KaomojiTool(database_filename=database_filename,
                              config_filename=config_filename)

    kaomojitool_other =\
        KaomojiTool(database_filename=other_database_filename,
                    config_filename=config_filename)

    if not kaomojitool.database or not kaomojitool_other.database:
        raise KaomojiToolNoDatabase

    diff_dict = kaomojitool.database.compare(other=kaomojitool_other.database,
                                             diff_type=diff_type)
    print(diff_dict)

    # TAKE SHA256, FORMAT FOR kaomojitool.database, WRITE


###############################################################################
# dbstatus                                                                    #
###############################################################################
@cli.command()
@database_filename_option
@config_filename_option
def dbstatus(database_filename, config_filename):
    """Show data from the database."""

    kaomojitool = KaomojiTool(database_filename=database_filename,
                              config_filename=config_filename)

    number_of_kaomoji = len(kaomojitool.database.kaomojis)

    print("database file:", kaomojitool.database.filename)
    print("number of kaomojis:", number_of_kaomoji)


###############################################################################
# query                                                                         #
###############################################################################
@cli.command()
@database_filename_option
@query_string_option
@config_filename_option
def query(database_filename, query_string, config_filename):
    """Adds the selected kaomoji to the selected database"""

    kaomojitool = KaomojiTool(database_filename=database_filename,
                              config_filename=config_filename)

    matches = kaomojitool.database.query(query_string)
    print(matches)

if __name__ == "__main__":

    cli()
