graph TD
    A[ConsciousFit/] --> B(backend/);
    A --> C(database/);
    A --> D(frontend/);
    A --> E(documentation/);
    A --> F(docker/);
    A --> G(.gitignore);
    A --> H(README.md);

    B --> B1(app/);
    B --> B2(tests/);
    B --> B3(requirements.txt);
    B --> B4(Dockerfile);

    C --> C1(init/);
    C --> C2(migrations/);
    C --> C3(Dockerfile);
    C --> C4(mariadb.cnf);

    D --> D1(web/);
    D --> D2(mobile/);

    E --> E1(architecture/);
    E --> E2(api/);
    E --> E3(database/);

    F --> F1(docker-compose.yml);

    B1 --> B11(__init__.py);
    B1 --> B12(main.py);
    B1 --> B13(models.py);
    B1 --> B14(routes.py);

    C1 --> C11(init.sql);

    D1 --> D11(public/);
    D1 --> D12(src/);
    D1 --> D13(package.json);