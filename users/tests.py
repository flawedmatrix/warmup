"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from users.models import User

from constants import *

class UserTests(TestCase):
    def test_valid_username_none(self):
        """
        Tests User.valid_username for a NoneType input
        """
        self.assertEqual(User.valid_username(None), False)

    def test_valid_username_empty(self):
        """
        Tests User.valid_username for a an empty string input
        """
        self.assertEqual(User.valid_username(""), False)
    
    def test_valid_username_normal(self):
        """
        Tests User.valid_username for a normal sized input
        """
        z = "x" * MAX_USERNAME_LENGTH
        self.assertEqual(User.valid_username(z), True)

    def test_valid_username_long(self):
        """
        Tests User.valid_username for input that's too long
        """
        z = "x" * (MAX_USERNAME_LENGTH + 1)
        self.assertEqual(User.valid_username(z), False)

    def test_valid_password_none(self):
        """
        Tests User.valid_password for a NoneType input
        """
        self.assertEqual(User.valid_password(None), True)

    def test_valid_password_empty(self):
        """
        Tests User.valid_password for a an empty string input
        """
        self.assertEqual(User.valid_password(""), True)
  
    def test_valid_password_normal(self):
        """
        Tests User.valid_password for a normal sized input
        """
        z = "x" * (MAX_USERNAME_LENGTH)
        self.assertEqual(User.valid_password(z), True)

    def test_valid_password_long(self):
        """
        Tests User.valid_password for input that's too long
        """
        z = "x" * (MAX_USERNAME_LENGTH + 1)
        self.assertEqual(User.valid_password(z), False)
  
    def test_successful_add(self):
        """
        Tests the add method of the User class
        """
        result = User.add("xxxxxx", "xxxxxx")
        self.assertEqual(result, 1)

    def test_successful_login(self):
        """
        Tests the login method of the User class
        """
        User.add("xxxxxx", "xxxxxx")
        result = User.login("xxxxxx", "xxxxxx")
        self.assertEqual(result, 2)

    def test_successful_increment(self):
        """
        Tests the login method of the User class for incrementing count
        """
        User.add("xxxxxx", "xxxxxx")
        result = User.login("xxxxxx", "xxxxxx")
        result = User.login("xxxxxx", "xxxxxx")
        result = User.login("xxxxxx", "xxxxxx")
        result = User.login("xxxxxx", "xxxxxx")
        self.assertEqual(result, 5)

    def test_longuser_add(self):
        """
        Tests the add method of the User class for adding
        a user with a long username
        """
        z = "x" * (MAX_USERNAME_LENGTH + 1)
        result = User.add(z, "xxxxxx")
        self.assertEqual(result, ERR_BAD_USERNAME)

    def test_emptyuser_add(self):
        """
        Tests the add method of the User class for adding
        a user with an empty username
        """
        result = User.add("", "xxxxxx")
        self.assertEqual(result, ERR_BAD_USERNAME)
 
    def test_longpass_add(self):
        """
        Tests the add method of the User class for adding
        a user with a long password
        """
        z = "x" * (MAX_PASSWORD_LENGTH + 1)
        result = User.add("xxxxxx", z)
        self.assertEqual(result, ERR_BAD_PASSWORD)

    def test_emptypass_add(self):
        """
        Tests the add method of the User class for adding
        a user with an empty password
        """
        result = User.add("xxxxxx", "")
        self.assertNotEqual(result, ERR_BAD_PASSWORD)   

    def test_duplicate_add(self):
        """
        Tests the add method of the User class for adding duplicate users
        """
        User.add("xxxxxx", "xxxxxx")
        result = User.add("xxxxxx", "password")
        self.assertEqual(result, ERR_USER_EXISTS)

    def test_wrong_login(self):
        """
        Tests the login method of the User class for
        testing bad credentials
        """
        User.add("xxxxxx", "xxxxxx")
        result = User.login("xxxxxx", "password")
        self.assertEqual(result, ERR_BAD_CREDENTIALS)

    def test_empty_login(self):
        """
        Tests the login method of the User class for
        testing empty credentials
        """
        result = User.login("", "")
        self.assertEqual(result, ERR_BAD_CREDENTIALS)

    def test_count_with_wrong_logins(self):
        """
        Tests the login method of the User class for
        preventing wrong credentials from modifying the count
        """
        User.add("xxxxxx", "xxxxxx")
        User.login("xxxxxx", "password")
        User.login("xxxxxx", "xxxxxx")
        User.login("xxxxxx", "password")
        result = User.login("xxxxxx", "xxxxxx")
        self.assertEqual(result, 3)
