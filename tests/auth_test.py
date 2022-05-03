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


def test_successful_register(client, auth):
    """Successful register redirects to the login"""
    response = auth.register()
    assert response.headers["Location"] == "/login"

def test_successful_login(client, auth):
    """Successful login redirects to the dashboard"""
    response2 = auth.register()
    response = auth.login()
    assert response.headers["Location"] == "/dashboard"

def test_dashboard_logged_in(client, auth):
    """If user is logged in can access dashboard page"""
    response1 = auth.register()
    response3 = auth.login()
    response2 = client.get("/dashboard")
    assert b"Welcome: test@email.com" in response2.data
    assert b"Dashboard" in response2.data


def test_dashboard_not_logged_in(client):
    """if user is not logged in can not access dashboard gets sent back to login page"""
    response = client.get("/dashboard")
    assert response.headers["Location"] == "/login?next=%2Fdashboard"

def test_denying_upload(client):
    """if user is not logged in can not access uploads page"""
    response = client.post("/locations/upload")
    assert response.headers["Location"] == "/login?next=%2Flocations%2Fupload"

def test_bad_password_confirmation_register(client):
    response = client.post("/register", data={"email": "tester@email.com", "password": "Tester4@", "confirm": "tester"})
    print(response.data)
    assert b"Passwords must match" in response.data

def test_email_registration(client):
    """If email is not in correct format shows an error message"""
    response = client.post("/register", data={"email": "sample", "password": "Tester1@", "confirm": "Tester1@"})
    print(response.data)
    assert b"Invalid email address." in response.data

def test_email_login(client):
    """If email is not in correct format shows an error message"""
    response = client.post("/login", data={"email": "sample", "password": "Tester1@"})
    assert b"Invalid email address." in response.data

def test_bad_password_registration(client):
    """If password does not meets requirements"""
    response = client.post("/register", data={"email": "sample@email.com", "password": "Tester1", "confirm": "Tester1"})
    print(response.data)
    assert b"Invalid Password" in response.data

def test_bad_password_login(client):
    """If password does not meets requirements"""
    response = client.post("/login", data={"email": "sample@email.com", "password": "Tester1"})
    print(response.data)
    assert b"Invalid Password" in response.data

def test_already_registered(client, auth):
    """If an email is already registered it redirects to the login page"""
    response = auth.register()
    response2 = auth.register()
    assert "/login" == response2.headers["Location"]

@pytest.mark.parametrize(
    ("email", "password", "confirm", "message"),
    (
        ("", "tester1@", "Tester1@", b"This field is required."),
        ("tester2@email.com", "", "tester", b"This field is required."),
        ("tester2@email.com", "Tester1@", "", b"Passwords must match")
    ),
)
def test_register_validate_input(client, email, password, confirm, message):
    """fields are required when registering"""
    response = client.post(
        "/register", data={"email": email, "password": password, "confirm": confirm}
    )
    assert message in response.data

@pytest.mark.parametrize(
    ("email", "password"),
    (("test@email.com", "Tester1!"),
     ("first2@email.com", "Tester1@")),
)
def test_login_validate_input(auth, email, password):
    """Bad password or username does not redirect to dashboard but back to log in page"""
    response1 = auth.register()
    response = auth.login(email, password)
    assert response.headers["Location"] == "/login"

def test_logout(client, auth):
    response = auth.register()
    response2 = auth.login()
    response3 = client.get('/logout')
    assert response3.headers["Location"] == "/login"

@pytest.mark.parametrize(
    ("email", "password", "message"),
    (
        ("", "tester1@", b"This field is required."),
        ("tester2@email.com", "", b"This field is required."),
    ),
)
def test_login_validate_input_checker(client, email, password, message):
    """fields are required for login"""
    response = client.post(
        "/login", data={"email": email, "password": password}
    )
    assert message in response.data