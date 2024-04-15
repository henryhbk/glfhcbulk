import sqlite3

import click
from flask import current_app, g


def get_db():
    """
    :return: A connection to the SQLite database.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
    Closes the database connection.

    :param e: The exception that occurred. Default is None.
    :return: None
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    Initialize the database by executing the SQL statements from the 'schema.sql' file.

    :return: None
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_app(app):
    """
    Initialize the Flask app and register

    :param app: The Flask app instance.
    :return: None.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def init_app(app):
    """
    Initializes the Flask application instance.

    :param app: Flask application instance.
    :return: None
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command('init-db')
def init_db_command():
    """
    Initialize the database via the click CLI

    :return: None
    """
    init_db()
    click.echo('Initialized the database.')
