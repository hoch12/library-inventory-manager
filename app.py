from flask import Flask, render_template, request, redirect, flash
from dao.book_dao import BookDao
from dao.report_dao import ReportDao
from services.import_service import ImportService

app = Flask(__name__)
app.secret_key = "super_tajny_klic_pro_session"

# Inicializace instancí
book_dao = BookDao()
report_dao = ReportDao()
import_service = ImportService()


@app.route('/')
def index():
    try:
        books = book_dao.get_all_books()
        return render_template('index.html', books=books)
    except Exception as e:
        return f"Kritická chyba aplikace: {e}"


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

            flash("Kniha byla úspěšně uložena.", "success")
            return redirect('/')

        except ValueError:
            flash("Chyba: Cena musí být číslo!", "danger")
        except Exception as e:
            flash(f"Chyba při ukládání: {e}", "danger")

    authors, categories = book_dao.get_authors_and_categories()
    return render_template('add_book.html', authors=authors, categories=categories)


@app.route('/report')
def report():
    try:
        stats = report_dao.get_stats()
        return render_template('report.html', stats=stats)
    except Exception as e:
        flash(f"Nepodařilo se načíst report: {e}", "danger")
        return redirect('/')


@app.route('/import', methods=['GET', 'POST'])
def import_data():
    if request.method == 'POST':
        # Kontrola, zda byl nahrán soubor
        if 'file' not in request.files:
            flash("Nebyl vybrán žádný soubor.", "warning")
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash("Název souboru je prázdný.", "warning")
            return redirect(request.url)

        try:
            # Volání služby pro zpracování
            count = import_service.process_json(file)
            flash(f"Úspěšně importováno {count} knih.", "success")
        except Exception as e:
            flash(f"Import selhal: {e}", "danger")

    return render_template('import.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)