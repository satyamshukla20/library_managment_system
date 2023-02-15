from flask import Flask,jsonify
from datetime import datetime,timedelta
from sqlobject import *

import os
class Books(SQLObject):
    """
    book table for library
    """
    name=StringCol(length=50,notNone=True,unique=True)
    author=StringCol(length=50,notNone=True,unique=True)
    quantity=IntCol(notNone=True ,default= 30)
    popularity=IntCol(default = 0 , notNone=True)
