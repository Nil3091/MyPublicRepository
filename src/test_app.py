from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_root_redirects_to_static_index():
    response = client.get("/")
    # Accept both 200 (if static file exists) or 307/302 for redirect
    assert response.status_code in (200, 302, 307)

def test_get_activities_returns_all():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data

def test_signup_for_activity_success():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"

def test_signup_for_activity_already_signed_up():
    email = "michael@mergington.edu"
    activity = "Chess Club"
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unsubscribe_from_activity_success():
    email = "emma@mergington.edu"
    activity = "Programming Class"
    response = client.post(f"/activities/{activity}/unsubscribe", params={"email": email})
    assert response.status_code == 200
    assert response.json()["message"] == f"Unsubscribed {email} from {activity}"

def test_unsubscribe_from_activity_not_signed_up():
    email = "not_signed_up@mergington.edu"
    activity = "Programming Class"
    response = client.post(f"/activities/{activity}/unsubscribe", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not signed up"

def test_unsubscribe_from_nonexistent_activity():
    response = client.post("/activities/Nonexistent/unsubscribe", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_signup_and_unsubscribe_cycle():
    email = "cycle@mergington.edu"
    activity = "Drama Club"
    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert signup_resp.status_code == 200
    # Unsubscribe
    unsubscribe_resp = client.post(f"/activities/{activity}/unsubscribe", params={"email": email})
    assert unsubscribe_resp.status_code == 200