import mariadb
import sys
import os 
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('DB_User')
password = os.getenv('DB_Password')
host = os.getenv('DB_Host')
port = int(os.getenv('DB_Port'))

try:
	conn = mariadb.connect(
		user=user,
		password=password,
		host=host,
  		port=port,
  		database="memo"
	)

except mariadb.Error as e:
	print(f"Error connecting to MariaDB Platform: {e}")
	sys.exit(1)

cur = conn.cursor()

# ---------------

# cur.execute("CREATE TABLE test (ID int PRIMARY KEY AUTO_INCREMENT, Content TEXT)")
Q_test = "INSERT INTO test (Content) VALUES (%s)"
cur.execute(Q_test,("huitre acajou",))
cur.execute("COMMIT")

cur.execute("SELECT * FROM test")

for x in cur :
	print(x)
# cur.execute("DROP TABLE test")

# ---------------


# Q1 = "CREATE TABLE Horaire (ID int PRIMARY KEY AUTO_INCREMENT, DateCreated DATETIME, DatePlanned DATETIME, CONSTRAINT UC_Date UNIQUE (DateCreated,DatePlanned))"
# Q2 = "CREATE TABLE Info (idMessage BigInt PRIMARY KEY, idHoraire int, idGuild BigInt, idChannel BigInt, idInvoker BigInt, Content TEXT, FOREIGN KEY(idHoraire) REFERENCES Horaire(ID) ON DELETE CASCADE, UNIQUE(idMessage))"

# Q_Add_Horaire = "INSERT INTO Horaire (DateCreated,DatePlanned) VALUES (%s,%s)"
# Q_Add_Requete = """INSERT INTO Info (idMessage, idHoraire, idGuild, idChannel, idInvoker, Content) 
# 				   VALUES (%s,(SELECT ID FROM Horaire WHERE DateCreated = %s and DatePlanned = %s),%s,%s,%s,%s)"""


# DateCreated = "2017-05-13 07:58"
# DatePlanned = "2017-05-13 07:59"
# idInvoker = 444444444444444444
# idMessage = 333333333333333333
# idGuild   = 222222222222222222
# idChannel = 111111111111111111
# Content = "Salut les bros c lrb"

# cur.execute(Q1)
# cur.execute(Q2)

# ---------------

# try :
#     cur.execute(Q_Add_Horaire,(DateCreated,DatePlanned))
# except:
#     print("Doublon")

# cur.execute(Q_Add_Requete,(idMessage,DateCreated,DatePlanned,idGuild,idChannel,idInvoker,Content))

# cur.execute("DELETE From Info") # Supprime tout
# cur.execute("DELETE From Horaire") 

# cur.execute("DROP TABLE Info")
# cur.execute("DROP TABLE Horaire")

# cur.execute("DELETE FROM Horaire")
# cur.execute("SELECT DATE_FORMAT(DateCreated, '%d/%m/%Y - %H:%i') FROM Horaire")
# cur.execute("SELECT DATE_FORMAT(DateCreated,'Crée %Y/%m/%d a %H:%i'),DATE_FORMAT(DatePlanned,'Prévu %Y/%m/%d a %H:%i'),Content FROM Horaire INNER JOIN Info ON Horaire.ID = Info.idHoraire")

# cur.execute("SHOW TABLES")
# cur.execute("SELECT DATE_FORMAT(DatePlanned,'%Y/%m/%d a %H:%i') FROM Horaire ORDER BY DatePlanned DESC")

# cur.execute("SELECT TIMESTAMPDIFF(MINUTE,'2020-05-13 07:58',DatePlanned) FROM Horaire WHERE TIMESTAMPDIFF(MINUTE,'2020-05-13 07:58',DatePlanned) > 100000")
# Q_Delete = """
# 			DELETE
# 			FROM INFO 
# 		   """
# for x in cur:
# 	print(x)

# cur.execute("COMMIT")