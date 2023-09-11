from datetime import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///library.db"
cors = CORS(app)

db = SQLAlchemy(app)

# Define the Book and Member models
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    authors = db.Column(db.String(255), nullable=False)

    borrowing_members = relationship(
        "Member",
        secondary="member_borrowed_books",
        back_populates="borrowed_books"
    )

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    outstanding_debt = db.Column(db.Float, default=0)

    # Define the many-to-many relationship with the Book model
    borrowed_books = relationship(
        "Book",
        secondary="member_borrowed_books",
        back_populates="borrowing_members"
    )

# Create a new table for the many-to-many relationship
member_borrowed_books = db.Table(
    "member_borrowed_books",
    db.Column("member_id", db.Integer, db.ForeignKey("member.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True)
)

# Create the database tables
with app.app_context():
    db.create_all()


# Endpoint for creating a new book
@app.route("/add-book", methods=["POST"])
def create_book():
    data = request.json
    new_book = Book(
        title=data["title"], authors=data["authors"]
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully"})


# Endpoint for listing all books
@app.route("/books", methods=["GET"])
def list_books():
    books = Book.query.all()
    book_list = [
        {
            "id": book.id,
            "title": book.title,
            "authors": book.authors,
        }
        for book in books
    ]
    return jsonify({"books": book_list})

# Endpoint for updating a book entry
@app.route('/update-book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        data = request.json
        book = Book.query.get(book_id)

        if not book:
            return jsonify({"error": "Book not found"}), 404

        # Update book details based on the data received
        book.title = data.get('title', book.title)
        book.authors = data.get('authors', book.authors)

        db.session.commit()

        return jsonify({"message": "Book updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Endpoint for creating a new member
@app.route("/add-member", methods=["POST"])
def create_member():
    data = request.json
    new_member = Member(name=data["name"])
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"message": "Member added successfully"})


# Custom function to serialize a book
def serialize_book(book):
    return {
        "id": book.id,
        "title": book.title,
        "authors": book.authors,
        # Add other book attributes as needed
    }

# Endpoint for listing all members
@app.route("/members", methods=["GET"])
def list_members():
    members = Member.query.all()
    member_list = []
    for member in members:
        member_data = {
            "id": member.id,
            "name": member.name,
            "outstanding_debt": member.outstanding_debt,
            "borrowed_books": [serialize_book(book) for book in member.borrowed_books],
        }
        member_list.append(member_data)
    return jsonify({"members": member_list})

# Endpoint for updating a member entry
@app.route('/update-member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    try:
        data = request.json
        member = Member.query.get(member_id)

        if not member:
            return jsonify({"error": "Member not found"}), 404

        # Update member details based on the data received
        member.name = data.get('name', member.name)
        member.outstanding_debt = float(data.get('outstanding_debt', member.outstanding_debt))

        db.session.commit()

        return jsonify({"message": "Member updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint for issuing a book to a member
@app.route("/issue-book", methods=["POST"])
def issue_book():
    data = request.json
    member_id_or_name = data.get("member")
    book_id_or_name = data.get("book")

    if not member_id_or_name or not book_id_or_name:
        return jsonify({"error": "Member and/or book information is missing"}), 400

    member = None
    book = None

    # Attempt to find the member by ID
    if isinstance(member_id_or_name, int):
        member = Member.query.get(member_id_or_name)

    # Attempt to find the book by ID
    if isinstance(book_id_or_name, int):
        book = Book.query.get(book_id_or_name)

    # If the member or book wasn't found by ID, attempt to find them by name
    if not member:
        member = Member.query.filter_by(name=member_id_or_name).first()
    if not book:
        book = Book.query.filter_by(title=book_id_or_name).first()

    if not member or not book:
        return jsonify({"error": "Member or book not found"}), 404

    # Check if the member's outstanding debt exceeds Rs. 500
    if member.outstanding_debt > 500:
        return jsonify({"error": "Member has exceeded the outstanding debt limit of Rs. 500. Cannot issue the book"}), 400

    # Check if the member has already borrowed the same book
    if book in member.borrowed_books:
        return jsonify({"error": "Member has already borrowed this book"}), 400

    # Add the borrowed book to the member's list of borrowed books
    member.borrowed_books.append(book)

    db.session.commit()
    return jsonify({"message": "Book issued successfully"})

# Endpoint for returning a book from a member
@app.route("/return-book", methods=["POST"])
def return_book():
    data = request.json
    member_id_or_name = data.get("member")
    book_id_or_name = data.get("book")
    return_date_str = data.get("return_date")

    if not member_id_or_name or not book_id_or_name:
        return jsonify({"error": "Member and/or book information is missing"}), 400

    member = None
    book = None

    # Attempt to find the member by ID
    if isinstance(member_id_or_name, int):
        member = Member.query.get(member_id_or_name)

    # Attempt to find the book by ID
    if isinstance(book_id_or_name, int):
        book = Book.query.get(book_id_or_name)

    # If the member or book wasn't found by ID, attempt to find them by name
    if not member:
        member = Member.query.filter_by(name=member_id_or_name).first()
    if not book:
        book = Book.query.filter_by(title=book_id_or_name).first()

    if not member or not book:
        return jsonify({"error": "Member or book not found"}), 404

    # Check if the member has borrowed this specific book
    if book not in member.borrowed_books:
        return jsonify({"error": "Member has not borrowed this book"}), 400

    try:
        return_date = datetime.strptime(str(return_date_str), "%Y-%m-%d")

        # Get the current date
        current_date = datetime.now()

        # Check if the return date is in the past
        if return_date < current_date:
            return jsonify({"error": "Return date cannot be in the past"}), 400

        # Calculate rental fees if applicable (Rs. 50 per book per day)
        rental_fee = calculate_rental_fee(return_date)

        # Update the member's outstanding debt and book quantity
        member.outstanding_debt += rental_fee

        # Remove the book from the member's borrowed_books array
        member.borrowed_books.remove(book)

        db.session.commit()

        return jsonify({"message": f"Book returned successfully. Rental fee: Rs. {rental_fee}"})

    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400


def calculate_rental_fee(return_date):
    try:
        # Get the current date
        current_date = datetime.now()

        # Calculate the difference in days between return_date and current_date
        delta = return_date - current_date

        # Calculate the rental fee (Rs. 50 per book per day)
        rental_fee = delta.days * 50

        # Ensure the rental fee is non-negative
        if rental_fee < 0:
            return 0

        return rental_fee

    except ValueError:
        # Handle invalid date format
        return 0


# Endpoint for importing books from the Frappe API
@app.route("/import-books", methods=["POST"])
def import_books_from_frappe():
    try:
        data = request.json

        num_books_to_import = data.get(
            "num_books", 20
        )  # Default to 20 books if not specified
        title_filter = data.get("title", "")

        all_imported_books = []

        page = 1

        while len(all_imported_books) < num_books_to_import:
            frappe_api_url = f"https://frappe.io/api/method/frappe-library"
            params = {
                "title": title_filter,
                "page": page,
            }
            response = requests.get(frappe_api_url, params=params)

            if response.status_code == 200:
                books_data = response.json()
                books_to_add = books_data["message"]
                books_to_add_count = len(books_to_add)
                
                if len(all_imported_books) + books_to_add_count <= num_books_to_import:
                    all_imported_books.extend(books_to_add)
                else:
                    # Add only the required number of books to reach num_books_to_import
                    remaining_books_count = num_books_to_import - len(all_imported_books)
                    all_imported_books.extend(books_to_add[:remaining_books_count])
                
                page += 1

                if len(all_imported_books) >= num_books_to_import:
                    break
            else:
                return (
                    jsonify({"error": "Failed to fetch books from the Frappe API."}),
                    500,
                )


        with app.app_context():
            for book_data in all_imported_books:
                new_book = Book(
                    title=book_data["title"], authors=book_data["authors"]
                )
                db.session.add(new_book)
            db.session.commit()

        return jsonify(
            {"message": f"Successfully imported {len(all_imported_books)} books."}
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
