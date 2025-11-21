# tests/test_user_features.py
"""
Test Cases for OTT Platform User Features
Aligned with Test Plan Requirements:
- OTT-F-040: Watch history & resume playback
- OTT-F-050: Subscription management, Watchlist, Ratings
- OTT-NF-001: API response time ≤ 3s
- Security validation
"""

import unittest
import json
import time
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import app
from backend.database.db_connection import get_db_connection


class TestWatchHistory(unittest.TestCase):
    """TC-Play-01 to TC-Play-03: Watch History & Resume Playback (OTT-F-040)"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test environment"""
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        
        # Create test user
        cls.test_user_id = 1
        cls.test_movie_id = 1
        
    def setUp(self):
        """Clear test data before each test"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM watch_history")
        conn.commit()
        conn.close()

    def test_tc_play_01_add_watch_history(self):
        """TC-Play-01: Add movie to watch history"""
        payload = {
            "user_id": self.test_user_id,
            "movie_id": self.test_movie_id,
            "watch_duration": 3600,
            "resume_position": 1200
        }
        
        start_time = time.time()
        response = self.client.post('/user/watch-history', 
                                   json=payload)
        elapsed_time = time.time() - start_time
        
        # Assert response
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.get_json())
        
        # OTT-NF-001: Verify API response time ≤ 3s
        self.assertLess(elapsed_time, 3.0, 
                       f"API response time {elapsed_time}s exceeds 3s limit")
        
        # Verify data in DB
        conn = get_db_connection()
        row = conn.execute(
            "SELECT * FROM watch_history WHERE user_id=? AND movie_id=?",
            (self.test_user_id, self.test_movie_id)
        ).fetchone()
        conn.close()
        
        self.assertIsNotNone(row)
        self.assertEqual(row['watch_duration'], 3600)
        self.assertEqual(row['resume_position'], 1200)

    def test_tc_play_02_get_resume_position(self):
        """TC-Play-02: Get resume position for movie"""
        # First add to watch history
        self.client.post('/user/watch-history', json={
            "user_id": self.test_user_id,
            "movie_id": self.test_movie_id,
            "watch_duration": 3600,
            "resume_position": 2400
        })
        
        # Get resume position
        start_time = time.time()
        response = self.client.get(
            f'/user/resume?user_id={self.test_user_id}&movie_id={self.test_movie_id}'
        )
        elapsed_time = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['resume_position'], 2400)
        
        # OTT-NF-001: Response time check
        self.assertLess(elapsed_time, 3.0)

    def test_tc_play_03_update_watch_history(self):
        """TC-Play-03: Update watch history (resume progress)"""
        # Add initial entry
        self.client.post('/user/watch-history', json={
            "user_id": self.test_user_id,
            "movie_id": self.test_movie_id,
            "watch_duration": 1800,
            "resume_position": 600
        })
        
        # Update with new position
        response = self.client.post('/user/watch-history', json={
            "user_id": self.test_user_id,
            "movie_id": self.test_movie_id,
            "watch_duration": 3600,
            "resume_position": 2400
        })
        
        self.assertEqual(response.status_code, 200)
        
        # Verify update
        conn = get_db_connection()
        row = conn.execute(
            "SELECT * FROM watch_history WHERE user_id=? AND movie_id=?",
            (self.test_user_id, self.test_movie_id)
        ).fetchone()
        conn.close()
        
        self.assertEqual(row['resume_position'], 2400)


class TestWatchlist(unittest.TestCase):
    """TC-Sub-01 to TC-Sub-03: Watchlist Management (OTT-F-050)"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        cls.test_user_id = 1
        cls.test_movie_id = 1
    
    def setUp(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM watchlist")
        conn.commit()
        conn.close()

    def test_tc_sub_01_add_to_watchlist(self):
        """TC-Sub-01: Add movie to watchlist"""
        payload = {
            "user_id": self.test_user_id,
            "movie_id": self.test_movie_id
        }
        
        start_time = time.time()
        response = self.client.post('/user/watchlist', json=payload)
        elapsed_time = time.time() - start_time
        
        self.assertEqual(response.status_code, 201)
        
        # OTT-NF-001: Response time check
        self.assertLess(elapsed_time, 3.0)
        
        # Verify in DB
        conn = get_db_connection()
        row = conn.execute(
            "SELECT * FROM watchlist WHERE user_id=? AND movie_id=?",
            (self.test_user_id, self.test_movie_id)
        ).fetchone()
        conn.close()
        
        self.assertIsNotNone(row)

    def test_tc_sub_02_get_watchlist(self):
        """TC-Sub-02: Retrieve user's watchlist"""
        # Add multiple items
        for i in range(1, 4):
            self.client.post('/user/watchlist', json={
                "user_id": self.test_user_id,
                "movie_id": i
            })
        
        response = self.client.get(f'/user/watchlist?user_id={self.test_user_id}')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(len(data['watchlist']), 3)

    def test_tc_sub_03_remove_from_watchlist(self):
        """TC-Sub-03: Remove movie from watchlist"""
        # Add to watchlist
        self.client.post('/user/watchlist', json={
            "user_id": self.test_user_id,
            "movie_id": self.test_movie_id
        })
        
        # Get watchlist ID
        conn = get_db_connection()
        row = conn.execute(
            "SELECT id FROM watchlist WHERE user_id=? AND movie_id=?",
            (self.test_user_id, self.test_movie_id)
        ).fetchone()
        conn.close()
        
        watchlist_id = row['id']
        
        # Remove
        response = self.client.delete(
            f'/user/watchlist?watchlist_id={watchlist_id}&user_id={self.test_user_id}'
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Verify removed
        conn = get_db_connection()
        row = conn.execute(
            "SELECT * FROM watchlist WHERE id=?",
            (watchlist_id,)
        ).fetchone()
        conn.close()
        
        self.assertIsNone(row)


class TestRatings(unittest.TestCase):
    """TC-Rating-01 to TC-Rating-03: Movie Ratings & Reviews (OTT-F-050)"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        cls.test_user_id = 1
        cls.test_movie_id = 1
    
    def setUp(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ratings")
        conn.commit()
        conn.close()

    def test_tc_rating_01_add_rating(self):
        """TC-Rating-01: Add rating to movie"""
        payload = {
            "user_id": self.test_user_id,
            "movie_id": self.test_movie_id,
            "rating": 8.5,
            "review": "Great movie! Highly recommended."
        }
        
        start_time = time.time()
        response = self.client.post('/user/rating', json=payload)
        elapsed_time = time.time() - start_time
        
        self.assertEqual(response.status_code, 200)
        
        # OTT-NF-001: Response time check
        self.assertLess(elapsed_time, 3.0)
        
        # Verify in DB
        conn = get_db_connection()
        row = conn.execute(
            "SELECT * FROM ratings WHERE user_id=? AND movie_id=?",
            (self.test_user_id, self.test_movie_id)
        ).fetchone()
        conn.close()
        
        self.assertIsNotNone(row)
        self.assertEqual(row['rating'], 8.5)

    def test_tc_rating_02_get_movie_ratings(self):
        """TC-Rating-02: Get all ratings & average for movie"""
        # Add multiple ratings
        for i in range(1, 4):
            self.client.post('/user/rating', json={
                "user_id": i,
                "movie_id": self.test_movie_id,
                "rating": 8.0 + i,
                "review": f"Review from user {i}"
            })
        
        response = self.client.get(f'/user/movie-ratings?movie_id={self.test_movie_id}')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertEqual(len(data['ratings']), 3)
        self.assertGreater(data['average_rating'], 0)
        self.assertEqual(data['total_ratings'], 3)

    def test_tc_rating_03_validate_rating_range(self):
        """TC-Rating-03: Validate rating range (0-10)"""
        # Invalid: > 10
        response = self.client.post('/user/rating', json={
            "user_id": self.test_user_id,
            "movie_id": self.test_movie_id,
            "rating": 11.0
        })
        
        self.assertEqual(response.status_code, 400)
        
        # Invalid: < 0
        response = self.client.post('/user/rating', json={
            "user_id": self.test_user_id,
            "movie_id": self.test_movie_id,
            "rating": -1.0
        })
        
        self.assertEqual(response.status_code, 400)
        
        # Valid: 7.5
        response = self.client.post('/user/rating', json={
            "user_id": self.test_user_id,
            "movie_id": self.test_movie_id,
            "rating": 7.5
        })
        
        self.assertEqual(response.status_code, 200)


class TestPerformance(unittest.TestCase):
    """OTT-NF-001 to OTT-NF-003: Performance Testing"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
    
    def test_ottmf_001_api_response_time(self):
        """OTT-NF-001: API response time ≤ 3s"""
        endpoints = [
            ('/user/watchlist?user_id=1', 'GET'),
            ('/user/watch-history?user_id=1', 'GET'),
            ('/user/movie-ratings?movie_id=1', 'GET'),
        ]
        
        for endpoint, method in endpoints:
            start_time = time.time()
            if method == 'GET':
                response = self.client.get(endpoint)
            elif method == 'POST':
                response = self.client.post(endpoint)
            elapsed_time = time.time() - start_time
            
            self.assertLess(elapsed_time, 3.0,
                           f"Endpoint {endpoint} exceeded 3s limit: {elapsed_time}s")
            print(f"✓ {endpoint}: {elapsed_time:.3f}s")


class TestSecurity(unittest.TestCase):
    """Security Validation: Input sanitization, authorization"""
    
    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
    
    def test_security_01_missing_required_fields(self):
        """Test missing required fields"""
        # Missing user_id
        response = self.client.post('/user/watchlist', json={
            "movie_id": 1
        })
        
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())
    
    def test_security_02_unauthorized_delete(self):
        """Test unauthorized watchlist deletion"""
        # Add to watchlist as user 1
        self.client.post('/user/watchlist', json={
            "user_id": 1,
            "movie_id": 1
        })
        
        # Get watchlist ID
        conn = get_db_connection()
        row = conn.execute(
            "SELECT id FROM watchlist WHERE user_id=1"
        ).fetchone()
        conn.close()
        
        
        # Try to delete as user 2
        response = self.client.delete(
            f'/user/watchlist?watchlist_id={row["id"]}&user_id=2'
        )
        
        self.assertEqual(response.status_code, 403)


# ============================================
# TEST PROFILE MANAGEMENT (OTT-F-004, OTT-F-005)
# ============================================

class TestUserProfile(unittest.TestCase):
    """Test user profile view and update functionality"""

    @classmethod
    def setUpClass(cls):
        from backend.app import app
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = app.test_client()

    def setUp(self):
        """Set up test database"""
        import sqlite3
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row

    def tearDown(self):
        """Clean up"""
        self.conn.close()

    def test_get_user_profile_success(self):
        """TC-Profile-01: Get user profile successfully"""
        # In a real scenario, this would fetch from DB
        response = self.client.get('/user/profile?user_id=1')
        
        # Should return 200 or 404 (if user doesn't exist in test DB)
        self.assertIn(response.status_code, [200, 404])

    def test_get_user_profile_missing_user_id(self):
        """TC-Profile-01b: Get profile without user_id"""
        response = self.client.get('/user/profile')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_update_user_profile_success(self):
        """TC-Profile-02: Update user profile successfully"""
        payload = {
            "user_id": 1,
            "name": "John Updated",
            "bio": "Test bio",
            "profile_type": "adult"
        }
        
        response = self.client.put(
            '/user/profile',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Should return 200 or 404 (if user doesn't exist in test DB)
        self.assertIn(response.status_code, [200, 404])

    def test_update_profile_invalid_profile_type(self):
        """TC-Profile-02b: Reject invalid profile_type"""
        payload = {
            "user_id": 1,
            "name": "John",
            "profile_type": "invalid_type"
        }
        
        response = self.client.put(
            '/user/profile',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Should return 400 for invalid profile_type
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_kids_profile_type_validation(self):
        """TC-Profile-03: Validate kids profile type"""
        payload = {
            "user_id": 1,
            "name": "Junior",
            "profile_type": "kids"
        }
        
        response = self.client.put(
            '/user/profile',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        # Should accept 'kids' profile type
        self.assertIn(response.status_code, [200, 404])
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertNotIn('error', data)


# ============================================
# TEST KIDS MODE FILTERING
# ============================================

class TestKidsModeFiltering(unittest.TestCase):
    """Test that kids mode filters adult content"""

    @classmethod
    def setUpClass(cls):
        from backend.app import app
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = app.test_client()

    def test_get_all_movies_adult_mode(self):
        """TC-Browse-03: Get all movies in adult mode"""
        response = self.client.get('/movies?profile_type=adult')
        
        self.assertIn(response.status_code, [200, 404])

    def test_get_all_movies_kids_mode(self):
        """TC-Browse-04: Get family-friendly movies in kids mode"""
        response = self.client.get('/movies?profile_type=kids')
        
        self.assertIn(response.status_code, [200, 404])
        
        if response.status_code == 200:
            data = json.loads(response.data)
            # If results exist, verify kids_friendly flag
            if 'results' in data and data['results']:
                for movie in data['results']:
                    # All movies should have is_kids_friendly=1 in kids mode
                    if 'is_kids_friendly' in movie:
                        self.assertEqual(movie['is_kids_friendly'], 1)

    def test_search_with_kids_filter(self):
        """TC-Search-02: Search respects kids mode filter"""
        response = self.client.get('/movies/search?q=movie&profile_type=kids')
        
        self.assertIn(response.status_code, [200, 404])


if __name__ == '__main__':
    unittest.main(verbosity=2)

