import mysql.connector
dbconfig = {'host': 'localhost',
            'user': 'root',
            'password': '6206086329@bittu',
            'database': 'vsearchlogdb',}
conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor()

_sql = """ALTER TABLE log RENAME letter TO letters varchar(255)"""

cursor.execute(_sql)
conn.commit()
# _sql="""select * from log"""
# cursor.execute(_sql)
# res = cursor.fetchall()
# for row in res:
#     print(row)
# print(res)
cursor.close()
conn.close()