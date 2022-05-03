def test_csv_upload(client, auth):
    response1 = auth.register()
    response3 = auth.login()
    csv = "tests/test_cities_short.csv"
    csv_data = open(csv, "rb")
    data = {"file": (csv_data, "test_cities_short.csv")}
    response2 = client.post("/locations/upload", data=data)
    print(response2.data)
    assert response2.status_code == 302
    assert response2.headers["Location"] == "/locations_datatables/"