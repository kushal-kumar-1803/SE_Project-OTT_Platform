# TEST EXECUTION GUIDE - OTT Platform v1.0

## Overview
This document maps test cases to the Software Test Plan requirements and provides execution instructions.

---

## 1. TEST CASE MAPPING

### Authentication & User Management (OTT-F-001)

| Test Case ID | Requirement | Description | Status |
|--------------|-------------|-------------|--------|
| TC-Auth-01 | OTT-F-001 | Register new user | ✅ Implemented |
| TC-Auth-02 | OTT-F-001 | Successful login with JWT | ✅ Implemented |
| TC-Auth-03 | OTT-F-001 | Invalid credentials handling | ✅ Implemented |
| TC-Auth-04 | OTT-F-001 | Duplicate email prevention | ✅ Implemented |
| TC-Auth-05 | OTT-F-001 | Password reset with OTP | ✅ Implemented |

**File:** `tests/test_authentication.py`

---

### Watch History & Resume (OTT-F-040)

| Test Case ID | Requirement | Description | Status |
|--------------|-------------|-------------|--------|
| TC-Play-01 | OTT-F-040 | Add movie to watch history | ✅ Implemented |
| TC-Play-02 | OTT-F-040 | Get resume position | ✅ Implemented |
| TC-Play-03 | OTT-F-040 | Update watch progress | ✅ Implemented |

**File:** `tests/test_user_features.py`

**Endpoints:**
- `POST /user/watch-history` - Add/update watch history
- `GET /user/watch-history` - Retrieve watch history
- `GET /user/resume` - Get resume position for movie

---

### Watchlist Management (OTT-F-050)

| Test Case ID | Requirement | Description | Status |
|--------------|-------------|-------------|--------|
| TC-Sub-01 | OTT-F-050 | Add movie to watchlist | ✅ Implemented |
| TC-Sub-02 | OTT-F-050 | Retrieve user watchlist | ✅ Implemented |
| TC-Sub-03 | OTT-F-050 | Remove from watchlist | ✅ Implemented |

**File:** `tests/test_user_features.py`

**Endpoints:**
- `POST /user/watchlist` - Add to watchlist
- `GET /user/watchlist` - Get watchlist
- `DELETE /user/watchlist` - Remove from watchlist

---

### Ratings & Reviews (OTT-F-050)

| Test Case ID | Requirement | Description | Status |
|--------------|-------------|-------------|--------|
| TC-Rating-01 | OTT-F-050 | Add/update rating | ✅ Implemented |
| TC-Rating-02 | OTT-F-050 | Get movie ratings & average | ✅ Implemented |
| TC-Rating-03 | OTT-F-050 | Validate rating range (0-10) | ✅ Implemented |

**File:** `tests/test_user_features.py`

**Endpoints:**
- `POST /user/rating` - Add/update rating
- `GET /user/movie-ratings` - Get all ratings for movie
- `GET /user/rating` - Get user's rating for movie

---

### Performance Testing (OTT-NF-001)

| Test Case ID | Requirement | Description | Status |
|--------------|-------------|-------------|--------|
| OTT-NF-001 | OTT-NF-001 | API response ≤ 3 seconds | ✅ Implemented |

**Target Metrics:**
- API response time: ≤ 3 seconds (all endpoints)
- Video start time: ≤ 5 seconds (depends on CDN)
- Platform availability: ≥ 99%

**File:** `tests/test_user_features.py` (TestPerformance class)

---

### Security Validation

| Test Case ID | Category | Description | Status |
|--------------|----------|-------------|--------|
| Sec-01 | Input Validation | Missing required fields | ✅ Implemented |
| Sec-02 | Authorization | Unauthorized watchlist deletion | ✅ Implemented |
| Sec-03 | Password Security | Password hashing verification | ✅ Implemented |
| Sec-04 | JWT Validation | Token expiry & refresh | ⏳ Planned |
| Sec-05 | HTTPS/TLS | Secure transmission | ⏳ Environment setup |

---

## 2. HOW TO RUN TESTS

### Prerequisites
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
python -m pytest tests/ -v
# OR
python -m unittest discover tests -v
```

### Run Specific Test File
```bash
# Authentication tests
python -m unittest tests.test_authentication -v

# User features tests
python -m unittest tests.test_user_features -v
```

### Run Specific Test Class
```bash
# Authentication only
python -m unittest tests.test_authentication.TestAuthentication -v

# Watch history tests
python -m unittest tests.test_user_features.TestWatchHistory -v

# Watchlist tests
python -m unittest tests.test_user_features.TestWatchlist -v

