# game_serveur.py
# coding: utf-8

import socket
import socketserver
import threading
from time import sleep

# GS: game server
# DBS: data base server


class GSNetwork():

    """
    @brief: Création d'objet game server Network
    @input: self: l'objet, port: le num de port
    @output: none
    """

    def __init__(self, port):
        # creating socket
        self.open_sockgs(port)
        self.numport = port
        self.sockDB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockDB.connect(("192.168.0.10", 9999))

    """
    @brief: receptionne les clients en lobby
    @input: self: l'objet
    @output: boolean
    """

    def reception_client(self):
        # Incoming connections
        print("Waiting for client ...")
        self.sockgs.listen()
        (clientSocket, ip) = self.sockgs.accept()
        print(ip[0])
        if ip[0] == "127.0.0.1":
            return 400  # demande de maintenance
        print("client accept...")

        return clientSocket

    """
    @brief: receptionne les clients pour les parties
    @input: self: l'objet, game:l'objet client, lock: verrous
    @output: boolean
    """

    def reception_game(self, game, lock):
        # Incoming connections
        print("Waiting for client ...")
        self.sockgs.listen()
        indice = -1
        lock.acquire()
        if len(game.clients) < 4:
            indice = len(game.clients)
            (clientSocket, _) = self.sockgs.accept()
            game.appendClient(clientSocket)
            print("client accept...")
        lock.release()

        return (clientSocket, indice)

    """
    @brief: Envoi un msg à un client
    @input: les données et le numéro de client
    @output: 0, succès d'envoi
    """

    def send_msg_cli(self, data, client):
        print("send : " + data)
        if (client == None):
            return -1
        sleep(0.2)
        client.send(data.encode())
        return 0

    """
    @brief: ferme la socket client
    @input: self: l'objet
    @output: boolean
    """

    def broadcast_cli(self, data, tab_client):
        for clients in tab_client:
            try:
                if(clients.joueur):
                    self.send_msg_cli(data, clients.socket)
            except socket.error:
                clients.joueur = False
                pass

    """
    @brief: Réception d'un msg d'un client spécifique
    @input: numéro client
    @output: r; le message reçu
    """

    def recv_msg_cli(self, client):
        if (client == -1):
            return -1

        print("Waiting data from client ...")
        # Data received from the client
        r = client.recv(2048).decode().strip('\n')
        print("data from client received ...")
        print(r)
        return r

    """
    @brief: ferme la socket client
    @input: self: l'objet
    @output: boolean
    """

    def close_sockgs(self):
        print("fermeture de la socket client")
        self.sockgs.close()
        return 0

    """
    @brief: ouvre la socket client
    @input: self: l'objet, port: le num de port
    @output: boolean
    """

    def open_sockgs(self, port):
        # creating socket
        print("ouverture de la socket client")
        self.sockgs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockgs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockgs.bind(("", port))
        return 0

    """
    @brief: Envoi d'un msg à la base de donnée
    @input: les données à envoyer
    @output: 0, succès
    """

    def send_msg_DBS(self, data):
        print("to bdd : " + data)
        self.sockDB.send(data.encode())
        print("msg sent to DBS.")
        return 0

    """
    @brief: Réception d'un msg de la base de données
    @input: objet courant
    @output: reply; message reçu
    """

    def recv_msg_DBS(self):
        print("from bdd: ...")
        retour = self.sockDB.recv(2048).decode()
        print(f"msg : {retour}")
        return retour

    """
    @brief: Fermeture d'une socket bdd
    @input: objet courant
    @output: 0, succès
    """

    def close_DBsock(self):
        self.sockDB.close()
        return 0


"""
overwrite la classe GSNetwork
"""


class Reseau:

    def __init__(self):
        self.valeur = 0

    def send_msg_DBS(self, param):
        return str(self.valeur)

    def send_msg_cli(self, param, numSocket):
        return str(self.valeur)

    def recv_msg_DBS(self):
        return str(self.valeur) + ";"

    def recv_msg_cli(self, num_cli=-1):
        return str(self.valeur) + ";"

    def ask_port(self):
        return 1
