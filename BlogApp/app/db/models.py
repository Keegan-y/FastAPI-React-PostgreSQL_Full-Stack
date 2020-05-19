from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import sys

sys.path.append("..")
from db.dbconf import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    # posts = relationship('Post', backref='author', lazy=True)

    posts = relationship("Post", back_populates="owner")

    def __repr__(self):
        return f"User('{self.email}','{self.name}')"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    post = Column(Text, nullable=False)
    post_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    owner = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"Post('{self.title}','{self.post}','{self.post_date}')"
