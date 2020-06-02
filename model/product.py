
class Product:
	"""This class deals with all database operations"""


	def __init__(self, connection):
		"""Initializing the class with connection details"""
		
		self.connection = connection
		self.database = "purbeurre"

	
	def insert_products(self, entire_list):
		"""This method populates table Product"""
		
		cursor = self.connection.cursor()	
		try:
			for line in entire_list:				
				add_product = ("INSERT IGNORE INTO Product "
							"(name, description, nutrition_grade, barcode, "
							"url, store, prd_cat, fat, "
							"saturated_fat, sugar, salt)"
							" VALUES (%(name)s, %(description)s, %(nutrition_grade)s, %(barcode)s, "
							"%(url)s, %(store)s, %(prd_cat)s, %(fat)s, "
							"%(saturated_fat)s, %(sugar)s, %(salt)s)")
				add_product_value = {
							'id': cursor.lastrowid,
							'name': line[0],
							'description': line[1],
							'nutrition_grade': line[2],
							'barcode': line[3],
							'url': line[4],
							'store': line[5],
							'prd_cat': line[6],
							'fat': line[7],
							'saturated_fat': line[8],
							'sugar': line[9],
							'salt': line[10],
							}
				cursor.execute(add_product, add_product_value)
			
			insert_data_into_product_result = True
		except:
			insert_data_into_product_result = False		
		self.connection.commit()
		return insert_data_into_product_result


	def list_products(self, selected_category):
		"""This method selects all products that belong to the chosen category"""

		cursor = self.connection.cursor()
		sql_request = ("SELECT id, name, nutrition_grade FROM Product WHERE prd_cat=(%(prd_cat)s)")
		sql_value = {'prd_cat': selected_category,}
		cursor.execute(sql_request, sql_value)
		prd_list = cursor.fetchall()
		cursor.close()
		return prd_list


	def find_substitute(self, selected_category, selected_product):
		"""This method finds a better food than the selected one"""

		cursor = self.connection.cursor(buffered=True)		
		sql_request = ("SELECT name,description,barcode,nutrition_grade,store,url FROM Product"
						" WHERE prd_cat=(%(prd_cat)s) AND "
						"nutrition_grade < (SELECT nutrition_grade FROM Product WHERE id=(%(id)s))")
		sql_value = {'id': selected_product,
					'prd_cat': selected_category,}
		cursor.execute(sql_request,sql_value)
		result = cursor.fetchone()
		cursor.close()
		return result


	def retrieve_old_prd(self):
		"""This method retrieves old product linked to the substitute food"""

		cursor = self.connection.cursor()
		cursor.execute("USE {}".format(self.database))
		sql_request = ("SELECT Product.name "
						"FROM Product INNER JOIN Favourite "
						"ON Product.id=Favourite.Category_Product_product_id ORDER BY id ASC")
		cursor.execute(sql_request)
		old_prd_result = cursor.fetchall()
		cursor.close()
		return old_prd_result
		



	