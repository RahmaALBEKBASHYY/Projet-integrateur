# @brief: ce fichier a pour but de rassembler toutes les chaines de caractere
#       utilise pour les appels mysql

CHECK_LOGIN_REQUEST             ="""
                                SELECT * FROM joueur WHERE login=%s;
                                """
CHECK_MAIL_REQUEST              ="""
                                SELECT * FROM joueur WHERE mailAddress=%s;
                                """
INSCRIPTION_REQUEST             ="""
                                INSERT INTO `joueur` (`login`,`mdp`,`mailAddress`,`codeMail`,`mailVerified`,`is_connected`,`is_in_room`)
                                VALUES (%s,SHA(%s),%s,%s,0,1,0);
                                """
CHECK_PW_REQUEST                ="""
                                SELECT * FROM joueur WHERE login=%s AND mdp=SHA(%s);
                                """
SET_CONNECTED_REQUEST           ="""
                                UPDATE joueur SET is_connected = 1 WHERE login = %s;
                                """
GET_ARCHIVE_DETAILLED_REQUEST   ="""
                                SELECT color, nbPoint, placement,nbGoodAnswer, nbBadAnswer, choux, knack,
                                pomme_de_terre, lard, vin, date_of_game, duree
                                FROM gamearchive WHERE Joueur_idJoueur = %s;
                                """
GET_NB_PLAYED_GAME_REQUEST      ="""
                                SELECT COUNT(idArchive) FROM gamearchive
                                WHERE Joueur_idJoueur = %s;
                                """
GET_NB_WINED_GAME_REQUEST       ="""
                                SELECT COUNT(idArchive) FROM gamearchive
                                WHERE Joueur_idJoueur = %s AND placement = 1;
                                """
GET_ARCHIVE_GLOBAL_REQUEST      ="""
                                SELECT SUM(duree), SUM(nbGoodAnswer), SUM(nbBadAnswer),
                                SUM(choux), SUM(knack), SUM(pomme_de_terre), SUM(lard), SUM(vin),
                                MAX(nbPoint), AVG(nbPoint) FROM gamearchive WHERE Joueur_idJoueur = %s;
                                """
SET_DISCONNECTED_REQUEST        ="""
                                UPDATE joueur SET is_connected = 0 WHERE login = %s;
                                """
CREATE_ARCHIVE_REQUEST          ="""
                                INSERT INTO gamearchive (Joueur_idJoueur, color, nbPoint, placement, nb_joueur,
                                nbGoodAnswer, nbBadAnswer, choux, knack, pomme_de_terre, lard, vin,
                                date_of_game, duree)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                """
FIND_PLAYER_ID_REQUEST          ="""
                                SELECT idJoueur FROM joueur WHERE login=%s;
                                """
IS_CONNECTED_REQUEST            ="""
                                SELECT * FROM joueur WHERE login=%s and is_connected=1;
                                """
CHECK_CODE_ROOM_REQUEST         ="""
                                SELECT * FROM partie WHERE partie_code = %s;
                                """
CREATE_ROOM_REQUEST             ="""
                                INSERT INTO partie (nbJoueur, date, partie_code, port_number, debut)
                                VALUES (0, %s, %s, %s, %s)
                                """
FIND_ROOM_ID_REQUEST            ="""
                                SELECT idPartie FROM partie WHERE partie_code = %s;
                                """
IS_IN_ROOM_REQUEST              ="""
                                SELECT is_in_room FROM joueur WHERE login = %s;
                                """
SET_PLAYER_IN_ROOM              ="""
                                UPDATE joueur SET is_in_room = 1 WHERE login = %s;
                                """
SET_PLAYER_NOT_IN_ROOM          ="""
                                UPDATE joueur SET is_in_room = 0 WHERE login = %s;
                                """
CREATE_PION_REQUEST             ="""
                                INSERT INTO pion VALUES (%s, %s, %s, 0, 1, 0, 0, 0, 0, 0, 0, 0);
                                """
UPDATE_PION_REQUEST             ="""
                                UPDATE pion SET nbPoint=%s, placement=%s, nbGoodAnswer=%s,
                                nbBadAnswer=%s, choux=%s, knack=%s, pomme_de_terre=%s, lard=%s, vin=%s
                                WHERE Joueur_idJoueur = %s;
                                """
GET_CATEGORIE_REQUEST           ="""
                                SELECT * FROM categorie;
                                """
GET_RANDOM_QUESTION             ="""
                                SELECT idQuestion, description FROM question
                                WHERE Categorie_idCategorie = %s and idQuestion NOT IN
                                    (SELECT Question_idQuestion FROM `partie-has-question` WHERE Partie_idPartie = %s)
                                ORDER BY RAND()
                                LIMIT 1;
                                """
ADD_QUESTION_PARTIE_REQUEST     ="""
                                INSERT INTO `partie-has-question` VALUES (%s, %s);
                                """
CLEAR_ALL_QUESTION_REQUEST      ="""
                                DELETE FROM `partie-has-question` WHERE Partie_idPartie = %s;
                                """
CLEAR_CATEGORIE_REQUEST         ="""
                                DELETE FROM `partie-has-question` WHERE Partie_idPartie = %s and
                                Question_idQuestion IN
                                    (SELECT idQuestion FROM question WHERE Categorie_idCategorie = %s);
                                """
ADD_PLAYER_ROOM_REQUEST         ="""
                                UPDATE partie SET nbJoueur = nbJoueur+1 WHERE partie_code = %s;
                                """
SUB_PLAYER_ROOM_REQUEST         ="""
                                UPDATE partie SET nbJoueur = nbJoueur-1 WHERE partie_code = %s;
                                """
GET_ROOM_PION_REQUEST           ="""
                                SELECT * FROM pion WHERE Partie_idPartie = %s;
                                """
DELETE_PION_REQUEST             ="""
                                DELETE FROM pion WHERE idJoueur = %s;
                                """
DELET_ROOM_REQUEST              ="""
                                DELETE FROM partie WHERE partie_code = %s;
                                """
GET_NB_PLAYER_ROOM              ="""
                                SELECT nbJoueur FROM partie WHERE partie_code = %s;
                                """
CHECK_PION_REQUEST              ="""
                                SELECT * FROM pion WHERE Joueur_idJoueur = %s;
                                """
GET_PORT_ROOM_REQUEST           ="""
                                SELECT port_number FROM partie;
                                """
GET_NUM_PORT_REQUEST            ="""
                                SELECT port_number FROM partie WHERE partie_code = %s;
                                """
VERIFIE_MAIL_REQUEST            ="""
                                SELECT * FROM joueur WHERE mailAddress=%s and codeMail=%s;
                                """
SET_MAIL_VERIFIED               ="""
                                UPDATE joueur SET mailVerified = 1 WHERE mailAddress = %s;
                                """
GET_ANSWERS_REQUEST             ="""
                                SELECT description, etat FROM reponses WHERE Question_idQuestion = %s;
                                """ 
