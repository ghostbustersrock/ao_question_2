"""This is where the app's endpoints are defined
for the various features implemented in the flask app."""

from flask import jsonify, request
from app import app, db
from app.models import Author, Book
from app.helper_functions import get_all_books, add_new_book, checkout_delete_books, delete_copies_of_book


@app.route("/books", methods=["GET", "POST"])
def books():
    """This endpoint gets all books from the library or
    adds a new one to it."""

    if request.method == "GET":
        return get_all_books()

    book_data = request.json

    return add_new_book(book_data=book_data)


@app.route("/checkout/<int:book_id>", methods=["POST"])
def checkout_book(book_id):
    """This endpoint checks out a book from the library
    using the book's ID."""

    copies_to_checkout = request.json.get(
        "copies", 1
    )
    book = Book.query.get(book_id)

    if not book:
        return jsonify({"ERROR": "Book not found!"}), 404

    return checkout_delete_books(
        book=book,
        copies=copies_to_checkout
    )


@app.route("/return/<int:book_id>", methods=["POST"])
def return_book(book_id):
    """This endpoint returns a number of copies of a book
    to the library, using the book's ID."""

    copies_to_return = request.json.get(
        "copies", 1
    )

    book = Book.query.get(book_id)

    if not book:
        return jsonify({"ERROR": "Book not found!"}), 404

    book.number_of_copies += copies_to_return
    db.session.commit()

    return jsonify(
        {
            "message": f"{copies_to_return} copies of the book returned successfully"
        }
    ), 200


@app.route("/delete_books/<int:book_id>", methods=["DELETE"])
def delete_books(book_id):
    """This endpoint deletes all or a number of copies of a book
    from the library, using the book's ID."""

    data = request.json
    delete_all_copies = data.get("delete_all", False)
    copies_to_delete = data.get("copies_to_delete", None)

    book = Book.query.get(book_id)

    if not book:
        return jsonify({"ERROR": "Book not found!"}), 404

    return delete_copies_of_book(
        book=book,
        delete_all=delete_all_copies,
        copies_to_delete=copies_to_delete
    )


@app.route("/delete_author/<int:author_id>", methods=["DELETE"])
def delete_author(author_id):
    """This endpoint deletes an author and all of its
    related books, from the library, using the author's ID."""

    author = Author.query.get(author_id)

    if not author:
        return jsonify({"ERROR": "Author not found!"}), 404

    books = Book.query.filter_by(author_id=author_id).all()

    for book in books:
        db.session.delete(book)

    db.session.delete(author)
    db.session.commit()

    return jsonify(
        {
            "message": "Author and associated books deleted successfully"
        }
    )
