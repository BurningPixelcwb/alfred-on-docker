import mysql.connector

mydb = mysql.connector.connect(
  host="mydb",
  user="root",
  password="root",
  database="alfred_db"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT id_conta, nome_conta FROM conta WHERE situacao = 'A';")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)