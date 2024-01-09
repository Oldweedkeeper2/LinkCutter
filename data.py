from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

Base = declarative_base()

db = SQLAlchemy(model_class=Base)


class Link(db.Model):
    __tablename__ = 'links'
    cute_link = db.Column(db.String, primary_key=True, index=True)
    link = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=db.func.now())
