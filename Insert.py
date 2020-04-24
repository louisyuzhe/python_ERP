import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    connection = psycopg2.connect(host="localhost",
                                  port = "5432",
                                  user="postgres",
                                  password="yuzhelim",
                                  database="try4")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)

fd = open('users.sql', 'r')
sqlFile = fd.read()
fd.close()

# all SQL commands (split on ';')
sqlCommands = sqlFile.split(';')

# Execute every command from the input file
for command in sqlCommands:
    try:
        cursor.execute(command)
    except (Exception, psycopg2.Error) as error:
        print("ERROR",error)

cursor.close()
connection.close()

