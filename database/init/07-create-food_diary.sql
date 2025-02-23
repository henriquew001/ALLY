CREATE TABLE IF NOT EXISTS food_diary (
    diary_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    meal_type_id INT,
    diary_date DATE,
    diary_time TIME,
    notes TEXT,
    feeling ENUM('Excellent', 'Good', 'Neutral', 'Poor', 'Very Poor'),
    feeling_details TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (meal_type_id) REFERENCES meal_types(meal_type_id)
);
