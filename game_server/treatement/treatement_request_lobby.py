from treatement.treatement_request_error import *
from ast import In
import os
import sys
import inspect
import re
import smtplib
import string
import time
import random
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

OK = 0
# macro vers bdd
CONNEXION = 1
INSCRIPTION = 2
STAT_GLOBALE = 3
STAT_DET = 4
CREATE_ROOM = 5
JOIN_ROOM = 6
BACK_TO_CONNEXION = 7
ASK_PORT = 15
NEED_RECONNECTED = 16
TEST_CONNECTED = 105
# macro vers client
REDIRECTION_LOBBY = 210
REDIRECTION_CONNEXION = 211
PATH = "src.GSNetwork"
RESEAU = __import__(PATH)

cmd = "/usr/bin/python3"


"""
@brief : traitement des regex
@input : input: valeur à tester
         code: type de valeur
@output : true si match sinon false
"""
# a tester


def treatement_regex(input, code):
    retour = None
    if(code == "mail"):
        retour = re.match("^[a-zA-Z0-9]+@([\w-]+\.)+[\w-]{2,4}$", input)
        print("mail" + str(retour != None))
    elif (code == "mdp"):
        retour = re.match(
            "^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-+!*$@%_])([-+!*$@%_\w]{8,15})$", input)
        print("mdp" + str(retour != None))
    elif(code == "usr"):
        retour = re.match(
            "^[a-zA-Z0-9]([.-](?![._-])|[a-zA-Z0-9]){2,18}[a-zA-Z0-9]$", input)
        print("usr" + str(retour != None))
    return retour != None


"""
@brief : cree le processus game
@input : param : les param pour la game
@output : true si match sinon false
"""


def forker(param):
    pid = os.fork()
    if pid == 0:

        os.execv(cmd, (cmd, "/home/florian/Documents/pi/projet-integrateur-5a-2021-2022/game_server/src/game/game.py",
                 ";".join([str(n) for n in param])))
        sys.exit(99)

    elif pid > 0:

        return 0
    else:
        print("fork error")
        return -1


"""
@brief: traitement d'une demande d'inscription
@input: reseau: objet reseau
        num_client: socket du client
        param: liste des param
        compteur: compte le nb d'iterations de la fonction
@output: True si tout est bon
"""


def treatement_inscription(reseau, num_client, param, compteur):
    if(compteur > 3):
        return False
    param.insert(0, INSCRIPTION)
    # param.append(send_mail(param[3]))
    param.append("AAA")
    reseau.send_msg_DBS(";".join([str(n) for n in param]))
    retour = reseau.recv_msg_DBS().split(";")

    if (int(retour[0]) == OK or int(retour[0]) == LOGIN_EXISTANT or int(retour[0]) == EMAIL_EXISTANT):
        reseau.send_msg_cli(";".join([str(n) for n in retour]), num_client)

    elif (int(retour[0]) == MYSQL_DOOMED):
        param.pop(0)
        return treatement_inscription(reseau, num_client, param, compteur+1)

    else:
        return False

    return int(retour[0]) == OK


"""
@brief: envoi des mails
@input: mail_adress: l'adresse mail
@output: le code
"""


def send_mail(mail_adress):
    # connexion gmail
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    # info d'envoi
    SMTP_USERNAME = "groupeproject5a@gmail.com"
    SMTP_PASSWORD = "VbSaAbCbRcFeEdMbTbRa"
    EMAIL_FROM = "groupeproject5a@gmail.com"
    EMAIL_TO = mail_adress
    EMAIL_SUBJECT = "Bienvenue chez Choucroute Poursuit - Merci de verifier votre Email"

    # generation d'un code aleatoire
    alphabet = list(string.ascii_uppercase)
    code = ""
    for i in range(5):
        code += alphabet[random.randint(0, 25)]
    EMAIL_MESSAGE = """Bonjour,\n
    Merci d'avoir creer un compte Choucroute Poursuit. Merci de verifier votre email en entrant le code suivant:
    """+code+"""\nMerci de ne pas repondre a ce mail."""

    # envoi du mail
    s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    s.starttls()
    s.login(SMTP_USERNAME, SMTP_PASSWORD)
    message = 'Subject: {}\n\n{}'.format(EMAIL_SUBJECT, EMAIL_MESSAGE)
    s.sendmail(EMAIL_FROM, EMAIL_TO, message)
    s.quit()
    return code


