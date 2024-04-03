-- -----------------------------------
--  tables de relation n à n
-- ----------------------------------
DROP TABLE IF EXISTS `partie-has-question` cascade;
DROP TABLE IF EXISTS `Permission_has_Role` cascade;
-- -----------------------------------
-- -----------------------------------
-- tables de relation n à 1 aka avec un clé etrangère
-- ----------------------------------
DROP TABLE IF EXISTS `reponsesjoueur` cascade;
DROP TABLE IF EXISTS `questionjoueur` cascade;
DROP TABLE IF EXISTS `reponses` cascade;
DROP TABLE IF EXISTS `gamearchive`cascade;
DROP TABLE IF EXISTS `pion` cascade;
DROP TABLE IF EXISTS `question` cascade;
-- -----------------------------------
-- -----------------------------------
-- indépendante tables
-- ----------------------------------
DROP TABLE IF EXISTS `partie` cascade;
DROP TABLE IF EXISTS `joueur` cascade;
DROP TABLE IF EXISTS `categorie` cascade;
DROP TABLE IF EXISTS `Role` cascade;
DROP TABLE IF EXISTS `Permission` cascade;
-- ----------------------------------
