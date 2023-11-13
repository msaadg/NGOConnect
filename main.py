import pyodbc
connection = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};SERVER=localhost;DATABASE=NGOConnect;UID=sa;PWD=Password.1;TrustServerCertificate=yes;Connection Timeout=30;'
)

cursor = connection.cursor()

select_query = "SELECT * FROM ngo"
cursor.execute(select_query)

for row in cursor:
    print(row)

connection.close()
