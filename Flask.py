from flask import Flask, request
from markupsafe import Markup
from flask_table import Table, Col


app = Flask(__name__)

WebElements = []


# Declare your table
class ItemTable(Table):
    name = Col('Name')
    description = Col('Description')
    options = {'border': '1'}


# Get some objects
class Item(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description

# items = [Item('Name1', 'Description1'),
#          Item('Name2', 'Description2'),
#          Item('Name3', 'Description3')]
# Or, equivalently, some dicts
items = [dict(name='Name1', description='Description1'),
         dict(name='Name2', description='Description2'),
         dict(name='Name3', description='Description3')]

# items = ItemModel.query.all()
table = ItemTable(items)


def ConcatElements():
    ConcatResult = "FUNWORK"
    for Element in WebElements:
        ConcatResult += str(Element)
    
    return str(ConcatElements)

@app.route('/')
def webapp_display():
    return ConcatElements()