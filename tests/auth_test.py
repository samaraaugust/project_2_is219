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


@pytest.mark.parametrize(
    ("email", "password"),
    (("random@email.com", "tester"),
     ("first@email.com", "tester1")),
)
def test_login_validate_input(auth, email, password):
    """Bad password or username does not redirect to dashboard but back to log in page"""
    response = auth.login(email, password)
    print(response.data)
    assert response.headers["Location"] == "/login"

def test_password_registration_bad(client):
    """Registration password should be min 6 and max 35"""
    response = client.post("/register", data={"email": "sec@email.com", "password": "a", "confirm": "a"})
    assert b"Field must be between 6 and 35 characters long." in response.data


def test_successful_registration(client):
    """Successful registration redirects to login page"""
    assert client.get("/register").status_code == 200
    response = client.post("/register", data={"email": "first2@email.com", "password": "tester", "confirm": "tester"})
    assert response.headers["Location"] == "/login"

def test_successful_login(client, auth):
    """Successful login redirects to the dashboard"""
    assert client.get("/login").status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/dashboard"


def test_already_registered(client):
    """If an email is already registered it redirects to the login page"""
    response = client.post("/register", data={"email": "first3@email.com", "password": "tester", "confirm": "tester"})
    response2 = client.post("/register", data={"email": "first3@email.com", "password": "tester", "confirm": "tester"})
    assert "/login" == response2.headers["Location"]

def test_bad_password_confirmation_register(client):
    """If password and confirmation does not match then it shows an error message"""
    response = client.post("/register", data={"email": "tester@email.com", "password": "tester4", "confirm": "tester"})
    assert b"Passwords must match" in response.data

def test_email_registration(client):
    """If email is not in correct format shows an error message"""
    response = client.post("/register", data={"email": "sample", "password": "tester", "confirm": "tester"})
    assert b"Invalid email address." in response.data

def test_email_login(client):
    """If email is not in correct format shows an error message"""
    response = client.post("/login", data={"email": "sample", "password": "tester"})
    assert b"Invalid email address." in response.data

def test_dashboard_not_logged_in(client):
    """if user is not logged in can not access dashboard gets sent back to login page"""
    response = client.get("/dashboard")
    assert response.headers["Location"] == "/login?next=%2Fdashboard"

def test_dashboard_logged_in(client):
    """If user is logged in can access dashboard page"""
    response = client.post("/login", data={"email": "first@email.com", "password": "Tester1"})
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
    """fields are required when registering"""
    response = client.post(
        "/register", data={"email": email, "password": password, "confirm": confirm}
    )
    assert message in response.data
