import contextlib
import mysql.connector
from sqlalchemy import create_engine, insert, Table, MetaData, select, and_, update
import pymysql

logger = Logger(__name__)
logger.info("hello")


@contextlib.contextmanager
def database():
    engine = create_engine("mysql+pymysql://root:Olduser@12345@localhost/sp_schema?host=localhost?port=3306")

    yield engine
    engine.dispose()


def db_select(name, account_number):
    with database() as engine:
        connection = engine.connect()
        metadata = MetaData()
        customer_tbl = Table('customer_tbl', metadata, autoload=True, autoload_with=engine)
        stmt = select([customer_tbl])
        stmt = stmt.where(
            and_(customer_tbl.columns.name == name, customer_tbl.columns.account_number == account_number))
        results = connection.execute(stmt).fetchall()
        connection.close()
        return results


res = db_select('Eshaan', 22370)
for i in res:
    print(i.name)
