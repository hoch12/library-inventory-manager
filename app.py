from flask import Flask, render_template, request, redirect, flash
from dao.book_dao import BookDao
from dao.report_dao import ReportDao
from services.import_service import ImportService

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "secret_key_for_session"

# Initialize Data Access Objects and Services
book_dao = BookDao()
report_dao = ReportDao()
import_service = ImportService()


@app.route('/')
def index():
    """
    Main Dashboard Route.
    Fetches the list of all books using the BookDao and renders the index page.

    :return: Rendered HTML template 'index.html' with books data.
    """
    try:
        books = book_dao.get_all_books()
        return render_template('index.html', books=books)
    except Exception as e:
        return f"Database Error: {e}"


@app.route('/loans')
def loans():
    """
    Active Loans Route.
    Displays a list of books that are currently borrowed and not yet returned.

    :return: Rendered HTML template 'loans.html'.
    """
    try:
        active_loans = book_dao.get_active_loans()
        return render_template('loans.html', loans=active_loans)
    except Exception as e:
        flash(f"Error loading loans: {e}", "danger")
        return redirect('/')


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    """
    Add Book Route.
    GET: Displays the form to add a new book (fetches authors/categories for dropdowns).
    POST: Processes the form data and saves the new book to the database using a transaction.
    """
    if request.method == 'POST':
        try:
            title = request.form['title']
            price = float(request.form['price'])
            status = request.form['status']
            category_id = int(request.form['category_id'])
            # Get list of selected authors (M:N relationship)
            author_ids = request.form.getlist('authors')

            book_dao.add_book_transaction(title, price, status, category_id, author_ids)

            flash("Book added successfully.", "success")
            return redirect('/')

        except ValueError:
            flash("Error: Price must be a number.", "danger")
        except Exception as e:
            flash(f"Error saving book: {e}", "danger")

    # For GET request: Load data for dropdowns
    authors, categories = book_dao.get_authors_and_categories()
    return render_template('add_book.html', authors=authors, categories=categories)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    """
    Edit Book Route.
    GET: Pre-fills the form with existing data for the book with the given ID.
    POST: Updates the book details and its author relationships.

    :param id: ID of the book to edit.
    """
    if request.method == 'POST':
        try:
            title = request.form['title']
            price = float(request.form['price'])
            status = request.form['status']
            category_id = int(request.form['category_id'])
            author_ids = request.form.getlist('authors')

            book_dao.update_book(id, title, price, status, category_id, author_ids)
            flash("Book updated successfully.", "success")
            return redirect('/')
        except Exception as e:
            flash(f"Error updating book: {e}", "danger")

    # For GET request: Load book data + dropdowns
    book, current_authors = book_dao.get_book_by_id(id)
    all_authors, categories = book_dao.get_authors_and_categories()
    return render_template('edit_book.html', book=book, current_authors=current_authors, authors=all_authors,
                           categories=categories)


@app.route('/delete/<int:id>')
def delete_book(id):
    """
    Delete Book Route.
    Removes a book from the database. Linked records in 'book_authors'
    are removed automatically via CASCADE.
    """
    try:
        book_dao.delete_book(id)
        flash("Book deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting book: {e}", "danger")
    return redirect('/')


@app.route('/borrow/<int:id>', methods=['GET', 'POST'])
def borrow_book(id):
    """
    Borrow Book Route.
    GET: Displays the form to enter borrower's name.
    POST: Creates a new loan record and marks the book as borrowed (unavailable).
    """
    if request.method == 'POST':
        borrower = request.form['borrower_name']
        if book_dao.create_loan(id, borrower):
            flash(f"Book borrowed to {borrower}.", "success")
        else:
            flash("Error creating loan.", "danger")
        return redirect('/')

    book, _ = book_dao.get_book_by_id(id)
    return render_template('borrow.html', book=book)


@app.route('/return/<int:id>')
def return_book(id):
    """
    Return Book Route.
    Marks an active loan as returned and sets the book status back to available.
    """
    if book_dao.return_book(id):
        flash("Book returned successfully.", "success")
    else:
        flash("Error returning book.", "danger")
    return redirect('/')


@app.route('/report')
def report():
    """
    Reporting Route.
    Displays aggregated statistics (using SQL View) about the library inventory.
    """
    try:
        stats = report_dao.get_stats()
        return render_template('report.html', stats=stats)
    except Exception as e:
        flash(f"Could not load report: {e}", "danger")
        return redirect('/')


@app.route('/import', methods=['GET', 'POST'])
def import_data():
    """
    Data Import Route.
    Allows users to upload a JSON file to bulk insert books into the database.
    Delegates processing to ImportService.
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file selected.", "warning")
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash("Filename is empty.", "warning")
            return redirect(request.url)

        try:
            count = import_service.process_json(file)
            flash(f"Successfully imported {count} books.", "success")
        except Exception as e:
            flash(f"Import failed: {e}", "danger")

    return render_template('import.html')


if __name__ == '__main__':
    # Run the application in debug mode for development
    app.run(debug=True, port=5000)