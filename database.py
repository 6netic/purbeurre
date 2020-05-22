
import mysql.connector
from mysql.connector import errorcode


class Database:
	"""This class creates the database and the three tables"""	

	def database_tables_creation(self, connection, database):

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
		    "  `prd_to_be_replaced` VARCHAR(250),"
		    "  `barcode` VARCHAR(250) NOT NULL,"
		    "  UNIQUE INDEX ind_prd_code (prd_to_be_replaced,barcode)"
		    ") ENGINE=InnoDB CHARACTER SET = 'utf8mb4'")
		

		# Establishing a connection			
		cursor = connection.cursor()
		# Creating the database
		try:
			# if already exists so that we use that database
			cursor.execute("USE {}".format(database))
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_BAD_DB_ERROR:
				try:
					cursor.execute(
						"CREATE DATABASE IF NOT EXISTS {} CHARACTER SET 'utf8'".format(database))					
				except mysql.connector.Error as err:
					print("Failed creating database: {}".format(err))
					exit(1)
				print("Database {} has been created successfully.".format(database))
				connection.database = database
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
		
		









