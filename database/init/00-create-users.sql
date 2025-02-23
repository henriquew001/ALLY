CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Store password as a hash!
    email VARCHAR(255) UNIQUE NOT NULL,
    role ENUM('basic', 'premium', 'professional', 'admin') NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    date_of_birth DATE,
    height INT,
    weight INT,
    goals TEXT,
    activation_code VARCHAR(255),
    activated BOOLEAN DEFAULT FALSE
);
