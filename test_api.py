import random

from fastapi.testclient import TestClient

from api import app
import time

client = TestClient(app)

def test_create_and_delete_document():
    # it should be done on a separate db
    text = "this text is done by pytest" + str(time.time())
    response = client.post(
        "/documents/",
        headers={"accept": "application/json",
                 "Content-Type": "application/json"},
        json={"text": text},
    )
    assert response.status_code == 200
    assert response.json()["text"] == text
    assert "id" in response.json()
    doc_id = response.json()["id"]
    response_del = client.delete(
        f"/documents/{doc_id}",
        headers={"accept": "application/json"},
        json={"document_id ": doc_id},
    )
    assert response_del.json()["text"] == text


def test_create_existing_item():
    # it should be done on a separate db
    text = "this text is done by pytest" + str(time.time())
    response = client.post(
        "/documents/",
        headers={"accept": "application/json",
                 "Content-Type": "application/json"},
        json={"text": text},
    )
    assert response.status_code == 200
    assert response.json()["text"] == text
    assert "id" in response.json()
    doc_id = response.json()["id"]

    response = client.post(
        "/documents/",
        headers={"accept": "application/json",
                 "Content-Type": "application/json"},
        json={"text": text},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Document with the same text already present in the db!"

    response_del = client.delete(
        f"/documents/{doc_id}",
        headers={"accept": "application/json"},
    )
    assert response_del.json()["text"] == text
