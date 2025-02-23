CREATE TABLE IF NOT EXISTS meals (
    meal_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    meal_type_id INT,
    meal_date DATE,
    meal_time TIME,
    description TEXT,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (meal_type_id) REFERENCES meal_types(meal_type_id)
);
