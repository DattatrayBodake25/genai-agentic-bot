-- mysql/init.sql
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    confirmed BOOLEAN DEFAULT TRUE
);
