CREATE DATABASE library;
USE library;

DROP VIEW IF EXISTS view_active_books;
DROP VIEW IF EXISTS view_overdue_loans;
DROP TABLE IF EXISTS loans;
DROP TABLE IF EXISTS book_author;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS categories;

CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL UNIQUE,
    label VARCHAR(50) NOT NULL,
    is_active TINYINT(1) DEFAULT 1
);

CREATE TABLE authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    birth_year INT
);

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    category_id INT NOT NULL,
    price FLOAT NOT NULL,
    condition_status ENUM('new', 'used', 'damaged') NOT NULL,
    publication_date DATE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
);

CREATE TABLE book_author (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
);

CREATE TABLE loans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    borrower_name VARCHAR(100) NOT NULL,
    borrowed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    returned_at DATETIME NULL,
    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE RESTRICT
);

CREATE VIEW view_active_books AS
SELECT b.id, b.title, c.label AS category, b.price
FROM books b
JOIN categories c ON b.category_id = c.id
WHERE c.is_active = 1;

CREATE VIEW view_overdue_loans AS
SELECT l.id, l.borrower_name, b.title, l.borrowed_at
FROM loans l
JOIN books b ON l.book_id = b.id
WHERE l.returned_at IS NULL;

INSERT INTO categories (code, label, is_active) VALUES
('SCI-FI', 'Science Fiction', 1),
('ROM', 'Romány', 1),
('EDU', 'Učebnice', 1),
('OLD', 'Vyřazené', 0);

INSERT INTO authors (name, birth_year) VALUES
('Karel Čapek', 1890),
('Isaac Asimov', 1920),
('J.K. Rowling', 1965);

INSERT INTO books (title, category_id, price, condition_status, publication_date) VALUES
('R.U.R.', 1, 150.50, 'used', '1920-01-01'),
('Válka s Mloky', 1, 200.00, 'new', '1936-01-01'),
('Harry Potter 1', 2, 499.90, 'damaged', '1997-06-26'),
('Matematika pro SŠ', 3, 350.00, 'new', '2015-09-01');

INSERT INTO book_author (book_id, author_id) VALUES
(1, 1), -- RUR - Čapek
(2, 1), -- Mloky - Čapek
(3, 3); -- Harry Potter - Rowling

INSERT INTO loans (book_id, borrower_name, borrowed_at) VALUES
(1, 'Jan Novák', NOW());