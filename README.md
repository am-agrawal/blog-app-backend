# Blog App Backend

A FastAPI backend application with modular architecture, featuring user authentication, email verification, and JWT token management.

## Features

- User registration with email verification
- OTP-based email verification
- JWT-based authentication (access and refresh tokens)
- Modular architecture with clean separation of concerns
- Docker containerization
- **Auto-reload during development** - Changes to code automatically refresh the container

## Architecture

```
.
├── blog_app/
│   ├── api/                 # API endpoints
│   ├── core/                # Configuration and security
│   ├── crud/                # Database operations
│   ├── db/                  # Database models and session
│   ├── decorators/          # JWT decorators
│   ├── schemas/             # Pydantic models
│   └── utils/               # Utility functions (email, etc.)
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker services
└── requirements.txt         # Python dependencies
```

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- **External MySQL/PostgreSQL server** (local or remote)
- Gmail account with App Password for email functionality

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd blog-app-backend
```

2. Configure environment variables:

   - Copy `env.example` to `.env`
   - Update `.env` with your Gmail credentials and **external MySQL connection details**
   - Set a secure `SECRET_KEY`

3. **Start the container**:

```bash
# Start basic services
docker-compose up -d
```

4. **Ensure your MySQL/PostgreSQL server is running** and accessible

5. Access the API:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

## API Endpoints

### Authentication

- `POST /api/auth/signup` - User registration
- `POST /api/auth/verify` - Email verification with OTP
- `POST /api/auth/login` - User login

## License

This project is licensed under the MIT License.
