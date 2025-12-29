from dao.base_dao import BaseDao


class BookDao(BaseDao):

    def get_all_books(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = """
            SELECT b.id, b.title, c.name, b.price, b.condition_status, 
                   GROUP_CONCAT(a.name SEPARATOR ', ') as authors
            FROM books b
            LEFT JOIN categories c ON b.category_id = c.id
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            GROUP BY b.id
            ORDER BY b.id DESC
        """
        cursor.execute(query)
        books = cursor.fetchall()
        cursor.close()
        conn.close()
        return books

    def get_authors_and_categories(self):
        """Pomocná metoda pro naplnění HTML formuláře."""
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
            query_book = """
                INSERT INTO books (title, price, condition_status, category_id, publication_date)
                VALUES (%s, %s, %s, %s, NOW())
            """
            cursor.execute(query_book, (title, price, status, category_id))

            # Získání ID nově vytvořené knihy
            new_book_id = cursor.lastrowid

            query_relation = "INSERT INTO book_authors (book_id, author_id) VALUES (%s, %s)"
            for auth_id in author_ids:
                cursor.execute(query_relation, (new_book_id, auth_id))

            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            print(f"Chyba transakce (Rollback): {e}")
            raise e
        finally:
            cursor.close()
            conn.close()