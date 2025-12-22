from dao.book_dao import BookDao

# Initialize our data access object
book_manager = BookDao()


def list_books():
    """Fetches and displays all books using the DAO."""
    print("\n--- BOOK LIST ---")
    books = book_manager.get_all_books()

    if not books:
        print("No books found in the library.")
        return

    for book in books:
        # book[0]=id, book[1]=title, book[2]=price, book[3]=condition
        print(f"[{book[0]}] {book[1]} | ${book[2]} | Condition: {book[3]}")


def add_new_book():
    """Collects user input and uses DAO to save a new book."""
    print("\n--- ADD NEW BOOK ---")
    title = input("Enter title: ")

    # Simple validation to prevent crashing if user enters text instead of number
    try:
        price = float(input("Enter price (e.g., 19.99): "))
    except ValueError:
        print("Invalid price format. Operation cancelled.")
        return

    condition = input("Enter condition (new/used/damaged): ")

    # Hardcoded values for now (we can improve this later)
    category_id = 1
    default_date = "2025-01-01"

    # Call the DAO to save the data
    book_manager.add_book(title, category_id, price, condition, default_date)


# --- Main Application Loop ---
if __name__ == "__main__":
    while True:
        print("\n=== LIBRARY MENU ===")
        print("1. List all books")
        print("2. Add a new book")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            list_books()
        elif choice == "2":
            add_new_book()
        elif choice == "0":
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")