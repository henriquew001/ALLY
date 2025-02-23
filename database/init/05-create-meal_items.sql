CREATE TABLE IF NOT EXISTS meal_items (
    meal_item_id INT AUTO_INCREMENT PRIMARY KEY,
    meal_id INT,
    food_item_id INT,
    quantity DECIMAL(10, 2),
    FOREIGN KEY (meal_id) REFERENCES meals(meal_id),
    FOREIGN KEY (food_item_id) REFERENCES food_items(food_item_id)
);
