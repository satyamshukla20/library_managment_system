import pytest
from app import init_app
from Models.Members import Members
from Models.Book import Books


@pytest.fixture()
def app():
    app = init_app()
    app.config.update({"TESTING": True})
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def search(app):
    return list(Members.select(Members.q.name == "prashant soni"))


@pytest.fixture()
def create_member(app):
    name = "xyz11"
    email = "xyz11@gmail.com"
    member = Members(name=name, email=email)
    return member


@pytest.fixture()
def create_member_issue(app):
    name = "xyz111"
    email = "xyz111@gmail.com"
    member = Members(name=name, email=email)
    return member


@pytest.fixture()
def create_book(app):
    name = "abracadabra"
    author = "me"
    book = Books(name=name, author=author)
    return book


@pytest.fixture()
def create_book_issue(app):
    name = "abracadabragiligili"
    author = "you"
    book = Books(name=name, author=author)
    return book