"""
@brief: traitement d'une demande de connexion au jeu
@input: reseau: objet reseau
        num_client: socket du client
        param: liste des param
        compteur: compte le nb d'iterations de la fonction
@output: True si tout est bon
"""


def treatement_connexion(reseau, num_client, param, compteur):
    # test connexion
    if(compteur > 3):
        return False
    param.insert(0, CONNEXION)
    reseau.send_msg_DBS(";".join([str(n) for n in param]))
    retour = reseau.recv_msg_DBS().split(";")
    if (int(retour[0]) == OK or int(retour[0]) == LOGIN_INEXISTANT or
            int(retour[0]) == MAUVAIS_MDP or int(retour[0]) == ALREADY_CONNECTED):

        reseau.send_msg_cli(";".join([str(n) for n in retour]), num_client)

    elif (int(retour[0]) == MYSQL_DOOMED):
        param.pop(0)
        return treatement_connexion(reseau, num_client, param, compteur+1)

    else:
        return False

    return int(retour[0]) == OK


"""
@brief: traitement d'une demande de stats d'un joueur
@input: reseau: objet reseau
        num_client: socket du client
        param: liste des param
        compteur: compte le nb d'iterations de la fonction
@output: True si tout est bon
"""


def treatement_stat_globales(reseau, num_client, param, compteur):

    if(compteur > 3):
        return False
    param.insert(0, STAT_GLOBALE)
    reseau.send_msg_DBS(";".join([str(n) for n in param]))
    retour = reseau.recv_msg_DBS().split(";")
    if (int(retour[0]) == OK or int(retour[0]) == LOGIN_INEXISTANT or
            int(retour[0]) == ALREADY_DISCONNECTED):
        reseau.send_msg_cli(";".join([str(n) for n in retour]), num_client)

    elif (int(retour[0]) == MYSQL_DOOMED):
        param.pop(0)
        return treatement_stat_globales(reseau, num_client, param, compteur+1)

    else:
        return False

    return int(retour[0]) == OK


"""
@brief: traitement d'une demande de stats det d'un joueur
@input: reseau: objet reseau
        num_client: socket du client
        param: liste des param
        compteur: compte le nb d'iterations de la fonction
@output: True si tout est bon
"""


def treatement_stat_det(reseau, num_client, param, compteur):
    if(compteur > 3):
        return False
    param.insert(0, STAT_DET)
    reseau.send_msg_DBS(";".join([str(n) for n in param]))
    retour = reseau.recv_msg_DBS().split(";")

    if (int(retour[0]) == OK or int(retour[0]) == LOGIN_INEXISTANT or
            int(retour[0]) == ALREADY_DISCONNECTED):
        reseau.send_msg_cli(";".join([str(n) for n in retour]), num_client)

    elif (int(retour[0]) == MYSQL_DOOMED):
        param.pop(0)
        return treatement_stat_det(reseau, num_client, param, compteur+1)

    else:
        return False

    return int(retour[0]) == OK


"""
@brief: traitement d'une creation de partie
@input: reseau: objet reseau
        num_client: socket du client
        param: liste des param
        compteur: compte le nb d'iterations de la fonction
@output: True si tout est bon
"""


