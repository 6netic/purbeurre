#! /usr/bin/env python3
# coding: utf-8

from product import *

my_product = Product()

looping = True
while looping:
	try:
		connection = mysql.connector.connect(
						user = user,
						password = password,
						host = host,
						database = dbname)
	except:
		my_product.get_categories_from_OFF_api(categories)
		my_product.database_tables_creation()
		connection = mysql.connector.connect(
						user = user,
						password = password,
						host = host,
						database = dbname)
		my_product.datas_insertion(connection)
		my_product.launch_interface(connection)
	else:
		my_product.launch_interface(connection)

