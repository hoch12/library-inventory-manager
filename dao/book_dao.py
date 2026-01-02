from dao.base_dao import BaseDao


class BookDao(BaseDao):
    """
    Data Access Object for managing Books.
    Handles all database operations related to books, authors, and loans.
    Implements transactions for complex operations.
    """

    def get_all_books(self):
        """
        Retrieves a list of all books from the database.
        Uses the SQL View 'view_book_details' to aggregate data (authors, categories).

        :return: List of tuples representing books.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # Using VIEW instead of complex JOINs to satisfy assignment requirements
        query = """
            SELECT id, title, category_name, price, condition_status, authors, is_borrowed 
            FROM view_book_details 
            ORDER BY id DESC
        """

        cursor.execute(query)
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        return books

    def get_book_by_id(self, book_id):
        """
        Fetches a single book record by its ID, including associated authors.
        Used for pre-filling the Edit form.

        :param book_id: ID of the book to retrieve.
        :return: Tuple (book_data, list_of_author_ids)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()

        cursor.execute("SELECT author_id FROM book_authors WHERE book_id = %s", (book_id,))
        author_ids = [row[0] for row in cursor.fetchall()]

        cursor.close()
        conn.close()
        return book, author_ids

    def get_authors_and_categories(self):
        """
        Helper method to fetch all available authors and categories.
        Used to populate dropdown menus in forms.

        :return: Tuple (authors_list, categories_list)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM authors")
        authors = cursor.fetchall()
        cursor.execute("SELECT id, name FROM categories WHERE is_active = 1")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()
        return authors, categories

    def add_book_transaction(self, title, price, status, category_id, author_ids):
        """
        Inserts a new book and its authors using a DATABASE TRANSACTION.
        Ensures that both the book and the M:N relationships are saved, or neither.

        :param title: Book title
        :param price: Book price
        :param status: Condition (new/used/damaged)
        :param category_id: Foreign key to Category
        :param author_ids: List of author IDs (M:N relation)
        :return: True if successful
        :raises: Exception if transaction fails
        """
        conn = self.get_connection()
        conn.autocommit = False  # Start Transaction
        cursor = conn.cursor()

        try:
            # 1. Insert Book
            query_book = "INSERT INTO books (title, price, condition_status, category_id, publication_date) VALUES (%s, %s, %s, %s, NOW())"
            cursor.execute(query_book, (title, price, status, category_id))

            # Get the ID of the newly created book
            new_book_id = cursor.lastrowid

            # 2. Insert Author Relations (M:N)
            query_relation = "INSERT INTO book_authors (book_id, author_id) VALUES (%s, %s)"
            for auth_id in author_ids:
                cursor.execute(query_relation, (new_book_id, auth_id))

            conn.commit()  # Commit Transaction
            return True

        except Exception as e:
            conn.rollback()  # Rollback on error
            raise e
        finally:
            cursor.close()
            conn.close()

    def update_book(self, book_id, title, price, status, category_id, author_ids):
        """
        Updates an existing book record and its authors within a transaction.
        First deletes old author relations, then inserts new ones.
        """
        conn = self.get_connection()
        conn.autocommit = False
        cursor = conn.cursor()
        try:
            query = "UPDATE books SET title=%s, price=%s, condition_status=%s, category_id=%s WHERE id=%s"
            cursor.execute(query, (title, price, status, category_id, book_id))

            # Update M:N relations (Delete old -> Insert new)
            cursor.execute("DELETE FROM book_authors WHERE book_id = %s", (book_id,))
            for auth_id in author_ids:
                cursor.execute("INSERT INTO book_authors (book_id, author_id) VALUES (%s, %s)", (book_id, auth_id))

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def delete_book(self, book_id):
        """
        Deletes a book. Due to 'ON DELETE CASCADE' in MySQL,
        this also removes related records in book_authors.
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))
            conn.commit()
            return True
        except Exception as e:
            return False
        finally:
            cursor.close()
            conn.close()

    def create_loan(self, book_id, borrower_name):
        """
        Creates a new loan record and marks the book as borrowed.
        Uses transaction to keep data consistent.
        """
        conn = self.get_connection()
        conn.autocommit = False
        cursor = conn.cursor()
        try:
            # 1. Create Loan Record
            query_loan = "INSERT INTO loans (book_id, borrower_name, loan_date) VALUES (%s, %s, NOW())"
            cursor.execute(query_loan, (book_id, borrower_name))

            # 2. Lock the book (Update is_borrowed flag)
            cursor.execute("UPDATE books SET is_borrowed = 1 WHERE id = %s", (book_id,))

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def return_book(self, book_id):
        """
        Marks a loan as returned and makes the book available again.
        """
        conn = self.get_connection()
        conn.autocommit = False
        cursor = conn.cursor()
        try:
            # 1. Update Loan (set returned_date)
            query_loan = "UPDATE loans SET returned_date = NOW() WHERE book_id = %s AND returned_date IS NULL"
            cursor.execute(query_loan, (book_id,))

            # 2. Unlock the book
            cursor.execute("UPDATE books SET is_borrowed = 0 WHERE id = %s", (book_id,))

            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_active_loans(self):
        """
        Retrieves a list of all currently active loans (where returned_date is NULL).
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT l.id, b.title, l.borrower_name, l.loan_date, b.id
            FROM loans l
            JOIN books b ON l.book_id = b.id
            WHERE l.returned_date IS NULL
            ORDER BY l.loan_date DESC
        """
        cursor.execute(query)
        loans = cursor.fetchall()
        cursor.close()
        conn.close()
        return loans