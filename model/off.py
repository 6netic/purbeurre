import requests

class OpenFoodFacts:
	"""This class extracts datas from OpenFoodFacts API"""
	
	def __init__(self, categories):
		self.categories = categories
	
	def get_categories_from_OFF_api(self):
		
		
		entire_list = []
		for category in self.categories:	

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
					products_list.append(self.categories.index(category) + 1)
					products_list.append(my_product["nutriments"]["fat_100g"])
					products_list.append(my_product["nutriments"]["saturated-fat_100g"])
					products_list.append(my_product["nutriments"]["sugars_100g"])
					products_list.append(my_product["nutriments"]["salt_100g"])
					
				except KeyError:
					pass

				else:			
					entire_list.append(products_list)
					i += 1
					
					if i == 100:
						break
			
		return entire_list



