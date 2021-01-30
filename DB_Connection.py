import contextlib
import mysql.connector
from mysql.connector.errors import Error
from sqlalchemy import create_engine, insert, Table, MetaData, select, and_, update
import pymysql
import logging


def my_logger(__name__):
    # Gets or creates a logger
    logger = logging.getLogger(__name__)

    # set log level
    logger.setLevel(logging.WARNING)

    # define handler
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler('logfile.log')
    file_handler.setLevel(logging.ERROR)
    stream_handler.setLevel(logging.WARNING)

    # Create formatters and add it to handlers
    stream_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    stream_handler.setFormatter(stream_format)
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger


logger = my_logger(__name__)


@contextlib.contextmanager
def database():
    url = "mysql+pymysql://root:Olduser@12345@localhost/sp_schema?host=localhost?port=3306"
    engine = create_engine(url)

    yield engine
    engine.dispose()


def db_insert(user):
    with database() as engine:
        try:
            connection = engine.connect()
            metadata = MetaData()
            customer_tbl = Table('customer_tbl', metadata, autoload=True, autoload_with=engine)
            insert_stmt = insert(customer_tbl).values(account_number=user.account['account_number'],
                                                      name=user.account['name'],
                                                      holdings=user.account['holdings'])
            results = connection.execute(insert_stmt)
            try:
                if results.rowcount < 1:
                    raise ValueError("No row inserted")
            except ValueError as ve:
                logger.error('Issue in Insert , no of rows inserted {}'.format(results.rowcount))
            finally:
                connection.close()

        except Exception as e:
            logger.error(e)
            exit(1)


def db_select(name, account_number):
    with database() as engine:
        try:
            connection = engine.connect()
            metadata = MetaData()
            customer_tbl = Table('customer_tbl', metadata, autoload=True, autoload_with=engine)
            stmt = select([customer_tbl])
            stmt = stmt.where(
                and_(customer_tbl.columns.name == name, customer_tbl.columns.account_number == account_number))

            results = connection.execute(stmt).fetchall()
            connection.close()
            return results

        except Exception as e:
            logger.error(e)
            exit(1)


def db_update(account_number, holdings):
    with database() as engine:
        try:
            connection = engine.connect()
            metadata = MetaData()
            customer_tbl = Table('customer_tbl', metadata, autoload=True, autoload_with=engine)
            stmt = update(customer_tbl)
            stmt = stmt.where(customer_tbl.columns.account_number == account_number)
            stmt = stmt.values(holdings=holdings)
            results = connection.execute(stmt)

            try:
                if results.rowcount > 1:
                    raise ValueError("Only 1 row should be updated")
            except ValueError as ve:
                logger.error('Issue in Update , no of rows updated {}'.format(results.rowcount))
            finally:
                connection.close()
        except Exception as e:
            logger.error(e)
            exit(1)
