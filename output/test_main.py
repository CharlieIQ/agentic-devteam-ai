import unittest
from main import Application

class TestApplication(unittest.TestCase):

    def setUp(self):
        self.app = Application()

    def test_register_user(self):
        self.app.register_user("testuser", "password123")
        self.assertIn("testuser", self.app.users)
        self.assertEqual(self.app.users["testuser"]["password"], "password123")

    def test_register_user_existing_username(self):
        self.app.register_user("testuser", "password123")
        with self.assertRaises(ValueError):
            self.app.register_user("testuser", "newpassword")

    def test_login_user_success(self):
        self.app.register_user("testuser", "password123")
        result = self.app.login_user("testuser", "password123")
        self.assertTrue(result)

    def test_login_user_failure(self):
        self.app.register_user("testuser", "password123")
        result = self.app.login_user("testuser", "wrongpassword")
        self.assertFalse(result)

    def test_create_post_success(self):
        self.app.register_user("testuser", "password123")
        self.app.create_post("testuser", "This is a post.")
        self.assertEqual(len(self.app.posts), 1)
        self.assertEqual(self.app.posts[0]["content"], "This is a post.")

    def test_create_post_user_not_registered(self):
        with self.assertRaises(ValueError):
            self.app.create_post("nonexistentuser", "This should fail.")

    def test_get_posts(self):
        self.app.register_user("testuser", "password123")
        self.app.create_post("testuser", "Post 1")
        self.app.create_post("testuser", "Post 2")
        posts = self.app.get_posts()
        self.assertEqual(len(posts), 2)

    def test_add_comment_success(self):
        self.app.register_user("testuser", "password123")
        self.app.create_post("testuser", "This is a post.")
        self.app.add_comment(0, "testuser", "Great post!")
        comments = self.app.get_comments(0)
        self.assertEqual(len(comments), 1)
        self.assertEqual(comments[0]["comment"], "Great post!")

    def test_add_comment_post_does_not_exist(self):
        self.app.register_user("testuser", "password123")
        with self.assertRaises(IndexError):
            self.app.add_comment(0, "testuser", "This should fail.")

    def test_add_comment_user_not_registered(self):
        self.app.create_post("testuser", "This is a post.")
        with self.assertRaises(ValueError):
            self.app.add_comment(0, "nonexistentuser", "This should fail.")

    def test_get_comments_success(self):
        self.app.register_user("testuser", "password123")
        self.app.create_post("testuser", "This is a post.")
        self.app.add_comment(0, "testuser", "Great post!")
        comments = self.app.get_comments(0)
        self.assertEqual(comments[0]["comment"], "Great post!")

    def test_get_comments_post_does_not_exist(self):
        with self.assertRaises(IndexError):
            self.app.get_comments(0)

if __name__ == '__main__':
    unittest.main()