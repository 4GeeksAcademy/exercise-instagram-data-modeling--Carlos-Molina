import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

from enum import Enum as PyEnum

Base = declarative_base()

class MediaType(PyEnum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(20), nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(30))
    email = Column(String(30), unique=True, nullable=False)
    
    # Relación con Post
    posts = relationship("Post", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "user_name": self.user_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

class Follower(Base):
    __tablename__ = 'follower'
    user_from_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    user_to_id = Column(Integer, ForeignKey(User.id), primary_key=True)

    def to_dict(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    
    # Relación con Media
    media = relationship("Media", back_populates="post")  
    
    # Relación con Comment
    comments = relationship("Comment", back_populates="post")  

    def to_dict(self):
        return {
            "post_id": self.id,
            "user_id": self.user_id
        }

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    type = Column(Enum(MediaType), nullable=False)
    url = Column(String(1500), nullable=False)
    post_id = Column(Integer, ForeignKey(Post.id), nullable=False)

    def to_dict(self):
        return {
            "media_id": self.id,
            "type": self.type.value,  # Usamos el valor del enum
            "url": self.url,
            "post_id": self.post_id
        }

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(500), nullable=False)
    author_id = Column(Integer, ForeignKey(User.id), nullable=False)
    post_id = Column(Integer, ForeignKey(Post.id), nullable=False)

    def to_dict(self):
        return {
            "comment_id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }

# Generación del diagrama
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
