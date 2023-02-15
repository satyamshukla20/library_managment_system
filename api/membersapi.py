from flask import Flask, jsonify, request, Blueprint
import requests, json
from datetime import datetime, timedelta
from sqlobject import *
from Models.Book import Books
from Models.Members import Members
from Models.Transactions import Transactions
import os

member_api = Blueprint("memberApi", __name__)


@member_api.route("/member", methods=["POST"])
def loadmembers():
    """
    this is the load_members endpoint
    """
    if request.method == "POST":
        name = request.json.get("name")
        email = request.json.get("email")
        try:
            Members(name=name, email=email)
            return {"message": "The user is successfully registered as member."}
        except:
            return {"message": "This user already exists."}


@member_api.route("/member", methods=["GET"])
def get_members():
    """
    this is the get_members endpoint
    """
    members = Members.select()
    list_of_member = []
    for member in members:
        list_of_member.append(
            {"id": member.id, "name": member.name, "email": member.email}
        )
    return {"members": list_of_member}


@member_api.route("/member/<id>", methods=["DELETE"])
def member_delete(id):
    """
    this is the delete_members endpoint
    """
    try:
        member = Members.get(id)
    except SQLObjectNotFound:
        return {"message": "please enter a valid id"}
    
    if member.debt > 0:
        return {
            "message": f"{member.name} with {id} as id has current debt of {member.debt} please pay the remaining amount."
        }
    id=int(id)
    list_of_transaction=list(Transactions.select(Transactions.q.member_id==id))
    if len(list_of_transaction)>0:
        for transaction in list_of_transaction:
            if transaction.transaction_status==1:
                return {"message":"This user cannot be deleted because he has issued a book."}
    id=str(id)
    member.delete(id)
    
    return {
        "message": f"{member.name} with {id} as id is deleted now you are no longer member of the library."
    }


@member_api.route("/member/<id>", methods=["PUT"])
def member_update(id):
    """
    this is the update endpoint
    """
    try:
        member = Members.get(id)
    except SQLObjectNotFound:
        return {"message": "please enter a valid user id"}
    request_data = request.json
    try:
        member.name = request_data.get("name")
    except:
        return {"message": "This user name already exist"}
    try:
        member.email = request_data.get("email")
        return f"member id : {id} has been updated"
    except:
        return {"message": "This email id already exist"}
