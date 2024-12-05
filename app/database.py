import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base


os.environ['PGGSSENCMODE'] = 'disable'
engine = create_engine(
    "postgresql://postgres.fqqhfswbaqorcblltgxn:FitLogSSE2425@aws-0-eu-west-2.pooler.supabase.com:6543/postgres"
)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import app.models
    Base.metadata.create_all(bind=engine)