#------------------------------------------------------------
#        Script MySQL.
#------------------------------------------------------------


#------------------------------------------------------------
# Table: journal
#------------------------------------------------------------

CREATE TABLE journal(
        id         int (11) Auto_increment  NOT NULL ,
        date_heure Datetime NOT NULL ,
        id_action  Int ,
        PRIMARY KEY (id )
)ENGINE=InnoDB;


#------------------------------------------------------------
# Table: action
#------------------------------------------------------------

CREATE TABLE action(
        id   int (11) Auto_increment  NOT NULL ,
        code Varchar (1) ,
        nom  Varchar (25) ,
        PRIMARY KEY (id ) ,
        UNIQUE (code ,nom )
)ENGINE=InnoDB;

ALTER TABLE journal ADD CONSTRAINT FK_journal_id_action FOREIGN KEY (id_action) REFERENCES action(id);
