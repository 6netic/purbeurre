from os import path

class Database:
	"""This class deals with all database operations"""

	def __init__(self, connection):
		"""Initializing the class with connection details"""
		
		self.connection = connection
		self.data_file = "tables.sql"
		self.database = "purbeurre"


	def create_database(self):
		"""This method creates the database"""
		
		cursor = self.connection.cursor()
		try:
			cursor.execute("CREATE DATABASE IF NOT EXISTS {} CHARACTER SET 'utf8'".format(self.database))	
			database_creation_result = True				
		except:
			database_creation_result = False
		cursor.close()
		return database_creation_result

	def create_tables(self):
		"""This method creates the 4 tables from a SQL file"""
		
		cursor = self.connection.cursor()
		try:
			directory = path.dirname(path.dirname(__file__))
			path_to_file = path.join(directory, "data", self.data_file)
			for line in open(path_to_file):
				cursor.execute(line)
			tables_creation_result = True
		except:
			tables_creation_result = False	
		cursor.close()
		return tables_creation_result

	
	def drop_database(self):
		"""This method drops database 'purbeurre' """

		cursor = self.connection.cursor()
		cursor.execute("DROP DATABASE IF EXISTS {}".format(self.database))
		cursor.close()


	


	
	


	

























		