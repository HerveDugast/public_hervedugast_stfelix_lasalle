-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Client: localhost
-- Généré le: Dim 25 Juin 2017 à 23:41
-- Version du serveur: 5.5.44-0ubuntu0.14.04.1-log
-- Version de PHP: 5.5.9-1ubuntu4.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données: 'dbsupervis'
--
CREATE DATABASE IF NOT EXISTS dbsupervis DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE dbsupervis;

-- --------------------------------------------------------

--
-- Structure de la table 'capteur'
--
-- Création: Mar 13 Juin 2017 à 16:55
--

DROP TABLE IF EXISTS capteur;
CREATE TABLE IF NOT EXISTS capteur (
  id int(11) NOT NULL AUTO_INCREMENT,
  nom varchar(45) DEFAULT NULL,
  freq_releve_sec int(11) DEFAULT NULL,
  local_id int(11) DEFAULT NULL,
  type_capteur_id int(11) DEFAULT NULL,
  emplacement_id int(11) DEFAULT NULL,
  systeme_embarque_id int(11) DEFAULT NULL,
  etat_capteur_id int(11) DEFAULT NULL,
  commentaire varchar(200) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY nom (nom),
  KEY FK_capteur_local_id (local_id),
  KEY FK_capteur_type_capteur_id (type_capteur_id),
  KEY FK_capteur_emplacement_id (emplacement_id),
  KEY FK_capteur_systeme_embarque_id (systeme_embarque_id),
  KEY FK_capteur_etat_capteur_id (etat_capteur_id)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Contenu de la table 'capteur'
--

INSERT INTO capteur (id, nom, freq_releve_sec, local_id, type_capteur_id, emplacement_id, systeme_embarque_id, etat_capteur_id, commentaire) VALUES
(1, 'Temperat_in_518', 900, 1, 1, NULL, 1, 1, 'Capteur température intérieure grove BMP280 situé en J518, freq_releve_sec = 900 (15 mn)'),
(2, 'Pression_518', 3600, 1, 3, NULL, 1, 1, 'Capteur pression atmosphérique grove BMP280 situé en J518, freq_releve_seq = 3600 (1h)'),
(3, 'ContactA_518', NULL, 1, 4, 3, 1, 1, 'Capteur contact porte 1 (A) situé en J518. Porte principale'),
(4, 'RaspA518', NULL, 1, 1, 3, 1, 1, 'Ce n''est pas un capteur mais permet de journaliser les mises sous tension de la carte raspberry');

-- --------------------------------------------------------

--
-- Structure de la table 'emplacement'
--
-- Création: Lun 12 Juin 2017 à 21:58
--

DROP TABLE IF EXISTS emplacement;
CREATE TABLE IF NOT EXISTS emplacement (
  id int(11) NOT NULL AUTO_INCREMENT,
  nom varchar(45) DEFAULT NULL,
  commentaire varchar(200) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY nom (nom)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=8 ;

--
-- Contenu de la table 'emplacement'
--

INSERT INTO emplacement (id, nom, commentaire) VALUES
(3, 'Porte 1', 'Porte entrée local'),
(4, 'Porte 2', 'Porte suivante en tournant dans le sens des aiguilles d''une montre'),
(7, 'Porte 3', 'Porte suivante à partir de la porte 2, en tournant dans le sens des aiguilles d''une montre');

-- --------------------------------------------------------

--
-- Structure de la table 'etat_capteur'
--
-- Création: Mar 02 Mai 2017 à 14:54
--

DROP TABLE IF EXISTS etat_capteur;
CREATE TABLE IF NOT EXISTS etat_capteur (
  id int(11) NOT NULL AUTO_INCREMENT,
  nom varchar(45) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY nom (nom)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

--
-- Contenu de la table 'etat_capteur'
--

INSERT INTO etat_capteur (id, nom) VALUES
(3, 'Désactivé'),
(1, 'En fonctionnement'),
(2, 'Hors service');

-- --------------------------------------------------------

--
-- Structure de la table 'journalisation'
--
-- Création: Mar 13 Juin 2017 à 22:55
--

DROP TABLE IF EXISTS journalisation;
CREATE TABLE IF NOT EXISTS journalisation (
  id int(11) NOT NULL AUTO_INCREMENT,
  date_heure datetime DEFAULT NULL,
  niveau_id int(11) NOT NULL,
  capteur_id int(11) DEFAULT NULL,
  message varchar(200) DEFAULT NULL,
  commentaire varchar(200) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY FK_journalisation_capteur_id (capteur_id),
  KEY fk_journalisation_niveau1_idx (niveau_id)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Contenu de la table 'journalisation'
--

INSERT INTO journalisation (id, date_heure, niveau_id, capteur_id, message, commentaire) VALUES
(1, '2017-06-25 23:40:08', 3, 4, 'Mise sous tension du système supervisor', NULL);

-- --------------------------------------------------------

--
-- Structure de la table 'local'
--
-- Création: Mar 02 Mai 2017 à 14:54
--

DROP TABLE IF EXISTS local;
CREATE TABLE IF NOT EXISTS `local` (
  id int(11) NOT NULL AUTO_INCREMENT,
  nom varchar(25) DEFAULT NULL,
  commentaire char(200) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY nom (nom)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Contenu de la table 'local'
--

INSERT INTO local (id, nom, commentaire) VALUES
(1, 'J518', NULL),
(2, 'J519', NULL);

-- --------------------------------------------------------

--
-- Structure de la table 'niveau'
--
-- Création: Lun 12 Juin 2017 à 22:07
--

DROP TABLE IF EXISTS niveau;
CREATE TABLE IF NOT EXISTS niveau (
  id int(11) NOT NULL AUTO_INCREMENT,
  `code` int(11) NOT NULL,
  niveau_alerte varchar(45) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY niveau_alerte_UNIQUE (niveau_alerte),
  UNIQUE KEY code_UNIQUE (`code`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Contenu de la table 'niveau'
--

INSERT INTO niveau (id, code, niveau_alerte) VALUES
(1, 1, 'Critical'),
(2, 2, 'Error'),
(3, 3, 'Warning'),
(4, 4, 'Info'),
(5, 5, 'Debug');

-- --------------------------------------------------------

--
-- Structure de la table 'releve_capteur'
--
-- Création: Mar 13 Juin 2017 à 19:31
--

DROP TABLE IF EXISTS releve_capteur;
CREATE TABLE IF NOT EXISTS releve_capteur (
  id int(11) NOT NULL AUTO_INCREMENT,
  date_heure datetime DEFAULT NULL,
  valeur int(11) DEFAULT NULL,
  capteur_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY FK_releve_capteur_capteur_id (capteur_id)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- Contenu de la table 'releve_capteur'
--

INSERT INTO releve_capteur (id, date_heure, valeur, capteur_id) VALUES
(1, '2017-06-25 23:40:10', 274, 1),
(2, '2017-06-25 23:40:11', 1013, 2),
(3, '2017-06-25 23:40:12', 0, 3),
(4, '2017-06-25 23:40:17', 1, 3),
(5, '2017-06-25 23:40:19', 0, 3);

-- --------------------------------------------------------

--
-- Structure de la table 'systeme_embarque'
--
-- Création: Mar 02 Mai 2017 à 14:54
--

DROP TABLE IF EXISTS systeme_embarque;
CREATE TABLE IF NOT EXISTS systeme_embarque (
  id int(11) NOT NULL AUTO_INCREMENT,
  nom varchar(45) DEFAULT NULL,
  commentaire varchar(200) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY nom (nom)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=2 ;

--
-- Contenu de la table 'systeme_embarque'
--

INSERT INTO systeme_embarque (id, nom, commentaire) VALUES
(1, 'raspi3-J518', NULL);

-- --------------------------------------------------------

--
-- Structure de la table 'type_capteur'
--
-- Création: Mar 02 Mai 2017 à 14:54
--

DROP TABLE IF EXISTS type_capteur;
CREATE TABLE IF NOT EXISTS type_capteur (
  id int(11) NOT NULL AUTO_INCREMENT,
  designation varchar(45) DEFAULT NULL,
  grandeur varchar(45) DEFAULT NULL,
  reference char(45) DEFAULT NULL,
  unite varchar(45) DEFAULT NULL,
  multiplicateur int(11) DEFAULT NULL,
  commentaire varchar(200) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY designation (designation)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- Contenu de la table 'type_capteur'
--

INSERT INTO type_capteur (id, designation, grandeur, reference, unite, multiplicateur, commentaire) VALUES
(1, 'bmp280_temperature', 'Température', 'Grove - Barometer sensor (BMP280)', 'degC', 10, 'Capteur de température et de pression atmosphérique, interface i2c, multiplicateur par 10 pour avoir des entiers (247 : 24,7 degC)'),
(3, 'bmp280_pression', 'Pression atmosphérique', 'Grove - Barometer sensor (BMP280)', 'mbar', 1, 'Capteur de température et de pression atmosphérique, interface i2c'),
(4, 'Détecteur ouverture porte', '0', 'Lextronic - ILS-SNM03', '0', 0, 'Détecteur d''ouverture "standard"');

--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table capteur
--
ALTER TABLE capteur
  ADD CONSTRAINT FK_capteur_emplacement_id FOREIGN KEY (emplacement_id) REFERENCES emplacement (id),
  ADD CONSTRAINT FK_capteur_etat_capteur_id FOREIGN KEY (etat_capteur_id) REFERENCES etat_capteur (id),
  ADD CONSTRAINT FK_capteur_local_id FOREIGN KEY (local_id) REFERENCES local (id),
  ADD CONSTRAINT FK_capteur_systeme_embarque_id FOREIGN KEY (systeme_embarque_id) REFERENCES systeme_embarque (id),
  ADD CONSTRAINT FK_capteur_type_capteur_id FOREIGN KEY (type_capteur_id) REFERENCES type_capteur (id);

--
-- Contraintes pour la table journalisation
--
ALTER TABLE journalisation
  ADD CONSTRAINT FK_journalisation_capteur_id FOREIGN KEY (capteur_id) REFERENCES capteur (id),
  ADD CONSTRAINT fk_journalisation_niveau1 FOREIGN KEY (niveau_id) REFERENCES niveau (id) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Contraintes pour la table releve_capteur
--
ALTER TABLE releve_capteur
  ADD CONSTRAINT FK_releve_capteur_capteur_id FOREIGN KEY (capteur_id) REFERENCES capteur (id);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
