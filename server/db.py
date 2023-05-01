import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv
load_dotenv()

DB_CONNECTION = os.getenv('DB_CONNECTION')

db_string = "postgresql://postgres:test@localhost:5432/test"

dbEngine = create_engine(DB_CONNECTION, isolation_level = "REPEATABLE READ")

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=dbEngine))
