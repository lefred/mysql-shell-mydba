import __builtin__
from mysqlsh import globals

# see https://lefred.be/content/mysql-when-will-the-password-of-my-users-expire/

def getPasswordExpiration(show_expired=True):
    # Get the session and ensure it is connected
    if not globals.session.is_open():
        print("Please create a connection first.")
        return False
    session=globals.session
    if show_expired:
        stmt = """select concat(sys.quote_identifier(user),'@',sys.quote_identifier(host)), 
              password_last_changed, IF((cast(
              IFNULL(password_lifetime, @@default_password_lifetime) as signed)
              + cast(datediff(password_last_changed, now()) as signed) > 0),
              concat(
               cast(
              IFNULL(password_lifetime, @@default_password_lifetime) as signed)
              + cast(datediff(password_last_changed, now()) as signed), ' days'), 'expired') expires_in
              from mysql.user
              where 
              user not like 'mysql.%'"""
    else:
        stmt = """select concat(sys.quote_identifier(user),'@',sys.quote_identifier(host)), 
              password_last_changed,
              concat(
               cast(
              IFNULL(password_lifetime, @@default_password_lifetime) as signed)
              + cast(datediff(password_last_changed, now()) as signed), ' days') expires_in
              from mysql.user
              where 
              cast(
               IFNULL(password_lifetime, @@default_password_lifetime) as signed)
              + cast(datediff(password_last_changed, now()) as signed) >= 0 
              and user not like 'mysql.%';"""
    
    query = session.sql(stmt)
    result = query.execute()
    accounts = result.fetch_all()
    fmt = "| {0:30s} | {1:30s} | {2:15s} |"
    header = fmt.format("User","Password last change","Expires in")
    bar = "+" + "-" * 32 + "+" + "-" * 32 + "+" + "-" * 17 + "+"
    if len(accounts) > 0:
        print bar
        print header
        print bar
    for account in accounts:
        sql = fmt.format(*account)
        print(sql)
    if len(accounts) > 0:
        print bar
 

