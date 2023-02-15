from api.booksapi import book_api
from api.membersapi import member_api
from api.operations import operation_api
from init_app import init_app
from Models.Book import Books

app = init_app()


if __name__== '__main__':
    app.run(debug=True)