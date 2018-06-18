-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Client: localhost
-- Généré le: Mar 02 Mai 2017 à 16:57
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
  commentaire varchar(45) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY nom (nom)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Structure de la table 'evenement'
--

DROP TABLE IF EXISTS evenement;
CREATE TABLE IF NOT EXISTS evenement (
  id int(11) NOT NULL AUTO_INCREMENT,
  `code` int(11) DEFAULT NULL,
  nom varchar(45) DEFAULT NULL,
  commentaire varchar(200) DEFAULT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY `code` (`code`,nom)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Structure de la table 'journalisation'
--

DROP TABLE IF EXISTS journalisation;
CREATE TABLE IF NOT EXISTS journalisation (
  id int(11) NOT NULL AUTO_INCREMENT,
  date_heure date DEFAULT NULL,
  capteur_id int(11) DEFAULT NULL,
  evenement_id int(11) DEFAULT NULL,
  PRIMARY KEY (id),
  KEY FK_journalisation_capteur_id (capteur_id),
  KEY FK_journalisation_evenement_id (evenement_id)
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table capteur
--
ALTER TABLE capteur
  ADD CONSTRAINT FK_capteur_etat_capteur_id FOREIGN KEY (etat_capteur_id) REFERENCES etat_capteur (id),
  ADD CONSTRAINT FK_capteur_emplacement_id FOREIGN KEY (emplacement_id) REFERENCES emplacement (id),
  ADD CONSTRAINT FK_capteur_local_id FOREIGN KEY (local_id) REFERENCES local (id),
  ADD CONSTRAINT FK_capteur_systeme_embarque_id FOREIGN KEY (systeme_embarque_id) REFERENCES systeme_embarque (id),
  ADD CONSTRAINT FK_capteur_type_capteur_id FOREIGN KEY (type_capteur_id) REFERENCES type_capteur (id);

--
-- Contraintes pour la table journalisation
--
ALTER TABLE journalisation
  ADD CONSTRAINT FK_journalisation_evenement_id FOREIGN KEY (evenement_id) REFERENCES evenement (id),
  ADD CONSTRAINT FK_journalisation_capteur_id FOREIGN KEY (capteur_id) REFERENCES capteur (id);

--
-- Contraintes pour la table releve_capteur
--
ALTER TABLE releve_capteur
  ADD CONSTRAINT FK_releve_capteur_capteur_id FOREIGN KEY (capteur_id) REFERENCES capteur (id);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
