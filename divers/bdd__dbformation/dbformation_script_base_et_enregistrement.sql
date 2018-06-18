-- phpMyAdmin SQL Dump
-- version 4.0.10.6
-- http://www.phpmyadmin.net
--
-- Host: mysql1.paris1.alwaysdata.com
-- Generation Time: Dec 10, 2016 at 11:55 PM
-- Server version: 10.1.13-MariaDB
-- PHP Version: 5.6.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: 'etubtssn44_dbformation'
--

-- --------------------------------------------------------

--
-- Table structure for table 'diplome'
--

CREATE TABLE IF NOT EXISTS diplome (
  numeroEtudiant int(11) NOT NULL,
  numeroModule int(11) NOT NULL,
  PRIMARY KEY (numeroEtudiant,numeroModule),
  KEY FK_a_obtenu_numeroModule (numeroModule)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table 'diplome'
--

INSERT INTO diplome (numeroEtudiant, numeroModule) VALUES
(12, 30),
(23, 10),
(34, 40),
(78, 40),
(89, 30),
(123, 30),
(123, 40);

-- --------------------------------------------------------

--
-- Table structure for table 'enseignant'
--

CREATE TABLE IF NOT EXISTS enseignant (
  numeroEnseignant int(11) NOT NULL,
  nom varchar(25) DEFAULT NULL,
  grade varchar(25) DEFAULT NULL,
  salaire int(11) DEFAULT NULL,
  PRIMARY KEY (numeroEnseignant)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table 'enseignant'
--

INSERT INTO enseignant (numeroEnseignant, nom, grade, salaire) VALUES
(12, 'Dupont', 'Assistant', 700),
(45, 'Simon', 'Assistant', 1000),
(56, 'Didier', 'Professeur', 980),
(67, 'Gray', 'Professeur', 1020),
(90, 'Collot', 'Professeur', 1200);

-- --------------------------------------------------------

--
-- Table structure for table 'etudiant'
--

CREATE TABLE IF NOT EXISTS etudiant (
  numeroEtudiant int(11) NOT NULL,
  nom varchar(25) DEFAULT NULL,
  adresse varchar(25) DEFAULT NULL,
  PRIMARY KEY (numeroEtudiant)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table 'etudiant'
--

INSERT INTO etudiant (numeroEtudiant, nom, adresse) VALUES
(12, 'Dupont', 'Lyon'),
(23, 'Durand', 'Lyon'),
(34, 'Martin', 'Saint-Étienne'),
(78, 'Paul', '⊥'),
(89, 'Simpson', 'Villeurbanne'),
(123, 'Durand', 'Villeurbanne');

-- --------------------------------------------------------

--
-- Table structure for table 'tbmodule'
--

CREATE TABLE IF NOT EXISTS tbmodule (
  numeroModule int(11) NOT NULL,
  titre varchar(25) DEFAULT NULL,
  numeroEnseignant int(11) DEFAULT NULL,
  PRIMARY KEY (numeroModule),
  KEY FK_Module_numeroEnseignant (numeroEnseignant)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table 'tbmodule'
--

INSERT INTO tbmodule (numeroModule, titre, numeroEnseignant) VALUES
(10, 'Mathématiques', 56),
(20, 'Physique', 56),
(30, 'Français', 12),
(40, 'Anglais', 67);

--
-- Constraints for dumped tables
--

--
-- Constraints for table diplome
--
ALTER TABLE diplome
  ADD CONSTRAINT FK_a_obtenu_numeroEtudiant FOREIGN KEY (numeroEtudiant) REFERENCES etudiant (numeroEtudiant),
  ADD CONSTRAINT FK_a_obtenu_numeroModule FOREIGN KEY (numeroModule) REFERENCES tbmodule (numeroModule);

--
-- Constraints for table tbmodule
--
ALTER TABLE tbmodule
  ADD CONSTRAINT FK_Module_numeroEnseignant FOREIGN KEY (numeroEnseignant) REFERENCES enseignant (numeroEnseignant);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
