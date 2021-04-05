from flask_table import create_table, Col, Table

# Declare your table
def build_table(cursor, data):
    if cursor is not None:
        db_columns = cursor.description
        TableMeta = create_table()

        # Create list with all the table columns
        cols = []
        for db_column in db_columns:
            val = str(db_column[0])
            TableMeta.add_column(val, Col(val))
            cols.append(val)
        
        #Add rows
        tableItems = []
        for rowIndex in range(len(data)):
            row = data[rowIndex]
            rowDict = dict()
            
            for colIndex in range(len(cols)):
                rowDict[cols[colIndex]] = row[colIndex]
            tableItems.append(rowDict)
        table = TableMeta(tableItems)
        table.classes   = ['table', 'table-bordered']
        table.no_items  = 'There are no results for this query'
        return table
    raise Exception("Cursor cannot be NoneType")
    
    
def get_column_names(cursor):
    return cursor.column_names


def isTable(table):
    return isinstance(table, Table)