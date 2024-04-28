"""This is where our app's database models are defined"""

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class Author(db.Model):
    """Model defining an author in our library
        along its personal information and books """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[int] = so.mapped_column(sa.String(100), index=True)
    surname: so.Mapped[int] = so.mapped_column(sa.String(100), index=True)

    book: so.WriteOnlyMapped["Book"] = so.relationship(
        back_populates="author", passive_deletes=True)


class Book(db.Model):
    """Model defining a Book in our library
        along its information and which author it belongs to."""

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    number_of_copies: so.Mapped[int] = so.mapped_column(sa.Integer, index=True)
    author_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Author.id), index=True)

    author: so.Mapped[Author] = so.relationship(back_populates="book")
