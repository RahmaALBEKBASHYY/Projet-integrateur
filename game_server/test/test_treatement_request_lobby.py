import unittest

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import treatement.treatement_request_lobby as trl
from src.GSNetwork import Reseau

"""
@brief: classe permettant de tester le fichier treatement_request_lobby en faisant varier
        les retours de la bdd
@input: unittest: test unitaire de python
@output: none
"""
class TestTreatementLobby(unittest.TestCase):

    """
    @brief: Cree l'objet reseau pour tester les diverses fonctions
    @input: self: instance de la classe
    @output: none
    """
    def setUp(self):
        self.reseau = Reseau()

    """
    @brief: Detruit l'objet reseau pour tester les diverses fonctions
    @input: self: instance de la classe
    @output: none
    """
    def tearDown(self):
        self.reseau = None

    """
    @brief: teste la fonction treatement_need_reconnected
    @input: self: instance de la classe
    @output: none
    """
    def test_need_reconnected(self):
        #test le premier cas si tout se passe bien
        self.reseau.valeur = trl.OK
        self.assertTrue(trl.treatement_need_reconnected(self.reseau, 0, ["+",],0))

        #test le cas d'une déconnection
        self.reseau.valeur = trl.ALREADY_DISCONNECTED
        self.assertFalse(trl.treatement_need_reconnected(self.reseau, 0, ["+",],0))

        #test si problème mysql
        self.reseau.valeur = trl.MYSQL_DOOMED
        self.assertFalse(trl.treatement_need_reconnected(self.reseau, 0, ["+",],0))

        #mauvais code 
        self.reseau.valeur = trl.CREATE_ROOM
        self.assertFalse(trl.treatement_need_reconnected(self.reseau, 0, ["+",],0))

    """
    @brief: teste la fonction treatement_connexion
    @input: self: instance de la classe
    @output: none
    """
    def test_connexion(self):
        #test le premier cas si tout se passe bien
        self.reseau.valeur = trl.OK
        self.assertTrue(trl.treatement_connexion(self.reseau, 0, ["+",],0))

        #test le cas d'un client deja connecte
        self.reseau.valeur = trl.ALREADY_CONNECTED
        self.assertFalse(trl.treatement_connexion(self.reseau, 0, ["+",],0))

        #test si le mdp est le mauvais
        self.reseau.valeur = trl.MAUVAIS_MDP
        self.assertFalse(trl.treatement_connexion(self.reseau, 0, ["+",],0))

        #test si le login n'existe pas
        self.reseau.valeur = trl.LOGIN_INEXISTANT
        self.assertFalse(trl.treatement_connexion(self.reseau, 0, ["+",],0))

        #test si problème mysql
        self.reseau.valeur = trl.MYSQL_DOOMED
        self.assertFalse(trl.treatement_connexion(self.reseau, 0, ["+",],0))

        #mauvais code 
        self.reseau.valeur = trl.CREATE_ROOM
        self.assertFalse(trl.treatement_connexion(self.reseau, 0, ["+",],0))

    """
    @brief: teste la fonction treatement_inscription
    @input: self: instance de la classe
    @output: none
    """
    def test_inscription(self):
        #test le premier cas si tout se passe bien
        self.reseau.valeur = trl.OK
        self.assertTrue(trl.treatement_inscription(self.reseau, 0, ["+"],0))

        #test si le login existe déjà
        self.reseau.valeur = trl.LOGIN_EXISTANT
        self.assertFalse(trl.treatement_inscription(self.reseau, 0, ["+"],0))

        #test si le mail existe deja
        self.reseau.valeur = trl.EMAIL_EXISTANT
        self.assertFalse(trl.treatement_inscription(self.reseau, 0, ["+"],0))

        #test si problème mysql
        self.reseau.valeur = trl.MYSQL_DOOMED
        self.assertFalse(trl.treatement_inscription(self.reseau, 0, ["+"],0))

        #mauvais code 
        self.reseau.valeur = trl.CREATE_ROOM
        self.assertFalse(trl.treatement_inscription(self.reseau, 0, ["+"],0))

    """
    @brief: test la fonction treatement_stat_globales
    @input: self: instance de la classe
    @output: none
    """
    def test_stat_glo(self):
        #test le premier cas si tout se passe bien
        self.reseau.valeur = trl.OK
        self.assertTrue(trl.treatement_stat_globales(self.reseau, 0, ["+"],0))

        #test si le login existe déjà
        self.reseau.valeur = trl.LOGIN_INEXISTANT
        self.assertFalse(trl.treatement_stat_globales(self.reseau, 0, ["+"],0))

        #test si le joueur n'est pas deco
        self.reseau.valeur = trl.ALREADY_DISCONNECTED
        self.assertFalse(trl.treatement_stat_globales(self.reseau, 0, ["+"],0))

        #test si problème mysql
        self.reseau.valeur = trl.MYSQL_DOOMED
        self.assertFalse(trl.treatement_stat_globales(self.reseau, 0, ["+"],0))

        #mauvais code 
        self.reseau.valeur = trl.CREATE_ROOM
        self.assertFalse(trl.treatement_stat_globales(self.reseau, 0, ["+"],0))


    """
    @brief: test la fonction treatement_stat_det
    @input: self: instance de la classe
    @output: none
    """
    def test_stat_det(self):
        #test le premier cas si tout se passe bien
        self.reseau.valeur = trl.OK
        self.assertTrue(trl.treatement_stat_det(self.reseau, 0, ["+"],0))

        #test si le login n'existe pas
        self.reseau.valeur = trl.LOGIN_INEXISTANT
        self.assertFalse(trl.treatement_stat_det(self.reseau, 0, ["+"],0))

        #test si le joueur est deco
        self.reseau.valeur = trl.ALREADY_DISCONNECTED
        self.assertFalse(trl.treatement_stat_det(self.reseau, 0, ["+"],0))

        #test si problème mysql
        self.reseau.valeur = trl.MYSQL_DOOMED
        self.assertFalse(trl.treatement_stat_det(self.reseau, 0, ["+"],0))

        #mauvais code 
        self.reseau.valeur = trl.CREATE_ROOM
        self.assertFalse(trl.treatement_stat_det(self.reseau, 0,["+"],0))

    
    """
    @brief: test la fonction treatement_create_room
    @input: self: instance de la classe
    @output: none
    """
    def test_create_room(self):
        #test le premier cas si tout se passe bien
        self.reseau.valeur = trl.OK
        self.assertTrue(trl.treatement_create_room(self.reseau, 0, ["+", "10001"],0))

        #test si le joueur est deja en game
        self.reseau.valeur = trl.ALREADY_IN_GAME
        self.assertFalse(trl.treatement_create_room(self.reseau, 0, ["+"],0))

        #test si le joueur est deco
        self.reseau.valeur = trl.ALREADY_DISCONNECTED
        self.assertFalse(trl.treatement_create_room(self.reseau, 0, ["+"],0))

        #test si problème mysql
        self.reseau.valeur = trl.MYSQL_DOOMED
        self.assertFalse(trl.treatement_create_room(self.reseau, 0, ["+"],0))

        #mauvais code 
        self.reseau.valeur = trl.CREATE_ROOM
        self.assertFalse(trl.treatement_create_room(self.reseau, 0,["+"],0))



    """
    @brief: test la fonction treatement_join_room
    @input: self: instance de la classe
    @output: none
    """
    def test_join_room(self):
        #test le premier cas si tout se passe bien
        self.reseau.valeur = trl.OK
        self.assertTrue(trl.treatement_join_room(self.reseau, 0, ["+"],0))

        #test si le joueur est deja en game
        self.reseau.valeur = trl.ALREADY_IN_GAME
        self.assertFalse(trl.treatement_join_room(self.reseau, 0, ["+"],0))

        #test si le joueur est deco
        self.reseau.valeur = trl.ALREADY_DISCONNECTED
        self.assertFalse(trl.treatement_join_room(self.reseau, 0, ["+"],0))

        #test si la room n'est pas trouve
        self.reseau.valeur = trl.ROOM_NOT_FIND
        self.assertFalse(trl.treatement_join_room(self.reseau, 0, ["+"],0))

        #test si il y a trop de personnes
        self.reseau.valeur = trl.TOO_MUCH_PERSONS
        self.assertFalse(trl.treatement_join_room(self.reseau, 0, ["+"],0))

        #test si problème mysql
        self.reseau.valeur = trl.MYSQL_DOOMED
        self.assertFalse(trl.treatement_join_room(self.reseau, 0, ["+"],0))

        #mauvais code 
        self.reseau.valeur = trl.CREATE_ROOM
        self.assertFalse(trl.treatement_join_room(self.reseau, 0,["+"],0))


    """
    @brief: test la fonction treatement_back_to
    @input: self: instance de la classe
    @output: none
    """
    def test_back_to(self):
        #test le premier cas si tout se passe bien
        self.reseau.valeur = trl.OK
        self.assertTrue(trl.treatement_back_to(self.reseau, 0, ["+"],0))

        #test si le joueur est deja en game
        self.reseau.valeur = trl.ALREADY_DISCONNECTED
        self.assertFalse(trl.treatement_back_to(self.reseau, 0, ["+"],0))

        #test si problème mysql
        self.reseau.valeur = trl.MYSQL_DOOMED
        self.assertFalse(trl.treatement_back_to(self.reseau, 0, ["+"],0))

        #mauvais code 
        self.reseau.valeur = trl.CREATE_ROOM
        self.assertFalse(trl.treatement_back_to(self.reseau, 0,["+"],0))

if __name__ == '__main__':
    unittest.main()
