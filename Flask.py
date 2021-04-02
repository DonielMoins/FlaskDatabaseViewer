from flask import Flask, request, render_template, redirect, url_for
from markupsafe import Markup
from flask_table import create_table, Col, Table
from functools import cache
import mariadb


# SET DB INFO HERE
# Unecessary Immutable list but it sure makes my code look cooler
# Sorry ive been writing this for about 7 hours now and im almost done
class DB_INFO:
    def __init__(self):
        self.host      =    "localhost"
        self.user      =    "anonymous"
        self.passwd    =    ""
        self.port      =    3306
        self.db_name   =    "test"
        self.pool_name =    "FlaskDatabaseviewer"
        self.pool_size =    10
        # self.database  =    "DATABASE_NAME"

global db_Info
global db_Conn_Pool

def GetConnection(connection_pool):
    try:
        if type(db_Conn_Pool) != None:  
            return connection_pool.get_connection()
        else:
            connection_pool = MakeConnectionPool(db_Info)
            return GetConnection(connection_pool)
    except mariadb.PoolError as e:
        print(f"Error opening connection from pool: {e}")

def MakeConnectionPool(db_info):
        try:
            db_conn_pool =   mariadb.ConnectionPool(
                            user=db_info.user,
                            password=db_info.passwd,
                            host=db_info.host,
                            port=db_info.port,
                            pool_name=db_info.pool_name,
                            pool_size=db_info.pool_size
                        )
            return db_conn_pool
        except mariadb.Error as e:
            return None

db_Info = DB_INFO()
db_Conn_Pool = MakeConnectionPool(db_Info)

# def CheckPool():
#     if type(db_Conn_Pool) is None:
#         db_Conn_Pool = MakeConnectionPool(db_Info)


# Setup Flask App
app = Flask(__name__)

# Declare your table
def build_table(cursor, data):
    
    # classes = ['table', 'table-bordered']
    # no_items    = 'There are no results for this query'
    if type(cursor) != None:
        db_columns = cursor.description
        TableMeta = create_table()
        cols = []
        for db_column in db_columns:
            TableMeta.add_column(str(db_column[0]), Col(str(db_column[0])))
            cols.append(str(db_column[0]))
        tableItems = []
        for rowIndex in range(len(data)):
            row = data[rowIndex]
            rowDict = dict()
            
            for colIndex in range(len(cols)):
                rowDict[cols[colIndex]] = row[colIndex]
            tableItems.append(rowDict)
            
    
    
        
            
    # result = []
    # for value in data:
    #     tmp = {}
    #     for (index,column) in enumerate(value):
    #         tmp[columns[index][0]] = column

    # table = TableMeta()    
    
    table = TableMeta(tableItems)
    table.classes = ['table', 'table-bordered']

    return table
                
    

def get_column_names(cursor):
    return cursor.column_names

# Get some objects

# class Item(object):
#     def __init__(self, name, description):
#         self.name = name
#         self.description = description




# Or, equivalently, some dicts
# items = [dict(name='Name1', description='Description1'),
#          dict(name='Name2', description='Description2'),
#          dict(name='Name3', description='Description3')]

# Initialize a Table with all the items then add it to element list

# items = [Item('Name1', 'Description1'),
#          Item('Name2', 'Description2'),
#          Item('Name3', 'Description3')]
# table = ItemTable(items)

WebElements = []

# Pretty sure we can do this since we dont change much with the webpage 
# TODO: Test it till it breaks
def StupidConcatElements():
    ConcatResult = ""
    for Element in WebElements:
        if isinstance(Element, Table):
            ConcatResult += Element.__html__()
        else:
            try:
                ConcatResult += str(Element)
            except:
                ConcatResult += "ELEMENT ERROR"
    WebElements.clear()
    return Markup(ConcatResult)

# Add function to 
app.jinja_env.globals.update(StupidConcatElements=StupidConcatElements())

# Fallback page for incorrect addresses
@cache
@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def fallbackRedirect(u_path):
    return redirect("/query", code=302)

# Landing Page
@cache
@app.route('/query', methods = ['GET'])
def queryPage(Error=None):
    return render_template("base.html", Error=Error)


# TODO: Save Queries in folder
# TODO: User specific Query folders?
# TODO: Only allow viewing of data

# Check else statement for info on GET method
@app.route('/data', methods = ['POST', 'GET'])
def tablePage():
        if request.method == 'POST':
            # listDicRec(0, request.form)
            
            use_Old_Data = True if "use_Old_Data" in request.form else False
            
            if "requested_Query" in request.form and str(request.form["requested_Query"]) != None and str(request.form["requested_Query"]).strip() != "":     
                requested_Query = request.form["requested_Query"]

                try:
                    curr = GetConnection(db_Conn_Pool).cursor()
                    curr.execute(f"USE {db_Info.db_name};")
                    curr.execute(requested_Query)

                    data = curr.fetchall()

                    table = build_table(curr, data)
                    WebElements.append(table)
                    app.jinja_env.globals.update(Elements=StupidConcatElements())
                    curr.close()
                except mariadb.Error as e:
                    return queryPage(e)
                return render_template("tableDisplay.html")
        # Added GET so that users dont hit a "Method Not Allowed Page" somehow
        return redirect("/query", code=302)

# Debug function
# def listDicRec(lev, data):
#     print("\n") 
#     if data.values() is not None:
#         for i in data:
            
#             if isinstance(i, list):
#                 print((lev*"\t") + i+":",),
#                 listDicRec(lev+1, i)
#             else:
#                 print((lev*"\t"),f"{i}:\t{data[i]}")
#     print("\n")           
#     print("DONE")
            
    


if __name__ == '__main__':
    app.run(debug=True)
