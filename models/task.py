from sqlalchemy import Column, Integer, String, Boolean
from conn.connection import Base, engine


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True)
    complete = Column(Boolean, unique=False, default=False)

    def __init__(self, title):
        self.title = title


Base.metadata.create_all(bind=engine)
