import mysql.connector
from mysql.connector import errorcode

class Category:
	"""This class deals with all database operations"""

	def __init__(self, connection):
		"""Initializing the class with connection details"""
		
		self.connection = connection
		self.database = "purbeurre"
		self.categories = ["Boissons", "Viandes", "Biscuits", "Fromages", "Desserts"]


	def insert_categories(self):
		"""This method populates table Category"""
		
		cursor = self.connection.cursor()	
		# Populating table 'Category' 
		try:
			for one_category in self.categories:
				add_category = ("INSERT IGNORE INTO Category (name) VALUES (%(name)s)")
				category_value = {'id': cursor.lastrowid, 'name': one_category,}
				cursor.execute(add_category, category_value)
			insert_data_into_category_result = True	
		except:
			insert_data_into_category_result = False
		
		self.connection.commit()
		return insert_data_into_category_result


	def list_categories(self):
		"""This method selects all categories"""

		cursor = self.connection.cursor()
		cursor.execute("USE {}".format(self.database))
		sql_request = ("SELECT * FROM Category ORDER BY id ASC")
		cursor.execute(sql_request)
		cat_list = cursor.fetchall()
		cursor.close()
		return cat_list


	

	









