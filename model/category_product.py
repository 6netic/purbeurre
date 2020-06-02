
class Category_Product:
	"""This class deals with ........"""

	def __init__(self, connection):
		"""Initializing the class with connection details"""
		
		self.connection = connection
		self.database = "purbeurre"


	def insert_categories_products(self):
		"""This method populates table Category_Product"""

		cursor = self.connection.cursor()
		cursor.execute("SELECT prd_cat,id FROM Product")
		result_products = cursor.fetchall()
		try:
			for result in result_products:
				sql_insert = ("INSERT IGNORE INTO Category_Product (category_id, product_id)"
								" VALUES (%(category_id)s, %(product_id)s)")
				sql_insert_value = { 'category_id': result[0],
									'product_id': result[1],}
				cursor.execute(sql_insert, sql_insert_value)
			insert_data_into_category_product_result = True
		except:
			insert_data_into_category_product_result = False		
		self.connection.commit()
		return result_products, insert_data_into_category_product_result


	

