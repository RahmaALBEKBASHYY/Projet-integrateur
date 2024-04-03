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

class TestLobbyRequestsTreatments(unittest.TestCase):

    # @brief: permet de verifier si un login existe ou non
    # @input: login de l'utilisateur
    # @output: True si le login existe dans la base, False sinon,
    # MYSQL_ERROR en cas de probleme sql
    def test_check_login(self):
        # le login existe
        self.assertTrue(lrt.check_login("test0"))
        # le login n'existe pas
        self.assertFalse(lrt.check_login("test1"))

    # @brief: permet de verifier si un mail existe ou non
    # @input: mail de l'utilisateur
    # @output: True si le mail existe dans la base, False sinon
    def test_check_mail(self):
        # le mail existe
        self.assertTrue(lrt.check_mail("test0mail"))
        # le mail n'existe pas
        self.assertFalse(lrt.check_mail("test1mail"))

    # @brief: permet de gerer une requete d'inscription
    # @input:
    # - login de l'utilisateur
    # - mot de passe de l'utilisateur
    # - mail de l'utilisateur
    # @output: 0 en cas de reussite, code d'erreur sinon
    def test_inscription_treatments(self):
        # on inscrit quelqu'un sans probleme
        self.assertEqual(lrt.inscription_treatments("test1", "test1mdp", "test1mail", "AAAA"), te.SUCCESS)
        # le login est deja pris
        self.assertEqual(lrt.inscription_treatments("test1","test1.1mdp","test1.1mail", "AAAA"), te.LOGIN_NOT_UNIQUE)
        # le mail est deja pris
        self.assertEqual(lrt.inscription_treatments("test1.1","test1.1mdp","test1mail", "AAAA"), te.MAIL_NOT_UNIQUE)

    # @brief: permet de tester le verification de mail
    # @input: l'adresse mail a verifier, le code recu par le joueur
    # @output: 0 en cas de reussite, code d'erreur sinon
    def test_verifie_mail(self):
        # on test un verification correcte
        self.assertEqual(lrt.verifie_mail("test0mail", "AAAA"), te.SUCCESS)
        # on test avec un mauvais code de verification
        self.assertEqual(lrt.verifie_mail("test1mail", "BBBB"), te.BAD_CODE_MAIL)

    # @brief: permet de gerer une requete de connexion
    # @input:
    # - login de l'utilisateur
    # - mot de passe de l'utilisateur
    # @output: 0 si la personne peut se connecter, code d'erreur sinon
    def test_login_treatments(self):
        # on deconnecte le joueur test
        lrt.logout_treatments("test0")
        # le login n'existe pas
        self.assertEqual(lrt.login_treatments("test2","test2mdp"),te.LOGIN_NOT_FOUND)
        # le mot de passe est incorrect
        self.assertEqual(lrt.login_treatments("test0","test1mdp"),te.BAD_PASSWORD)
        # on arrive a se connecter
        self.assertEqual(lrt.login_treatments("test0","test0mdp"),te.SUCCESS)
        # on est deja connecte
        self.assertEqual(lrt.login_treatments("test0","test0mdp"),te.PLAYER_CONNECTED)

    # @brief: permet de gerer une requete de consultation d'archive detaillee
    # @input:
    # - login de l'utilisateur
    # @output: 0 + tableau des archives detaillees ou code d'erreur
    def test_archive_detailed_consultation_treatments(self):
        # on recupere ses archives sans probleme
        self.assertEqual(lrt.archive_detailed_consultation_treatments("test0",0,10),
        [0,('r', 200, 2, 4, 4, 1, 1, 1, 1, 1, None, None)])
        # le login n'existe pas
        self.assertEqual(lrt.archive_detailed_consultation_treatments("test1",0,10),te.LOGIN_NOT_FOUND)
        # on deconnecte le joueur test
        lrt.logout_treatments("test0")
        # le joueur n'est pas connecte
        self.assertEqual(lrt.archive_detailed_consultation_treatments("test0",0,10),te.PLAYER_NOT_CONNECTED)
        # on reconnecte le joueur de test
        lrt.login_treatments("test0", "test0mdp")

    # @brief: permet de recuperer le nombre de partie jouees par le joueur
    # @input: l'identifiant du joueur dans la base de donnees
    # @output: le nombre de partie jouee par le joueur ou un code d'erreur
    def test_get_nb_played_game(self):
        # le test a joue une game
        self.assertEqual(lrt.get_nb_played_game(1)[0][0],1)

    # @brief: permet de recuperer le nombre de partie gagnees par le joueur
    # @input: l'identifiant du joueur dans la base de donnees
    # @output: le nombre de partie gagnee par le joueur ou un code d'erreur
    def test_get_nb_wined_game(self):
        # le test n'a pas gagne de game
        self.assertEqual(lrt.get_nb_wined_game(1)[0][0],0)

    # @brief: permet de gerer une requete de consultation d'archive globale
    # @input:
    # - login de l'utilisateur
    # @output: 0 + tableau des archives globales ou code d'erreur
    def test_archive_global_consultation_treatments(self):
        # on recupere les stats sans probleme
        self.assertEqual(lrt.archive_global_consultation_treatments("test0"),
        [0, None, 4,4,1,1,1,1,1,200,200,1,0])
        # le login n'existe pas
        self.assertEqual(lrt.archive_global_consultation_treatments("test1"),
        te.LOGIN_NOT_FOUND)
        # on deconnecte le joueur test
        lrt.logout_treatments("test0")
        # le joueur n'est pas connecte
        self.assertEqual(lrt.archive_global_consultation_treatments("test0"),
        te.PLAYER_NOT_CONNECTED)
        # on reconnecte le joueur de test
        lrt.login_treatments("test0", "test0mdp")

    # @brief: permet de gerer une requete de deconnexion
    # @input:
    # - login de l'utilisateur
    # @output: true en cas de reussite, false sinon
    def test_logout_treatments(self):
        # on deconnecte le joueur test sans probleme
        self.assertEqual(lrt.logout_treatments("test0"),te.SUCCESS)
        # le login n'existe pas
        self.assertEqual(lrt.logout_treatments("test2"), te.LOGIN_NOT_FOUND)
        # le joueur est deja deconnecte
        self.assertEqual(lrt.logout_treatments("test0"), te.PLAYER_NOT_CONNECTED)

if __name__ == '__main__':
    # on réinitilise la bdd
    mmysql.clear_bdd()
    mmysql.create_tables()
    mmysql.insert_data()

    # on ajoute un joueur de test
    lrt.inscription_treatments("test0","test0mdp","test0mail", "AAAA")

    # on ajoute une archive pour le joueur test
    rrt.create_archive("test0",'r',200,2,3,4,4,1,1,1,1,1,None, None)

    # on lance les tests
    unittest.main()
