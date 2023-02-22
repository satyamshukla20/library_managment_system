import pytest
import json
from Models.Members import Members


def test_member(client):
    res1 = client.get("/member")
    assert res1.status_code == 200


def test_add_member(client):
    data1 = {"name": "prashant soni", "email": "p@gmail.com"}
    data2 = {"name": "satyam", "email": "satya@gmail.com"}
    res1 = client.post("/member", json=data1)
    res2 = client.post("/member", json=data2)
    assert res1.status_code == 200
    assert res2.status_code == 200


def test_deleting_member(client, search, create_member):
    member_id = create_member.id
    print(member_id)
    res1 = client.delete(f"/member/{member_id}")
    assert res1.status_code == 200
    res2 = client.delete(f"/member/{member_id}")
    assert res2.status_code == 404


def test_add_books(client):
    data1 = {"name": "lion king", "author": "disney", "quantity": 20}
    res1 = client.post("/addbook", json=data1)
    assert res1.status_code == 200
    assert res1.status_code == 200


def test_load_books_in_database_when_they_are_not_loaded(client):
    """
    Empty the database then only you can test this route.
    """
    res = client.get("/")
    assert res.status_code == 200


def test_load_books_in_database_when_they_are_are_already_loaded(client):
    res = client.get("/")
    assert res.status_code == 200


def test_deleting_book(client, create_book):
    book_id = create_book.id
    res1 = client.delete(f"/book/{book_id}")
    assert res1.status_code == 200
    res2 = client.delete(f"/book/{book_id}")
    assert res2.status_code == 404


def test_search_book(client, create_book):
    book_name = create_book.name
    book_id = create_book.id
    data1 = {"book_name": book_name}
    data2 = {"book_name": "shiva"}
    res1 = client.post("/search", json=data1)
    res2 = client.post("/search", json=data2)
    client.delete(f"/book/{book_id}")
    assert res1.status_code == 200
    assert res2.status_code == 404


# def test_end_to_end_testing(client):
def test_end_to_end_testing(client, create_member_issue, create_book_issue):
    """
    we have create user and book using fixture and then done the issuing,returning and payment billing.
    """
    member_id = create_member_issue.id
    book_name = create_book_issue.name
    book_id = create_book_issue.id
    data1 = {"member_id": member_id, "book_name": book_name}
    data2 = {"member_id": member_id, "book_name": "Beacher Read"}

    res1 = client.post("/issue", json=data1)
    res2 = client.post("/issue", json=data2)
    print("+++++++r", res1.json)
    assert res1.status_code == 200
    assert res2.status_code == 404

    transaction_id = res1.json["transaction_id"]
    res3 = client.post("/return", json={"transaction_id": transaction_id})
    assert res3.status_code == 200
    assert res3.status_code != 404

    data3 = {"member_id": member_id, "payment_amount": 100}
    data4 = {"member_id": 1200, "payment_amount": 100}

    res4 = client.post("/payment", json=data3)
    res5 = client.post("/payment", json=data4)
    assert res4.status_code == 200
    assert res5.status_code == 404


def test_popularity(client):
    res = client.get("/popular")
    assert res.status_code == 200



