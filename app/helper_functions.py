"""This is where helper functions, performing a specific action in
various endpoints, are implemented"""

from flask import jsonify
from app import db
from app.models import Author, Book


def author_full_name(book):
    """Function returning the author's
    full name in a neatly formatted way."""

    name = book.author.name
    surname = book.author.surname

    return f"{name.capitalize()} {surname.capitalize()}"


def get_all_books():
    """Function to retrieve all books saved
    in the library."""

    books = Book.query.all()

    if not books:
        return {
            "message": "No books are currently available in the library"
        }, 404

    books_data = [
        {
            "book_id": book.id,
            "title": book.title,
            "author": author_full_name(book),
            "number_of_copies": book.number_of_copies
        }
        for book in books
    ]

    return jsonify(books_data), 200


def add_author_and_book(author_data, book_title, book_copies):
    """This function is called when we want to add a new book
    but the author doesn't exist on our database yet. Here a
    new author is first created and then the new book is associated
    to them."""

    new_author = Author(
        name=author_data["name"],
        surname=author_data["surname"]
    )

    db.session.add(new_author)
    db.session.commit()

    book = Book.query.filter_by(title=book_title).first()

    if book:
        book.number_of_copies += book_copies
    else:
        book = Book(
            title=book_title,
            number_of_copies=book_copies,
            author=new_author
        )
        db.session.add(book)

    db.session.commit()

    return jsonify({"message": "Book and author added successfully"}), 201


def add_book_to_existing_author(title, copies, author):
    """This function is called when an author exists
    and we want to associate a new book with them."""

    book = Book.query.filter_by(title=title).first()

    if book:
        book.number_of_copies += copies
    else:
        book = Book(
            title=title,
            number_of_copies=copies,
            author=author
        )
        db.session.add(book)
    db.session.commit()

    return jsonify({"message": "Book added successfully"}), 201


def add_new_book(book_data):
    """Function used to add a new book to our library and
    associating this book to a specific author if they already
    exists in our library, otherwise they are first created and
    then have a new book associated to them."""

    book_title = book_data.get("title")
    book_copies = book_data.get("copies", 1)
    author_data = book_data.get("author")

    if not author_data:
        return jsonify({"ERROR": "Author data is required!"}), 400

    # Checking if the author already exists
    existing_author = Author.query.filter_by(
        name=author_data["name"],
        surname=author_data["surname"]
    ).first()

    if existing_author:
        return add_book_to_existing_author(
            title=book_title,
            copies=book_copies,
            author=existing_author
        )
    else:
        return add_author_and_book(
            author_data=author_data,
            book_title=book_title,
            book_copies=book_copies
        )


def checkout_delete_books(book, copies, action="checkout"):
    """This function mimicks the checking out/deletion process
    of a Library, where a number of copies of a specific
    book are decreased, thus simulating a checkout/deletion process."""

    if action == "checkout":
        success_msg = f"{copies} copies of the book checked out successfully"
        error_msg = "Not enough copies available for checkout!"
    else:
        success_msg = f"{copies} copies of the book deleted successfully"
        error_msg = "Not enough copies available to delete!"

    if book.number_of_copies >= copies:
        book.number_of_copies -= copies
        db.session.commit()
        return jsonify(
            {
                "message": success_msg
            }
        ), 200
    else:
        return jsonify(
            {
                "ERROR": error_msg
            }
        ), 400


def delete_copies_of_book(book, delete_all, copies_to_delete):
    """Function in charge of deleteing all copies of a book
    or only some."""

    if delete_all:
        db.session.delete(book)
        db.session.commit()
        return jsonify(
            {
                "message": "All occurrences of the book deleted successfully"
            }
        ), 200
    elif copies_to_delete is not None and isinstance(copies_to_delete, int):
        return checkout_delete_books(
            book=book,
            copies=copies_to_delete,
            action="delete"
        )
    else:
        return jsonify({"ERROR": "Invalid request!"}), 400
