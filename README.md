# Blog Management API

This repository contains the source code for a simple **Blog Management API** built using FastAPI. The API allows users to manage users, groups, posts, and group participants, and includes authentication through JWT (JSON Web Tokens) for secure access.

## Features

- **User Authentication**: Secure login with JWT-based authentication.
- **User Management**: Create, retrieve, and delete user records.
- **Group Management**: Create, retrieve, and delete groups with region-based details.
- **Post Management**: Create, retrieve, and delete blog posts associated with users.
- **Group Participants**: Manage participants in groups.
- **Group Posts**: Link posts to groups.
  
## Technology Stack

- **FastAPI**: The web framework for building the API.
- **MySQL**: The database used for storing user, group, and post data.
- **JWT**: JSON Web Tokens for secure access and user authentication.

## Getting Started

### Prerequisites

- Python 3.8+
- MySQL server
- Install the required packages:

```bash
pip install fastapi[all] mysql-connector-python python-jose
```

### Database Setup

1. Set up a MySQL database with the following tables: `user`, `groups`, `posts`, `group_participants`, `group_posts`.
2. Update the MySQL connection settings in `main.py` to match your MySQL configuration.

### Running the API

1. Clone this repository:
   ```bash
   git clone https://github.com/AayushChhabra42/Blog_Managment_API.git
   cd blog-management-api
   ```

2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

3. The API will be accessible at `http://127.0.0.1:8000`.

## API Endpoints

### Authentication

- **POST `/login`**: User login. Returns a JWT token for authorized access.

### User Management

- **GET `/Users`**: Retrieve a list of all users.
- **GET `/Users/{id}`**: Retrieve a specific user by ID.
- **POST `/Users`**: Create a new user.

### Group Management

- **GET `/Groups`**: Retrieve all groups.
- **POST `/Groups`**: Create a new group.
- **GET `/Groups/{id}`**: Retrieve a specific group by ID.
- **DELETE `/Groups/{id}`**: Delete a group by ID.

### Post Management

- **GET `/Posts`**: Retrieve all posts.
- **POST `/Posts`**: Create a new post.
- **GET `/Posts/{id}`**: Retrieve a specific post by ID.
- **DELETE `/Posts/{id}`**: Delete a post by ID.

### Group Participants Management

- **GET `/group_participants`**: Retrieve all group participants.
- **POST `/group_participants`**: Add a participant to a group.

### Group Posts Management

- **GET `/group_posts`**: Retrieve all group posts.
- **POST `/group_posts`**: Link a post to a group.

## Authentication & Authorization

The API uses JWT for secure access. The token is required for creating or deleting groups, posts, and managing group-related data.

- To obtain a token, use the `/login` endpoint.
- Include the token in the `Authorization` header as a Bearer token for protected endpoints.

## Example Usage

- **Login**:
  ```http
  POST /login
  Content-Type: application/json
  {
    "username": "testuser",
    "password": "testpassword"
  }
  ```

- **Create a New User**:
  ```http
  POST /Users
  Authorization: Bearer <your-token>
  Content-Type: application/json
  {
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123"
  }
  ```

## License

This project is licensed under the MIT License.

---

Contributions are welcome!
