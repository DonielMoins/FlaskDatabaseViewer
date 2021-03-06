# import all the py file because we need a reference to the vars 
# when using from ? import var, it makes a copy of the var's value instead
# We need a reference so that we can access this var from wherever, in case we need it.
from helper.db_helper import DB_INFO, MakeConnectionPool, GetConnection
from helper.table_helper import build_table, isTable
from flask import Flask, request, render_template, redirect, url_for
from markupsafe import Markup
from config import db_settings, sqlSuffix
from config import debug as debugFlask
from os import path, walk, getcwd


# Setup Flask App
app = Flask(__name__)


db_Info = DB_INFO(db_settings)
db_Conn_Pool = MakeConnectionPool(db_Info)

WebElements = []
# Pretty sure we can do this since we dont change much with the webpage 
# TODO: Test it till it breaks


def ConcatElements():
    ConcatResult = ""
    for Element in WebElements:
        if isTable(Element):
            ConcatResult += Element.__html__()
        else:
            try:
                ConcatResult += str(Element)
            except Exception:
                ConcatResult += "ELEMENT ERROR"
    WebElements.clear()
    return Markup(ConcatResult)

# Fallback page for incorrect addresses


@app.route('/', defaults={'u_path': ''})
@app.route('/<path:u_path>')
def fallbackRedirect(u_path):
    return redirect("/query", code=302)

# Landing Page


@app.route('/query', methods=['GET'])
def queryPage(error=""):
    if SQLfilesMarkup(dirDict) not in app.jinja_env.globals:
        app.jinja_env.globals.update(sqlFiles=SQLfilesMarkup(dirDict))
    if ConcatElements() not in app.jinja_env.globals:
        app.jinja_env.globals.update(Elements=ConcatElements())
    return render_template("base.html", Error=error)
# TODO: Save Queries in folder
# TODO: User specific Query folders?
# TODO: Only allow viewing of data
# Check else statement for info on GET method


@app.route('/data', methods=['POST', 'GET'])
def tablePage():
    app.jinja_env.globals.update(sqlFiles=SQLfilesMarkup(dirDict))
    if request.method == 'POST':
        # listDicRec(0, request.form)
        # Im thinking this isnt even useful
        # use_Old_Data = True if "use_Old_Data" in request.form else False
        if "sqlFile" in request.form and \
             str(request.form["sqlFile"]) is not None and \
                str(request.form["sqlFile"]).strip() != "":
            sqlFile = request.form["sqlFile"]
            try:
                # 
                curr = GetConnection(db_Info, db_Conn_Pool).cursor()
                curr.execute(f"USE {db_Info.db_name};")
                f = open(sqlFile)
                for line in f.readlines():
                    curr.execute(line)
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

def SQLfilesMarkup(dirDict):
    result = "<form action = \'"+ url_for('tablePage') + "\' method = \'post\'>\n"
    for key in dirDict.keys():
        result += f"<button id=\'{dirDict.get(key)}\' name=\'sqlFile\' value=\'{dirDict.get(key)}\' type = \'submit\' class =\'mdl-cell mdl-cell--3-col mdl-button resize mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent material-icons\'>" + key + "</button>\n"
        result += f"<div class='mdl-tooltip mdl-tooltip--large' for='{dirDict.get(key)}' style='overflow-wrap: anywhere;'>File: {dirDict.get(key)} </div>\n"
    result += "</form>"
    return Markup(result)
dirDict = {}

# Checks every dir from location specified for file
#  that ends with any suffix from config.sqlSuffix 
# (imported as just sqlSuffix), recursively. 
def getSQLfiles(loc):
    
    dictionary = {}
    dirnames, filenames = [], []

    for (__dirpath, _dirnames, _filenames) in walk(loc):
        dirnames.extend(_dirnames)
        filenames.extend(_filenames)
        break
    
    for filename in filenames:
        for suffix in sqlSuffix:
            if str(filename).endswith(suffix ):
                dictionary[filename] = path.join(loc, filename) 
                
    for dirname in dirnames:
        recLoc = path.join(loc, dirname)
        recResult = getSQLfiles(recLoc) 
        if recResult is not None: dictionary[recLoc] = recResult
        
    if any(dictionary.values()):
        return dictionary  
    else: return 
    
    

dirDict = getSQLfiles(getcwd())




if __name__ == "__main__":
    # ray.init(num_cpus=num_cpus, local_mode=True)

    # run.remote()
    
    app.run(debug=debugFlask)

