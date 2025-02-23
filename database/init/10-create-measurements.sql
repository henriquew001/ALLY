CREATE TABLE IF NOT EXISTS measurements (
    measurement_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    measurement_datetime DATETIME,
    weight DECIMAL(5, 2),
    abdominal_circumference DECIMAL(5, 2),
    arms DECIMAL(5, 2),
    calves DECIMAL(5, 2),
    hips DECIMAL(5, 2),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
