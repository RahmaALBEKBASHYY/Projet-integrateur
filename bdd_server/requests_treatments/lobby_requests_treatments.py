# @brief: ce fichier a pour but de gerer les traitements en lien
#       avec la base de donnees de type "lobby"

import mysql.connector
from connexion_mysql import *
from requests_treatments.treatments_error import *
from requests_treatments.requests_mysql import *


# @brief: permet de verifier si un login existe ou non
# @input: login de l'utilisateur
# @output: True si le login existe dans la base, False sinon,
# MYSQL_ERROR en cas de probleme sql
def check_login(login):
    ret = get_data(CHECK_LOGIN_REQUEST, (login,))
    if ret == MYSQL_ERROR:
        return ret
    if len(ret) >= 1:
        return True
    return False

# @brief: permet de verifier si un mail existe ou non
# @input: mail de l'utilisateur
# @output: True si le mail existe dans la base, False sinon
def check_mail(mail):
    ret = get_data(CHECK_MAIL_REQUEST, (mail,))
    if ret == MYSQL_ERROR:
        return ret
    if len(ret) >= 1:
        return True
    return False

# @brief: permet de gerer une requete d'inscription
# @input:
# - login de l'utilisateur
# - mot de passe de l'utilisateur
# - mail de l'utilisateur
# @output: 0 en cas de reussite, code d'erreur sinon
def inscription_treatments(login, pw, mail, codeMail):
    if check_login(login):
        return LOGIN_NOT_UNIQUE
    if check_mail(mail):
        return MAIL_NOT_UNIQUE
    ret = insert_or_update_data(INSCRIPTION_REQUEST, (login, pw, mail, codeMail))
    if ret == 1:
        return SUCCESS
    return MYSQL_ERROR

# @brief: permet de tester le verification de mail
# @input: l'adresse mail a verifier, le code recu par le joueur
# @output: 0 en cas de reussite, code d'erreur sinon
def verifie_mail(mail, code):
    ret = get_data(VERIFIE_MAIL_REQUEST, (mail,code))
    if len(ret) >= 1:
        ret = insert_or_update_data(SET_MAIL_VERIFIED, (mail,))
        if ret == 1:
            return SUCCESS
        return MYSQL_ERROR
    return BAD_CODE_MAIL

# @brief: permet de gerer une requete de connexion
# @input:
# - login de l'utilisateur
# - mot de passe de l'utilisateur
# @output: 0 si la personne peut se connecter, code d'erreur sinon
def login_treatments(login, pw):
    if not check_login(login):
        return LOGIN_NOT_FOUND
    if is_connected(login):
        return PLAYER_CONNECTED
    ret = get_data(CHECK_PW_REQUEST, (login, pw))
    if ret == MYSQL_ERROR:
        return MYSQL_ERROR
    if len(ret) >= 1:
        if insert_or_update_data(SET_CONNECTED_REQUEST, (login,)) == 1:
            return SUCCESS
        return MYSQL_ERROR
    return BAD_PASSWORD

# @brief: permet de gerer une requete de consultation d'archive detaillee
# @input:
# - login de l'utilisateur
# @output: 0 + tableau des archives detaillees ou code d'erreur
def archive_detailed_consultation_treatments(login,born_inf, born_sup):
    if not check_login(login):
        return LOGIN_NOT_FOUND
    if not is_connected(login):
        return PLAYER_NOT_CONNECTED
    idPlayer = find_player_id(login)
    if idPlayer == MYSQL_ERROR:
        return MYSQL_ERROR
    ret = get_data(GET_ARCHIVE_DETAILLED_REQUEST, (idPlayer,))
    if ret == MYSQL_ERROR:
        return MYSQL_ERROR
    if len(ret) != 0:
        ret = ret[born_inf:born_sup]
        ret.insert(0, SUCCESS[0])
        return ret
    ret.insert(0, SUCCESS[0])
    return ret

# @brief: permet de convertir les decimal mysql en int
# @input: une variable de type mysql decimal_object
# @output: None si la valeur vaut None, la valeur en int sinon
def convert_mysql_decimal_to_int(decimal_object):
    if (decimal_object == None):
        return None
    else:
        return int(decimal_object)

# @brief: permet de recuperer le nombre de partie jouees par le joueur
# @input: l'identifiant du joueur dans la base de donnees
# @output: le nombre de partie jouee par le joueur ou un code d'erreur
def get_nb_played_game(idPlayer):
    return get_data(GET_NB_PLAYED_GAME_REQUEST, (idPlayer,))

# @brief: permet de recuperer le nombre de partie gagnees par le joueur
# @input: l'identifiant du joueur dans la base de donnees
# @output: le nombre de partie gagnee par le joueur ou un code d'erreur
def get_nb_wined_game(idPlayer):
    return get_data(GET_NB_WINED_GAME_REQUEST, (idPlayer,))

# @brief: permet de gerer une requete de consultation d'archive globale
# @input:
# - login de l'utilisateur
# @output: 0 + tableau des archives globales ou code d'erreur
def archive_global_consultation_treatments(login):
    if not check_login(login):
        return LOGIN_NOT_FOUND
    if not is_connected(login):
        return PLAYER_NOT_CONNECTED
    idPlayer = find_player_id(login)
    if idPlayer == MYSQL_ERROR:
        return MYSQL_ERROR
    ret = get_data(GET_ARCHIVE_GLOBAL_REQUEST, (idPlayer,))
    if ret == MYSQL_ERROR:
        return ret
    if len(ret) != 0:
        final_ret = []
        for val in ret[0]:
            final_ret.append(convert_mysql_decimal_to_int(val))
        nb_played_game = get_nb_played_game(idPlayer)
        nb_wined_game = get_nb_wined_game(idPlayer)
        if nb_played_game == MYSQL_ERROR or nb_wined_game == MYSQL_ERROR:
            return MYSQL_ERROR
        final_ret.append(nb_played_game[0][0])
        final_ret.append(nb_wined_game[0][0])
        final_ret.insert(0,SUCCESS[0])
        return final_ret
    else:
        ret.insert(0, SUCCESS[0])
        return ret

# @brief: permet de gerer une requete de deconnexion
# @input:
# - login de l'utilisateur
# @output: true en cas de reussite, false sinon
def logout_treatments(login):
    if not check_login(login):
        return LOGIN_NOT_FOUND
    if not is_connected(login):
        return PLAYER_NOT_CONNECTED
    ret = insert_or_update_data(SET_DISCONNECTED_REQUEST, (login,))
    if ret == MYSQL_ERROR:
        return MYSQL_ERROR
    if ret == 1:
        return SUCCESS
    return MYSQL_ERROR
