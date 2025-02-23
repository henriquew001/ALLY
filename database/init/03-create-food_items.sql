CREATE TABLE IF NOT EXISTS food_items (
    food_item_id INT AUTO_INCREMENT PRIMARY KEY,
    food_group_id INT,
    food_item_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (food_group_id) REFERENCES food_groups(food_group_id)
);

INSERT INTO food_items (food_group_id, food_item_name) VALUES
-- Cereals and Tubers
(1, 'Rice'),
(1, 'Potatoes'),
(1, 'Bread'),
(1, 'Oats'),
(1, 'Corn'),
(1, 'Quinoa'),

-- Vegetables
(2, 'Carrots'),
(2, 'Broccoli'),
(2, 'Spinach'),
(2, 'Tomatoes'),
(2, 'Lettuce'),
(2, 'Onions'),
(2, 'Bell peppers'),
(2, 'Cucumbers'),

-- Fruits
(3, 'Apples'),
(3, 'Bananas'),
(3, 'Oranges'),
(3, 'Grapes'),
(3, 'Strawberries'),
(3, 'Blueberries'),

-- Beans
(4, 'Black beans'),
(4, 'Lentils'),
(4, 'Chickpeas'),
(4, 'Kidney beans'),

-- Dairy
(5, 'Milk'),
(5, 'Yogurt'),
(5, 'Cheese'),

-- Meats, Eggs, and Vegetable Proteins
(6, 'Chicken'),
(6, 'Beef'),
(6, 'Fish'),
(6, 'Eggs'),
(6, 'Tofu'),
(6, 'Almonds'),
(6, 'Walnuts'),
(6, 'Chia seeds'),

-- Oils and Fats
(7, 'Olive oil'),
(7, 'Avocado oil'),
(7, 'Butter'),

-- Sugars and Sweets
(8, 'Sugar'),
(8, 'Honey'),
(8, 'Chocolate'),
(8, 'Candy');
