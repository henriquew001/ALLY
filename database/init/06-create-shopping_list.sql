CREATE TABLE IF NOT EXISTS shopping_list (
    shopping_list_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    meal_id INT,
    item_date DATE,
    quantity DECIMAL(10, 2),
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
);
