
class Favourite:
	"""This class deals with all database operations"""

	def __init__(self, connection):
		"""Initializing the class with connection details"""
		
		self.connection = connection
		self.database = "purbeurre"


	def save_substitute(self, selected_category, selected_product, result):
		"""This method will save the substitute food in the database"""
		
		cursor = self.connection.cursor()
		add_favourite = ("INSERT INTO Favourite "
							"(new_prd_barcode,Category_Product_category_id,Category_Product_product_id) "
							"VALUES (%(new_prd_barcode)s, %(Category_Product_category_id)s, %(Category_Product_product_id)s)")
		add_value = {'new_prd_barcode': result[2],
					'Category_Product_category_id': selected_category,
					'Category_Product_product_id': selected_product,}
		try:
			cursor.execute(add_favourite, add_value)
			saving_result = True					
		except:
			saving_result = False
		self.connection.commit()	
		cursor.close()		
		return saving_result


	def list_substitutes(self):
		"""This method lists all substitute that have been saved"""
		
		cursor = self.connection.cursor()
		sql_request = ("SELECT Product.name, Product.description, Product.store, Product.url, Product.nutrition_grade "
						"FROM Favourite INNER JOIN Product "
						"ON Favourite.new_prd_barcode=Product.barcode ")
		cursor.execute(sql_request)
		substitute_results = cursor.fetchall()
		cursor.close()
		return substitute_results
		















