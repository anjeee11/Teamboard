# TeamBoard API

A B2B Knowledge Base API built with Django REST Framework, PostgreSQL, Docker, and JWT Authentication. TeamBoard enables companies to register, securely access curated technical knowledge, track API usage, and view platform analytics through role-based access control.

## Key Features

- Company Registration and Authentication
- JWT-Based Authorization (SimpleJWT)
- Automatic API Key Generation via Django Signals
- Knowledge Base Search with Keyword Matching
- Query Usage Tracking and Logging
- Admin-Only Usage Analytics Dashboard
- Custom Role-Based Permissions

## Technology Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Docker
- SimpleJWT
- python-dotenv

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/anjeee11/Teamboard.git
cd Teamboard
```

### Configure Environment Variables

Create a `.env` file in the project root:

```env
DB_NAME=teamboard
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your_secret_key
DEBUG=True
```

### Start PostgreSQL

```bash
docker compose up -d
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Seed Knowledge Base Data

````bash

The knowledge base was seeded with 10 predefined technical Q&A entries covering:

* API Concepts
* Django ORM
* JWT Authentication
* PostgreSQL
* Docker
* Django Signals
* Transactions
* Migrations

To reseed manually:

```bash
python manage.py shell
````

Then execute the KBEntry creation script available in the project documentation or source code.

### Run the Application

```bash
python manage.py runserver

```

## API Endpoints

| Method | Endpoint                    | Description                                |
| ------ | --------------------------- | ------------------------------------------ |
| POST   | `/api/auth/register/`       | Register a company and receive credentials |
| POST   | `/api/auth/login/`          | Authenticate and receive a JWT token       |
| POST   | `/api/kb/query/`            | Search the knowledge base                  |
| GET    | `/api/admin/usage-summary/` | View platform usage analytics (Admin Only) |

## Authentication

Protected endpoints require a JWT access token:

```http
Authorization: Bearer <access_token>
```

## Assignment Requirements Covered

- PostgreSQL database running via Docker
- Environment variables managed through `.env`
- Global JWT authentication using SimpleJWT
- Automatic Company profile creation using Django Signals
- Secure API key generation with `secrets.token_urlsafe(32)`
- Atomic query logging with `transaction.atomic()`
- Custom `IsAdminUser` permission class
- Usage analytics with aggregation and grouped queries

## Testing Artifacts

The repository includes:

- `responses.json` — API request and response evidence for assignment validation.

## Author

Anjali Nimesh
