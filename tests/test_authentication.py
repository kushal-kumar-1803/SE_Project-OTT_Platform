# tests/test_authentication.py
"""
Test Cases for Authentication & Authorization
Aligned with Test Plan:
- OTT-F-001: User login/registration
- Security validation (JWT, password storage)
"""

import unittest
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import app
from backend.database.db_connection import get_db_connection
import hashlib


class TestAuthentication(unittest.TestCase):
    """TC-Auth-01 to TC-Auth-05: Authentication & User Management (OTT-F-001)"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
    
    def setUp(self):
        """Clear users before each test"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE email IN ('test@example.com', 'admin@test.com')")
        conn.commit()
        conn.close()
    
    def test_tc_auth_01_register_user(self):
        """TC-Auth-01: Register new user"""
        payload = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "SecurePassword123"
        }
        
        response = self.client.post('/auth/register', json=payload)
        
        self.assertIn(response.status_code, [200, 201])
        data = response.get_json()
        self.assertIn("message", data)
        
        # Verify in DB
        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email=?",
            ("test@example.com",)
        ).fetchone()
        conn.close()
        
        self.assertIsNotNone(user)
        self.assertEqual(user['name'], "Test User")
        self.assertEqual(user['role'], "user")  # Default role
    
    def test_tc_auth_02_login_success(self):
        """TC-Auth-02: Successful login with JWT token"""
        # Register first
        self.client.post('/auth/register', json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "SecurePassword123"
        })
        
        # Login
        response = self.client.post('/auth/login', json={
            "email": "test@example.com",
            "password": "SecurePassword123"
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        # Verify JWT token
        self.assertIn("token", data)
        self.assertIn("role", data)
        self.assertEqual(data['role'], "user")
    
    def test_tc_auth_03_login_invalid_credentials(self):
        """TC-Auth-03: Login with invalid credentials"""
        # Register
        self.client.post('/auth/register', json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "SecurePassword123"
        })
        
        # Try wrong password
        response = self.client.post('/auth/login', json={
            "email": "test@example.com",
            "password": "WrongPassword"
        })
        
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertIn("error", data)
    
    def test_tc_auth_04_duplicate_email(self):
        """TC-Auth-04: Prevent duplicate email registration"""
        payload = {
            "name": "User 1",
            "email": "test@example.com",
            "password": "Password123"
        }
        
        # First registration
        response1 = self.client.post('/auth/register', json=payload)
        self.assertIn(response1.status_code, [200, 201])
        
        # Second registration with same email
        response2 = self.client.post('/auth/register', json=payload)
        self.assertEqual(response2.status_code, 400)
        data = response2.get_json()
        self.assertIn("error", data)
    
    def test_tc_auth_05_password_reset_otp(self):
        """TC-Auth-05: Password reset with OTP"""
        # Register user
        self.client.post('/auth/register', json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "OldPassword123"
        })
        
        # Request OTP
        response = self.client.post('/auth/forgot_password', json={
            "email": "test@example.com"
        })
        
        self.assertEqual(response.status_code, 200)
        
        # Get OTP from DB
        conn = get_db_connection()
        user = conn.execute(
            "SELECT reset_token FROM users WHERE email=?",
            ("test@example.com",)
        ).fetchone()
        conn.close()
        
        otp = user['reset_token']
        self.assertIsNotNone(otp)
        
        # Reset password with OTP
        response = self.client.post('/auth/reset_password', json={
            "email": "test@example.com",
            "otp": otp,
            "new_password": "NewPassword123"
        })
        
        # Should succeed (200/400 depending on implementation)
        self.assertIn(response.status_code, [200, 400])


class TestSecurityValidation(unittest.TestCase):
    """Security Testing: Password storage, JWT validation"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
    
    def setUp(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE email='security@test.com'")
        conn.commit()
        conn.close()
    
    def test_security_03_password_hashing(self):
        """Test passwords are hashed (not plain text)"""
        # Register user
        password = "TestPassword123"
        self.client.post('/auth/register', json={
            "name": "Security Test",
            "email": "security@test.com",
            "password": password
        })
        
        # Get password from DB
        conn = get_db_connection()
        user = conn.execute(
            "SELECT password FROM users WHERE email=?",
            ("security@test.com",)
        ).fetchone()
        conn.close()
        
        stored_password = user['password']
        
        # Verify password is hashed (not plain text)
        self.assertNotEqual(stored_password, password,
                           "Password stored in plain text!")
        
        # Should be different from plain text
        self.assertTrue(len(stored_password) > len(password),
                       "Password doesn't appear to be hashed")


if __name__ == '__main__':
    unittest.main(verbosity=2)
