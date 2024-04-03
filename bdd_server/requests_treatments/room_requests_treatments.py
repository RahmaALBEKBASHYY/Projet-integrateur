# @brief: ce fichier a pour but de gerer les traitements en lien
#       avec la base de donnees de type "room"

from contextlib import asynccontextmanager
import mysql.connector
from connexion_mysql import *
from requests_treatments.treatments_error import *
from requests_treatments.requests_mysql import *
import string
import random

NUM_PORT_MIN = 10001
NUM_PORT_MAX = 10007

# @brief: permet de generer une archive pour le joueur donne
# @input: tout le necessaire pour creer une archive
# @output: 0 si tout est ok, code d'erreur sinon
def create_archive(login,color,nbPoint, placement, nb_joueur, nbGoodAnswer,
    nbBadAnswer, choux, knack, pomme_de_terre, lard, vin, date, duree):
    if isinstance(login, int):
        idPlayer = login
    else:
        idPlayer = find_player_id(login)
        if idPlayer == MYSQL_ERROR:
            return MYSQL_ERROR
    params = (idPlayer,color, nbPoint, placement, nb_joueur, nbGoodAnswer, nbBadAnswer,
    choux, knack, pomme_de_terre, lard, vin, date, duree)
    ret = insert_or_update_data(CREATE_ARCHIVE_REQUEST, params)
    if ret != 1:
        return MYSQL_ERROR
    else:
        return SUCCESS

# @brief: permet de savoir si le code d'une room existe ou non
# @input: code de la room a tester
# @output: true si elle existe, false sinon
def check_code_room(code_room):
    ret = get_data(CHECK_CODE_ROOM_REQUEST,(code_room,))
    if ret == MYSQL_ERROR:
        return False
    if len(ret) >= 1:
        return True
    return False

# @brief: permet de savoir si un joueur est dans une room ou non
# @input: le login de l'utilisateur
# @output: true si c'est le cas, false sinon
def is_in_room(login):
    ret = get_data(IS_IN_ROOM_REQUEST,(login,))
    if ret == MYSQL_ERROR or len(ret) < 1:
        return False
    if ret[0][0] == 1:
        return True
    return False

# @brief: permet de recupere un code de room valide
# @output: un code de room valide
def get_valid_room_code():
    alphabet = list(string.ascii_uppercase)
    valid_code = False
    code_room = ""
    while not valid_code:
        for i in range(4):
            code_room += alphabet[random.randint(0,25)]
        if not check_code_room(code_room):
            valid_code = True
    return code_room

# @brief: permet d'incrementer le nombre de joueur dans la partie de 1
# @input: le code de la room en question
# @output: 0 ou un code d'erreur
def add_nbplayer_room(code_room):
    ret = insert_or_update_data(ADD_PLAYER_ROOM_REQUEST,(code_room,))
    if ret != 1:
        return MYSQL_ERROR
    return SUCCESS

# @brief: permet decrementer le nombre de joueur dans la partie de 1
# @input: le code de la room en question
# @output: 0 ou un code d'erreur
def sub_nbplayer_room(code_room):
    ret = insert_or_update_data(SUB_PLAYER_ROOM_REQUEST, (code_room,))
    if ret != 1:
        return MYSQL_ERROR
    return SUCCESS

# @brief: permet de mettre le statut d'un joueur "dans une room"
# @input: le login de l'utilisateur
# @output: 0 et le numero de port si tout va bien, code d'erreur sinon
def set_player_in_room_treatments(login, code_room):
    if not is_connected(login):
        return PLAYER_NOT_CONNECTED
    if is_in_room(login):
        return PLAYER_ALREADY_IN_ROOM
    if not check_code_room(code_room):
        return ROOM_CODE_NOT_FOUND
    if get_data(GET_NB_PLAYER_ROOM, (code_room,))[0][0] == 4:
        return ROOM_FULL
    ret = insert_or_update_data(SET_PLAYER_IN_ROOM, (login,))
    if ret != 1:
        return MYSQL_ERROR
    if add_nbplayer_room(code_room) != SUCCESS:
        return MYSQL_ERROR
    num_port = get_num_port(code_room)
    ret = []
    ret.append(SUCCESS[0])
    ret.append(num_port)
    return ret

# @brief: permet de recuperer le numero de port d'une room
# @input: le code de la room
# @output: le numero de port de la room
def get_num_port(code_room):
    ret = get_data(GET_NUM_PORT_REQUEST, (code_room,))
    if len(ret) != 1:
        return MYSQL_ERROR
    return ret[0][0]

# @brief: permet de mettre le statut d'un joueur "pas dans une room"
# @input: le login de l'utilisateur
# @output: 0 si tout va bien, code d'erreur sinon
def set_player_not_in_room_treatments(login, code_room):
    if not is_connected(login):
        return PLAYER_NOT_CONNECTED
    if not is_in_room(login):
        return PLAYER_NOT_IN_ROOM
    if not check_code_room(code_room):
        return ROOM_CODE_NOT_FOUND
    ret = insert_or_update_data(SET_PLAYER_NOT_IN_ROOM, (login,))
    if ret != 1:
        return MYSQL_ERROR
    ret = sub_nbplayer_room(code_room)
    if ret == MYSQL_ERROR:
        return MYSQL_ERROR
    if get_data(GET_NB_PLAYER_ROOM, (code_room,))[0][0] <= 0:
        return delete_room(code_room)
    return SUCCESS

