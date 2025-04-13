# Backend: FastAPI + PostgreSQL

## Prerequisites

- **Python 3.12 or newer** (required for development)
  - Install it from the [Python official website](https://www.python.org/downloads/).
  - Verify installation:
    ```bash
    python --version
    ```
    Ensure the version is `3.12.x`.

- **Docker & Docker Compose** (required for database and production setup)
  - Install Docker from the [Docker official website](https://www.docker.com/).
  - Install Docker Compose by following the instructions on the [Docker Compose installation page](https://docs.docker.com/compose/install/).
  - Verify installation:
    ```bash
    docker --version
    docker-compose --version
    ```

---

## Troubleshooting

If you encounter an error similar to the following when running the application:

```
ImportError: dlopen(.../_psycopg.cpython-312-darwin.so, 0x0002): Library not loaded: @rpath/libpq.5.dylib
```

It means that the PostgreSQL client library (`libpq`) is not found. To fix this issue on macOS, run the following command to install `libpq` via Homebrew:

```bash
brew install libpq
```

This should resolve the missing library error.  

---

## How to set up and run the application:

### Development Setup (With Hot Reload)

1. **Clone the repository**:

   ```bash
   git clone https://github.com/PBL-Akatsuki/backend.git
   ```

2. **Navigate to the project root directory**:

   ```bash
   cd backend
   ```

3. **Start PostgreSQL and pgAdmin (via Docker Compose)**:

   ```bash
   docker-compose up -d postgres pgadmin
   ```

   - This starts the database and pgAdmin services. You can access pgAdmin at [http://localhost:8080](http://localhost:8080).
   - Use these credentials to log in:
     - **Email**: `admin@example.com`
     - **Password**: `admin`

4. **Set up a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install dependencies**:

   ```bash
   pip install -r app/requirements.txt
   ```

6. **Run the FastAPI application with hot reload**:

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   - The API will be available at [http://localhost:8000](http://localhost:8000).
   - The Swagger UI (API documentation) is available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

### Production Setup (Dockerized Deployment)

1. **Clone the repository**:

   ```bash
   git clone https://github.com/PBL-Akatsuki/backend.git
   ```

2. **Navigate to the project root directory**:

   ```bash
   cd backend
   ```

3. **Build the Docker image**:

   ```bash
   docker-compose up --build -d
   ```

4. **Access the FastAPI application**:

   - The API will be available at [http://localhost:8000](http://localhost:8000).
   - The Swagger UI (API documentation) is available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## Testing the Application

### Running Tests

**Run all tests**:

```bash
PYTHONPATH=. pytest -v tests/
```

This will run all the test cases in the `tests/` directory. It includes tests for:

- User creation and authentication.
- Retrieving user information.
- Database operations like adding, updating, and deleting users.

**To check test coverage**:

```bash
PYTHONPATH=. pytest --cov=app tests/
```

This will show how much of your code is covered by the tests.

### What Tests Are Included?

- **User Routes**:
  - Test user creation (`/signup`).
  - Test user login (`/login`).
  - Test user deletion (`/delete-user/{id}`).
  - Test user updates (`/update-user/{id}`).

- **Database Operations**:
  - Verify database integration for CRUD operations.

- **Edge Cases**:
  - Attempting to create a user with missing fields.
  - Logging in with invalid credentials.
  - Deleting a non-existent user.

---

## How It Works

### Development

- **Hot Reload**: FastAPI runs with `uvicorn --reload` for automatic code reload on changes.
- **Database & pgAdmin**: PostgreSQL and pgAdmin run via Docker Compose to avoid local installation.

### Production

- **Dockerized Deployment**: FastAPI, PostgreSQL, and pgAdmin run inside containers.

### Testing

- Tests are implemented using `pytest` to ensure the reliability of the application.
- Covers both happy paths and edge cases to prevent regressions and ensure robustness.