#! /usr/bin/env python3
# coding: utf-8

from connection import *
from database import *
from product import *

# 5 categories choosen for our application
categories = ["Boissons", "Viandes", "Biscuits", "Fromages", "Desserts"]
database = "purbeurre"
entire_list = []

main_loop = True
while main_loop:
	#Initializing the object
	first_product = Product()
	#Connecting to MySQL server
	db_connection = Connection()
	connection = db_connection.databaseConnect()

	try:
		cursor = connection.cursor()
		cursor.execute("USE {}".format(database))
	except:
		#Creating the database and the tables
		new_database = Database()
		new_database.database_tables_creation(connection, database)	
		#Importing requested datas
		first_product.get_categories_from_OFF_api(categories, entire_list)
		#Inserting datas from entire_list
		first_product.datas_insertion(connection, categories, entire_list)
	cursor.close()

	loop1 = True
	# Launching main window
	print("*********************** Application de substitut Alimentaire - Pur Beurre ****************************")
	print()
	print("1 - Quel aliment souhaitez-vous remplacer ?")
	print("2 - Retrouver mes aliments substitués")
	print("3 - Quitter")
	print()
	print("******************************************************************************************************")

	while loop1:		
		print()
		welcome_choice = input("Votre choix de programme: ")
		try:
			welcome_choice = int(welcome_choice)
		except:
			pass

		if welcome_choice not in [1, 2, 3]:
			continue
		else:
			loop1 = False

	if welcome_choice == 1:			
		category_choice = first_product.categories_show(categories)
		prd_to_change = first_product.products_show(category_choice, connection)
		prd_to_change_name = prd_to_change[0]
		prd_to_change_nutrition = prd_to_change[1]
		first_product.substitute_show(category_choice, prd_to_change_name, prd_to_change_nutrition, connection, database)

	if welcome_choice == 2:
		first_product.substitute_list(connection, database)

	if welcome_choice == 3:
		print("Merci d'avoir utilisé ce programme.")
		exit(1)

