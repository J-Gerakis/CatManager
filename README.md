Mini production-ready project
========================================

Project: Task Management system\
Objective: Build a production-ready FastAPI application with an OOP-based architecture, two microservices, and a fully tested codebase.

Overview
--------

### Tech Stack

-   FastAPI -- API framework

-   SQLAlchemy -- ORM for database interactions

-   PostgreSQL -- Relational database

-   Redis -- For caching and message queue

-   Docker + Docker Compose -- For containerization

-   Pytest + Hypothesis -- Testing

-   GitHub Actions -- CI/CD pipeline

### Microservices

1.  User Service (Handles user accounts, authentication, and profile management)

2.  Task Service (Manages tasks, statuses, and deadlines)

The two services communicate via HTTP (REST API) and event-driven messaging using Redis.

System Architecture
-------------------

### Directory Structure

```
taskflow/
│── user_service/
│   ├── app/
│   │   ├── models.py  # SQLAlchemy models
│   │   ├── services.py  # Business logic (OOP-style services)
│   │   ├── routes.py  # FastAPI route definitions
│   │   ├── db.py  # Database session setup
│   │   ├── main.py  # FastAPI entry point
│   ├── tests/
│   │   ├── test_routes.py  # API route tests
│   │   ├── test_services.py  # Unit tests for business logic
│   ├── Dockerfile
│   ├── requirements.txt
│
│── task_service/
│   ├── app/
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── routes.py
│   │   ├── db.py
│   │   ├── main.py
│   ├── tests/
│   │   ├── test_routes.py
│   │   ├── test_services.py
│   ├── Dockerfile
│   ├── requirements.txt
│
│── docker-compose.yml
│── README.md
│── .github/workflows/ci.yml  # CI/CD workflow

```

Features
--------

### User Service Features

-   User registration and authentication

-   User profile management

-   API authentication using JWT

### Task Service Features

-   Create, update, and delete tasks

-   Assign tasks to users

-   Fetch tasks by status and deadline

### Communication Between Services

-   The Task Service calls the User Service to validate user ownership of tasks.

-   The User Service sends an event when a new user is created.

**Implementing Microservices**
------------------------------

### **User Service (**user_service/app/main.py**)**

```
from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="User Service")

app.include_router(router)

```

User Model (user_service/app/models.py)

```
from sqlalchemy import Column, Integer, String
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

```

**Task Service (**task_service/app/models.py**)**

```
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.db import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    status = Column(String, default="pending")
    due_date = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

```

Testing Strategy
----------------

### **Final Deliverables**

-   Two microservices (User Service and Task Service)

-   OOP-based architecture with FastAPI

-   Fully tested with unit, integration, and property-based tests

-   Dockerised for production

-   CI/CD pipeline for automated testing and deployment
