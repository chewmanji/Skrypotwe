from init_db import engine
from sqlalchemy import MetaData


metadata = MetaData()
metadata.reflect(bind=engine)
with engine.begin() as conn:
    conn.execute(metadata.tables["students_classes"].delete())