# @brief: permet de supprimer la room de code code_room
# @input: le code de la room a supprimer
# @output: 0 si tout va bien, code d'erreur sinon
def delete_room(code_room):
    if not check_code_room(code_room):
        return ROOM_CODE_NOT_FOUND
    ret = insert_or_update_data(DELET_ROOM_REQUEST, (code_room,))
    if ret != 1:
        return MYSQL_ERROR
    return SUCCESS

# @brief: permet de trouver un numero de port dispo
# @output: un numero de port ou NUM_PORT_NOT_VALID si aucun disponible
def find_num_port():
    ports = get_data(GET_PORT_ROOM_REQUEST, ())
    if len(ports) == 0:
        return NUM_PORT_MIN
    ports_tab = []
    for port in ports:
        ports_tab.append(port[0])
    for i in range(NUM_PORT_MIN, NUM_PORT_MAX+1):
        if i not in ports_tab:
            return i
    return NUM_PORT_NOT_VALID

# @brief: permet de gerer une requete de creation de room
# @input: le code de la room a creer
# @output: 0, code et port de la room en cas de reussite, code d'erreur sinon
def create_room_treatments(login):
    num_port = find_num_port()
    if num_port == NUM_PORT_NOT_VALID:
        return NUM_PORT_NOT_VALID
    if not is_connected(login):
        return PLAYER_NOT_CONNECTED
    if is_in_room(login):
        return PLAYER_ALREADY_IN_ROOM
    code_room = get_valid_room_code()
    # @TODO: date et time
    ret = insert_or_update_data(CREATE_ROOM_REQUEST,(None,code_room,num_port,None))
    if ret != 1:
        return MYSQL_ERROR
    if set_player_in_room_treatments(login, code_room)[0] != SUCCESS[0]:
        return MYSQL_ERROR
    return [SUCCESS[0], code_room, num_port]

# @brief: permet de recupere l'id d'un partie a partie de son code de room
# @input: le code de la room en question
# @output: l'id de la room ou un code d'erreur en cas de probleme
def find_room_id(code_room):
    if not check_code_room(code_room):
        return ROOM_CODE_NOT_FOUND
    ret = get_data(FIND_ROOM_ID_REQUEST,(code_room,))
    if ret == MYSQL_ERROR or len(ret) == 0:
        return MYSQL_ERROR
    return ret[0][0]

# @brief: permet de savoir si un joueur a un pion ou non
# @input: le joueur en question
# @output: True si un pion existe, False sinon
def check_pion(login):
    id_player = find_player_id(login)
    ret = get_data(CHECK_PION_REQUEST,(id_player,))
    if ret == MYSQL_ERROR:
        return False
    if len(ret) >= 1:
        return True
    return False

# @brief: permet d'ajouter un joueur a une room existante
# @input: le code de la room et le joueur
# @output: 0 en cas de reussite, code d'erreur sinon
def create_pion_treatments(login, code_room, color):
    if not is_connected(login):
        return PLAYER_NOT_CONNECTED
    if not is_in_room(login):
        return PLAYER_NOT_IN_ROOM
    if not check_code_room(code_room):
        return ROOM_CODE_NOT_FOUND
    if check_pion(login):
        return PION_FIND
    # recuperation de l'id de la partie
    id_room = find_room_id(code_room)
    # recuperation de l'id de l'utilisateur
    id_player = find_player_id(login)
    # creer le pion du joueur
    ret = insert_or_update_data(CREATE_PION_REQUEST, (id_player, id_room, color))
    if ret != 1:
        return MYSQL_ERROR
    return SUCCESS

# @brief: permet de mettre a jour les stats du pion
#       (apres reponse a une question)
# @input: le joueur, le nombre de points, le classement du joueur
#       reponse juste ou fausse, un aliment de complete en cas de question speciale
# @output: 0 en cas de reussite, code d'erreur sinon
def update_pion_treatments(login, nb_point, classement, nb_good_answer, nb_bad_answer, choux, knack, pdt, lard, vin):
    if not is_connected(login):
        return PLAYER_NOT_CONNECTED
    if not is_in_room(login):
        return PLAYER_NOT_IN_ROOM
    if not check_pion(login):
        return PION_NOT_FOUND
    id_player = find_player_id(login)
    if id_player == MYSQL_ERROR:
        return MYSQL_ERROR
    params = (nb_point, classement, nb_good_answer, nb_bad_answer, choux, knack, pdt, lard, vin, id_player)
    ret = insert_or_update_data(UPDATE_PION_REQUEST, params)
    if ret != 1:
        return MYSQL_ERROR
    return SUCCESS

