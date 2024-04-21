from sqlalchemy import create_engine
from models import Base


# engine - responsible for connecting to DB and executing sQL commands
# dialect - responsbile for "translating" sqlalchemy code to the specific db
# create_engine(connection_string)

# template
"dialect+driver://username:password@host:port/database"

# PostgreSQL
"postgresql+psycopg2://scott:tiger@localhost/mydatabase"

# MySQL
"mysql://scott:tiger@localhost/foo"

# Oracle
"oracle+cx_oracle://scott:tiger@tnsname"

# MS SQL
"mssql+pyodbc://scott:tiger@mydsn"

# SQLite
"sqlite://<nohostname>/<path>"

conn_string = "sqlite:///test.db"
engine = create_engine(conn_string, echo=True)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print(f"{__name__} was run")
