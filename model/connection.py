import mysql.connector

class Connection:
	"""This class holds credentials to connect to MySQL DBMS"""

	def __init__(self):
		self.username = "ooc_student"
		self.password = "P5_project"
		self.hostname = "localhost"

		
	def connect_to_dbms(self):
				
		connection = mysql.connector.connect(
			user = self.username,
			password = self.password,
			host = self.hostname)
		return connection