-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Client: localhost
-- Généré le: Mar 13 Juin 2017 à 00:15
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
  PRIMARY KEY (id),
  UNIQUE KEY nom (nom),
  KEY FK_capteur_local_id (local_id),
  KEY FK_capteur_type_capteur_id (type_capteur_id),
  KEY FK_capteur_emplacement_id (emplacement_id),
  KEY FK_capteur_systeme_embarque_id (systeme_embarque_id),
  KEY FK_capteur_etat_capteur_id (etat_capteur_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Structure de la table 'emplacement'
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

DROP TABLE IF EXISTS journalisation;
CREATE TABLE IF NOT EXISTS journalisation (
  id int(11) NOT NULL AUTO_INCREMENT,
  date_heure date DEFAULT NULL,
  niveau_id int(11) NOT NULL,
  capteur_id int(11) DEFAULT NULL,
  nom_court varchar(45) DEFAULT NULL,
  message varchar(250) DEFAULT NULL,
  commentaire varchar(200) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY FK_journalisation_capteur_id (capteur_id),
  KEY fk_journalisation_niveau1_idx (niveau_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Structure de la table 'local'
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

DROP TABLE IF EXISTS releve_capteur;
CREATE TABLE IF NOT EXISTS releve_capteur (
  id int(11) NOT NULL AUTO_INCREMENT,
  date_heure date DEFAULT NULL,
  valeur int(11) DEFAULT NULL,
  capteur_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY FK_releve_capteur_capteur_id (capteur_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Structure de la table 'systeme_embarque'
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
  ADD CONSTRAINT fk_journalisation_niveau1 FOREIGN KEY (niveau_id) REFERENCES niveau (id) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT FK_journalisation_capteur_id FOREIGN KEY (capteur_id) REFERENCES capteur (id);

--
-- Contraintes pour la table releve_capteur
--
ALTER TABLE releve_capteur
  ADD CONSTRAINT FK_releve_capteur_capteur_id FOREIGN KEY (capteur_id) REFERENCES capteur (id);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
