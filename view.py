

class View:
	"""This class deals with view methods"""


	def show_result_creation_database(self, database_creation_result, database):
		"""view for create_database method"""

		if database_creation_result:
			print("Database '{}' has been created successfully.".format(database))
		else:
			print("Impossible to create the database '{}'.".format(databse))


	def show_result_creation_tables(self, tables_creation_result):
		"""view for create_tables method"""

		if tables_creation_result:
			print("Tables have been created successfully in the database.")
		else:
			print("Impossible to create the tables in the database.")


	def show_result_insert_categories(self, insert_data_into_category_result, categories):
		"""view for insert_categories method"""

		if insert_data_into_category_result:
			print("{} entries have been inserted in the table 'Category'.".format(len(categories)))
		else:
			print("Impossible to populate table 'Category'")


	def show_result_insert_products(self, insert_data_into_product_result, entire_list):
		"""view for insert_products method"""

		if insert_data_into_product_result:
			print("{} entries have been inserted in the table 'Product'.".format(len(entire_list)))
		else:
			print("Impossible to populate table 'Product'")


	def show_result_insert_categories_products(self, result_products, insert_data_into_category_product_result):
		"""view for insert_categories_products method"""

		if insert_data_into_category_product_result:
			print("{} entries have been inserted in the table 'Category_Product'.".format(len(result_products)))
		else:
			print("Impossible to populate table 'Category_Product'")


	def show_list_categories(self, cat_list):
		"""Showing categories to select"""

		print("************** Catégories des Aliments *****************")
		for category in cat_list:
			print(category[0],"- ",category[1])

		print("********************************************************")


	def show_list_products(self, prd_list):
		"""Showing products to select"""

		print("************** Liste des Produits *****************")

		for prd in prd_list:
			print(prd[0], "- ", prd[1], "--Indice nutritionnel:",prd[2])

		print("********************************************************")


	def show_substitute(self, result, selected_product):
		"""This method shows the list of saved food"""
		
		if not result:			
			print()
			print("Il n'y a pas d'élément meilleur que le votre")
			print()
			substitute_found = False
			
		else:
			print()
			print("-----------------------------------------------------------------------------------------")
			print("Numéro du produit à remplacer:", selected_product)
			print("Nom du meilleur produit:", result[0])
			print("Description du produit: ", result[1])
			print("Code barre: ", result[2])
			print("Indice nutritionnel: ", result[3])
			print("Vente en magasin: ", result[4])
			print("Url du produit: ", result[5])
			print("-----------------------------------------------------------------------------------------")
			print()
			substitute_found = True
		return substitute_found


	def show_save_substitute(self, saving_result):
		"""Shows the result of trying to save the substitute food"""

		if saving_result:
			print()
			print("Substitute food has been saved in the database.")
			print()
		else:
			print()
			print("This substitute food for that product and category has already been saved in the database.")
			print()


	def show_list_saved_substitutes(self, old_prd_result, substitute_results):
		"""view for listing saved susbtitute foods"""
	
		i = 0
		for i in range(len(old_prd_result)):
			old = str(old_prd_result[i]).strip("(',)")
			print("----------------------------------------------------------------------------")
			print("Produit à substituer:",old)
			print("Meilleur produit:",substitute_results[i][0])
			print("Description du meilleur produit:",substitute_results[i][1])
			print("Indice nutritionnel du meilleur produit:",substitute_results[i][4])
			print("Magasin(s) où le trouver:",substitute_results[i][2])
			print("Url du nouveau produit:",substitute_results[i][3])
			print("----------------------------------------------------------------------------")





