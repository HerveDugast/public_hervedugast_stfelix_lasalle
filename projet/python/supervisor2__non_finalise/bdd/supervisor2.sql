#------------------------------------------------------------
#        Script MySQL.
#------------------------------------------------------------


#------------------------------------------------------------
# Table: emplacement
#------------------------------------------------------------

CREATE TABLE emplacement(
        id  Int  Auto_increment  NOT NULL ,
        nom Varchar (50) NOT NULL COMMENT "Salle_C205" 
	,CONSTRAINT PK_emplacement PRIMARY KEY (id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: grandeur
#------------------------------------------------------------

CREATE TABLE grandeur(
        id             Int  Auto_increment  NOT NULL ,
        nom            Varchar (50) NOT NULL COMMENT "Température intérieure"  ,
        unite          Varchar (5) NOT NULL ,
        coeff_multipli Int NOT NULL COMMENT "Valeur dans l'unité a été multiplié par le coeff (exemple, coeff = 10 et valeur = 237 correspond à 23,7 °C)"  ,
        commentaire    Varchar (250)
	,CONSTRAINT PK_grandeur PRIMARY KEY (id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: releve
#------------------------------------------------------------

CREATE TABLE releve(
        id             Int  Auto_increment  NOT NULL ,
        date_heure     Datetime NOT NULL ,
        valeur         Int NOT NULL ,
        id_emplacement Int NOT NULL ,
        id_grandeur    Int NOT NULL
	,CONSTRAINT PK_releve PRIMARY KEY (id)

	,CONSTRAINT FK_releve_emplacement FOREIGN KEY (id_emplacement) REFERENCES emplacement(id)
	,CONSTRAINT FK_releve_grandeur0 FOREIGN KEY (id_grandeur) REFERENCES grandeur(id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: etat_capteur
#------------------------------------------------------------

CREATE TABLE etat_capteur(
        id          Int  Auto_increment  NOT NULL ,
        message     Varchar (50) NOT NULL COMMENT "OK , Inactif , Hors service"  ,
        commentaire Varchar (250)
	,CONSTRAINT PK_etat_capteur PRIMARY KEY (id)
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: journal
#------------------------------------------------------------

CREATE TABLE journal(
        id              Int  Auto_increment  NOT NULL ,
        date_heure      Datetime NOT NULL ,
        id_emplacement  Int NOT NULL ,
        id_etat_capteur Int NOT NULL
	,CONSTRAINT PK_journal PRIMARY KEY (id)

	,CONSTRAINT FK_journal_emplacement FOREIGN KEY (id_emplacement) REFERENCES emplacement(id)
	,CONSTRAINT FK_journal_etat_capteur0 FOREIGN KEY (id_etat_capteur) REFERENCES etat_capteur(id)
)ENGINE=InnoDB;

