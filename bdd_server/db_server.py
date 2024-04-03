# db_serveur.py
# coding: utf-8

import socket


class DBNetwork():

    """
    @brief: Création d'objet data base Network
    @input: self
    @output: none
    """

    def __init__(self):
        self.sockdb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockdb.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sockdb.bind(("", 9999))

    def reception_server(self):
        print("Attente de connexion")
        self.sockdb.listen()
        (server_socket, server_adress) = self.sockdb.accept()
        print("Nouvelle connexion")
        return server_socket

    """
    @brief: Envoi un message à un thread game server
    @input: self; l'objet courant. data;les données à envoyer. num_thr; thread recepteur.
    @output: 0, succès
    """

    def send_msg_GS(self, data, server_socket):
        print("Envoi message: "+str(data))
        server_socket.send(data.encode())
        print("Message envoyé")
        return 0

    """
    @brief: Réception d'un msg du game server
    @input: self; l'objet courant. num_thr; thread recepteur.
    @output: r; le message reçu
    """

    def recv_msg_GS(self, server_socket):
        r = server_socket.recv(2048).decode()
        print("Message reçu: "+str(r))
        return r
