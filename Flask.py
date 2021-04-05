# import all the py file because we need a reference to the vars 
# when using from ? import var, it makes a copy of the var's value instead
# We need a reference so that we can access this var from wherever, in case we need it.
from flask import Flask, request, render_template, redirect, url_for
import multiprocessing.managers


from markupsafe import Markup
from functools import cache
from helper.db_helper import DB_INFO, MakeConnectionPool, GetConnection
from config import db_settings
from helper.table_helper import build_table, get_column_names, isTable
from multiprocessing.managers import DictProxy
from dataTypes.multiprocessing import DataCouple

from dataManager import startDataManager, ConnectionPool


# Setup Flask App
app             = Flask(__name__)
memoryManager   = multiprocessing.Manager()

db_Info = None
db_Conn_Pool = None

# class Flask:
#     # def __init__(self, namespaces, accessEvents):
#     #     self.namespaces = namespaces
#     #     self.accessEvents = accessEvents
#     #     for namespace in namespaces:
#     #         if namespace == "db":
#     #             self += namespace
            
#     def __init__(self, DataCoupleDict: DictProxy):
#         for value in DataCoupleDict.values():
#             print(value.namespace.values())
        
#         # for key, dataCouple in iter(DataCoupleDict):
            
#         #     if str(key) is "db":
#         #         dc.namespace["db_Info"], self.db_Info = DB_INFO(db_settings, "   ", "TEST")
#         #         dc.namespace["db_Conn_Pool"], self.db_Conn_Pool = MakeConnectionPool(self.db_Info)
#         super().__init__()
   
WebElements = []
# Pretty sure we can do this since we dont change much with the webpage 
# TODO: Test it till it breaks
@cache
def ConcatElements():
    ConcatResult = ""
    for Element in WebElements:
        if isTable(Element):
            ConcatResult += Element.__html__()
        else:
            try:
                ConcatResult += str(Element)
            except:
                ConcatResult += "ELEMENT ERROR"
    WebElements.clear()
    return Markup(ConcatResult)

# Fallback page for incorrect addresses
@cache
@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def fallbackRedirect(u_path):
    return redirect("/query", code=302)

# Landing Page
@cache
@app.route('/query', methods = ['GET'])
def queryPage(E=None):
    if ConcatElements() not in app.jinja_env.globals:
        app.jinja_env.globals.update(Elements=ConcatElements())
    return render_template("base.html", Error=E)
# TODO: Save Queries in folder
# TODO: User specific Query folders?
# TODO: Only allow viewing of data
# Check else statement for info on GET method

@app.route('/data', methods = ['POST', 'GET'])
def tablePage():
    if request.method == 'POST':
        # listDicRec(0, request.form)
        # Im thinking this isnt even useful
        # use_Old_Data = True if "use_Old_Data" in request.form else False
        if "requested_Query" in request.form and str(request.form["requested_Query"]) != None and str(request.form["requested_Query"]).strip() != "":     
            requested_Query = request.form["requested_Query"]
            try:
                # 
                curr = GetConnection(db_Info, db_Conn_Pool).cursor()
                curr.execute(f"USE {db_Info.db_name};")
                curr.execute(requested_Query)
                data = curr.fetchall()
                table = build_table(curr, data)
                WebElements.append(table)
                app.jinja_env.globals.update(Elements=ConcatElements())
                curr.close()
            except Exception as e:
                return queryPage(e)
            return render_template("tableDisplay.html")
    # Added GET so that users dont hit a "Method Not Allowed Page" somehow
    return redirect("/query", code=302)
    
# def startFlask(self, data):
#     global db_Info
#     global db_Conn_Pool
#     globals().update(db_Info, DB_INFO(db_settings)
#     globals()["db"].db_Conn_Pool, db_Conn_Pool = MakeConnectionPool(db_Info)
    
data = startDataManager(memoryManager)
DataCouplesProxy = dict([dc for dc in data.items()])

DataCouples = [DataCouplesProxy[key].get() for key in DataCouplesProxy.keys()]

namespaceDict = list()

for DataCouple in DataCouples:
    namespaceDict.append(DataCouple.namespace._getvalue().__dict__)
namespaceDict = namespaceDict.pop(namespaceDict.__len__() - 1)
for varName in namespaceDict:    
    if db_Info == None:
        connPool = MakeConnectionPool(namespaceDict["db_Info"].get())
        memoryManager.Value(type(ConnectionPool), connPool)
        namespaceDict[varName].set() 
    globals()[varName] = namespaceDict[varName]

print("all ready")
