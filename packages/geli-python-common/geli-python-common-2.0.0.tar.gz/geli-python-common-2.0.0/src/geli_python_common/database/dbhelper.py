import functools
from sqlalchemy import exc
from alembic import command
from time import sleep
from sqlalchemy_utils.functions import drop_database, create_database, database_exists

from logbook import Logger
logger = Logger(__name__)

def sqlalchemy_exception_wrapper(session: 'Session'):
    """
    This is a decorator function which wraps the SQLAlchemy exception handling for the DB functions

    Issue explained here: https://docs.sqlalchemy.org/en/13/faq/sessions.html#this-session-s-transaction-has-been-rolled-back-due-to-a-previous-exception-during-flush-or-similar

    If a session.commit or session.flush fails, we need to explicitly rollback the session, to avoid the below mentioned error. Otherwise, future
    DB transactions will continue to fail.

    Error: "This Session's transaction has been rolled back due to a previous exception during flush.
             To begin a new transaction with this Session, first issue Session.rollback()"
    """

    def actual_decorator(db_func):
        @functools.wraps(db_func)
        def inner(*args, **kwargs):
            try:
                return db_func(*args, **kwargs)
            except exc.SQLAlchemyError as e:
                session.rollback()
                raise
        return inner
    return actual_decorator


def sqlalchemy_commit(session: 'Session'):
    """

    If a session.commit fails, we need to explicitly rollback the session, to avoid the below mentioned error. Otherwise, future
    commits will continue to fail.

    Error: "This Session's transaction has been rolled back due to a previous exception during flush.
            To begin a new transaction with this Session, first issue Session.rollback()"

    Issue explained here: https://docs.sqlalchemy.org/en/13/faq/sessions.html#this-session-s-transaction-has-been-rolled-back-due-to-a-previous-exception-during-flush-or-similar

    """

    try:
        session.commit()
    except:
        session.rollback()
        raise


def sqlalchemy_flush(session: 'Session'):
    """

    If a session.commit fails, we need to explicitly rollback the session, to avoid the below mentioned error. Otherwise, future
    commits will continue to fail.

    Error: "This Session's transaction has been rolled back due to a previous exception during flush.
            To begin a new transaction with this Session, first issue Session.rollback()"

    Issue explained here: https://docs.sqlalchemy.org/en/13/faq/sessions.html#this-session-s-transaction-has-been-rolled-back-due-to-a-previous-exception-during-flush-or-similar

    """

    try:
        session.flush()
    except:
        session.rollback()
        raise


def create_database_and_apply_migrations(app: 'Flask', db: 'SQLAlchemy', db_uri: str):
    """
    Create the database, if it does not exist and apply the migrations
    :param app: Flask application instance
    :param db: SQLAlchemy instance
    :param db_uri: uri of the database
    :return:
    """

    # Create the database specified in the db_uri, if it does not exist
    if not database_exists(db_uri):
        retry_count = 0
        while retry_count < 3:
            try:
                create_database(db_uri)
                break
            except Exception as e:
                logger.error(f'Error during database creation: {e}')
                retry_count+=1
                logger.error(f'Retrying database creation...')
                sleep(20)

    # Apply migrations
    from flask_migrate import Migrate
    with app.app_context():
        config = Migrate(app, db).get_config()
        command.upgrade(config, 'head')
