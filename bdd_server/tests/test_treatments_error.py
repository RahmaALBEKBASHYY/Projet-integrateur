# import des modules de test
import unittest

# import du fichier a tester
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import requests_treatments.treatments_error as te
import managment_mysql as mmysql
import requests_treatments.lobby_requests_treatments as lrt

class TestTreatmentsError(unittest.TestCase):
    def setUp(self):
        # on réinitilise la bdd
        mmysql.clear_bdd()
        mmysql.create_tables()
        mmysql.insert_data()
        # on ajoute un joueur de test
        lrt.inscription_treatments("test0","test0mail","test0mdp")
        return

    # @brief: permet de verifier si un joueur est connecte ou non
    # @input: login de l'utilisateur
    # @output: True si le joueur est connecte, False sinon
    def test_is_connected(self):
        # le joueur est connecte
        self.assertTrue(te.is_connected("test0"))
        # le joueur n'est pas connecte
        lrt.logout_treatments("test0")
        self.assertFalse(te.is_connected("test0"))

    # @brief: permet de trouver l'id d'un joueur a partir de son login
    # @input: login de l'utilisateur
    # @output: id de l'utilisateur ou code d'erreur
    def test_find_player_id(self):
        # on trouve l'id du joueur
        self.assertEqual(te.find_player_id("test0"),1)
        # le joueur n'existe pas
        self.assertEqual(te.find_player_id("test1"),te.MYSQL_ERROR)

if __name__ == '__main__':
    unittest.main()
