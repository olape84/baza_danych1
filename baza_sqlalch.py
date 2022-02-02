import sqlalchemy

print(sqlalchemy.__version__)

from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db')

print(engine.driver)

print(engine.table_names())

print(engine.execute("SELECT * FROM tasks"))

results = engine.execute("SELECT * FROM tasks")

for r in results:
   print(r)

# sqlalchemy_ex_02.py
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database.db')

meta = MetaData()

students = Table(
   'students', meta,
   Column('id', Integer, primary_key=True),
   Column('name', String),
   Column('lastname', String),
)

meta.create_all(engine)
print(engine.table_names())

engine = create_engine('sqlite:///database.db', echo=True)
