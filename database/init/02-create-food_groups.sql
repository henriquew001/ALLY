CREATE TABLE IF NOT EXISTS food_groups (
    food_group_id INT AUTO_INCREMENT PRIMARY KEY,
    food_group_name VARCHAR(255) UNIQUE NOT NULL
);

INSERT INTO food_groups (food_group_name) VALUES
('Cereals and Tubers'),
('Vegetables'),
('Fruits'),
('Beans'),
('Dairy'),
('Meats, Eggs, and Vegetable Proteins'),
('Oils and Fats'),
('Sugars and Sweets');
