#------------------------------------------------------------
#        Script MySQL.
#------------------------------------------------------------


#------------------------------------------------------------
# Table: type_capteur
#------------------------------------------------------------

CREATE TABLE type_capteur(
        id             int (11) Auto_increment  NOT NULL ,
        designation    Varchar (45) ,
        grandeur       Varchar (45) ,
        reference      Char (45) ,
        unite          Varchar (45) ,
        multiplicateur Int ,
        commentaire    Varchar (200) ,
        PRIMARY KEY (id ) ,
        UNIQUE (designation )
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: local
#------------------------------------------------------------

CREATE TABLE local(
        id          int (11) Auto_increment  NOT NULL ,
        nom         Varchar (25) ,
        commentaire Char (200) ,
        PRIMARY KEY (id ) ,
        UNIQUE (nom )
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: capteur
#------------------------------------------------------------

CREATE TABLE capteur(
        id                  int (11) Auto_increment  NOT NULL ,
        nom                 Varchar (45) ,
        freq_releve_sec     Int ,
        id_local            Int ,
        id_type_capteur     Int ,
        id_emplacement      Int ,
        id_systeme_embarque Int ,
        id_etat_capteur     Int ,
        PRIMARY KEY (id ) ,
        UNIQUE (nom )
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: emplacement
#------------------------------------------------------------

CREATE TABLE emplacement(
        id          int (11) Auto_increment  NOT NULL ,
        nom         Varchar (45) ,
        commentaire Varchar (45) ,
        PRIMARY KEY (id ) ,
        UNIQUE (nom )
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: systeme_embarque
#------------------------------------------------------------

CREATE TABLE systeme_embarque(
        id          int (11) Auto_increment  NOT NULL ,
        nom         Varchar (45) ,
        commentaire Varchar (200) ,
        PRIMARY KEY (id ) ,
        UNIQUE (nom )
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: releve_capteur
#------------------------------------------------------------

CREATE TABLE releve_capteur(
        id         int (11) Auto_increment  NOT NULL ,
        date_heure Date ,
        valeur     Int ,
        id_capteur Int ,
        PRIMARY KEY (id )
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: etat_capteur
#------------------------------------------------------------

CREATE TABLE etat_capteur(
        id  int (11) Auto_increment  NOT NULL ,
        nom Varchar (45) ,
        PRIMARY KEY (id ) ,
        UNIQUE (nom )
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: journalisation
#------------------------------------------------------------

CREATE TABLE journalisation(
        id           int (11) Auto_increment  NOT NULL ,
        date_heure   Date ,
        id_capteur   Int ,
        id_evenement Int ,
        PRIMARY KEY (id )
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: evenement
#------------------------------------------------------------

CREATE TABLE evenement(
        id          int (11) Auto_increment  NOT NULL ,
        code        Int ,
        nom         Varchar (45) ,
        commentaire Varchar (200) ,
        PRIMARY KEY (id ) ,
        UNIQUE (code ,nom )
)ENGINE=InnoDB;

ALTER TABLE capteur ADD CONSTRAINT FK_capteur_id_local FOREIGN KEY (id_local) REFERENCES local(id);
ALTER TABLE capteur ADD CONSTRAINT FK_capteur_id_type_capteur FOREIGN KEY (id_type_capteur) REFERENCES type_capteur(id);
ALTER TABLE capteur ADD CONSTRAINT FK_capteur_id_emplacement FOREIGN KEY (id_emplacement) REFERENCES emplacement(id);
ALTER TABLE capteur ADD CONSTRAINT FK_capteur_id_systeme_embarque FOREIGN KEY (id_systeme_embarque) REFERENCES systeme_embarque(id);
ALTER TABLE capteur ADD CONSTRAINT FK_capteur_id_etat_capteur FOREIGN KEY (id_etat_capteur) REFERENCES etat_capteur(id);
ALTER TABLE releve_capteur ADD CONSTRAINT FK_releve_capteur_id_capteur FOREIGN KEY (id_capteur) REFERENCES capteur(id);
ALTER TABLE journalisation ADD CONSTRAINT FK_journalisation_id_capteur FOREIGN KEY (id_capteur) REFERENCES capteur(id);
ALTER TABLE journalisation ADD CONSTRAINT FK_journalisation_id_evenement FOREIGN KEY (id_evenement) REFERENCES evenement(id);
