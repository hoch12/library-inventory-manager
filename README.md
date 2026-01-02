# Library Inventory Manager

A professional web application for managing library inventory, loans, and reporting. This project is built using **Python (Flask)** and **MySQL**, demonstrating the implementation of the **DAO (Data Access Object) Design Pattern**, database transactions, and SQL Views.

> **Note:** This project was created as a school assignment satisfying the **D1 (DAO Pattern)** requirement.

## Features

* **Book Management (CRUD):** Add, Edit, Delete, and View books.
* **Complex Data Entry:** Supports **M:N relationships** (assigning multiple authors to a single book) using **Database Transactions** to ensure data integrity.
* **Loan System:**
    * Borrow books (marks book as unavailable).
    * Return books (tracks return date).
    * View active loans.
* **Reporting:** Management dashboard displaying aggregated statistics (Total Inventory Value, Average Price, Count per Category) utilizing **SQL Views**.
* **Data Import:** Bulk import functionality using **JSON** files.
* **Architecture:** Strict separation of concerns using the **DAO Pattern** (`dao/` layer) and **Services** (`services/` layer).

## Technology Stack

* **Backend:** Python 3.9+, Flask
* **Database:** MySQL 8.0+ (Relational)
* **Frontend:** HTML5, Bootstrap 5 (Jinja2 Templates)
* **Architecture:** MVC, DAO Pattern

## Project Structure

    /library-inventory-manager
    │
    ├── /config            # Database configuration (JSON) & Loader
    ├── /dao               # Data Access Objects (Database logic)
    ├── /services          # Business logic (e.g., Import processing)
    ├── /sql               # Database installation scripts (DDL/DML)
    ├── /templates         # HTML Templates (Views)
    ├── /docs              # Documentations
    ├── app.py             # Main application controller
    └── requirements.txt   # Python dependencies

## Installation & Setup

Follow these steps to get the application running on your local machine.

### 1. Prerequisites
* Python 3.9 or higher installed.
* MySQL Server installed and running.

### 2. Clone the Repository

    git clone https://github.com/hoch12/library-inventory-manager.git
    cd library-inventory-manager

### 3. Install Dependencies
It is recommended to use a virtual environment.

    # Create virtual environment
    python -m venv .venv
    
    # Activate it (Windows)
    .venv\Scripts\activate
    
    # Activate it (Mac/Linux)
    source .venv/bin/activate

    # Install libraries
    pip install -r requirements.txt

### 4. Database Setup
Import the provided SQL script to create the database, tables, views, and dummy data.
**Using Terminal:**

    mysql -u root -p < sql/install.sql

*Enter your MySQL root password when prompted.*

### 5. Configuration
Open the file `config/db_config.json` and update it with your MySQL credentials:

    {
      "host": "localhost",
      "user": "root",
      "password": "YOUR_ACTUAL_PASSWORD",
      "database": "library_db"
    }

### 6. Run the Application

    python app.py

The application will start at: `http://127.0.0.1:5000`

## Usage Guide

1.  **Dashboard:** View the list of all books. Borrowed books are marked red.
2.  **Add Book:** Use the form to add a new book. You can select multiple authors by holding `CTRL` (or `CMD` on Mac).
3.  **Loans:** Click **"Borrow"** on any available book to assign it to a reader. Click **"Return"** to mark it as returned.
4.  **Import:** Upload a `.json` file (see `test_import.json` for format) to bulk add books.
5.  **Reports:** Navigate to the "Reports" tab to see automatic statistics generated from the database View.

## License

This project is open-source and available under the [MIT License](LICENSE).
