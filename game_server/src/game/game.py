import os
import sys
import inspect
import time
from random import *
import socket
from pion import Pion
from plateau import Plateau
from categorie import Categorie
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
gparentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, gparentdir)
from src.ClientThread import *
from src.GSNetwork import GSNetwork
import treatement.treatement_request_lobby as trl
import treatement.treatement_request_game as trg
import treatement.treatement_request_error as tre

class NetworkThread(threading.Thread):

    """
    @brief: initialise un networkThread
    @input: self, le thread du client
    @output: none
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.tab_thread = []

    """
    @brief: run gère un client du début à la fin
    @input: self, le thread du client
    @output: 0, tout est bien qui finit bien
    """

    def run(self):

        #############################################
        # 1ere phase accueil du client
        #############################################
        while True:
            try:
                client_code, indice = network.reception_game(game, lock)
                if indice != -1:
                    newthread = PreGameThread(client_code)
                    newthread.start()
                    self.tab_thread.append(newthread)
            except socket.timeout:
                print("to")
                lock.release()
                if game.statement == 'i':
                    break
                pass
        # attend la fin de tous les threads
        for t in self.tab_thread:
            t.join()
        #############################################

        #############################################
        # 2eme phase initialisation
        #############################################
        # couleur definitive
        to_send = str(trg.SEND_COLOR) + ";" + \
            (";".join(str(c.color)+';' + c.login for c in game.clients))
        network.broadcast_cli(to_send, game.clients)

        # creation de pion
        if(not(trg.treatement_request_create_pion(network, game))):
            print('exit')

        # envoi du board (couleur)
        time.sleep(0.2)
        network.broadcast_cli(str(trg.INIT_BOARD) + ';' +
                              board.print_theme(), game.clients)

        # remet les threads vide pour recreer des threads apres
        self.tab_thread = []

        # setup de la barriere pour synchro les threads
        thread_barrier = threading.Barrier(len(game.clients))
        #############################################

        #############################################
        # Phase de pre game (lancer de de pour definir l'ordre)
        #############################################
        for i in range(len(game.clients)):
            newthread = GameThread(
                game.clients[i].socket, game.clients[i].login, i, thread_barrier)
            newthread.start()
            self.tab_thread.append(newthread)

        for t in self.tab_thread:
            t.join()
        #############################################

        #############################################
        # 3eme phase le deroulement d'une partie
        #############################################
        win = False  # statut de la partie
        turn = 0  # le tour du joueur
        tdeb = time.time()
        while not(win):
            game.clients[turn].socket.settimeout(30)
            # Previens de l'ordre
            for i in range(len(game.clients)):
                try:
                    if i == turn and game.clients[turn].joueur:
                        network.send_msg_cli(
                            str(trg.UR_TURN), game.clients[i].socket)
                    else:
                        # not ur turn
                        network.send_msg_cli(
                            str(trg.NUR_TURN) + ';' + game.clients[turn].login, game.clients[i].socket)
                except socket.error:
                    game.clients[i].joueur = False
                    pass

            #############################################
            # Lancer de de
            #############################################
            if game.clients[turn].joueur:
                try:
                    message = network.recv_msg_cli(
                        game.clients[turn].socket).split(";")
                    if message == ['']:
                        network.send_msg_DBS(
                            str(trl.BACK_TO_CONNEXION) + ";" + game.clients[turn].login)
                        print(network.recv_msg_DBS())
                        game.clients[turn].joueur = False
                    elif int(message[0]) != trg.REQUEST_DE or message[1] != game.clients[turn].login:
                        print("BAD REQUEST")
                except socket.timeout:
                    pass
                except socket.error:
                    game.clients[turn].joueur = False
                    pass
            else:
                print('IA')
            #############################################

            #############################################
            # calcule les cases et envoie à tout le monde
            #############################################
            # lance le dé
            game.clients[turn].last_de = board.lancer_des()

            # liste de cases
            cases = board.liste_case(
                game.clients[turn].num_case, game.clients[turn].last_de)
            to_send = str(trg.SEND_VALUE) + ";" + str(
                game.clients[turn].last_de) + ';' + (';'.join(str(num) for num in cases))
            time.sleep(0.2)
            network.broadcast_cli(to_send, game.clients)
            #############################################

            #############################################
            # Selection de cases
            #############################################

            # Prend une case random
            x = randint(0, len(cases)-1)
            game.clients[turn].num_case = cases[x]

            # demande une case
            if game.clients[turn].joueur:
                try:
                    message = network.recv_msg_cli(
                        game.clients[turn].socket).split(";")
                    if message == ['']:
                        network.send_msg_DBS(
                            str(trl.BACK_TO_CONNEXION) + ";" + game.clients[turn].login)
                        print(network.recv_msg_DBS())
                        game.clients[turn].joueur = False

                    elif int(message[0]) != trg.REQUEST_CASE or message[1] != game.clients[turn].login:
                        print("BAD REQUEST")
                    else:
                        game.clients[turn].num_case = int(message[2])
                except socket.timeout:
                    pass
            else:
                print("IA")
            #############################################

            #############################################
            # Calcule du prochain tour et update du tour
            #############################################

            # update position
            time.sleep(0.2)
            network.broadcast_cli(str(trg.UPDATE_CASE) + ';' + game.clients[turn].login + ';' + str(
                game.clients[turn].num_case), game.clients)

            # arrive ne fait rien pour l'instant
            if board.cases[game.clients[turn].num_case].categorie.theme == 'a':
                turn = (turn+1) % len(game.clients)

            # une case avec un theme
            elif board.cases[game.clients[turn].num_case].categorie.theme != 'd':
                # demande des questions
                network.send_msg_DBS(str(trg.NEED_QUESTIONS) + ';' + game.code_room + ';' + str(
                    board.cases[game.clients[turn].num_case].categorie.id))

                # recup et parsage des questions
                retour = network.recv_msg_DBS()
                split = retour.split(';')
                code_request = int(split.pop(0))
                question = split.pop(0)
                tab_string = []
                tab_bool = []
                for i in range(len(split)):
                    if i % 2 == 0:
                        tab_string.append(split[i])
                    else:
                        tab_bool.append(split[i])
                if code_request != trg.OK:
                    return

                # broadcast de la question et ses reponses
                time.sleep(0.2)
                network.broadcast_cli(str(
                    trg.OK) + ';' + question + ';' + (';'.join(t for t in tab_string)), game.clients)

                # num rep est un random si le joueur ne repond pas
                num_rep = randint(0, len(tab_string))
                if game.clients[turn].joueur:
                    try:
                        message = network.recv_msg_cli(
                            game.clients[turn].socket).split(";")
                        if message == ['']:
                            network.send_msg_DBS(
                                str(trl.BACK_TO_CONNEXION) + ";" + game.clients[turn].login)
                            print(network.recv_msg_DBS())
                            game.clients[turn].joueur = False

                        elif int(message[0]) != trg.REQUEST_REP or message[1] != game.clients[turn].login:
                            print("BAD REQUEST")
                        else:
                            num_rep = int(message[2])
                    except socket.timeout:
                        pass
                    except socket.error:
                        game.clients[turn].joueur = False
                        pass

                else:
                    print("IA")

                # trouves la reponse qui est la bonne
                num_rep_true = -1
                for i in range(len(tab_bool)):
                    if tab_bool[i] == "1":
                        num_rep_true = i

                # broadcast le resultat
                time.sleep(0.2)
                network.broadcast_cli(str(
                    trg.SEND_RESULTAT) + ';' + str(num_rep_true) + ';' + str(num_rep), game.clients)
                time.sleep(1)

                # si c'est la bonne reponse il y a un changement de classement et de points possible
                if num_rep == num_rep_true:

                    # case qui fait remporter un aliment?
                    if board.cases[game.clients[turn].num_case].special:
                        game.clients[turn].Choucroute.setIngredient(
                            board.cases[game.clients[turn].num_case].categorie)
                    game.clients[turn].nbpoint += 1
                    game.clients[turn].nbGoodAnswer += 1

                    # tri du classement
                    sort_clients = sorted(game.clients, key=lambda x: (
                        x.Choucroute.nbIngredient(), x.nbpoint), reverse=True)

                    # changer classement
                    for c in game.clients:
                        for i in range(len(sort_clients)):
                            if c.login == sort_clients[i].login:
                                c.classement = i

                    # distrib les changements
                    for c in game.clients:
                        network.broadcast_cli(
                            str(trg.UPDATE_PION) + ';' + c.toStr(), game.clients)
                        time.sleep(0.2)

                    # verif win
                    if game.clients[turn].Choucroute.win():
                        game.statement = 'e'
                        win = True

                # pas de changement sauf notre joueur
                else:
                    game.clients[turn].nbBadAnswer += 1
                    network.broadcast_cli(
                        str(trg.UPDATE_PION) + ';' + game.clients[turn].toStr(), game.clients)
                    time.sleep(0.2)

                turn = (turn+1) % len(game.clients)
            #############################################
        #############################################

        # envoi la fin pour sauvegarder la partie
        network.send_msg_DBS(str(trg.END_GAME) + ";" +
                             game.code_room + ";" + str(time.time() - tdeb))
        # TODO
        # Finir recv_msg
        network.recv_msg_DBS()

        # broadcast fin de partie
        network.broadcast_cli(str(trg.END_GAME), game.clients)


class PreGameThread(ClientThread):

    def __init__(self, socket):
        super().__init__(socket)
        self.client_login = ''
        self.Client_code.settimeout(5)

    """
    @brief: run gère un client du début à la fin
    @input: self, le thread du client
    @output: 0, tout est bien qui finit bien
    """

    def run(self):
        # envoyer les couleurs disponibles des le debut
        to_send = str(trg.SEND_COLOR) + ";" + \
            (";".join(c.color + ';' + c.login for c in game.clients))
        print(to_send)
        network.send_msg_cli(to_send, self.Client_code)

        # boucle tant que la partie n'est pas lancee
        while True:
            try:
                # recoit
                message = network.recv_msg_cli(self.Client_code).split(";")

                # deco
                if message == ['']:
                    game.removeClient(self.client_login, self.Client_code)
                    if(self.client_login != ""):
                        network.send_msg_DBS(
                            str(trl.BACK_TO_CONNEXION) + ";" + self.client_login)
                        print(network.recv_msg_DBS())
                    print("Mort du thread \n")
                    return 0

                # recup du code de requete
                code_request = int(message.pop(0))

                # requete pour changement de couleur
                if code_request == trg.REQUEST_COLOR:

                    # stocker le login pour retrouver dans le game.clients
                    if self.client_login == '':
                        # verif si le login n'est pas dedans
                        print(175)
                        for c in game.clients:
                            if message[0].strip('\n') == c.login:

                                print('message : ' +
                                      message[0] + ' login :' + c.login)
                                game.removeClient(
                                    self.client_login, self.Client_code)
                                trg.treatement_request_leave_game(
                                    network, game, self.Client_code, message, 0)
                                return
                        self.client_login = message[0]

                    # le joueur change de login = soucis
                    elif self.client_login != message[0].strip('\n'):
                        print(186)
                        trg.treatement_request_leave_game(
                            network, game, self.Client_code, message, 0)

                    # changement de couleur une fois verif
                    trg.treatement_request_color(
                        network, game, self.client_login, message, self.Client_code)

                # le joueur veut quitter la room proprement
                elif code_request == trg.REQUEST_LEAVE_GAME:

                    # verif que c'est bien son login sinon on met le sien
                    if message[0].strip('\n') != self.client_login:
                        message[0] = self.client_login

                    # puis traitement pour quitter
                    trg.treatement_request_leave_game(
                        network, game, self.Client_code, message, 0)
                    game.removeClient(self.client_login, self.Client_code)

                # le joueur se met pret
                elif code_request == trg.REQUEST_READY:

                    # si la partie est commence ca sert a rien on cut
                    if game.statement != 'i':

                        if message[0].strip('\n') != self.client_login:
                            game.removeClient(
                                self.client_login, self.Client_code)
                            trg.treatement_request_leave_game(
                                network, game, self.Client_code, message, 0)

                        # puis traitement pour mettre pret
                        trg.treatement_request_ready(
                            network, game, self.Client_code, message)

                else:
                    print("Bad request")

            except socket.timeout:
                print("to thread")
                print(game.statement)
                if game.statement == 'r' or game.statement == 'i':
                    game.statement = 'i'
                    break
                pass
            except:
                # deco les joueurs
                pass
        # room finit


class GameThread(ClientThread):

    """
    @brief: init l'objet Gamethread
    @input: self: l'objet, Client_code: socket, login: login du joueur, indice: dans le tab, bar: barrière
    @output: none
    """

    def __init__(self, Client_code, login, indice, bar):
        super().__init__(Client_code)
        self.client_login = login
        self.Client_code.settimeout(30)
        self.indice = indice
        self.last_send = trg.NEED_DICE
        self.bar = bar

    """
    @brief: fais le premier lancer de dé
    @input: self: l'objet, indice: pour redemander
    @output: boolean
    """

    def setupGame(self, indice):

        # trop de soucis de requete on quitte tout
        if(indice > 2):
            network.broadcast_cli(str(trg.END_GAME), game.clients)
            return False

        # si le joueur est humain et qu'il n'est pas deco
        time.sleep(1)
        if game.clients[self.indice].joueur:
            try:
                network.send_msg_cli(str(trg.NEED_DICE), self.Client_code)
                message = network.recv_msg_cli(self.Client_code).split(";")
                if message == ['']:
                    if(self.client_login != ""):
                        network.send_msg_DBS(
                            str(trl.BACK_TO_CONNEXION) + ";" + self.client_login)
                        print(network.recv_msg_DBS())
                    print("Passage mode IA \n")
                    game.clients[self.indice].joueur = False
                    return self.setupGame(indice)

                code_request = int(message.pop(0))

                if code_request != trg.REQUEST_DE:
                    self.setupGame(indice+1)

            # timeout
            except socket.timeout:
                print("to thread")
                pass

            # erreur d'envoi socket down?
            except socket.error:
                game.clients[self.indice].joueur = False

        else:
            print('IA')

        # send le score
        game.clients[self.indice].last_de = board.lancer_des()
        network.broadcast_cli(str(trg.SEND_SCORE) + ';' + self.client_login +
                              ';' + str(game.clients[self.indice].last_de), game.clients)
        return True

    """
    @brief: run gère un client du début à la fin
    @input: self, le thread du client
    @output: 0, tout est bien qui finit bien
    """

    def run(self):
        # demande de lancer de dé
        self.setupGame(0)

        # synchro les threads
        self.bar.wait()

        if self.indice == 0:
            game.clients.sort(key=lambda x: x.last_de, reverse=True)
            time.sleep(1)
            network.broadcast_cli(str(
                trg.SEND_ORDER) + ';' + (';'.join(c.login for c in game.clients)), game.clients)


# objet contenant les clients ainsi que l'état de la partie et le code de la room
class Game():

    """
    @brief: add un client
    @input: self: objet game, code: code de la partie
    @output: none
    """

    def __init__(self, code):
        self.statement = "w"  # w pour wait, i pour in-game, e pour end, k pour kill
        self.code_room = code  # code de la room
        self.clients = []  # tableau de client

    """
    @brief: add un client
    @input: self: objet game, socket: la socket du joueur
    @output: none
    """

    def appendClient(self, socket):
        self.clients.append(Pion(socket, ""))

    """
    @brief: supprime un client
    @input: self: objet game, login: login du client, socket: la socket du joueur
    @output: none
    """

    def removeClient(self, login="", socket=None):
        for c in self.clients:
            if c.login == login and c.socket == socket:
                self.clients.remove(c)

    """
    @brief: regarde si tout le monde est pret
    @input: self: objet game
    @output: True si all ready sinon False
    """

    def all_ready(self):
        for c in self.clients:
            if c.ready == False:
                return False
        return True

    """
    @brief: change la couleur d'un joueur
    @input: self: objet game, login: login du client, color: la couleur
    @output: none
    """

    def change_color(self, login, color):
        for c in self.clients:
            if c.login == login:
                c.color = color
                return

    """
    @brief: change pour la première fois le login
    @input: self: objet game, login: login du client, socket: socket du client
    @output: none
    """

    def change_login(self, login, socket):
        for c in self.clients:
            if c.login == "" and c.socket == socket:
                c.login = login
                return

    """
    @brief: indice d'un client
    @input: self: objet game, login: login du client
    @output: l'indice dans le tableau
    """

    def get_indice(self, login):
        for c in range(len(self.clients)):
            if game.clients[c].login == login:
                return c
        return -1


# initialisation avec les arg
param = sys.argv[1].split(";")
print(param)
if(param[1] == "+"):
    exit()

# init gs network
network = GSNetwork(int(param[2]))
network.sockgs.settimeout(5)

# recup et parsage des categories
network.send_msg_DBS(str(trg.RECUP_CATEGORIE))
categories = network.recv_msg_DBS().split(";")
tab_categorie = []
categories.pop(0)
for cat in categories:
    cat = cat.replace('(', '')
    cat = cat.replace(')', '')
    cat = cat.replace('"', '')
    cat = cat.replace(' ', '')
    cat = cat.split(',')
    tab_categorie.append(
        Categorie(cat[0], cat[1][1:-1], cat[2][1:-1], cat[3][1:-1]))

# fin initialisation
board = Plateau(tab_categorie)
game = Game(param[1])
lock = threading.Lock()
netThread = NetworkThread()
netThread.start()
netThread.join()

exit()
