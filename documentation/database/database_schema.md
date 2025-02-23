# Database Schema for ConsciousFit

This document outlines the database schema for the ConsciousFit application.

## Tables

### `users`

Stores user account information.

| Column             | Type             | Constraints          | Description                                 |
|--------------------|------------------|----------------------|---------------------------------------------|
| `user_id`          | INT              | AUTO_INCREMENT, PRIMARY KEY | Unique identifier for the user.             |
| `username`         | VARCHAR(255)     | UNIQUE, NOT NULL     | User's username.                             |
| `password`         | VARCHAR(255)     | NOT NULL             | User's hashed password.                     |
| `email`            | VARCHAR(255)     | UNIQUE, NOT NULL     | User's email address.                     |
| `role`             | ENUM('basic', 'premium', 'professional', 'admin') | NOT NULL             | User's role (basic, premium, professional, admin). |
| `first_name`       | VARCHAR(255)     |                      | User's first name.                          |
| `last_name`        | VARCHAR(255)     |                      | User's last name.                           |
| `date_of_birth`    | DATE             |                      | User's date of birth.                      |
| `height`           | INT              |                      | User's height (in cm or inches).            |
| `weight`           | INT              |                      | User's weight (in kg or lbs).              |
| `goals`            | TEXT             |                      | User's fitness goals.                       |
| `activation_code`  | VARCHAR(255)     |                      | User's account activation code.           |
| `activated`        | BOOLEAN          | DEFAULT FALSE        | Indicates if the user's account is activated. |

### `meal_types`

Stores predefined meal types.

| Column             | Type             | Constraints          | Description                                 |
|--------------------|------------------|----------------------|---------------------------------------------|
| `meal_type_id`     | INT              | AUTO_INCREMENT, PRIMARY KEY | Unique identifier for the meal type.        |
| `meal_type_name`   | VARCHAR(255)     | UNIQUE, NOT NULL     | Name of the meal type (e.g., Breakfast).   |

### `food_groups`

Stores predefined food groups.

| Column             | Type             | Constraints          | Description                                 |
|--------------------|------------------|----------------------|---------------------------------------------|
| `food_group_id`    | INT              | AUTO_INCREMENT, PRIMARY KEY | Unique identifier for the food group.        |
| `food_group_name`  | VARCHAR(255)     | UNIQUE, NOT NULL     | Name of the food group (e.g., Vegetables). |

### `food_items`

Stores individual food items.

| Column             | Type             | Constraints          | Description                                 |
|--------------------|------------------|----------------------|---------------------------------------------|
| `food_item_id`     | INT              | AUTO_INCREMENT, PRIMARY KEY | Unique identifier for the food item.        |
| `food_group_id`    | INT              | FOREIGN KEY referencing `food_groups(food_group_id)` | Identifier of the food group.              |
| `food_item_name`   | VARCHAR(255)     | NOT NULL             | Name of the food item (e.g., Apple).      |

### `meals`

Stores user meal records.

| Column             | Type             | Constraints          | Description                                 |
|--------------------|------------------|----------------------|---------------------------------------------|
| `meal_id`          | INT              | AUTO_INCREMENT, PRIMARY KEY | Unique identifier for the meal.             |
| `user_id`          | INT              | FOREIGN KEY referencing `users(user_id)` | Identifier of the user who recorded the meal. |
| `meal_type_id`     | INT              | FOREIGN KEY referencing `meal_types(meal_type_id)` | Identifier of the meal type.              |
| `meal_date`        | DATE             |                      | Date of the meal.                           |
| `meal_time`        | TIME             |                      | Time of the meal.                           |
| `description`      | TEXT             |                      | Description of the meal.                    |
| `notes`            | TEXT             |                      | Additional notes about the meal.           |

### `meal_items`

Stores individual food items within a meal.

| Column             | Type             | Constraints          | Description                                 |
|--------------------|------------------|----------------------|---------------------------------------------|
| `meal_item_id`     | INT              | AUTO_INCREMENT, PRIMARY KEY | Unique identifier for the meal item.        |
| `meal_id`          | INT              | FOREIGN KEY referencing `meals(meal_id)` | Identifier of the meal.                      |
| `food_item_id`     | INT              | FOREIGN KEY referencing `food_items(food_item_id)` | Identifier of the food item.                  |
| `quantity`         | DECIMAL(10, 2)   |                      | Quantity of the food item consumed.         |

### `shopping_list`

Stores shopping list items.

| Column             | Type             | Constraints          | Description                                 |
|--------------------|------------------|----------------------|---------------------------------------------|
| `shopping_list_id` | INT              | AUTO_INCREMENT, PRIMARY KEY | Unique identifier for the shopping list item. |
| `user_id`          | INT              | FOREIGN KEY referencing `users(user_id)` | Identifier of the user.                      |
| `meal_id`          | INT              | FOREIGN KEY referencing `meals(meal_id)` | Identifier of the related meal (optional).  |
| `item_date`        | DATE             |                      | Date the item was added to the list.       |
| `quantity`         | DECIMAL(10, 2)   |                      | Quantity of the item.                        |
| `notes`            | TEXT             |                      | Additional notes about the item.           |

### `food_diary`

Stores general food diary entries.

| Column             | Type             | Constraints          | Description                                 |
|--------------------|------------------|----------------------|---------------------------------------------|
| `diary_id`         | INT              | AUTO_INCREMENT, PRIMARY KEY | Unique identifier for the diary entry.        |
| `user_id`          | INT              | FOREIGN KEY referencing `users(user_id)` | Identifier of the user.                      |
| `meal_type_id`     | INT              | FOREIGN KEY referencing `meal_types(meal_type_id)` | Identifier of the meal type.                  |
| `diary_date`       | DATE             |                      | Date of the diary entry.                    |
| `diary_time`       | TIME             |                      | Time of the diary entry.                    |
| `notes`            | TEXT             |                      | General notes about the day.               |
| `feeling`          | ENUM('Excellent', 'Good', 'Neutral', 'Poor', 'Very Poor') |                      | User's general feeling.                     |
| `feeling_details`  | TEXT             |                      | Detailed description of the user's feeling.   |

### `food_diary_entries`

Stores detailed food diary entries.

| Column             | Type             | Constraints          | Description                                 |
|--------------------|------------------|----------------------|---------------------------------------------|
| `entry_id`         | INT              | AUTO_INCREMENT, PRIMARY KEY | Unique identifier for the diary entry.        |
| `user_id`          | INT              | FOREIGN KEY referencing `users(user_id)` | Identifier of the user.                      |
| `diary_date`       | DATE             |                      | Date of the diary entry.                    |
| `entry_time`       | TIME             |                      | Time of the diary entry.                    |
| `meal_type_id`     | INT              | FOREIGN KEY referencing `meal_types(meal_type_id)` | Identifier of the meal type.                  |
| `hunger_level`     | ENUM('Not at all', 'Slightly', 'Moderately', 'Very', 'Extremely') |                      | User's hunger level.                        |
| `food_consumed`    | TEXT             |                      | Description of the food consumed.            |
| `quantity`         | VARCHAR(255)     |                      | Quantity of the food consumed.            |
| `feeling`          | ENUM('Excellent', 'Good', 'Neutral', 'Poor', 'Very Poor') |                      | User's feeling after eating.                |
| `feeling_details`  | TEXT             |                      | Detailed description of the user's feeling.   |

### `habits`

Stores user habit tracking.

| Column             | Type             | Constraints          | Description                                 |
|--------------------|------------------|----------------------|---------------------------------------------|
| `habit_id`         | INT              | AUTO_INCREMENT, PRIMARY KEY
