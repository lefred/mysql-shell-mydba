import __builtin__
from mysqlsh import globals

# initial code from Jesper Wisborg
# visit https://mysql.wisborg.dk/2018/12/02/mysql-8-drop-several-stored-events-procedures-or-functions/

def __returnProcedures(session, schema, routine_type):
    # Define the query to get the routines
    i_s = session.get_schema("information_schema")
    filters = ["ROUTINE_SCHEMA = :schema"]
    if routine_type is not None:
        filters.append("ROUTINE_TYPE = :type")
    stmt = i_s.ROUTINES.select(
        "sys.quote_identifier(ROUTINE_SCHEMA) AS RoutineSchema",
        "sys.quote_identifier(ROUTINE_NAME) AS RoutineName",
        "ROUTINE_TYPE")
    stmt = stmt.where(" AND ".join(filters))
 
    # Execute the query and check for warnings
    stmt = stmt.bind("schema", schema)
    if routine_type is not None:
        stmt = stmt.bind("type", routine_type)
    result = stmt.execute()
    #routines = result.fetch_all()
    routines = result.fetch_all()
    if (result.get_warnings_count() > 0):
        # Bail out and print the warnings
        print("Warnings occurred - bailing out:")
        print(result.get_warnings())
        return False
    return routines
 

def getProcedures(schema, routine_type=None):
    # Get the session and ensure it is connected
    if not globals.session.is_open():
        print("Please create a connection first.")
        return False
    session=globals.session
    routines=__returnProcedures(session, schema, routine_type)

    sql_fmt = "{2} {0}.{1}"
    for routine in routines:
        sql = sql_fmt.format(*routine)
        print(sql)
 
    return "Total: %d" % len(routines) 

def deleteProcedures(schema, routine_type=None, verbose=True):
    # Get the session and ensure it is connected
    if not globals.session.is_open():
        print("Please create a connection first.")
        return False
    session=globals.session
    routines=__returnProcedures(session, schema, routine_type)

    # Drop the routines and check for warnings after each routine
    sql_fmt = "DROP {2} {0}.{1}"
    for routine in routines:
        sql = sql_fmt.format(*routine)
        if verbose:
            print(sql)
 
        drop_result = globals.session.sql(sql).execute()
 
        if (drop_result.get_warnings_count() > 0):
            print("Warnings occurred:")
            print(result.get_warnings())
 
    return "Total dropped: %d" % len(routines)
