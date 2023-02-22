from flask import Flask, jsonify, request, Blueprint
import requests, json
from datetime import datetime, timedelta
from sqlobject import *
from Models.Book import Books
from Models.Members import Members
from Models.Transactions import Transactions

operation_api = Blueprint("operationApi", __name__)


@operation_api.route("/search", methods=["POST"])
def search():
    """
    this is the search endpoint
    """
    request_data = request.json
    book_name = request_data.get("book_name")
    book_list = list(Books.select(Books.q.name == book_name))
    if len(book_list) != 0:
        book = book_list[0]
        if book.quantity > 0:
            return {"message": "This book is available."}, 200
        else:
            {
                "message": "This book was available in library but they have been issued."
            }, 200
    return {"message": "This book is not available."}, 404


@operation_api.route("/hypersearch", methods=["POST"])
def hypersearch():
    """
    this is the hypersearch endpoint it's a higher level of search.
    """
    request_data = request.json
    book_name = request_data.get("book_name")
    if len(book_name) < 3:
        return {"messege": "Please provide atleast three letters of the book name"}
    book_list = list(Books.select())
    result = []
    for book in book_list:
        if str.__contains__(book.name, book_name):
            result.append(
                {
                    "id": book.id,
                    "name": book.name,
                }
            )
    return {"members": result}, 200


@operation_api.route("/issue", methods=["POST"])
def issue():
    """
    this is the issue endpoint
    """
    request_data = request.json
    member_id = request_data.get("member_id")
    book_name = request_data.get("book_name")
    list_of_member = list(Members.select(Members.q.id == member_id))
    if len(list_of_member) == 0:
        return {
            "message": "The member_id is incorrect.please check it or create a new membership"
        }, 400
    member = list_of_member[0]
    list_of_book = list(Books.select(Books.q.name == book_name))
    if len(list_of_book) == 0:
        return {
            "message": f"{book_name} is not available in the library kindly look for another book."
        }, 404

    book = list_of_book[0]
    if book.quantity == 0:
        return {
            "message": f"{book_name} is not available whenever it will be returned we will let you know"
        }, 400
    if member.debt > 500:
        return {
            "message": "Your balance is less than minimum criteria. Please recharge your account"
        }, 400
    book_id = book.id
    transaction = Transactions(book_id=book_id, member_id=member_id)

    book.quantity -= 1
    book.popularity += 1

    # print(transaction)
    return jsonify({"book_name": book_name, "transaction_id": transaction.id}), 200


@operation_api.route("/return", methods=["POST"])
def book_return():
    """
    this is the return endpoint
    """
    request_data = request.json
    transaction_id = request_data.get("transaction_id")
    list_of_transaction: Transactions = list(
        Transactions.select(Transactions.q.id == transaction_id)
    )
    print(list_of_transaction)
    if len(list_of_transaction) != 0:
        transaction = list_of_transaction[0]
        if transaction.transaction_status == 1:
            transaction.date_from
            current_time = datetime.utcnow()
            print(current_time)
            print(transaction.date_from)
            deltatime: timedelta = current_time - transaction.date_from
            total_days = deltatime.days + 100
            fine = 0

            book_id = transaction.book_id
            list_of_book = list(Books.select(Books.q.id == book_id))
            book = list_of_book[0]
            book.quantity += 1
            transaction.transaction_status = 0

            if total_days > 14:
                fine = (total_days - 14) * 10
                transaction.fine = fine
                member = list(Members.select(Members.q.id == transaction.member_id))[0]
                member.debt += fine

            if member.debt > 500:
                return {
                    "message": f"your fine is rupees {fine} , and your debt is {member.debt} which is less than minimum criteria, please RECHARGE otherwise you will be unable to use our services.Thanks for using the book"
                }, 200
            return {
                "message": f"your fine is rupees {fine} , and your debt is {member.debt} thanks for using the book"
            }, 200
        else:
            return {
                "message": "This transaction is now expired kindly give a appropriate transaction id."
            }, 200
    else:
        return {
            "message": "this is a wrong transaction_id, Please provide a valid one"
        }, 404


@operation_api.route("/payment", methods=["POST"])
def fine():
    """
    this is the payment endpoint
    """
    request_data = request.json
    member_id = request_data.get("member_id")
    payment = request_data.get("payment_amount")
    member_list = list(Members.select(Members.q.id == member_id))
    if len(member_list) != 0:
        member = member_list[0]
        member.debt -= payment
        member.total_payment += payment
        return {
            "message": f"{payment} rupee has been transferred and now the remaining debt is {member.debt} "
        }, 200
    return {"message": "This id is not a valid member_id. Please register first."}, 404


@operation_api.route("/popular", methods=["GET"])
def popular():
    """
    this is the popular endpoint
    """
    books = Books.select().orderBy(Books.sqlrepr("popularity"))
    members = Members.select().orderBy(Members.sqlrepr("total_payment"))
    most_popular_book = max(books, key=lambda x: x.popularity).name
    most_paying_member = max(members, key=lambda x: x.total_payment).name
    return {
        "message": f"{most_popular_book} is the most popular book and {most_paying_member} is the most paying member."
    }, 200
