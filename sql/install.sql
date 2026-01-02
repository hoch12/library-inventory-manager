SET FOREIGN_KEY_CHECKS = 0;

DROP DATABASE IF EXISTS library_db;
CREATE DATABASE library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE library_db;

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    is_active TINYINT(1) DEFAULT 1
);

CREATE TABLE authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL,
    condition_status ENUM('new', 'used', 'damaged') NOT NULL,
    publication_date DATE DEFAULT (CURRENT_DATE),
    category_id INT,
    is_borrowed TINYINT(1) DEFAULT 0,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE book_authors (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
);

CREATE TABLE loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    borrower_name VARCHAR(100),
    loan_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    returned_date DATETIME NULL,
    FOREIGN KEY (book_id) REFERENCES books(id)
);

CREATE VIEW view_book_details AS
SELECT
    b.id, b.title, c.name AS category_name, b.price, b.condition_status, b.is_borrowed,
    GROUP_CONCAT(a.name SEPARATOR ', ') AS authors
FROM books b
LEFT JOIN categories c ON b.category_id = c.id
LEFT JOIN book_authors ba ON b.id = ba.book_id
LEFT JOIN authors a ON ba.author_id = a.id
GROUP BY b.id;

CREATE VIEW view_library_stats AS
SELECT
    c.name AS category_name,
    COUNT(b.id) AS total_books,
    IFNULL(SUM(b.price), 0) AS total_value,
    IFNULL(AVG(b.price), 0) AS avg_price
FROM categories c
LEFT JOIN books b ON c.id = b.category_id
GROUP BY c.id, c.name;


INSERT INTO categories (name, is_active) VALUES
('Sci-Fi', 1),
('Učebnice', 1),
('Romány', 1);

INSERT INTO authors (name) VALUES
('Karel Čapek'),
('J.K. Rowling'),
('Isaac Asimov');

INSERT INTO books (title, price, condition_status, publication_date, category_id) VALUES
('Válka s Mloky', 250.0, 'new', '1936-01-01', 1),
('R.U.R.', 199.0, 'used', '1920-01-01', 1),
('Harry Potter a Kámen mudrců', 499.0, 'used', '1997-06-26', 3),
('Matematika pro Gymnázia', 150.0, 'damaged', '2010-09-01', 2);

INSERT INTO book_authors (book_id, author_id) VALUES
(1, 1),
(2, 1),
(3, 2),
(4, 3);

SET FOREIGN_KEY_CHECKS = 1;