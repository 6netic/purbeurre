
import requests
import mysql.connector
from mysql.connector import errorcode
from connection import *

class Product:
	"""This class defines object Product and contains its methods."""

	def get_categories_from_OFF_api(self, categories, entire_list):

		double = []
		for category in categories:	

			payload = {
				"action": "process",
				"tagtype_0": "categories",
				"tag_contains_0": "contains",
				"tag_0": category,
				"page_size": "100",
				"json": "1"
			}

			my_request = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=payload)
			result = my_request.json()
			my_products = result["products"]

			i = 0
			# Browsing the list of products
			for my_product in my_products:
				
				#Creating a list containing each line of products
				products_list = []

				try:
					products_list.append(my_product["product_name_fr"])
					products_list.append(my_product["generic_name"])
					products_list.append(my_product["nutrition_grades"])
					products_list.append(my_product["code"])
					products_list.append(my_product["url"])
					products_list.append(my_product["stores"])
					products_list.append(categories.index(category) + 1)
					products_list.append(my_product["nutriments"]["fat_100g"])
					products_list.append(my_product["nutriments"]["saturated-fat_100g"])
					products_list.append(my_product["nutriments"]["sugars_100g"])
					products_list.append(my_product["nutriments"]["salt_100g"])
					double.append(products_list[3])
					
				except KeyError:
					pass

				else:			
					# Let's be sure we take only one occurence
					if double.count(my_product["code"]) == 2:
						pass
					else:
						entire_list.append(products_list)
						i += 1
					
					if i == 100:
						break
		
		return entire_list


	def datas_insertion(self, connection, categories, entire_list):

		cursor = connection.cursor()
		
		# Populating 'Category' table
		try:
			for one_category in categories:
				add_category = ("INSERT INTO Category "
							"(name) "
							"VALUES (%(name)s)")
				category_value = {
							'id': cursor.lastrowid,
							'name': one_category,
							}
				cursor.execute(add_category, category_value)
		except:
			pass
		else:
			print("{} categories have been inserted in the 'Category' table.".format(len(categories)))	
		
		# Populating table 'Product'
		try:
			for line in entire_list:
				
				add_category = ("INSERT INTO Product "
							"(name, description, nutrition_grade, barcode, "
							"url, store, prd_cat, fat, "
							"saturated_fat, sugar, salt)"
							" VALUES (%(name)s, %(description)s, %(nutrition_grade)s, %(barcode)s, "
							"%(url)s, %(store)s, %(prd_cat)s, %(fat)s, "
							"%(saturated_fat)s, %(sugar)s, %(salt)s)")
				category_value = {
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
				cursor.execute(add_category, category_value)

		except:
			pass
		else:
			print("{} entries have been inserted in the 'Product' table.".format(len(entire_list)))

		connection.commit()


	def categories_show(self, categories):
		
		print("************** Catégories des Aliments *****************")
		i_number = []
		for i, elt in enumerate(categories):
			print("{} - {}".format(i+1, elt))
			i_number.append(i+1) 
		print("********************************************************")
		
		loop2 = True
		while loop2:
			print()
			category_choice = input("Votre choix de catégorie: ")
			try:
				category_choice = int(category_choice)
			except:
				pass
			if category_choice not in i_number:
				continue
			else:
				loop2 = False

		return category_choice


	def products_show(self, category_choice, connection):
		
		cursor = connection.cursor()
		sql_request = ("SELECT name,nutrition_grade FROM Product WHERE prd_cat=(%(prd_cat)s)")
		sql_value = {'prd_cat': category_choice,}
		cursor.execute(sql_request, sql_value)

		# Executing SELECT request depending on chosen category
		myresult = cursor.fetchall()
		i = 0
		total = []

		for w in myresult:
			prd_line = []
			i += 1
			print(i,"- ",w[0]," - Indice nutritionnel:",w[1])
			prd_line.append(w[0])
			prd_line.append(w[1])
			total.append(prd_line)
		
		loop3 = True
		while loop3:
			print()
			product_choice = input("Votre choix de produit: ")
			try:
				product_choice = int(product_choice)
			except:
				pass
			if product_choice not in range(1, (i+1)):
				continue
			else:
				loop3 = False

		choosen_prd = total[product_choice-1]		
		depreciated_product = choosen_prd[0]
		depreciated_nutrition = choosen_prd[1]

		cursor.close()
		return depreciated_product, depreciated_nutrition


	def substitute_show(self, category_choice, prd_to_change_name, prd_to_change_nutrition, connection, database):
		
		cursor = connection.cursor(buffered=True)
		cursor.execute("USE {}".format(database))

		sql_request = ("SELECT name,description,barcode,nutrition_grade,store,url FROM Product"
						" WHERE prd_cat=(%(prd_cat)s) AND nutrition_grade < (%(nutrition_grade)s)")
		sql_value = {'prd_cat': category_choice,
					'nutrition_grade': prd_to_change_nutrition,}
		cursor.execute(sql_request,sql_value)
		result = cursor.fetchone()

		if not result:			
			print()
			print("Il n'y a pas d'élément meilleur que le votre")
			print()
			cursor.close()
			connection.close()
		else:
			print()
			print("-----------------------------------------------------------------------------------------")
			print("Produit à remplacer:", prd_to_change_name, "avec un indice nutritionnel: ", prd_to_change_nutrition)
			print("Nom du meilleur produit: ", result[0])
			print("Description du produit: ", result[1])
			print("Indice nutritionnel: ", result[3])
			print("Vente en magasin: ", result[4])
			print("Url du produit: ", result[5])
			print("-----------------------------------------------------------------------------------------")
			print()
			
			record_result = input("Voulez-vous enregistrer ce résultat? (tapez 'O' ou 'o' pour Oui): ")
			if record_result not in ["O","o"]:
				pass
			else:
				add_favourite = ("INSERT INTO Favourite "
								"(prd_to_be_replaced,barcode) "
								"VALUES (%(prd_to_be_replaced)s, %(barcode)s)")
				add_value = {
							'prd_to_be_replaced': prd_to_change_name,
							'barcode': result[2],
							}
				try:
					cursor.execute(add_favourite, add_value)					
				except:
					print()
					print("Ce produit de substitution a déjà été enregistré !.")
					print()
				else:
					connection.commit()
					print()
					print("Ce nouveau produit a bien été enregistré dans la base.")
					print()
					cursor.close()
					connection.close()


	def substitute_list(self, connection, database):

		cursor = connection.cursor()
		cursor.execute("USE {}".format(database))
		sql_request = ("SELECT Favourite.prd_to_be_replaced, Product.name, Product.description, Product.store, Product.url, Product.nutrition_grade "
						"FROM Favourite INNER JOIN Product "
						"ON Favourite.barcode=Product.barcode ")
				
		cursor.execute(sql_request)
		results = cursor.fetchall()

		for result in results:
			print("----------------------------------------------------------------------------------------")
			print("Produit à substituer:",result[0])
			print("Meilleur produit:",result[1])
			print("Description du produit:",result[2])
			print("Indice nutritionnel:",result[5])
			print("Magasin(s) où le trouver:",result[3])
			print("Lien Web du produit:",result[4])
			print("----------------------------------------------------------------------------------------")

		cursor.close()
		connection.close()









