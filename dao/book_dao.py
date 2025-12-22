import mysql.connector
from config.db_config import db_config

class BookDao:
    """
    Data Access Object for managing Book-related database operations.
    """

    def __init__(self):
        # We don't open the connection in __init__ to avoid keeping it open unnecessarily
        pass

    def _get_connection(self):
        """Helper method to establish a database connection."""
        return mysql.connector.connect(**db_config)

    def get_all_books(self):
        """
        Retrieves all books from the database.
        Returns: A list of tuples containing book details.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # We select specific columns to keep it clean
        query = "SELECT id, title, price, condition_status FROM books"
        cursor.execute(query)
        books = cursor.fetchall()

        cursor.close()
        conn.close()
        return books

    def add_book(self, title, category_id, price, condition, pub_date):
        """
        Inserts a new book into the database.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        query = """
        INSERT INTO books (title, category_id, price, condition_status, publication_date)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (title, category_id, price, condition, pub_date)

        try:
            cursor.execute(query, values)
            conn.commit()  # Commit is crucial for saving changes
            print("(DAO): Book saved successfully.")
        except mysql.connector.Error as err:
            print(f"(DAO): Error while saving book: {err}")
        finally:
            cursor.close()
            conn.close()