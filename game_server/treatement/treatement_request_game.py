import os
import sys
import inspect
import re
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import treatement.treatement_request_error as tre

OK = 0
#from client
REQUEST_COLOR = 8
REQUEST_LEAVE_GAME = 9
REQUEST_READY = 10
REQUEST_DE = 11
REQUEST_CASE = 12
REQUEST_REP = 13
REQUEST_END_TOUR = 14
REQUEST_RETOUR_LOBBY = 15

#to bdd
RECUP_CATEGORIE = 100
CREATE_PION = 101
NEED_QUESTIONS = 102
UPDATE_PION = 103
END_GAME = 104

#to client
SEND_COLOR = 200
ALL_READY = 201
UR_TURN = 202
SEND_VALUE = 203
UPDATE_CASE = 204
SEND_RESULTAT = 205
NUR_TURN = 206
SUCCESS_SAVE = 207
NEED_DICE = 210
SEND_SCORE = 211
SEND_ORDER = 212
REDIR_TO_LOBBY = 220
REDIR_TO_CONNEXION = 221
INIT_BOARD = 299



"""
@brief: traite la requete de changement de couleur
@input: reseau: l'objet GSNetwork, game: l'objet Game, login: le login du joueur, param: les parametres de la requete, socket: socket du joueur
@output: boolean
"""
def treatement_request_color(reseau, game, login, param, socket):

    #si la game est kill ou fini alors la requete n'est pas possible
    if game.statement == 'k' or game.statement == 'e':
        reseau.broadcast_cli(str(END_GAME), game.clients)

    #verif login necessaire
    game.change_login(param[0], socket)

    #verif la couleur si elle est dispo
    for c in game.clients:
        if c.color == param[1].strip('\n') and c.login != param[0]:
            param.insert(0, tre.IMPOSSIBLE_COLOR)
            reseau.send_msg_cli(";".join([str(n) for n in param]), socket)
            return False

    #changement de la couleur en dur dans l'objet
    game.change_color(param[0], param[1].strip('\n'))

    #envoi le changement de couleur a tout le monde
    to_send = ";".join(c.color +';' + c.login for c in game.clients)
    to_send = str(SEND_COLOR) + ';' + to_send
    reseau.broadcast_cli(to_send, game.clients)
    return True


"""
@brief: traite la requete pour quitter la partie
@input: reseau: l'objet GSNetwork, game: l'objet Game, num_client: socket du joueur, param: les parametres de la requete, compteur: nb de probleme
@output: boolean
"""
def treatement_request_leave_game(reseau, game, num_client, param, compteur):

    #trop d'erreur
    if(compteur >3):
        return False

    #Pour la version test en ligne de commande il faut enlever les \n
    param[0].strip('\n')

    #creation de la requete pour la bdd
    param.insert(0, REQUEST_LEAVE_GAME)
    param.append(str(game.code_room))
    reseau.send_msg_DBS(";".join([str(n) for n in param]))
    retour = reseau.recv_msg_DBS().split(";")
    print(retour[0])
    
    #retourne le retour de la bdd
    if int(retour[0]) == tre.ALREADY_DISCONNECTED or int(retour[0]) == tre.PLAYER_NOT_IN_GAME or int(retour[0]) == tre.ROOM_NOT_FIND:
        reseau.send_msg_cli(";".join([str(n) for n in retour]),num_client)
     
    elif (int(retour[0]) == tre.MYSQL_DOOMED or int(retour[0]) != OK):
        param.pop(0)
        return treatement_request_leave_game(reseau, game, num_client, param, compteur+1)

    #on enleve le joueur de la partie
    game.removeClient(param[1].strip('\n'), num_client)

    #nouveau tab de joueur
    to_send = ";".join( + c.color +';' + c.login  for c in game.clients)
    to_send = str(SEND_COLOR) + ';' + to_send
    reseau.broadcast_cli(to_send, game.clients)

    #on verif si tout le monde est pret 
    if game.all_ready() and len(game.clients) >=2 :
        game.statement = 'r'
        reseau.broadcast_cli(str(ALL_READY), game.clients)
    return True


"""
@brief: traite la requete pour se mettre pret
@input: reseau: l'objet GSNetwork, game: l'objet Game, num_client: socket du joueur, param: les parametres de la requete
@output: boolean
"""
def treatement_request_ready(reseau, game, num_client, param):

    #si la game est kill ou end soucis
    if game.statement == 'k' or game.statement == 'e':
        reseau.broadcast_cli(str(END_GAME), game.clients)

    #on le met pret
    game.clients[game.get_indice(param[0].strip('\n'))].ready = not(game.clients[game.get_indice(param[0].strip('\n'))].ready)

    #on envoie l'etat actuel
    to_send = ";".join(c.login +';' + str(c.ready) for c in game.clients)
    to_send = str(OK) + ';' + to_send
    reseau.broadcast_cli(to_send, game.clients)
    
    #on teste si tout le monde est pret
    if game.all_ready() and len(game.clients) >=2:
        game.statement = 'r'
        reseau.broadcast_cli(str(ALL_READY), game.clients)
    return True


"""
@brief: creation de pion pour la bdd
@input: reseau: l'objet GSNetwork, game: l'objet Game
@output: boolean
"""
def treatement_request_create_pion(reseau, game):

    #on doit etre in game a ce moment
    if game.statement != 'i':
        reseau.broadcast_cli(str(END_GAME), game.clients)

    #parcours de la game puis envoi
    for c in game.clients:
        to_send = str(CREATE_PION) + ";" + c.login +';' + game.code_room + ';' + c.color
        reseau.send_msg_DBS(to_send)

        retour = reseau.recv_msg_DBS().split(';')

        if(int(retour[0]) != OK):
            return False

    return True

