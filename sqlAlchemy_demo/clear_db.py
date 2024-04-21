from init_db import engine
from sqlalchemy import MetaData


metadata = MetaData()
metadata.reflect(bind=engine)
with engine.begin() as conn:
    for table in metadata.sorted_tables:
        conn.execute(table.delete())
