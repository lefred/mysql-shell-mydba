import __builtin__
from mysqlsh import globals

# to answer https://forums.mysql.com/read.php?101,670682

def __returnDefaults(session, schema, table):
    # Define the query to get the routines
    i_s = session.get_schema("information_schema")
    filters = ["TABLE_SCHEMA = :schema"]
    filters.append("TABLE_NAME = :table")
    stmt = i_s.COLUMNS.select(
        "COLUMN_NAME AS ColName",
        "DATA_TYPE AS DataType",
        "COLUMN_DEFAULT")
    stmt = stmt.where(" AND ".join(filters))
 
    # Execute the query and check for warnings
    stmt = stmt.bind("schema", schema).bind("table", table)
    result = stmt.execute()
    #routines = result.fetch_all()
    defaults = result.fetch_all()
    if (result.get_warnings_count() > 0):
        # Bail out and print the warnings
        print("Warnings occurred - bailing out:")
        print(result.get_warnings())
        return False
    return  defaults
 

def getDefaults(schema, table):
    # Get the session and ensure it is connected
    if not globals.session.is_open():
        print("Please create a connection first.")
        return False
    session=globals.session
    defaults=__returnDefaults(session, schema, table)

    fmt = "| {0:30s} | {1:15s} | {2:50s} | {3:25s} |"
    header = fmt.format("ColumnName","Type","Default","Example")
    bar = "+" + "-" * 32 + "+" + "-" * 17 + "+" + "-" * 52 + "+" + "-" * 27 + "|"
    print bar
    print header
    print bar
    for row in defaults:
        col_expr = row[2]
        if col_expr is None:
            col_expr='NULL'
        else:
            col_expr = col_expr.replace('\\','')
        query = session.sql("select {0}".format(col_expr))
        if col_expr == 'NULL':
            ex_str = col_expr
        else:
            try:
                example = query.execute()
                for col in example.fetch_all():
                    ex_str=str(col[0])
            except:
                ex_str=row[2]
        print fmt.format(row[0], row[1], row[2], ex_str)
    print bar
 
    return "Total: %d" % len(defaults) 

