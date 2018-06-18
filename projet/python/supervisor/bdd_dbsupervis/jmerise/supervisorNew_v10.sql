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
        local_id            Int ,
        type_capteur_id     Int ,
        emplacement_id      Int ,
        systeme_embarque_id Int ,
        etat_capteur_id     Int ,
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
        capteur_id Int ,
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
        capteur_id   Int ,
        evenement_id Int ,
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

ALTER TABLE capteur ADD CONSTRAINT FK_capteur_local_id FOREIGN KEY (local_id) REFERENCES local(id);
ALTER TABLE capteur ADD CONSTRAINT FK_capteur_type_capteur_id FOREIGN KEY (type_capteur_id) REFERENCES type_capteur(id);
ALTER TABLE capteur ADD CONSTRAINT FK_capteur_emplacement_id FOREIGN KEY (emplacement_id) REFERENCES emplacement(id);
ALTER TABLE capteur ADD CONSTRAINT FK_capteur_systeme_embarque_id FOREIGN KEY (systeme_embarque_id) REFERENCES systeme_embarque(id);
ALTER TABLE capteur ADD CONSTRAINT FK_capteur_etat_capteur_id FOREIGN KEY (etat_capteur_id) REFERENCES etat_capteur(id);
ALTER TABLE releve_capteur ADD CONSTRAINT FK_releve_capteur_capteur_id FOREIGN KEY (capteur_id) REFERENCES capteur(id);
ALTER TABLE journalisation ADD CONSTRAINT FK_journalisation_capteur_id FOREIGN KEY (capteur_id) REFERENCES capteur(id);
ALTER TABLE journalisation ADD CONSTRAINT FK_journalisation_evenement_id FOREIGN KEY (evenement_id) REFERENCES evenement(id);
