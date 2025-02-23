CREATE TABLE IF NOT EXISTS meal_types (
    meal_type_id INT AUTO_INCREMENT PRIMARY KEY,
    meal_type_name VARCHAR(255) UNIQUE NOT NULL
);

INSERT INTO meal_types (meal_type_name) VALUES
('Breakfast'),
('Brunch'),
('Lunch'),
('Dinner'),
('Snack'),
('Dessert'),
('Pre-workout Meal'),
('Post-workout Meal'),
('Midnight Snack');
