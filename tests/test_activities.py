import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

TEST_EMAIL = "pytest_user@example.com"
TEST_ACTIVITY = "Chess Club"


def setup_function():
    # ensure test email not present before each test
    participants = activities[TEST_ACTIVITY]["participants"]
    if TEST_EMAIL in participants:
        participants.remove(TEST_EMAIL)


def teardown_function():
    # cleanup after tests
    participants = activities[TEST_ACTIVITY]["participants"]
    if TEST_EMAIL in participants:
        participants.remove(TEST_EMAIL)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert TEST_ACTIVITY in data
    assert "participants" in data[TEST_ACTIVITY]


def test_signup_and_unregister_flow():
    # signup
    resp = client.post(f"/activities/{TEST_ACTIVITY}/signup?email={TEST_EMAIL}")
    assert resp.status_code == 200
    assert TEST_EMAIL in activities[TEST_ACTIVITY]["participants"]

    # duplicate signup should fail
    resp2 = client.post(f"/activities/{TEST_ACTIVITY}/signup?email={TEST_EMAIL}")
    assert resp2.status_code == 400

    # unregister
    resp3 = client.delete(f"/activities/{TEST_ACTIVITY}/unregister?email={TEST_EMAIL}")
    assert resp3.status_code == 200
    assert TEST_EMAIL not in activities[TEST_ACTIVITY]["participants"]


def test_unregister_nonexistent():
    # ensure email not in list
    if TEST_EMAIL in activities[TEST_ACTIVITY]["participants"]:
        activities[TEST_ACTIVITY]["participants"].remove(TEST_EMAIL)

    resp = client.delete(f"/activities/{TEST_ACTIVITY}/unregister?email={TEST_EMAIL}")
    assert resp.status_code == 404
