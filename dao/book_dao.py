from dao.base_dao import BaseDao


class BookDao(BaseDao):

    def get_all_books(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = "SELECT b.id, b.title, c.name, b.price, b.condition_status, GROUP_CONCAT(a.name SEPARATOR ', ') as authors FROM books b LEFT JOIN categories c ON b.category_id = c.id LEFT JOIN book_authors ba ON b.id = ba.book_id LEFT JOIN authors a ON ba.author_id = a.id GROUP BY b.id ORDER BY b.id DESC"
        cursor.execute(query)
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        return books

    def get_book_by_id(self, book_id):
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
        conn = self.get_connection()
        conn.autocommit = False
        cursor = conn.cursor()

        try:
            query_book = "INSERT INTO books (title, price, condition_status, category_id, publication_date) VALUES (%s, %s, %s, %s, NOW())"
            cursor.execute(query_book, (title, price, status, category_id))

            new_book_id = cursor.lastrowid

            query_relation = "INSERT INTO book_authors (book_id, author_id) VALUES (%s, %s)"
            for auth_id in author_ids:
                cursor.execute(query_relation, (new_book_id, auth_id))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def update_book(self, book_id, title, price, status, category_id, author_ids):
        conn = self.get_connection()
        conn.autocommit = False
        cursor = conn.cursor()
        try:
            query = "UPDATE books SET title=%s, price=%s, condition_status=%s, category_id=%s WHERE id=%s"
            cursor.execute(query, (title, price, status, category_id, book_id))

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
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO loans (book_id, borrower_name, loan_date) VALUES (%s, %s, NOW())"
            cursor.execute(query, (book_id, borrower_name))
            conn.commit()
            return True
        except Exception as e:
            return False
        finally:
            cursor.close()
            conn.close()