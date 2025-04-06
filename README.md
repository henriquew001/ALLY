# Ally

A L L Y is a platform designed to empower users with the knowledge and tools to achieve their fitness goals through informed nutritional choices.

## Features

* **Nutritional Tracking:** Log daily food intake and track macronutrient and micronutrient consumption.
* **Personalized Recommendations:** Receive tailored nutritional recommendations based on your fitness goals, dietary restrictions, and activity levels.
* **Recipe Database:** Access a database of healthy recipes, filtered by dietary preferences and nutritional needs.
* **Progress Tracking:** Monitor progress towards fitness goals and visualize nutritional intake over time with charts and graphs.
* **Educational Resources:** Learn about nutrition, fitness, and healthy living through articles, tips, and interactive tools.
* **Community Support:** (Optional) Connect with other users, share experiences, and find motivation in a supportive community.

## Project Structure

```

ConsciousFit/
├── backend/        \# Python API code
├── database/       \# MariaDB configuration and scripts
├── frontend/       \# Web and/or mobile app code
├── documentation/  \# Project documentation (architecture, API, etc.)
├── docker/         \# Dockerfiles and docker-compose.yml
├── scripts/        \# Bash scripts for setup and maintenance
├──.gitignore      \# Files to be ignored by Git
├── LICENSE         \# MIT License
└── README.md       \# Project description and instructions

```

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone git@github.com:henriquew001/ConsciousFit.git
   ```

2.  **Navigate to the project directory:**

    ```bash
    cd ConsciousFit
    ```

4.  **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

## Running with Docker Compose

To run the application using Docker Compose:

1.  **Navigate to the `docker/` directory:**

    ```bash
    cd docker
    ```

2.  **Run Docker Compose:**

    ```bash
    docker-compose up --build
    ```

## Documentation

The project documentation is available in the `documentation/` directory. It includes:

  * Architecture diagrams and explanations.
  * API documentation.
  * Database schema details.
  * User guides and tutorials.

## Contributing

Contributions are welcome\! Please follow these guidelines:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes and commit them with descriptive messages.
4.  Push your changes to your fork.
5.  Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions or inquiries, please contact [your contact information here].
