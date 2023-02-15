# from flask import Flask,jsonify
from datetime import datetime,timedelta
from sqlobject import *

class Transactions(SQLObject):
    book_id=IntCol(notNone=True)
    member_id=IntCol(notNone=True)
    date_from=DateTimeCol(default=datetime.utcnow)
    fine=IntCol(default=0)
    transaction_status=IntCol(default=1,notNone=True)