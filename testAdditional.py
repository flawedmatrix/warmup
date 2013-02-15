"""
Each file that starts with test... in this directory is scanned for subclasses of unittest.TestCase or testLib.RestTestCase
"""

import unittest
import os
import testLib

class TestAddUser(testLib.RestTestCase):
    """Test adding users"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def test_successful_add(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)

    def test_user_exists(self):
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'xxxxxx1', 'password' : 'password' } )
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'xxxxxx1', 'password' : 'xxxxxx' } )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_USER_EXISTS)

    def test_empty_name(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : '', 'password' : 'password' } )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)

    def test_empty_password(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'xxxxxx2', 'password' : '' } )
        self.assertResponse(respData, count = 1)
    
    def test_long_name(self):
        user = "x"*130
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : user, 'password' : 'password' } )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_USERNAME)
    
    def test_long_password(self):
        password = "x"*130
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'xxxxxx3', 'password' : password } )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_PASSWORD)

class TestLoginUser(testLib.RestTestCase):
    """Test login counting"""
    def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count is not None:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    def test_one_login(self):
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'xxxxxx4', 'password' : 'password' } )
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'xxxxxx4', 'password' : 'password' } )
        self.assertResponse(respData, count = 2)

    def test_multiple_logins(self):
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'xxxxxx5', 'password' : 'password' } )
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'xxxxxx5', 'password' : 'password' } )
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'xxxxxx5', 'password' : 'password' } )
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'xxxxxx5', 'password' : 'password' } )
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'xxxxxx5', 'password' : 'password' } )
        self.assertResponse(respData, count = 5)

    def test_bad_credentials(self):
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'xxxxxx6', 'password' : 'password' } )
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'xxxxxx6', 'password' : 'xxxxxx' } )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)

    def test_empty_login(self):
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : '', 'password' : '' } )
        self.assertResponse(respData, count = None, errCode = testLib.RestTestCase.ERR_BAD_CREDENTIALS)

    def test_wrong_counts(self):
        self.makeRequest("/users/add", method="POST", data = { 'user' : 'xxxxxx7', 'password' : 'password' } )
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'xxxxxx7', 'password' : 'xxxxxx' } )
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'xxxxxx7', 'password' : 'password' } )
        self.makeRequest("/users/login", method="POST", data = { 'user' : 'xxxxxx7', 'password' : 'xxxxxx' } )
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'xxxxxx7', 'password' : 'password' } )
        self.assertResponse(respData, count = 3)

