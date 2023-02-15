from flask import Flask,jsonify,request,Blueprint
import requests,json
from sqlobject import *
from Models.Book import Books
from Models.Members import Members
from Models.Transactions import Transactions 
from dotenv import load_dotenv
import os



book_api = Blueprint('bookApi' , __name__)

@book_api.route('/')
def loadbooks():
    """
    this is the load_books endpoint
    """
    secret_key = os.getenv('SECRET_KEY')
    url = "https://hapi-books.p.rapidapi.com/nominees/romance/2020"
    headers = {
        "X-RapidAPI-Key": secret_key,
        "X-RapidAPI-Host": "hapi-books.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers)
    print(response.json)
    lst = response.json()
    print(headers["X-RapidAPI-Key"])
   
    try:
        for i in lst:
                name=i['name']
                author=i['author']
                Books(name=name,author=author)
    except dberrors.DuplicateEntryError:
        return {"message":"books are already loaded."}, 200

    return {"message":"books have been successfully loaded in the database."}

@book_api.route('/addbook', methods = ['POST'])
def addbooks():
    """
    this is the add_book endpoint
    """
    request_data=request.json
    name=request_data.get('name')
    author=request_data.get('author')
    quantity=request_data.get('quantity')
    book=Books(name=name,author=author,quantity=quantity)
    return {"message":f"{name} has been successfully added."},200

@book_api.route('/book/<id>', methods = ['DELETE'])
def book_delete(id):
    """
    this is the delete_book endpoint
    """
    try:
        book = Books.get(id)
    except SQLObjectNotFound:
        return {"message":"please enter a valid id"},404
    book.delete(id)
    return {"message":f"book with {id} as id is deleted"},200
 
@book_api.route("/book/<id>", methods=["PUT"])
def book_update(id):
    """
    this is the update_book endpoint
    """
    try:
        book = Books.get(id)
    except SQLObjectNotFound:
        return {"message":"please enter a valid book_id"},400
    request_data=request.json
    book.name=request_data.get("name")
    book.author=request_data.get("author")
    book.quantity=request_data.get("quantity")
    return f"book id : {id} has been updated",200
