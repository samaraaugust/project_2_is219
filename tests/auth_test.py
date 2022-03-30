"""This test the homepage"""
import pytest

def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_auth_pages(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200

"""
@pytest.mark.parametrize(
    ("email", "password", "message"),
    (("randomemail.com", "tester", b"Invalid username or password"),
     ("firstemail.com", "tester1", b"Invalid username or password")),
)
def test_login_validate_input(auth, email, password, message):
    response = auth.login(email, password)
    print(response.data)
    assert message in response.data
"""
def test_password_registration_bad(client):
    response = client.post("/register", data={"email": "sec@email.com", "password": "a", "confirm": "a"})
    assert b"Field must be between 6 and 35 characters long." in response.data

@pytest.fixture()
def test_successful_registration(client):
    assert client.get("/register").status_code == 200
    response = client.post("/register", data={"email": "first2@email.com", "password": "tester", "confirm": "tester"})
    assert response.headers["Location"] == "http://localhost/login"

def test_successful_login(client, auth):
    assert client.get("/login").status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "http://localhost/dashboard"

@pytest.fixture()
def test_already_registered(client):
    response = client.post("/register", data={"email": "first3@email.com", "password": "tester", "confirm": "tester"})
    response2 = client.post("/register", data={"email": "first3@email.com", "password": "tester", "confirm": "tester"})
    assert "http://localhost/login" == response2.headers["Location"]

def test_bad_confirmation(client):
    response = client.post("/register", data={"email": "tester@email.com", "password": "tester4", "confirm": "tester"})
    assert b"Passwords must match" in response.data

def test_email_registration(client):
    response = client.post("/register", data={"email": "sample", "password": "tester", "confirm": "tester"})
    assert b"Invalid email address." in response.data

def test_email_login(client):
    response = client.post("/login", data={"email": "sample", "password": "tester"})
    assert b"Invalid email address." in response.data

def test_dashboard_not_logged_in(client):
    response = client.get("/dashboard")
    assert "http://localhost/login?next=%2Fdashboard" == response.headers["Location"]

def test_dashboard_logged_in(client):
    response = client.post("/login", data={"email": "first@email.com", "password": "tester"})
    response2 = client.get("/dashboard")
    assert b"Welcome: first@email.com" in response2.data
    assert b"Dashboard" in response2.data


@pytest.mark.parametrize(
    ("email", "password", "confirm", "message"),
    (
        ("", "tester", "tester", b"This field is required."),
        ("tester@email.com", "", "tester", b"This field is required."),
        ("tester@email.com", "tester", "", b"Passwords must match")
    ),
)
def test_register_validate_input(client, email, password, confirm, message):
    response = client.post(
        "/register", data={"email": email, "password": password, "confirm": confirm}
    )
    assert message in response.data
