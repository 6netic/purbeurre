#! /usr/bin/env python3
# coding: utf-8

from controller import *

def main():
	
	test_if_database_exists()

	main_loop = True
	while main_loop:


		print("*********************** Application de substitut Alimentaire - Pur Beurre ****************************")
		print()
		print("1 - Quel aliment souhaitez-vous remplacer ?")
		print("2 - Retrouver mes aliments substitués")
		print("3 - Quitter")
		print()
		print("******************************************************************************************************")

		menu_loop = True
		while menu_loop:		
			print()
			welcome_choice = input("Votre choix de programme: ")
			try:
				welcome_choice = int(welcome_choice)
			except:
				pass

			if welcome_choice not in [1, 2, 3]:
				continue
			else:
				menu_loop = False


		if welcome_choice == 1:
			search_save_food()

		if welcome_choice == 2:
			show_saved_substitute_list()

		if welcome_choice == 3:
			print("Merci d'avoir utilisé ce programme.")
			exit(1)

	

if __name__ == "__main__":
	main()


















