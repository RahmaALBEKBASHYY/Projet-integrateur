SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `choucroute_pursuit`
--

-- --------------------------------------------------------

--
-- Table structure for table `categorie`
--

DROP TABLE IF EXISTS `categorie`;
CREATE TABLE IF NOT EXISTS `categorie` (
  `idCategorie` int NOT NULL AUTO_INCREMENT,
  `color` char(1) NOT NULL,
  `nom` char(1) NOT NULL,
  `foodAssociated` char(1) NOT NULL,
  PRIMARY KEY (`idCategorie`),
  UNIQUE KEY `color_UNIQUE` (`color`),
  UNIQUE KEY `nom_UNIQUE` (`nom`),
  UNIQUE KEY `foodAssociated_UNIQUE` (`foodAssociated`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

--
-- Table structure for table `gamearchive`
--

DROP TABLE IF EXISTS `gamearchive`;
CREATE TABLE IF NOT EXISTS `gamearchive` (
  `idArchive` int NOT NULL AUTO_INCREMENT,
  `Joueur_idJoueur` int NOT NULL,
  `color` varchar(45) DEFAULT NULL,
  `nbPoint` int DEFAULT NULL,
  `placement` int DEFAULT NULL,
  `nb_joueur` int DEFAULT NULL,
  `nbGoodAnswer` int DEFAULT NULL,
  `nbBadAnswer` int DEFAULT NULL,
  `choux` tinyint DEFAULT NULL,
  `knack` tinyint DEFAULT NULL,
  `pomme_de_terre` tinyint DEFAULT NULL,
  `lard` tinyint DEFAULT NULL,
  `vin` tinyint DEFAULT NULL,
  `date_of_game` date DEFAULT NULL,
  `duree` time DEFAULT NULL,
  PRIMARY KEY (`idArchive`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

ALTER TABLE `gamearchive`
	ADD CONSTRAINT `fk_gamearchive_User1`
    FOREIGN KEY (`Joueur_idJoueur`)
    REFERENCES `joueur` (`idJoueur`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;


-- --------------------------------------------------------

--
-- Table structure for table `joueur`
--

DROP TABLE IF EXISTS `joueur`;
CREATE TABLE IF NOT EXISTS `joueur` (
  `idJoueur` int NOT NULL AUTO_INCREMENT,
  `login` varchar(45) NOT NULL,
  `mailAddress` varchar(45) NOT NULL,
  `codeMail` varchar(45) DEFAULT NULL,
  `mailVerified` tinyint NOT NULL,
  `mdp` varchar(45) NOT NULL,
  `is_connected` tinyint NOT NULL,
  `is_in_room` tinyint NOT NULL,
  PRIMARY KEY (`idJoueur`),
  UNIQUE KEY `login_UNIQUE` (`login`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `partie`
--

DROP TABLE IF EXISTS `partie`;
CREATE TABLE IF NOT EXISTS `partie` (
  `idPartie` int NOT NULL AUTO_INCREMENT,
  `nbJoueur` int NOT NULL,
  `date` date DEFAULT NULL,
  `partie_code` varchar(45) NOT NULL,
  `port_number` int NOT NULL,
  `debut` time DEFAULT NULL,
  PRIMARY KEY (`idPartie`),
  UNIQUE KEY `partie_code_UNIQUE` (`partie_code`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `partie-has-question`
--

DROP TABLE IF EXISTS `partie-has-question`;
CREATE TABLE IF NOT EXISTS `partie-has-question` (
  `Partie_idPartie` int NOT NULL,
  `Question_idQuestion` int NOT NULL,
  PRIMARY KEY (`Partie_idPartie`,`Question_idQuestion`),
  KEY `fk_Partie_has_Question_Question1_idx` (`Question_idQuestion`),
  KEY `fk_Partie_has_Question_Partie1_idx` (`Partie_idPartie`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

ALTER TABLE `partie-has-question`
	ADD CONSTRAINT `fk_Partie_has_Question_Partie1`
     FOREIGN KEY (`Partie_idPartie`)
    REFERENCES `partie` (`idPartie`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE `partie-has-question`
	ADD CONSTRAINT `fk_Partie_has_Question_Question1`
    FOREIGN KEY (`Question_idQuestion`)
    REFERENCES `question` (`idQuestion`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
-- --------------------------------------------------------

--
-- Table structure for table `pion`
--

DROP TABLE IF EXISTS `pion`;
CREATE TABLE IF NOT EXISTS `pion` (
  `Joueur_idJoueur` int NOT NULL,
  `Partie_idPartie` int NOT NULL,
  `color` char DEFAULT NULL,
  `nbPoint` int DEFAULT NULL,
  `placement` int DEFAULT NULL,
  `nbGoodAnswer` int DEFAULT NULL,
  `nbBadAnswer` int DEFAULT NULL,
  `choux` tinyint DEFAULT NULL,
  `knack` tinyint DEFAULT NULL,
  `pomme_de_terre` tinyint DEFAULT NULL,
  `lard` tinyint DEFAULT NULL,
  `vin` tinyint DEFAULT NULL,
  PRIMARY KEY (`Joueur_idJoueur`,`Partie_idPartie`),
  KEY `fk_Pion_Joueur1_idx` (`Joueur_idJoueur`),
  KEY `fk_Pion_Partie1_idx` (`Partie_idPartie`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

ALTER TABLE `pion`
	ADD CONSTRAINT `fk_Pion_Joueur1`
   FOREIGN KEY (`Joueur_idJoueur`)
    REFERENCES `joueur` (`idJoueur`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE `pion`
	ADD CONSTRAINT `fk_Pion_Partie1`
    FOREIGN KEY (`Partie_idPartie`)
    REFERENCES `partie` (`idPartie`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;
-- --------------------------------------------------------

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
CREATE TABLE IF NOT EXISTS `question` (
  `idQuestion` int NOT NULL AUTO_INCREMENT,
  `description` longtext NOT NULL,
  `lang` varchar(45) CHARACTER SET utf8mb4 DEFAULT 'fr',
  `Categorie_idCategorie` int NOT NULL,
  PRIMARY KEY (`idQuestion`,`Categorie_idCategorie`),
  KEY `fk_Question_Categorie1_idx` (`Categorie_idCategorie`)
) ENGINE=MyISAM AUTO_INCREMENT=123 DEFAULT CHARSET=utf8mb4;

ALTER TABLE `question`
	ADD CONSTRAINT `fk_Question_Categorie1`
    FOREIGN KEY (`Categorie_idCategorie`)
    REFERENCES `categorie` (`idCategorie`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- --------------------------------------------------------

--
-- Table structure for table `questionjoueur`
--

DROP TABLE IF EXISTS `questionjoueur`;
CREATE TABLE IF NOT EXISTS `questionjoueur` (
  `idQuestionJoueur` int NOT NULL AUTO_INCREMENT,
  `description` longtext,
  `lang` varchar(45) DEFAULT NULL,
  `Joueur_idJoueur` int NOT NULL,
  `Partie_idPartie` int NOT NULL,
  `Categorie_idCategorie` int NOT NULL,
  PRIMARY KEY (`idQuestionJoueur`,`Joueur_idJoueur`,`Partie_idPartie`,`Categorie_idCategorie`),
  KEY `fk_QuestionJoueur_Joueur_idx` (`Joueur_idJoueur`),
  KEY `fk_QuestionJoueur_Partie1_idx` (`Partie_idPartie`),
  KEY `fk_QuestionJoueur_Categorie1_idx` (`Categorie_idCategorie`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

ALTER TABLE `questionjoueur`
	ADD CONSTRAINT `fk_QuestionJoueur_Joueur`
    FOREIGN KEY (`Joueur_idJoueur`)
    REFERENCES `joueur` (`idJoueur`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE `questionjoueur`
	ADD CONSTRAINT `fk_QuestionJoueur_Partie1`
     FOREIGN KEY (`Partie_idPartie`)
    REFERENCES `partie` (`idPartie`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE `questionjoueur`
	ADD CONSTRAINT `fk_QuestionJoueur_Categorie1`
    FOREIGN KEY (`Categorie_idCategorie`)
    REFERENCES `categorie` (`idCategorie`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

-- --------------------------------------------------------

--
-- Table structure for table `reponses`
--

DROP TABLE IF EXISTS `reponses`;
CREATE TABLE IF NOT EXISTS `reponses` (
  `idReponses` int NOT NULL AUTO_INCREMENT,
  `description` mediumtext,
  `etat` tinyint DEFAULT '0',
  `Question_idQuestion` int NOT NULL,
  PRIMARY KEY (`idReponses`),
  KEY `fk_Reponses_Question1_idx` (`Question_idQuestion`)
) ENGINE=MyISAM AUTO_INCREMENT=486 DEFAULT CHARSET=utf8mb4;

ALTER TABLE `reponses`
	ADD CONSTRAINT `fk_Reponses_Question1`
    FOREIGN KEY (`Question_idQuestion`)
    REFERENCES `question` (`idQuestion`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

--
-- Table structure for table `reponsesjoueur`
--

DROP TABLE IF EXISTS `reponsesjoueur`;
CREATE TABLE IF NOT EXISTS `reponsesjoueur` (
  `idReponsesJoueur` int NOT NULL AUTO_INCREMENT,
  `description` longtext NOT NULL,
  `etat` tinyint NOT NULL,
  `QuestionJoueur_idQuestionJoueur` int NOT NULL,
  PRIMARY KEY (`idReponsesJoueur`),
  KEY `fk_ReponsesJoueur_QuestionJoueur1_idx` (`QuestionJoueur_idQuestionJoueur`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

ALTER TABLE `reponsesjoueur`
	ADD CONSTRAINT `fk_Reponses_Question1`
    FOREIGN KEY (`QuestionJoueur_idQuestionJoueur`)
    REFERENCES `questionjoueur` (`idQuestionJoueur`)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

COMMIT;
