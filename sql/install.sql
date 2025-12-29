DROP DATABASE IF EXISTS library_db;
CREATE DATABASE library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE library_db;

-- 1. Tabulka kategorií (Bool typ)
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    is_active TINYINT(1) DEFAULT 1
);

-- 2. Tabulka autorů
CREATE TABLE authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- 3. Tabulka knih (Float, Enum, Date typy)
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    condition_status ENUM('new', 'used', 'damaged') NOT NULL,
    publication_date DATE DEFAULT (CURRENT_DATE),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- 4. Vazební tabulka M:N (Kniha <-> Autoři)
CREATE TABLE book_authors (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
);

-- 5. Tabulka výpůjček
CREATE TABLE loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    borrower_name VARCHAR(100),
    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- VIEW 1: Detailní přehled knih (Povinný pohled č. 1)
CREATE VIEW view_book_details AS
SELECT
    b.id,
    b.title,
    c.name AS category_name,
    b.price,
    b.condition_status,
    GROUP_CONCAT(a.name SEPARATOR ', ') AS authors
FROM books b
LEFT JOIN categories c ON b.category_id = c.id
LEFT JOIN book_authors ba ON b.id = ba.book_id
LEFT JOIN authors a ON ba.author_id = a.id
GROUP BY b.id;

-- VIEW 2: Statistiky (Povinný pohled č. 2)
CREATE VIEW view_library_stats AS
SELECT
    c.name AS category_name,
    COUNT(b.id) AS total_books,
    IFNULL(SUM(b.price), 0) AS total_value,
    IFNULL(AVG(b.price), 0) AS avg_price
FROM categories c
LEFT JOIN books b ON c.id = b.category_id
GROUP BY c.id, c.name;

-- Vložení testovacích dat
INSERT INTO categories (name, is_active) VALUES ('Sci-Fi', 1), ('Učebnice', 1), ('Romány', 1);
INSERT INTO authors (name) VALUES ('Karel Čapek'), ('J.K. Rowling'), ('Isaac Asimov');