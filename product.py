
import requests
from constants import *
import mysql.connector
from mysql.connector import errorcode

class Product:
	"""This class will initiate and give all the methods for the class Product"""

	def __init__(self):
		Product.saved_code = 0
		Product.category_choice = 0
		self.entire_list = []


	def get_categories_from_OFF_api(self, categories):

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
						self.entire_list.append(products_list)
						i += 1
					
					if i == 100:
						break
		
		return self.entire_list


	def database_tables_creation(self):
		
		# Establishing a connection	
		connection1 = mysql.connector.connect(
				user = user,
				password = password,
				host= host)

		cursor = connection1.cursor()

		tables = {}  # Creating a dictionnary to store the tables

		tables['Category'] = (
		    "CREATE TABLE IF NOT EXISTS `Category` ("
		    "  `id` TINYINT(1) UNSIGNED NOT NULL AUTO_INCREMENT,"
		    "  `name` VARCHAR(20) NOT NULL,"
		    "  PRIMARY KEY (`id`),"
		    "  UNIQUE INDEX ind_uni_cat (name)"
		    ") ENGINE=InnoDB CHARACTER SET = 'utf8mb4'")

		tables['Product'] = (
			"CREATE TABLE IF NOT EXISTS `Product` ("
		    "  `id` SMALLINT NOT NULL AUTO_INCREMENT,"
		    "  `name` VARCHAR(255),"
		    "  `description` VARCHAR(255),"
		    "  `nutrition_grade` CHAR(1),"
		    "  `barcode` VARCHAR(250) NOT NULL,"
		    "  `url` VARCHAR(255),"
		    "  `store` VARCHAR(255),"
		    "  `prd_cat` TINYINT(1) UNSIGNED,"
		    "  `fat` DECIMAL(5,2) UNSIGNED,"
		    "  `saturated_fat` DECIMAL(5,2) UNSIGNED,"
		    "  `sugar` DECIMAL(5,2) UNSIGNED,"
		    "  `salt` DECIMAL(5,2) UNSIGNED,"
		    "  PRIMARY KEY (`id`),"
		    "  INDEX ind_nutri (nutrition_grade),"
			"  UNIQUE INDEX ind_uni_code (barcode),"
		    "  CONSTRAINT fk_prd_cat FOREIGN KEY (prd_cat) REFERENCES Category(id)"	    
		    ") ENGINE=InnoDB CHARACTER SET = 'utf8mb4'")
				
		tables['Favourite'] = (
			"CREATE TABLE IF NOT EXISTS `Favourite` ("
		    "  `id` SMALLINT NOT NULL AUTO_INCREMENT,"
		    "  `prd_to_be_replaced` VARCHAR(250) NOT NULL,"
		    "  `barcode` VARCHAR(250),"
		    "  PRIMARY KEY (`id`),"
		    "  UNIQUE INDEX ind_prd_code (prd_to_be_replaced,barcode)"
		    ") ENGINE=InnoDB CHARACTER SET = 'utf8mb4'")
		

		# Creating the database
		try:
			# if already exists so that we use that database
			cursor.execute("USE {}".format(dbname))
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_BAD_DB_ERROR:
				try:
					cursor.execute(
						"CREATE DATABASE IF NOT EXISTS {} CHARACTER SET 'utf8'".format(dbname))
				except mysql.connector.Error as err:
					print("Failed creating database: {}".format(err))
					exit(1)
				print("Database {} has been created successfully.".format(dbname))
				connection1.database = dbname
			else:
				print(err)
				exit(1)

		# Creating the tables
		for table_name in tables:
			table_description = tables[table_name]
			try:
				cursor.execute(table_description)
			except mysql.connector.Error as err:
				print(err.msg)
			print("Table {} has been created successfully.".format(table_name))
				
		cursor.close()
		connection1.close()


	def datas_insertion(self, connection):

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
		
		# Populating 'Product' table
		try:
			for line in self.entire_list:
				
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
			print("{} entries have been inserted in the 'Product' table.".format(len(self.entire_list)))

		connection.commit()
		
		cursor.close()


	@classmethod
	def categories_show(cls, categories):
		
		print("************** Catégories des Aliments *****************")
		i_number = []
		for i, elt in enumerate(categories):
			print("{} - {}".format(i+1, elt))
			i_number.append(i+1) 
		print("********************************************************")
		
		loop2 = True
		while loop2:
			Product.category_choice = input("Votre choix de catégorie: ")
			try:
				Product.category_choice = int(Product.category_choice)
			except:
				pass
			if Product.category_choice not in i_number:
				continue
			else:
				loop2 = False

		return Product.category_choice

	@classmethod
	def products_show(cls, category_choice, connection):
		
		cursor = connection.cursor()

		sql_request = ("SELECT name,barcode FROM Product WHERE prd_cat=(%(category_choice)s)")
		sql_value = {'category_choice': Product.category_choice,}

		cursor.execute(sql_request, sql_value)

		# Exécution de la requête de SELECTION en fonction de la catégorie choisie
		myresult = cursor.fetchall()
		i = 0
		new_prd_list = []

		for w in myresult:
			i += 1
			new_prd_list.append(w[1])
			print(i,"- ",w[0]," - Code barre:",w[1])
		
		loop3 = True
		while loop3:
			product_choice = input("Votre choix de produit: ")
			try:
				product_choice = int(product_choice)
			except:
				pass
			if product_choice not in range(1, (i+1)):
				continue
			else:
				loop3 = False

		Product.saved_code = new_prd_list[product_choice-1]
		
		cursor.close()


		return Product.saved_code


	@classmethod
	def substitute_show(cls, saved_code, connection):
		
		cursor = connection.cursor()

		# Saving barcode for chosen product
		sql1_request = ("SELECT name,nutrition_grade,prd_cat FROM Product"
						" WHERE barcode=(%(barcode)s)")
		sql1_value = {'barcode': Product.saved_code,}
		cursor.execute(sql1_request, sql1_value)
		
		# Exécution de la requête de SELECTION en fonction de la catégorie choisie
		myresult1 = cursor.fetchone()
		name_to_replace = myresult1[0]
		nutrition_to_replace = myresult1[1]
		cat_to_keep = myresult1[2]

		sql2_request = ("SELECT name,nutrition_grade,barcode FROM Product"
						" WHERE prd_cat=(%(prd_cat)s) AND nutrition_grade < (%(nutrition_grade)s)")
		sql2_value = {	'prd_cat': cat_to_keep,
						'nutrition_grade': nutrition_to_replace,
					}
		cursor.execute(sql2_request, sql2_value)
		
		myresult2 = cursor.fetchone()
		
		
		if not myresult2:
			print("Il n'y a pas d'élément meilleur que le votre")
		else:
			
			print("------------------------------------------------------")
			print("Produit à remplacer:", name_to_replace, "avec un indice nutritionnel: ", nutrition_to_replace)
			print("Nom du meilleur produit: ", myresult2[0])
			print("Indice nutritionnel: ", myresult2[1])
			print("Code barre: ", myresult2[2])
			print("------------------------------------------------------")
			
			record_result = input("Voulez-vous enregistrer ce résultat? (tapez 'O' ou 'o' pour Oui): ")
			if record_result not in ["O","o"]:
				pass
			else:			
				connection = mysql.connector.connect(
								user = user,
								password = password,
								host = host,
								database = dbname)
				cursor = connection.cursor()
				add_category = ("INSERT INTO Favourite "
								"(prd_to_be_replaced,barcode) "
								"VALUES (%(prd_to_be_replaced)s, %(barcode)s)")
				category_value = {
							'id': cursor.lastrowid,
							'prd_to_be_replaced': name_to_replace,
							'barcode': myresult2[2],
							}
				try:
					cursor.execute(add_category, category_value)
					
					
				except:
					print("Ce produit de substitution a déjà été enregistré !.")
				else:
					print("Ce nouveau produit a bien été enregistré dans la base.")
					connection.commit()
					cursor.close()
					connection.close()


	def launch_interface(self, connection):
		
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
			Product.categories_show(categories)
			Product.products_show(Product.category_choice, connection)
			Product.substitute_show(Product.saved_code, connection)

		if welcome_choice == 2:
			cursor = connection.cursor()
			sql_request = ("SELECT Favourite.prd_to_be_replaced, Product.name, Product.description, Product.store, Product.url "
							"FROM Favourite INNER JOIN Product "
							"ON Favourite.barcode=Product.barcode ")
					
			cursor.execute(sql_request)
			results = cursor.fetchall()

			for result in results:
				print("----------------------------------------------------------------------------------------")
				print("Produit à substituer:",result[0])
				print("Meilleur produit:",result[1])
				print("Description du produit:",result[2])
				print("Magasin(s) où le trouver:",result[3])
				print("Lien Web du produit:",result[4])
				print("----------------------------------------------------------------------------------------")

			cursor.close()
			connection.close()

		if welcome_choice == 3:
			print("Merci d'avoir utilisé ce programme.")
			exit(1)