def treatement_create_room(reseau, num_client, param, compteur):
    # si compteur >3 agir dans le programme lobby
    if(compteur > 3):
        return False

    param.insert(0, CREATE_ROOM)
    reseau.send_msg_DBS(";".join([str(n) for n in param]))
    retour = reseau.recv_msg_DBS().split(";")

    if(int(retour[0]) == OK):
        if(forker(retour) == -1):
            retour[0] = str(MYSQL_DOOMED)
        retour[2] = str(int(retour[2]) + 0)
        time.sleep(3)
        reseau.send_msg_cli(";".join([str(n) for n in retour]), num_client)

    elif(int(retour[0]) == ALREADY_DISCONNECTED or
         int(retour[0]) == ALREADY_IN_GAME):
        reseau.send_msg_cli(";".join([str(n) for n in retour]), num_client)

    elif (int(retour[0]) == MYSQL_DOOMED):
        param.pop(0)
        return treatement_create_room(reseau, num_client, param, compteur+1)
    else:
        return False
    return int(retour[0]) == OK


"""
@brief: traitement d'une requete pour rejoindre une partie
@input: reseau: objet reseau
        num_client: socket du client
        param: liste des param
        compteur: compte le nb d'iterations de la fonction
@output: True si tout est bon
"""


def treatement_join_room(reseau, num_client, param, compteur):
    # si compteur >3 agir dans le programme lobby
    if(compteur > 3):
        return False

    param.insert(0, JOIN_ROOM)
    reseau.send_msg_DBS(";".join([str(n) for n in param]))
    retour = reseau.recv_msg_DBS().split(";")
    if(int(retour[0]) == OK or int(retour[0]) == ALREADY_DISCONNECTED or
            int(retour[0]) == ALREADY_IN_GAME or int(retour[0]) == ROOM_NOT_FIND or
            int(retour[0]) == TOO_MUCH_PERSONS):
        retour[1] = str(int(retour[1]) + 0)
        reseau.send_msg_cli(";".join([str(n) for n in retour]), num_client)

    elif (int(retour[0]) == MYSQL_DOOMED):
        param.pop(0)
        return treatement_join_room(reseau, num_client, param, compteur+1)
    else:
        return False
    return int(retour[0]) == OK


"""
@brief: traitement d'une requete pour revenir apres une partie
@input: reseau: objet reseau
        num_client: socket du client
        param: liste des param
        compteur: compte le nb d'iterations de la fonction
@output: True si tout est bon
"""


def treatement_back_to(reseau, num_client, param, compteur):
    # si compteur >3 agir dans le programme lobby
    if(compteur > 3):
        return False

    param.insert(0, BACK_TO_CONNEXION)
    reseau.send_msg_DBS(";".join([str(n) for n in param]))
    retour = reseau.recv_msg_DBS().split(";")
    if(int(retour[0]) == OK or int(retour[0]) == ALREADY_DISCONNECTED):
        reseau.send_msg_cli(";".join([str(n) for n in retour]), num_client)

    elif (int(retour[0]) == MYSQL_DOOMED):
        param.pop(0)
        return treatement_back_to(reseau, num_client, param, compteur+1)
    else:
        return False
    return int(retour[0]) == OK


"""
@brief: traitement d'une demande de reconnexion au lobby
@input: reseau: objet reseau
        num_client: socket du client
        param: liste des param
        compteur: compte le nb d'iterations de la fonction
@output: True si tout est bon
"""


def treatement_need_reconnected(reseau, num_client, param, compteur):
    # si compteur >3 agir dans le programme lobby
    if(compteur > 3):
        return False

    param.insert(0, NEED_RECONNECTED)
    reseau.send_msg_DBS(";".join([str(n) for n in param]))
    retour = reseau.recv_msg_DBS().split(";")
    if(int(retour[0]) == OK or int(retour[0]) == ALREADY_DISCONNECTED):
        reseau.send_msg_cli(";".join([str(n) for n in retour]), num_client)

    elif (int(retour[0]) == MYSQL_DOOMED):
        param.pop(0)
        return treatement_need_reconnected(reseau, num_client, param, compteur+1)
    else:
        return False
    return int(retour[0]) == OK
