# @brief: ce fichier a pour but de gerer la base de donnée
#       à l'aide de ligne de commandes
import mysql.connector
import sys
from connexion_mysql import *

# @brief: permet d'afficher un message d'erreur
#       concernant les arguments en entrees
# @input: error permettant d'afficger le message d'erreur specifique


def usage(error):
    print(error)
    print('Usage: python3 managment_mysql.py [paramName] ... [paramName]' +
          '\n- create_tables' +
          '\n- insert_data' +
          '\n- clear_data' +
          '\n- clear_bdd')

# @brief: permet d'éxecuter les lignes d'un fichier sql,
#       les requetes sql doivent etre ecrites dans un fichier
#       et doivent etre separer par un ';' suivit d'un saut de ligne
# @input: file, le chemin vers le fichier sql a executer


def execute_sql_file(file):
    db = get_connexion_db()
    # with db.cursor() as c, open(file) as f:
    c = db.cursor()
    f = open(file)
    for line in f.read().split(";\n"):
        c.execute(line)
    close_connexion_db(db)

# @brief: fonction permettant de creer les tables dans la base de donnees,
#       d'apres le fichier sql/create_tables.sql


def create_tables():
    execute_sql_file("sql/create_tables.sql")

# @brief: fonction permettant d'inserer les donnees dans la base de données,
#       d'apres le fichier sql/insert_data.sql


def insert_data():
    execute_sql_file("sql/insert_data.sql")

# @brief: fonction permettant de supprimmer les donnees
#       de la base de données, d'apres le fichier sql/clear_data.sql


def clear_data():
    execute_sql_file("sql/clear_data.sql")

# @brief: fonction permettant de supprimmer les tables
#       de la base de données, d'apres le fichier sql/clear_bdd.sql


def clear_bdd():
    execute_sql_file("sql/clear_bdd.sql")


# @brief: programme principale recuperant les arguments,
#       les verifiants et appellant les fonctions demandees
if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage('Bad number of arguments')
    else:
        for i in range(len(sys.argv)):
            if i == 0:
                pass
            elif sys.argv[i] == 'create_tables':
                create_tables()
            elif sys.argv[i] == 'insert_data':
                insert_data()
            elif sys.argv[i] == 'clear_data':
                clear_data()
            elif sys.argv[i] == 'clear_bdd':
                clear_bdd()
            else:
                usage('Invalid arguments for param n°'+str(i))
