
import mysql.connector

class Connection:
	"""This class contains credentials to connect to the DBMS"""

	def __init__(self):
		self.username = "ooc_student"
		self.password = "P5_project"
		self.hostname = "localhost"

		
	def databaseConnect(self):
				
		connection = mysql.connector.connect(
			user = self.username,
			password = self.password,
			host = self.hostname)
		return connection
