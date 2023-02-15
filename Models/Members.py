from datetime import datetime,timedelta
from sqlobject import *

import os
class Members(SQLObject):
    name=StringCol(length=50,notNone=True,unique=True)
    email=StringCol(length=50,notNone=True,unique=True)
    debt=IntCol(default=0,notNone=True)
    total_payment=IntCol(default=0,notNone=True)