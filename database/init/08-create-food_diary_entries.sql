CREATE TABLE IF NOT EXISTS food_diary_entries (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    diary_date DATE,
    entry_time TIME,
    meal_type_id INT,
    hunger_level ENUM('Not at all', 'Slightly', 'Moderately', 'Very', 'Extremely'),
    food_consumed TEXT,
    quantity VARCHAR(255),
    feeling ENUM('Excellent', 'Good', 'Neutral', 'Poor', 'Very Poor'),
    feeling_details TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (meal_type_id) REFERENCES meal_types(meal_type_id)
);
