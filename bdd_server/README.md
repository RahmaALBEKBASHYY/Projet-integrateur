# BDD - Chourcroute poursuite

## Initialisation de la VM

Voici la démarche à suivre affin de lancer le code de la BDD sur la VM:

### 1) Verifier l'environement MySQL
Pour cela lancer la commande suivante:
```shell
mysql -u root -p
```
A la suite de celle-ci on vous demandera un mot de passe. Entrez, le mot de passe choisi en privé.
Exécutez ensuite la commande suivante dans MySQL:
```sql
show databases;
```
Un tableau apparaîtra alors. Vérifiez qu'une ligne contient ```choucroute_poursuite```. Si ce n'est pas le cas exécutez la commande suivante:
```sql
create database choucroute_pousuite;
```
Re-vérifier maintenant sa présence.

### 2) Verifier la connexion entre le code et MySQL
Pour cela ouvrez le fichier ```projet-integrateur-5a-2021-2022/bdd_server/connexion_mysql.py```.
Dans celui-ci vous devriez trouver les lignes suivantes:
```python
...
connection_params = {
    'host': "localhost",
    'user': "root",
    'password': "...", # mot de passe choisi en privé
    'database': "choucroute_poursuite", # nom de la base de données dans MySQL
}
...
```
Si ce n'est pas le cas, modifiez comme indiqué.

### 3) (Ré)initiliser la BDD
Vous devriez alors maintenant pouvoir effectuer la commande suivante (depuis le dossier ```projet-integrateur-5a-2021-2022/bdd_server/```):
```shell
pyhton3 managment_mysql.py [paramName] ... [paramName]
```
Avec comme paramètres (cumulable sur un même appel, dans l'ordre logique d'exécution):
- ```clear_data```, permettant de supprimer les données;
- ```clear_bdd```, permettant de supprimer toutes les tables (et donc les données correspondantes);
- ```create_tables```, permettant de créer les tables MySQL;
- ```insert_data```, permettant d'insérer les données de base (questions, réponses, etc...).

Quelques exemples d'utilisation:
- Si vous voulez initialiser une première fois la BDD, exécutez:
```shell
python3 managment_mysql.py create_tables insert_data
```
- Si vous voulez réinitialiser TOUTE la BDD:
```shell
python3 managment_mysql.py clear_bdd create_tables insert_data
```
- Si vous voulez simplement réinitialiser les données:
```shell
python3 managment_mysql.py clear_data insert_data
```

### 4) Mettre le bon port d'écoute
Pour cela, rendez-vous dans le fichier ```projet-integrateur-5a-2021-2022/bdd_server/db_server.py```.
Dans celui-ci vous devriez trouver les lignes suivantes:
```py
def __init__(self):
      # creating socket
      self.sockdb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.sockdb.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.sockdb.bind(("", 10000)) # ip et port d'écoute
```
Si ce n'est pas le cas, modifiez comme indiqué (par défaut, nous nous sommes accordé sur le port d'écoute 10000, ce n'est pas obligatoire, veillez juste à correspondre avec le code de ```game_server```).

### 5) lancer les tests
Pour lancer les tests, lancez la commande suivante:
```shell
python3 tests/nom_fichier.py
```
pour tout les fichier du dossier tests.

### 6) Lancer le programme
Pour cela exécuter simplement la commande suivante (depuis le dossier ```projet-integrateur-5a-2021-2022/bdd_server/```):
```shell
python3 main.py
```
Les message ```Attente de connexion``` devrait directement apparaître, et le programme devrait bloquer.
