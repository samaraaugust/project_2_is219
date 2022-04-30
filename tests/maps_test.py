def test_csv_upload(client, auth):
    response1 = auth.register()
    response3 = auth.login()
    csv = "tests/test_music.csv"
    csv_data = open(csv, "rb")
    data = {"file": (csv_data, "test_music.csv")}
    response2 = client.post("/songs", data=data)
    print(response2.data)
    assert response2.status_code == 302
    assert response2.headers["Location"] == "/songs_tables"