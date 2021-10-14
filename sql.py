import mysql.connector as database
from decouple import config

sqlhost = config("MYSQL_HOST")
sqluser = config("MYSQL_USER")
sqlpass = config("MYSQL_PASS")
sqldb = config("MYSQL_DB")

def ordinal(n):
  s = ('th', 'st', 'nd', 'rd') + ('th',)*10
  v = n%100
  if v > 13:
    return f'{n}{s[v%10]}'
  else:
    return f'{n}{s[v]}'

def add_data(nick, command):
    connection = database.connect(
        user=sqluser,
        password=sqlpass,
        host=sqlhost,
        port=3306,
        database=sqldb
    )
    cursor = connection.cursor(buffered=True)
    try:
        statement = "INSERT INTO points (nick,command) VALUES (%s, %s)"
        data = (nick, command)
        cursor.execute(statement, data)
        connection.commit()
        print(f"Successfully added entry to database with variables {nick} & {command}")
        connection.close()
    except database.Error as e:
        print(f"Error adding entry to database: {e}")
        connection.close()

def get_data(command,nick):
    connection = database.connect(
        user=sqluser,
        password=sqlpass,
        host=sqlhost,
        port=3306,
        database=sqldb
    )
    cursor = connection.cursor(buffered=True)
    try:
        sql = "SELECT COUNT(*) FROM points WHERE nick = %s AND command = %s"
        args = (nick, command)
        cursor.execute(sql, args)
        result=cursor.fetchone()
        number_of_rows = result[0]
        connection.close()
        return number_of_rows
        
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        connection.close()
        return e

def get_data_command(command):
    connection = database.connect(
        user=sqluser,
        password=sqlpass,
        host=sqlhost,
        port=3306,
        database=sqldb
    )
    cursor = connection.cursor(buffered=True)
    try:
        sql = "SELECT COUNT(*) FROM points WHERE command = %s"
        args = (command,)
        cursor.execute(sql, args)
        result=cursor.fetchone()
        number_of_rows = result[0]
        connection.close()
        return number_of_rows
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        connection.close()
        return e


def get_data_dbleaderboard():
    connection = database.connect(
        user=sqluser,
        password=sqlpass,
        host=sqlhost,
        port=3306,
        database=sqldb
    )
    cursor = connection.cursor(buffered=True)
    try:
        sql = "SELECT nick, COUNT(command) FROM points WHERE command LIKE 'dejabeug' GROUP BY nick ORDER BY COUNT(command) DESC LIMIT 5"
        cursor.execute(sql)
        records = cursor.fetchall()
        connection.close()
        return records
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        connection.close()
        return e