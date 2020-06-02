
from model.off import *
from model.connection import *
from model.database import *
from model.category import *
from model.product import *
from model.category_product import *
from model.favourite import *
from view import *


def initiate_app():
	"""Initiating application"""
	
	
	#Connecting to MySQL server
	db_connection = Connection()
	connection = db_connection.connect_to_dbms()

	#Deleting database
	my_database = Database(connection)
	my_database.drop_database()

	#Retrieving the category list defined by User
	my_category = Category(connection)
	categories = my_category.categories

	#Extracting datas from OFF Api
	off_datas = OpenFoodFacts(categories)
	entire_list = off_datas.get_categories_from_OFF_api()
		
	#Initializing the view
	my_view = View()

	#Creating MySQL database and tables
	database = my_database.database
	database_creation_result = my_database.create_database()
	my_view.show_result_creation_database(database_creation_result, database)
	tables_creation_result = my_database.create_tables()
	my_view.show_result_creation_tables(tables_creation_result)
	#Inserting categories
	insert_data_into_category_result = my_category.insert_categories()
	my_view.show_result_insert_categories(insert_data_into_category_result, categories)
	#Inserting products
	my_product = Product(connection)
	insert_data_into_product_result = my_product.insert_products(entire_list)
	my_view.show_result_insert_products(insert_data_into_product_result, entire_list)
	#Inserting categories_products
	my_category_product = Category_Product(connection)
	result_products, insert_data_into_category_product_result = my_category_product.insert_categories_products()
	my_view.show_result_insert_categories_products(result_products, insert_data_into_category_product_result)


#Launch Initiation
#initiate_app()

def search_save_food():
	"""This method launches the application"""


	#Connecting to MySQL server
	db_connection = Connection()
	connection = db_connection.connect_to_dbms()
	my_database = Database(connection)
	my_view = View()
	#Instanciate object Product
	my_category = Category(connection)
	categories = my_category.categories
	#Categories to show
	cat_list = my_category.list_categories()
	my_view.show_list_categories(cat_list)

	loop1 = True
	while loop1:
		print()
		selected_category = input("Choisissez votre catégorie: ")
		try:
			selected_category = int(selected_category)
		except:
			continue
		if (selected_category < 1 or selected_category > len(categories)):
			continue
		else:
			loop1 = False
	
	my_product = Product(connection)
	prd_list = my_product.list_products(selected_category)
	my_view.show_list_products(prd_list)
	
	loop2 = True
	while loop2:
		print()
		selected_product = input("Choisissez maintenant un produit: ")
		try:
			selected_product = int(selected_product)
		except:
			continue
		if (selected_product < (prd_list[0][0]) or selected_product > (prd_list[len(prd_list)-1][0])):
			continue
		else:
			loop2 = False
	
	result = my_product.find_substitute(selected_category, selected_product)
	substitute_found = my_view.show_substitute(result, selected_product)

	#Saving substitute food is needed	
	if substitute_found:
		record_result = input("Voulez-vous enregistrer ce résultat? (tapez 'O' ou 'o' pour Oui): ")
		if record_result not in ["O","o"]:
			pass
		else:
			my_favourite = Favourite(connection)
			saving_result = my_favourite.save_substitute(selected_category, selected_product, result)
			my_view.show_save_substitute(saving_result)

	
#search_save_food()


def show_saved_substitute_list():
	"""This method shows the list of all saved substitute foods"""
	
	#Connecting to MySQL server
	db_connection = Connection()
	connection = db_connection.connect_to_dbms()
	my_product = Product(connection)
	my_favourite = Favourite(connection)
	my_view = View()
	#Retrieving old product and substitute food and showing the list
	old_prd_result = my_product.retrieve_old_prd()
	substitute_results = my_favourite.list_substitutes()	
	my_view.show_list_saved_substitutes(old_prd_result, substitute_results)


#show_saved_substitute_list()



def test_if_database_exists():
	"""This method tests if the database already exists. If not, it will initiate the app"""

	db_connection = Connection()
	connection = db_connection.connect_to_dbms()
	my_database = Database(connection)
	database = my_database.database
	try:
		cursor = connection.cursor()
		cursor.execute("USE {}".format(database))
	except:
		initiate_app()



































