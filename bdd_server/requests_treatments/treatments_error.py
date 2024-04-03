import mysql.connector
from connexion_mysql import *
from requests_treatments.requests_mysql import *

# @brief: definition des codes d'erreur
SUCCESS                 = [0]
LOGIN_NOT_FOUND         = [300]
BAD_PASSWORD            = [301]
PLAYER_CONNECTED        = [302]
LOGIN_NOT_UNIQUE        = [303]
MAIL_NOT_UNIQUE         = [304]
PLAYER_NOT_CONNECTED    = [305]
PLAYER_ALREADY_IN_ROOM  = [306]
ROOM_CODE_NOT_FOUND     = [307]
PION_NOT_FOUND          = [308]
PION_FIND               = [309]
PLAYER_NOT_IN_ROOM      = [310]
ROOM_FULL               = [311]
NUM_PORT_NOT_VALID      = [312]
BAD_CATEGORIE_ID        = [313]
BAD_REQUEST_FORMAT      = [314]
UNKNOWN_REQUEST_CODE    = [315]
BAD_CODE_MAIL           = [316]
MYSQL_ERROR             = [999]

# @brief: permet de verifier si un joueur est connecte ou non
# @input: login de l'utilisateur
# @output: True si le joueur est connecte, False sinon
def is_connected(login):
    ret = False
    ret = get_data(IS_CONNECTED_REQUEST, (login,))
    if ret == MYSQL_ERROR:
        return ret
    if len(ret) == 1:
        return True
    return False

# @brief: permet de trouver l'id d'un joueur a partir de son login
# @input: login de l'utilisateur
# @output: id de l'utilisateur ou code d'erreur
def find_player_id(login):
    ret = get_data(FIND_PLAYER_ID_REQUEST, (login,))
    if ret == MYSQL_ERROR:
        return ret
    if len(ret) != 0:
        return ret[0][0]
    else:
        return MYSQL_ERROR
