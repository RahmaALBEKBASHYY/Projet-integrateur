# @brief: ce fichier permet de stpper le serveur de la bdd et d'exécuter la maintenance, avant de le relancer

from connexion_mysql import *

LEAVE_ROOM_REQUEST = "UPDATE joueur SET is_in_room = 0;"
DISCONNECT_REQUEST = "UPDATE joueur SET is_connected = 0;"
CLEAR_PARTIE_HAS_QUESTION = "DELETE FROM `partie-has-question`;"
CLEAR_ALL_PION = "DELETE FROM pion;"
CLEAR_ALL_ROOM = "DELETE FROM partie;"

def maintenance():
    insert_or_update_data(LEAVE_ROOM_REQUEST, [])
    insert_or_update_data(DISCONNECT_REQUEST, [])
    insert_or_update_data(CLEAR_PARTIE_HAS_QUESTION, [])
    insert_or_update_data(CLEAR_ALL_PION, [])
    insert_or_update_data(CLEAR_ALL_ROOM, [])