# @brief: permet d'envoyer les categories disponibles au serveur
# @output: 0 + tableau categorie en cas de reussite, code d'erreur sinon
def send_categorie_treatments():
    ret = get_data(GET_CATEGORIE_REQUEST, ())
    if ret == MYSQL_ERROR:
        return MYSQL_ERROR
    ret.insert(0, SUCCESS[0])
    return ret

# @brief: permet d'ajouter une question a partie-has-question
#       pour eviter de reprendre la meme
# @input: l'id de la partie et l'id de la question
# @output: 0 si tout va bien, code d'erreur sinon
def add_partie_has_question(id_room, id_question):
    ret = insert_or_update_data(ADD_QUESTION_PARTIE_REQUEST, (id_room, id_question))
    if ret != 1:
        return MYSQL_ERROR
    return SUCCESS

# @brief: permet de savoir si des question sont encore disponible
#       pour une categorie et une partie donnee
# @input: l'id de la categorie et de la partie
# @output: True s'il n'y a plus de question diponible, False sinon
def is_empty_question_categorie_room(id_categorie, id_room):
    ret = get_data(GET_RANDOM_QUESTION, (id_categorie, id_room))
    if len(ret) == 0:
        return True
    return False

# @brief: permet de remettre en jeu toutes les questions
#       d'une ou toutes les categorie(s) pour une partie donnee
# @input: l'id de la categorie a remettre en jeu (-1 si toutes)
#       l'id de la partie en question
# @output: 0 si tout va bien, code d'erreur sinon
def clear_partie_has_qestion(categorie, id_room):
    if categorie == -1:
        request = CLEAR_ALL_QUESTION_REQUEST
        params = (id_room,)
    else:
        request = CLEAR_CATEGORIE_REQUEST
        params = (id_room, categorie)
    ret = insert_or_update_data(request, params)
    if ret == 1:
        return MYSQL_ERROR
    return SUCCESS

def get_answers(id_question):
    ret = get_data(GET_ANSWERS_REQUEST, (id_question,))
    if len(ret)<=0:
        return MYSQL_ERROR
    return ret

# @brief: permet d'envoyer une question aleatoire pour une categorie donnee
# @input: le joueur et la couleur choisie
# @output: 0 + la question en cas de reussite, code d'erreur sinon
def send_question_treatments(code_room, id_categorie):
    id_categorie = int(id_categorie)
    if id_categorie < 1 or id_categorie > 6: # a changer en fonction
        return BAD_CATEGORIE_ID
    if not check_code_room(code_room):
        return ROOM_CODE_NOT_FOUND
    id_room = find_room_id(code_room)
    if id_room == MYSQL_ERROR:
        return MYSQL_ERROR
    # selectionner question aleatoire qui n'est pas dans partie-has-question
    ret = get_data(GET_RANDOM_QUESTION, (id_categorie, id_room))
    if len(ret) != 1:
        return MYSQL_ERROR
    # ajouter la question dans les questions tirées
    if add_partie_has_question(id_room, ret[0][0]) != SUCCESS:
        return MYSQL_ERROR
    # si plus de question de la categorie qui n'est pas dans partie-has-question
    if is_empty_question_categorie_room(id_categorie, id_room):
        # alors vider partie-has-question pour toutes les question de la categorie
        if clear_partie_has_qestion(id_categorie, id_room) != SUCCESS:
            return MYSQL_ERROR
    answers = get_answers(ret[0][0])
    if answers == MYSQL_ERROR:
        return MYSQL_ERROR
    ret_tmp = []
    ret_tmp.append(SUCCESS[0])
    ret_tmp.append(ret[0][1])
    ret = ret_tmp
    for val in answers:
        ret.append(val[0])
        ret.append(val[1])
    return ret

 # @brief: permet de gerer la fin d'une partie et nettoyer la bdd en consequence
 # @input: l'id de la partie, le temps de la partie
 # @output: 0 si tout va bien, code d'erreur sinon
def end_game_treatments(code_room, time):
    if not check_code_room(code_room):
        return ROOM_CODE_NOT_FOUND
    id_room = find_room_id(code_room)
    if id_room == MYSQL_ERROR:
        return MYSQL_ERROR
    # recuperer la liste des pion
    pions = get_data(GET_ROOM_PION_REQUEST, (id_room,))
    # pour chaque pion:
    for pion in pions:
        #   generer l'archive pour le joueur correspondant
        create_archive(pion[0], pion[2], pion[3], pion[4], len(pions), pion[5],
        pion[6], pion[7], pion[8], pion[9], pion[10], pion[11], None, time)
        #   supprimer le pion
        delete_pion(pion[0])
    # supprimer les parties-has-question
    if clear_partie_has_qestion(-1,id_room) != SUCCESS:
        return MYSQL_ERROR
    # supprimer la partie
    if delete_room(code_room) != SUCCESS:
        return MYSQL_ERROR
    return SUCCESS

# @brief: permet de supprimer un pion
# @input: l'id du joueur ayant le pion
# @output: 0 si tout va bien, code d'erreur sinon
def delete_pion(id_joueur):
    ret = insert_or_update_data(DELETE_PION_REQUEST, (id_joueur,))
    if ret != 1:
        return MYSQL_ERROR
    return SUCCESS
