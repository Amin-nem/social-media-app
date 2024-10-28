from .database import Base
from sqlalchemy import  Column,Integer,String, Boolean, TIMESTAMP
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,nullable=True,server_default='true')
    creted_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('NOW()'))