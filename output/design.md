```python
# main.py

class Application:
    def __init__(self):
        """
        Initializes the Application instance.
        Initializes data structures for users, posts, and comments.
        """
        self.users = {}  # Dictionary to store user information
        self.posts = []  # List to store posts
        self.comments = {}  # Dictionary to store comments for each post

    def register_user(self, username: str, password: str):
        """
        Registers a new user in the application.

        Args:
            username (str): The username for the new user.
            password (str): The password for the new user.
        """
        if username in self.users:
            raise ValueError("Username already exists.")
        self.users[username] = {"password": password, "posts": []}

    def login_user(self, username: str, password: str) -> bool:
        """
        Logs in a user to the application.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: True if login is successful, otherwise False.
        """
        user_data = self.users.get(username)
        if user_data and user_data['password'] == password:
            return True
        return False

    def create_post(self, username: str, content: str):
        """
        Creates a new post for a registered user.

        Args:
            username (str): The username of the user creating the post.
            content (str): The content of the post.
        """
        if username not in self.users:
            raise ValueError("User not registered.")
        post = {
            "author": username,
            "content": content,
            "comments": []
        }
        self.posts.append(post)
        self.users[username]["posts"].append(post)

    def get_posts(self):
        """
        Retrieves all posts in the application.

        Returns:
            list: A list of all posts.
        """
        return self.posts

    def add_comment(self, post_index: int, username: str, comment: str):
        """
        Adds a comment to a specified post.

        Args:
            post_index (int): The index of the post in the posts list.
            username: The username of the user adding the comment.
            comment (str): The content of the comment.
        """
        if post_index < 0 or post_index >= len(self.posts):
            raise IndexError("Post does not exist.")
        if username not in self.users:
            raise ValueError("User not registered.")
        self.posts[post_index]["comments"].append({"author": username, "comment": comment})

    def get_comments(self, post_index: int):
        """
        Retrieves all comments for a specified post.

        Args:
            post_index (int): The index of the post in the posts list.

        Returns:
            list: A list of comments for the specified post.
        """
        if post_index < 0 or post_index >= len(self.posts):
            raise IndexError("Post does not exist.")
        return self.posts[post_index]['comments']
```

### Steps for Implementation:
1. **Create Module**: Create a new file named `main.py` in the project's root directory.
2. **Define Application Class**: Implement the `Application` class with the methods outlined.
3. **Initialize Data Structures**: Make sure to initialize data structures in the `__init__` method.
4. **Implement Methods**: Write out the logic for each method:
   - `register_user`: Handle unique usernames and store user credentials.
   - `login_user`: Verify credentials and manage user sessions.
   - `create_post`: Allow users to create posts and store them.
   - `get_posts`: Return a comprehensive list of posts.
   - `add_comment`: Append comments to specified posts after validation.
   - `get_comments`: Retrieve comments for given posts.
5. **Testing**: Write unit tests for each method to ensure the expected behavior and handle edge cases.
6. **UI Integration**: Create simple UI inputs for users to register, log in, create posts, and view comments, hooking up each interaction to the methods in the `Application` class. 
7. **Documentation**: Comment on the code clearly to maintain readability, and provide usage examples in the module for future reference. 

This design provides a complete backend structure for the Instagram clone, encapsulating all necessary functionalities for user management, post handling, and comment interactions while maintaining simplicity for further development or a user interface.