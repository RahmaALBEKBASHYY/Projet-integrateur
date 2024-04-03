# coding: utf-8
# ctrl + maj + /
import threading
import os
import sys
import inspect
import socket
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
gparentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, gparentdir)
import treatement.treatement_request_error as tre
import treatement.treatement_request_lobby as trl
from src.GSNetwork import GSNetwork
from src.ClientThread import *


class lobbyThread(ClientThread):

    def __init__(self,Client_code):
        super().__init__(Client_code)


    """
    @brief: run gère un client du début à la fin
    @input: self, le thread du client
    @output: 0, tout est bien qui finit bien
    """
    def run(self):
        while(True):
            print("coucou")
            param = network.recv_msg_cli(self.Client_code).split(";")
            print(param)
            if(param == ['']):
                print(self.client_login)

                if(self.client_login != ""):
                    network.send_msg_DBS(str(trl.BACK_TO_CONNEXION) + ";" + self.client_login)
                    print(network.recv_msg_DBS())
                print("Mort du thread \n")
                return 0
            code_request = int(param.pop(0))

            if code_request == trl.INSCRIPTION:
                print("INSCRIPTION")
                if(trl.treatement_regex(param[0], "usr") and trl.treatement_regex(param[1], "mdp") and
                    trl.treatement_regex(param[2], "mail")):
                    self.client_login = param[0]
                    trl.treatement_inscription(network, self.Client_code, param, 0)
                else:
                    network.send_msg_cli(str(tre.ERROR_REGEX) + ";", self.Client_code)

            elif code_request == trl.CONNEXION:
                #renvoyer client si erreur
                if(trl.treatement_regex(param[0], "usr") and trl.treatement_regex(param[1], "mdp")):
                    self.client_login = param[0]
                    trl.treatement_connexion(network, self.Client_code, param, 0)
                else:

                    network.send_msg_cli(str(tre.ERROR_REGEX) + ";", self.Client_code)


            elif code_request == trl.STAT_GLOBALE:
                trl.treatement_stat_globales(network, self.Client_code, param, 0)

            elif code_request == trl.STAT_DET:
                trl.treatement_stat_det(network, self.Client_code, param, 0)

            elif code_request == trl.CREATE_ROOM:#creer_room
                #multiprocessig pour verifier l'etat de game pour savoir si c'est bien lance
                trl.treatement_create_room(network, self.Client_code, param, 0)
                break

            elif code_request == trl.JOIN_ROOM: #rejoindre_room
                trl.treatement_join_room(network, self.Client_code, param, 0)
                break

            elif code_request == trl.BACK_TO_CONNEXION: #retour en arriere
                trl.treatement_back_to(network, self.Client_code, param, 0)
                return 0

            elif code_request == trl.NEED_RECONNECTED: #Le client veut se rediriger au lobby
                trl.treatement_need_reconnected(network, self.Client_code, param, 0)

            else:#Attention prévoir le cas exit
                trl.treatement_back_to(network, self.Client_code, param, 0)
                break
        self.Client_code.close()
                #return 0;
        #threading.Thread.join()



network = GSNetwork(10000) #du main
while True:
    client_code = network.reception_client()
    if client_code == 400:
        
        # fermer la socket d'ecoute
        network.close_sockgs()
        # demander mainetance a la bdd
        network.send_msg_DBS("400;")
        # attente de reponse
        message = network.recv_msg_DBS()
        # reouvrir la socket d'ecoute
        network.open_sockgs(network.numport)
    else:
        newthread = lobbyThread(client_code)
        newthread.start()
