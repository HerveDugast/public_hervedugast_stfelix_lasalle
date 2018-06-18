-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Client :  127.0.0.1
-- Généré le :  Lun 09 Avril 2018 à 14:50
-- Version du serveur :  5.7.14
-- Version de PHP :  5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  dbsav
--
DROP DATABASE dbsav;
CREATE DATABASE IF NOT EXISTS dbsav DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE dbsav;

-- --------------------------------------------------------

--
-- Structure de la table `action`
--

DROP TABLE IF EXISTS action;
CREATE TABLE `action` (
  id int(11) NOT NULL,
  code varchar(1) NOT NULL,
  nom varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `action`
--

INSERT INTO `action` (id, `code`, nom) VALUES
(1, 'R', 'Réparation'),
(2, 'E', 'Echange'),
(3, 'D', 'Devis');

-- --------------------------------------------------------

--
-- Structure de la table journal
--

DROP TABLE IF EXISTS journal;
CREATE TABLE journal (
  id int(11) NOT NULL,
  date_heure datetime NOT NULL,
  id_action int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Index pour les tables exportées
--

--
-- Index pour la table `action`
--
ALTER TABLE `action`
  ADD PRIMARY KEY (id),
  ADD UNIQUE KEY code (code),
  ADD UNIQUE KEY nom (nom);

--
-- Index pour la table journal
--
ALTER TABLE journal
  ADD PRIMARY KEY (id),
  ADD KEY FK_journal_id_action (id_action);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `action`
--
ALTER TABLE `action`
  MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;
--
-- AUTO_INCREMENT pour la table journal
--
ALTER TABLE journal
  MODIFY id int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table journal
--
ALTER TABLE journal
  ADD CONSTRAINT FK_journal_id_action FOREIGN KEY (id_action) REFERENCES action (id);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
