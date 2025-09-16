```markdown
# Instagram Clone

This is a simple Instagram clone project built with Python for the backend and React for the frontend. The application allows users to register, log in, create posts, and comment on them. 

## Table of Contents
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)

## Requirements

- Python 3.x
- Flask (for the backend)
- React (for the frontend)
- Node.js and npm (for React setup)
- A web browser for testing

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd instagram-clone
   ```

2. **Backend Setup**:
   - Navigate to the backend directory.
   - Install the required packages:
     ```bash
     pip install Flask
     ```

   - Run the Flask backend server:
     ```bash
     python app.py
     ```
   - The backend server will start on `http://localhost:8000`.

3. **Frontend Setup**:
   - Navigate to the frontend directory.
   - Install the required packages:
     ```bash
     cd frontend
     npm install
     ```

   - Start the React application.
     ```bash
     npm start
     ```
   - The frontend will be available at `http://localhost:3000`.

## API Documentation

### User Registration
- **Endpoint**: `POST /register`
- **Request Body**:
  ```json
  {
      "username": "string",
      "password": "string"
  }
  ```
- **Response**: 
  - `200 OK` on success
  - `400 Bad Request` if username already exists

### User Login
- **Endpoint**: `POST /login`
- **Request Body**:
  ```json
  {
      "username": "string",
      "password": "string"
  }
  ```
- **Response**: 
  - `200 OK` on success with logged-in status
  - `401 Unauthorized` if login fails

### Create Post
- **Endpoint**: `POST /posts`
- **Request Body**:
  ```json
  {
      "username": "string",
      "content": "string"
  }
  ```
- **Response**: 
  - `201 Created` on post creation success
  - `400 Bad Request` if user is not registered

### Get Posts
- **Endpoint**: `GET /posts`
- **Response**:
  ```json
  [
      {
          "author": "string",
          "content": "string",
          "comments": [
              {
                  "author": "string",
                  "comment": "string"
              }
          ]
      }
  ]
  ```

### Add Comment
- **Endpoint**: `POST /posts/{post_index}/comments`
- **Request Body**:
  ```json
  {
      "username": "string",
      "comment": "string"
  }
  ```
- **Response**: 
  - `201 Created` if comment is added successfully
  - `404 Not Found` if the post does not exist or user is not registered

### Get Comments
- **Endpoint**: `GET /posts/{post_index}/comments`
- **Response**:
  ```json
  [
      {
          "author": "string",
          "comment": "string"
      }
  ]
  ```

## Usage Examples

1. **Register a User**:
   - Send a `POST` request to `/register` with the new username and password.

2. **Login a User**:
   - Send a `POST` request to `/login` with the registered username and password.

3. **Create a Post**:
   - After logging in, send a `POST` request to `/posts` with the content of the post.

4. **View All Posts**:
   - Send a `GET` request to `/posts` to retrieve a list of all posts along with comments.

5. **Comment on a Post**:
   - Send a `POST` request to `/posts/{post_index}/comments` with the username and comment to add a comment.

6. **View Comments on a Post**:
   - Send a `GET` request to `/posts/{post_index}/comments` to retrieve all comments for a specific post.

## Conclusion

This project provides a basic implementation of an Instagram-like application, demonstrating user registration, authentication, posting, and commenting functionalities. Feel free to extend it further by adding features like user profiles, likes for posts, or media uploads!
```