# Ratings tests
python -m unittest tests.test_user_features.TestRatings -v

# Performance tests
python -m unittest tests.test_user_features.TestPerformance -v
```

### Run Specific Test Case
```bash
# Single test
python -m unittest tests.test_authentication.TestAuthentication.test_tc_auth_01_register_user -v

python -m unittest tests.test_user_features.TestWatchHistory.test_tc_play_01_add_watch_history -v
```

---

## 3. TEST EXECUTION CHECKLIST

### Unit Testing Phase
- [ ] Start Flask server: `python -m flask --app backend.app run --debug`
- [ ] Run TC-Auth-01 through TC-Auth-05
- [ ] Run TC-Play-01 through TC-Play-03
- [ ] Run TC-Sub-01 through TC-Sub-03
- [ ] Run TC-Rating-01 through TC-Rating-03
- [ ] Run performance tests (OTT-NF-001)
- [ ] Run security tests

### Integration Testing Phase
- [ ] Test API → Database interactions
- [ ] Test JWT token flow
- [ ] Test OTP email sending
- [ ] Test TMDB API integration

### System Testing Phase
- [ ] End-to-end user registration flow
- [ ] End-to-end login flow
- [ ] Complete watch + resume flow
- [ ] Watchlist + rating flow
- [ ] Admin panel access

### Acceptance Testing Phase
- [ ] UAT with sample users
- [ ] Cross-browser testing (Chrome, Firefox, Safari)
- [ ] Mobile device testing
- [ ] Load testing (50+ concurrent users)

---

## 4. TEST DATA SETUP

### Sample User Accounts
```json
{
  "users": [
    {
      "id": 1,
      "email": "user1@test.com",
      "password": "Password123",
      "role": "user"
    },
    {
      "id": 2,
      "email": "admin@test.com",
      "password": "Admin123",
      "role": "admin"
    }
  ]
}
```

### Sample Movies
```json
{
  "movies": [
    {
      "id": 1,
      "title": "Inception",
      "genre": "Sci-Fi",
      "description": "A mind-bending thriller...",
      "poster_url": "https://..."
    }
  ]
}
```

---

## 5. EXPECTED TEST RESULTS

### Pass Criteria
- ✅ All 18 functional test cases pass
- ✅ All API responses ≤ 3 seconds
- ✅ 0 critical security issues
- ✅ 100% requirement traceability

### Fail Criteria
- ❌ Any critical defect not fixed
- ❌ API response > 3 seconds
- ❌ Security vulnerabilities (SQL injection, XSS, etc.)
- ❌ < 95% test case pass rate

---

## 6. DEFECT TRACKING

### Report Template
```
Defect ID: DEF-001
Title: [Short description]
Component: [e.g., Auth, Watchlist, etc.]
Severity: Critical | High | Medium | Low
Steps to Reproduce:
1. ...
2. ...
Expected Result: ...
Actual Result: ...
Attachments: [Screenshots/logs]
```

---

## 7. TEST METRICS & REPORTING

### Daily Execution Report
- Test cases executed: X / Y
- Pass: X
- Fail: X
- Blocked: X
- Pass Rate: X%

### Final Test Summary Report (after all phases)
- Total test cases: 18+
- Executed: 100%
- Passed: X%
- Failed: X%
- Defect density: X/KLOC
- Requirement coverage: 100%

---

## 8. TEST ENVIRONMENT

### Hardware
- Web client: Modern browser (Chrome 90+, Firefox 88+)
- Mobile: Android 10+, iOS 13+
- Admin desktop: Windows/Mac

### Software
- Python 3.13+
- Flask 3.x
- SQLite3
- Flask-Mail (Gmail SMTP)
- JWT for authentication

### Tools
- Postman (API testing)
- Pytest/Unittest (automated testing)
- Chrome DevTools (browser testing)

---

## 9. ENTRY & EXIT CRITERIA

### Entry Criteria
- ✅ Stable build deployed
- ✅ Test environment ready
- ✅ Test data loaded
- ✅ All test cases documented
- ✅ Test team trained

### Exit Criteria
- ✅ 100% planned test cases executed
- ✅ 0 critical defects
- ✅ ≥ 95% pass rate
- ✅ All requirements traced to test cases
- ✅ UAT sign-off received
- ✅ Test report approved

---

## 10. SIGN-OFF

| Role | Name | Signature | Date |
|------|------|-----------|------|
| QA Lead | [Name] | __________ | ________ |
| Dev Lead | [Name] | __________ | ________ |
| Product Owner | [Name] | __________ | ________ |

---

**Document Version:** 1.0  
**Last Updated:** November 21, 2025  
**Status:** Active
