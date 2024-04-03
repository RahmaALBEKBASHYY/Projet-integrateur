# @brief: ce fichier a pour but de gerer les connexion a mysql
import mysql.connector

# @brief: parametres de connexion a mysql
#       a changer en cas de besoin
#       peut-etre differents profiles a creer dans la bdd ?
connection_params = {
    'host': "localhost",
    'user': "root",
    'password': "root",
    'database': "choucroute_poursuite",
}

MYSQL_ERROR = [999]

# @brief: permet de créer une connexion avec la base de donnee
# @output: un objet permettant d'intéragir avec la base de donnée


def get_connexion_db():
    db = mysql.connector.connect(**connection_params)
    db.autocommit = True
    return db

# @brief: permet de fermer une connexion avec la base de donnee
# @input: db etant la connexion a fermer


def close_connexion_db(db):
    db.close()
    return

# @brief: permet d'executer la requete et de renvoyer les donnees demandees
# @input: la requete et ses parametres
# @output: les donnees demandees ou un code d'erreur


def get_data(request, params):
    try:
        db = get_connexion_db()
        # with db.cursor() as c:
        c = db.cursor()
        c.execute(request, params)
        res = c.fetchall()
        close_connexion_db(db)
    except mysql.connector.Error as e:
        print("error: "+e.msg)
        res = MYSQL_ERROR
    return res

# @brief: permet d'executer la requete de modification/insertion/suppression
# @input: la requete et ses parametres
# @output: le nombre de lignes modifiees/inserees/suppimees ou un code d'erreur


def insert_or_update_data(request, params):
    try:
        db = get_connexion_db()
        # with db.cursor() as c:
        c = db.cursor()
        c.execute(request, params)
        ret = c.rowcount
        close_connexion_db(db)
    except mysql.connector.Error as e:
        print("error: " + e.msg)
        ret = MYSQL_ERROR
    return ret
