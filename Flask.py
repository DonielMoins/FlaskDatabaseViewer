# import all the py file because we need a reference to the vars 
# when using from ? import var, it makes a copy of the var's value instead
# We need a reference so that we can access this var from wherever, in case we need it.
from helper.db_helper import DB_INFO, MakeConnectionPool, GetConnection
from helper.table_helper import build_table, isTable
from flask import Flask, request, render_template, redirect
from markupsafe import Markup
from shared.varsClass import VarsClass
import ray
import psutil

# from os import name
# if name == 'linux':
#    import pyarrow.plasma as plasma
# elif name == 'win32':
#    import multiprocessing as deps
# del name

num_cpus = psutil.cpu_count(logical=False)

# store = plasma.start_plasma_store("/tmp/plasma")
# client = plasma.connect("/tmp/plasma")
# Setup Flask App
app = Flask(__name__)

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
    if ConcatElements() not in app.jinja_env.globals:
        app.jinja_env.globals.update(Elements=ConcatElements())
    return render_template("base.html", Error=error)
# TODO: Save Queries in folder
# TODO: User specific Query folders?
# TODO: Only allow viewing of data
# Check else statement for info on GET method


@app.route('/data', methods=['POST', 'GET'])
def tablePage():
    if request.method == 'POST':
        # listDicRec(0, request.form)
        # Im thinking this isnt even useful
        # use_Old_Data = True if "use_Old_Data" in request.form else False
        if "requested_Query" in request.form and \
             str(request.form["requested_Query"]) is not None and \
                str(request.form["requested_Query"]).strip() != "":
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


def setupRay():
    ray.init(num_cpus=num_cpus, local_mode=True)
    dbI = DB_INFO({
            "host": "localhost",
            "user": "root",
            "passwd": "default",
            "port": 3306,
            "db_name": "db_name",
            "pool_name": "pool_name",
            "pool_size": 10,
    })
    db_Info = ray.put(dbI)
    db_Conn_Pool = ray.put(MakeConnectionPool(dbI))
    print(ray.objects().values())


if __name__ == "Flask":
    # ray.init(num_cpus=num_cpus, local_mode=True)

    # run.remote()
    setupRay()

app.run(debug=True)
