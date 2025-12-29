from flask import Flask, render_template, request, redirect, flash
from dao.book_dao import BookDao
from dao.report_dao import ReportDao
from services.import_service import ImportService

app = Flask(__name__)
app.secret_key = "secret_key_for_session"

book_dao = BookDao()
report_dao = ReportDao()
import_service = ImportService()


@app.route('/')
def index():
    try:
        books = book_dao.get_all_books()
        return render_template('index.html', books=books)
    except Exception as e:
        return f"Database Error: {e}"


@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        try:
            title = request.form['title']
            price = float(request.form['price'])
            status = request.form['status']
            category_id = int(request.form['category_id'])
            author_ids = request.form.getlist('authors')

            book_dao.add_book_transaction(title, price, status, category_id, author_ids)

            flash("Book added successfully.", "success")
            return redirect('/')

        except ValueError:
            flash("Error: Price must be a number.", "danger")
        except Exception as e:
            flash(f"Error saving book: {e}", "danger")

    authors, categories = book_dao.get_authors_and_categories()
    return render_template('add_book.html', authors=authors, categories=categories)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
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

    book, current_authors = book_dao.get_book_by_id(id)
    all_authors, categories = book_dao.get_authors_and_categories()
    return render_template('edit_book.html', book=book, current_authors=current_authors, authors=all_authors,
                           categories=categories)


@app.route('/delete/<int:id>')
def delete_book(id):
    try:
        book_dao.delete_book(id)
        flash("Book deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting book: {e}", "danger")
    return redirect('/')


@app.route('/borrow/<int:id>', methods=['GET', 'POST'])
def borrow_book(id):
    if request.method == 'POST':
        borrower = request.form['borrower_name']
        if book_dao.create_loan(id, borrower):
            flash(f"Book borrowed to {borrower}.", "success")
        else:
            flash("Error creating loan.", "danger")
        return redirect('/')

    book, _ = book_dao.get_book_by_id(id)
    return render_template('borrow.html', book=book)


@app.route('/report')
def report():
    try:
        stats = report_dao.get_stats()
        return render_template('report.html', stats=stats)
    except Exception as e:
        flash(f"Could not load report: {e}", "danger")
        return redirect('/')


@app.route('/import', methods=['GET', 'POST'])
def import_data():
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
    app.run(debug=True, port=5000)