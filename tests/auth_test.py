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