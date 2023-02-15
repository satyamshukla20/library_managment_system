from dotenv import load_dotenv
from flask import Flask
from sqlobject import *
from Models.Book import Books
from Models.Members import Members
from Models.Transactions import Transactions
import os

from api.booksapi import book_api
from api.membersapi import member_api
from api.operations import operation_api

def init_app():
    load_dotenv()
    app=Flask(__name__)

    db_filename = os.path.abspath("libraryDB.sqlite")
    connection_string = 'sqlite:' + db_filename
    connection = connectionForURI(connection_string)
    sqlhub.processConnection = connection
    
    Books.createTable(ifNotExists= True)
    Members.createTable(ifNotExists= True)
    Transactions.createTable(ifNotExists= True)

    app.register_blueprint(book_api)
    app.register_blueprint(member_api)
    app.register_blueprint(operation_api)

    
    
    return app
