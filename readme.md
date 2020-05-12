The goal of this application is to suggest a better aliment than the one you're going to use.
It's based on the nutritional grade, provided for each food.
Only one substitute will be suggested in this program.
Thus, you could find no better product than yours if it has the best grade.
When a substitute is found, you can save it to the database when typing in 'O' or 'o'.
You can change the categories content stored in start.py file.
This program is developped with Python v.3.7.6
Librairies requested are : requests and mysql.connector.

To make it, we must have a MySQL instance running in the background.
Then, you create a user with a password and give him full rights to the new database called 'purbeurre'.
To do that, type in the following in the MySQL instance:
- CREATE USER 'ooc_student'@'localhost' IDENTIFIED BY 'P5_project';
- GRANT ALL PRIVILEGES ON purbeurre.* TO 'ooc_student'@'localhost';

The second step is to download the repo from GitHub with this command:
- git remote add PB https://github.com/6netic/purbeurre.git
- git clone https://github.com/6netic/purbeurre.git


In your (virtual) python environment, install the required librairies by typing the following :
- pip3 install -r requirements.txt


Then, you can launch the programm while typing in the terminal :
- python3 start.py

At the begining, a test is performed to check if the database already exists.
If not, the datas will be extracted via the API and the database containing requested products will be created and populated.
Otherwise, the interface appears directly.

When the interface comes in, you can:
- look for a product from the database by selecting the category and then the product by typing 1
- Look at substitutes already saved by the user by typing 2
- Quit the application by hitting 3.