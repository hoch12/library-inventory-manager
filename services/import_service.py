import json
from dao.book_dao import BookDao


class ImportService:
    def __init__(self):
        self.book_dao = BookDao()

    def process_json(self, file_storage):
        """Načte JSON soubor a vloží knihy přes transakci."""
        try:
            data = json.load(file_storage)

            if not isinstance(data, list):
                raise ValueError("JSON soubor musí obsahovat seznam (pole) objektů.")

            count = 0
            for item in data:
                if 'title' in item and 'price' in item:
                    authors = item.get('authors', [1])
                    cat_id = item.get('category_id', 1)

                    self.book_dao.add_book_transaction(
                        item['title'],
                        item['price'],
                        'new',
                        cat_id,
                        authors
                    )
                    count += 1
            return count

        except Exception as e:
            print(f"Chyba ve službě importu: {e}")
            raise