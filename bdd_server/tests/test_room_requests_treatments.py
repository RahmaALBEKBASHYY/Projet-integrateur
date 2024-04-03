# import des modules de test
import unittest

# import du fichier a tester
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import requests_treatments.lobby_requests_treatments as lrt
import managment_mysql as mmysql
import requests_treatments.treatments_error as te
import requests_treatments.room_requests_treatments as rrt
from connexion_mysql import *

class TestRoomRequestsTreatments(unittest.TestCase):
    def setUp(self):
        # on réinitilise la bdd
        mmysql.clear_bdd()
        mmysql.create_tables()
        mmysql.insert_data()
        # on ajoute un joueur de test
        lrt.inscription_treatments("test0","test0mdp","test0mail")
        # on ajoute une partie de test
        insert_or_update_data("insert into partie values(0,0,Null,'AAAA',10001,Null);",())
        return

    # @brief: permet de generer une archive pour le joueur donne
    # @input: tout le necessaire pour creer une archive
    # @output: 0 si tout est ok, code d'erreur sinon
    def test_create_archive(self):
        # on test de creer une archive
        self.assertEqual(rrt.create_archive("test0","r",200,2,3,4,4,1,1,1,1,1,None,None),te.SUCCESS)
        return

    # @brief: permet de savoir si le code d'une room existe ou non
    # @input: code de la room a tester
    # @output: true si elle existe, false sinon
    def test_check_code_room(self):
        # on test si la partie de test existe
        self.assertTrue(rrt.check_code_room("AAAA"))
        # on test si une room quelconque existe
        self.assertFalse(rrt.check_code_room("BBBB"))
        return

    # @brief: permet de savoir si un joueur est dans une room ou non
    # @input: le login de l'utilisateur
    # @output: true si c'est le cas, false sinon
    def test_is_in_room(self):
        # le joueur de test n'est pas dans une room
        self.assertFalse(rrt.is_in_room("test0"))
        # on le met dans le room de test
        rrt.set_player_in_room_treatments("test0", 'AAAA')
        # le joueur de test est dans une room
        self.assertTrue(rrt.is_in_room("test0"))
        return

    # @brief: permet d'incrementer le nombre de joueur dans la partie de 1
    # @input: le code de la room en question
    # @output: 0 ou un code d'erreur
    def test_add_nbplayer_room(self):
        # on test l'ajout d'un joueur dans une room du point de vue de la room
        self.assertEqual(rrt.add_nbplayer_room("AAAA"),te.SUCCESS)
        return

    # @brief: permet decrementer le nombre de joueur dans la partie de 1
    # @input: le code de la room en question
    # @output: 0 ou un code d'erreur
    def test_sub_nbplayer_room(self):
        # on test la suppression d'un joueur dans une room du point de vue de la room
        self.assertEqual(rrt.sub_nbplayer_room("AAAA"), te.SUCCESS)
        return

    # @brief: permet de mettre le statut d'un joueur "dans une room"
    # @input: le login de l'utilisateur
    # @output: 0 et numero de port si tout va bien, code d'erreur sinon
    def test_set_player_in_room_treatments(self):
        # on deconnecte le joueur test
        lrt.logout_treatments("test0")
        self.assertEqual(rrt.set_player_in_room_treatments("test0", "AAAA"), te.PLAYER_NOT_CONNECTED)
        # on reconnecte le joueur
        lrt.login_treatments("test0", "test0mdp")
        # on le met dans une room inexistante
        self.assertEqual(rrt.set_player_in_room_treatments("test0", "BBBB"), te.ROOM_CODE_NOT_FOUND)
        # on ajoute 4 joueurs dans la room
        rrt.add_nbplayer_room("AAAA")
        rrt.add_nbplayer_room("AAAA")
        rrt.add_nbplayer_room("AAAA")
        rrt.add_nbplayer_room("AAAA")
        self.assertEqual(rrt.set_player_in_room_treatments("test0", "AAAA"), te.ROOM_FULL)
        # on libert une place
        rrt.sub_nbplayer_room("AAAA")
        # on le met dans la bonne room
        ret = te.SUCCESS
        ret.append(10001)
        self.assertEqual(rrt.set_player_in_room_treatments("test0", "AAAA"), ret)
        # on le remet dans la room
        self.assertEqual(rrt.set_player_in_room_treatments("test0", "AAAA"), te.PLAYER_ALREADY_IN_ROOM)
        return

    # @brief: permet de mettre le statut d'un joueur "pas dans une room"
    # @input: le login de l'utilisateur
    # @output: 0 si tout va bien, code d'erreur sinon
    def test_set_player_not_in_room_treatments(self):
        # on deconnecte le joueur
        lrt.logout_treatments("test0")
        # on quitte la room
        self.assertEqual(rrt.set_player_not_in_room_treatments("test0", "AAAA"), te.PLAYER_NOT_CONNECTED)
        # on le reconnecte
        lrt.login_treatments("test0", "test0mdp")
        # on quitte la room
        self.assertEqual(rrt.set_player_not_in_room_treatments("test0", "AAAA"), te.PLAYER_NOT_IN_ROOM)
        # on le met dans la room
        rrt.set_player_in_room_treatments("test0", "AAAA")
        # on quitte une room inexistante
        self.assertEqual(rrt.set_player_not_in_room_treatments("test0", "BBBB"), te.ROOM_CODE_NOT_FOUND)
        # on quitte vraiment la room
        self.assertEqual(rrt.set_player_not_in_room_treatments("test0", "AAAA"), te.SUCCESS)

    # @brief: permet de supprimer la room de code code_room
    # @input: le code de la room a supprimer
    # @output: 0 si tout va bien, code d'erreur sinon
    def test_delete_room(self):
        # on supprime une partie inexistante
        self.assertEqual(rrt.delete_room("BBBB"), te.ROOM_CODE_NOT_FOUND)
        # on supprime la bonne partie
        self.assertEqual(rrt.delete_room("AAAA"), te.SUCCESS)

    # @brief: permet de trouver un numero de port dispo
    # @output: un numero de port ou -1 si aucun disponible
    def test_find_num_port(self):
        rrt.delete_room("AAAA")
        self.assertEqual(rrt.find_num_port(), 10001)
        insert_or_update_data("insert into partie values(0,0,Null,'AAAA',10001,Null);",())
        self.assertEqual(rrt.find_num_port(), 10002)
        insert_or_update_data("insert into partie values(0,0,Null,'BBBB',10002,Null);",())
        self.assertEqual(rrt.find_num_port(), 10003)
        insert_or_update_data("insert into partie values(0,0,Null,'CCCC',10003,Null);",())
        self.assertEqual(rrt.find_num_port(), 10004)
        insert_or_update_data("insert into partie values(0,0,Null,'DDDD',10004,Null);",())
        self.assertEqual(rrt.find_num_port(), 10005)
        insert_or_update_data("insert into partie values(0,0,Null,'EEEE',10005,Null);",())
        self.assertEqual(rrt.find_num_port(), 10006)
        insert_or_update_data("insert into partie values(0,0,Null,'FFFF',10006,Null);",())
        self.assertEqual(rrt.find_num_port(), 10007)
        insert_or_update_data("insert into partie values(0,0,Null,'GGGG',10007,Null);",())
        self.assertEqual(rrt.find_num_port(), te.NUM_PORT_NOT_VALID)
        return

    # @brief: permet de gerer une requete de creation de room
    # @input: le code de la room a creer
    # @output: 0 et code de la room en cas de reussite, code d'erreur sinon
    def test_create_room_treatments(self):
        # on deconnecte le joueur
        lrt.logout_treatments("test0")
        # il ne peut pas creer de room
        self.assertEqual(rrt.create_room_treatments("test0"), te.PLAYER_NOT_CONNECTED)
        # on le reconnecte
        lrt.login_treatments("test0", "test0mdp")
        # on le met dans une room
        rrt.set_player_in_room_treatments("test0", 'AAAA')
        # il ne peut pas creer de room
        self.assertEqual(rrt.create_room_treatments("test0"), te.PLAYER_ALREADY_IN_ROOM)
        # on le sort de la room
        rrt.set_player_not_in_room_treatments("test0", "AAAA")
        # il peut creer une room
        rrt.create_room_treatments("test0")
        return

    # @brief: permet de recupere l'id d'un partie a partie de son code de room
    # @input: le code de la room en question
    # @output: l'id de la room ou un code d'erreur en cas de probleme
    def test_find_room_id(self):
        # on regarde si la room de test a bien l'id 1
        self.assertEqual(rrt.find_room_id("AAAA"),1)
        # on regarde pour une room inexistante
        self.assertEqual(rrt.find_room_id("BBBB"),te.ROOM_CODE_NOT_FOUND)
        return

    # @brief: permet de savoir si un joueur a un pion ou non
    # @input: le joueur en question
    # @output: True si un pion existe, False sinon
    def test_check_pion(self):
        self.assertFalse(rrt.check_pion("test0"))
        rrt.set_player_in_room_treatments("test0","AAAA")
        rrt.create_pion_treatments("test0", "AAAA", 'r')
        self.assertTrue(rrt.check_pion("test0"))
        return

    # @brief: permet d'ajouter un joueur a une room existante
    # @input: le code de la room et le joueur
    # @output: 0,num_port en cas de reussite, code d'erreur sinon
    def test_create_pion_treatments(self):
        # on deconnecte le client
        lrt.logout_treatments("test0")
        # on cree son pion
        self.assertEqual(rrt.create_pion_treatments("test0","AAAA",'r'), te.PLAYER_NOT_CONNECTED)
        # on reconnecte le client
        lrt.login_treatments("test0","test0mdp")
        # on cree son pion
        self.assertEqual(rrt.create_pion_treatments("test0","AAAA",'r'), te.PLAYER_NOT_IN_ROOM)
        # on ajoute le client a la room
        rrt.set_player_in_room_treatments("test0","AAAA")
        # on cree son pion avec une room inexistante
        self.assertEqual(rrt.create_pion_treatments("test0", "BBBB", 'r'),te.ROOM_CODE_NOT_FOUND)
        # on cree son pion
        self.assertEqual(rrt.create_pion_treatments("test0", "AAAA", 'r'), te.SUCCESS)
        # on recree son pion
        self.assertEqual(rrt.create_pion_treatments("test0", "AAAA", 'r'), te.PION_FIND)
        return

    # @brief: permet de mettre a jour les stats du pion
    #       (apres reponse a une question)
    # @input: le joueur, le nombre de points, le classement du joueur
    #       reponse juste ou fausse, un aliment de complete en cas de question speciale
    # @output: 0 en cas de reussite, code d'erreur sinon
    def test_update_pion_treatments(self):
        # on deconnecte le client
        lrt.logout_treatments("test0")
        # on met a jour son pion
        self.assertEqual(rrt.update_pion_treatments("test0", 200, 3, 2, 2, 0, 0, 0, 0, 0), te.PLAYER_NOT_CONNECTED)
        # on reconnecte le client
        lrt.login_treatments("test0","test0mdp")
        # on met a jour son pion
        self.assertEqual(rrt.update_pion_treatments("test0", 200, 3, 2, 2, 0, 0, 0, 0, 0), te.PLAYER_NOT_IN_ROOM)
        # on l'ajoute a une room
        rrt.set_player_in_room_treatments("test0","AAAA")
        # on met a jour son pion
        self.assertEqual(rrt.update_pion_treatments("test0", 200, 3, 2, 2, 0, 0, 0, 0, 0), te.PION_NOT_FOUND)
        # on cree son pion
        rrt.create_pion_treatments("test0","AAAA",'r')
        # on update son pion
        self.assertEqual(rrt.update_pion_treatments("test0", 200, 3, 2, 2, 0, 0, 0, 0, 0), te.SUCCESS)
        return

    # @brief: permet d'envoyer les categories disponibles au serveur
    # @output: 0 + tableau categorie en cas de reussite, code d'erreur sinon
    def test_send_categorie_treatments(self):
        self.assertEqual(rrt.send_categorie_treatments(),
        [0,(1, 'b', 'h', 'c'),
        (2, 'r', 's', 'k'),
        (3, 'j', 'n', 'p'),
        (4, 'v', 'c', 'l'),
        (5, 'g', 'g', 'v'),
        (6, 'o', 'a', 'f')])
        return

    # @brief: permet d'ajouter une question a partie-has-question
    #       pour eviter de reprendre la meme
    # @input: l'id de la partie et l'id de la question
    # @output: 0 si tout va bien, code d'erreur sinon
    def test_add_partie_has_question(self):
        # on test l'ajout de la question a la room
        self.assertEqual(rrt.add_partie_has_question(1,1), te.SUCCESS)
        return

    # @brief: permet de savoir si des question sont encore disponible
    #       pour une categorie et une partie donnee
    # @input: l'id de la categorie et de la partie
    # @output: True s'il n'y a plus de question diponible, False sinon
    def test_is_empty_question_categorie_room(self):
        # on test si une question est dispo
        self.assertFalse(rrt.is_empty_question_categorie_room(1,1))
        # on ajoute toute les questions
        for i in range(1,121):
            rrt.add_partie_has_question(1,i)
        # on test si bien aucune question de dispo pour une cat
        self.assertTrue(rrt.is_empty_question_categorie_room(1,1))
        return

    # @brief: permet de remettre en jeu toutes les questions
    #       d'une ou toutes les categorie(s) pour une partie donnee
    # @input: l'id de la categorie a remettre en jeu (-1 si toutes)
    #       l'id de la partie en question
    # @output: 0 si tout va bien, code d'erreur sinon
    def test_clear_partie_has_qestion(self):
        # on ajoute toute les questions a la partie
        for i in range(1,121):
            rrt.add_partie_has_question(1,i)
        # on clear que celle de categorie 1
        self.assertEqual(rrt.clear_partie_has_qestion(1,1), te.SUCCESS)
        # on test si c'est bon
        self.assertFalse(rrt.is_empty_question_categorie_room(1,1))
        self.assertTrue(rrt.is_empty_question_categorie_room(2,1))
        # on clear tout le reste
        self.assertEqual(rrt.clear_partie_has_qestion(-1,1), te.SUCCESS)
        # on test si c'est bon
        self.assertFalse(rrt.is_empty_question_categorie_room(2,1))
        self.assertFalse(rrt.is_empty_question_categorie_room(3,1))
        return

    # @brief: permet de gerer la fin d'une partie et nettoyer la bdd en consequence
    # @input: l'id de la partie, le temps de la partie
    # @output: 0 si tout va bien, code d'erreur sinon
    def test_send_question_treatments(self):
        # on test avec categorie inexistante
        self.assertEqual(rrt.send_question_treatments(7,"AAAA"), te.BAD_CATEGORIE_ID)
        # on test avec room inexistante
        self.assertEqual(rrt.send_question_treatments(2,"BBBB"), te.ROOM_CODE_NOT_FOUND)
        return

    # @brief: permet de gerer la fin d'une partie et nettoyer la bdd en consequence
    # @input: l'id de la partie, le temps de la partie
    # @output: 0 si tout va bien, code d'erreur sinon
    def test_end_game_treatments(self):
        # on ajoute le joueur a la game
        rrt.create_pion_treatments("test0", "AAAA", 'r')
        # on test la fin d'une game
        self.assertEqual(rrt.end_game_treatments("AAAA", None), te.SUCCESS)
        return

    # @brief: permet de supprimer un pion
    # @input: l'id du joueur ayant le pion
    # @output: 0 si tout va bien, code d'erreur sinon
    def delete_pion(id_joueur):
        # on supprimer un pion inexistant
        self.assertEqual(rrt.delete_pion(2), te.MYSQL_ERROR)
        # on ajoute le joueur a la partie
        rrt.create_pion_treatments("test0", "AAAA", 'r')
        # on supprime son pion
        self.assertEqual(rrt.delete_pion(1), te.SUCCESS)

if __name__ == '__main__':
    # on lance les tests
    unittest.main()

    # on réinitilise la bdd
    mmysql.clear_bdd()
    mmysql.create_tables()
    mmysql.insert_data()
