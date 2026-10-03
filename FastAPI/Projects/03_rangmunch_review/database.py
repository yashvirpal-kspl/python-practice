from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL =  "sqlite:///rangmanch.db"

engine  = create_engine(DATABASE_URL,echo=True)  #Echo use to print sql query

def create_tables():
    """Create all tables defined by SQLModel class"""
    SQLModel.metadata.create_all(engine)
    
def get_session():
    """ Depenedancy that provide a database session per request """    
    with Session(engine) as session:
        yield session