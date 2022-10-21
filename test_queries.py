import libs

UserName='root'
Password='root'
DatabaseName='alfred_db'
 
# Creating the database connection
db_connection_str = "mysql+pymysql://"+UserName+ ":" +Password +"@mydb/"+ DatabaseName
db_connection = libs.create_engine(db_connection_str)

query = "SELECT id_conta, nome_conta FROM conta WHERE situacao = 'A';"
df_contas = libs.pd.read_sql(query, con=db_connection)

print(df_contas)