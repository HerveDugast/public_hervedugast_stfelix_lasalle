#!/usr/bin/python3.4
# coding: utf-8
"""
Programme classe : essai_LoggerConsoleFichierRot.py     version : 1.0
Auteur : H. Dugast
Date : 04-04-2018
Source : https://deusyss.developpez.com/tutoriels/Python/Logger/
Auteur source : GALODE Alexandre

Fonctionnement :
  Programme d'essai de la classe LoggerConsoleFichierRot.
  Dans le code ci-dessous
  - trace l'activité au niveau demandé dans la console
  - trace l'activité au niveau demandé (peut-être différent de celui choisi pour la console) 
    dans un fichier rotatif
    
------------------ Affichage console ---------------------------------------------------------------
2018-04-08 21:37:01,320 -- essai -- CRITICAL -- msg critical 1
2018-04-08 21:37:01,321 -- essai -- ERROR -- msg error 1

----- Affichage contenu fichier essai.log -----
2018-04-08 21:37:01,319 -- essai -- WARNING -- msg warning 10
2018-04-08 21:37:01,320 -- essai -- CRITICAL -- msg critical 1
2018-04-08 21:37:01,321 -- essai -- ERROR -- msg error 1
2018-04-08 21:37:01,322 -- essai -- WARNING -- msg warning 1
2018-04-08 21:37:01,322 -- essai -- INFO -- msg info 1
2018-04-08 21:37:01,323 -- essai -- DEBUG -- msg debug 1

----- Fichier essai.log : affichage informations parsées dans une variable -----
['2018-04-08 21:37:01,319 ', 'essai ', 'WARNING ', 'msg warning 10\n']
['2018-04-08 21:37:01,320 ', 'essai ', 'CRITICAL ', 'msg critical 1\n']
['2018-04-08 21:37:01,321 ', 'essai ', 'ERROR ', 'msg error 1\n']
['2018-04-08 21:37:01,322 ', 'essai ', 'WARNING ', 'msg warning 1\n']
['2018-04-08 21:37:01,322 ', 'essai ', 'INFO ', 'msg info 1\n']
['2018-04-08 21:37:01,323 ', 'essai ', 'DEBUG ', 'msg debug 1\n']
----- Fichier essai.log : affichage informations parsées par type -----
<time>2018-04-08 21:37:01,319  <logger>essai  <level>WARNING  <message>msg warning 10
<time>2018-04-08 21:37:01,320  <logger>essai  <level>CRITICAL  <message>msg critical 1
<time>2018-04-08 21:37:01,321  <logger>essai  <level>ERROR  <message>msg error 1
<time>2018-04-08 21:37:01,322  <logger>essai  <level>WARNING  <message>msg warning 1
<time>2018-04-08 21:37:01,322  <logger>essai  <level>INFO  <message>msg info 1
<time>2018-04-08 21:37:01,323  <logger>essai  <level>DEBUG  <message>msg debug 1
2018-04-08 21:37:01,325 -- essai -- DEBUG -- ESSAI 2 debug
----------------------------------------------------------------------------------------------------

Compléments d'informations :
   - logger : objet mémoire tampon filtrant un niveau de criticité. Le logger envoie à ses handlers
              uniquement les messages de niveau supérieur ou égal à son niveau de criticité.
              ordre hiérarchique : CRITICAL > ERROR > WARNING > INFO > DEBUG
   - niveau de criticité : importance des messages 
      Voici les niveaux de criticité classés du plus important au moins important :
         - CRITICAL (C) : plantage application...
         - ERROR (E) : erreur sévère sans plantage...
         - WARNING (W) : événement important pouvant entrainer un dysfonctionnement...
         - INFO (I) : information, événement normal venant de se passer...
         - DEBUG (G) : débogage, valeur de variables...
   - handler : gestionnaire qui redirige le message vers un endroit désigné par le type de handler
     Types de handlers existant :
        - console : StreamHandler
        - fichier : FileHandler, WatchedFileHandler, RotatingFileHandler, TimeRotatingFileHandler
        - mail : SmtpHandler
        - réseau : SocketHandler
        - web : HTTPHandler
        ...
   - formatter : permet de mettre en forme le message
     Attributs de format existant :
       %(asctime)s : Date au format  AAAA-MM-JJ HH:MM:SS,xxx 
       %(filename)s : Nom du fichier ayant écrit dans le log
       %(funcName)s : Nom de la fonction contenant l'appel à l'écriture dans le log
       %(levelname)s : Niveau du message
       %(module)s : Nom du module ayant appelé l'écriture dans le log
       %(message)s : Le message à logger
       %(name)s : Nom donné au logger avec méthode getLogger
       %(thread)d : L'ID du thread courant
       %(threadName)s : Le nom du thread courant
       ...
"""
# classe gérant les loggers et les handlers
from LoggerConsoleFichier import LoggerConsoleFichier

nomFichier = "essai.log"
logger = LoggerConsoleFichier(loggerName="essai", loggerLevel="DEBUG", \
                              fileName=nomFichier, fileLevel="DEBUG", consoleLevel="ERROR")
logger.envoyerMessageTestNiveau(niveauMsg="WARNING", num=10)
logger.envoyerMessageTestTousNiveaux(num=1)
#logger.envoyerMessageBoucle(niveauMsg="TOUS", nbMsg=2, timeSleep=0.5)
print("")
logger.afficherContenuFichier(fileName=nomFichier)
logger.afficherDonneesFichier(fileName=nomFichier)
logger.afficherDataFichierInfoLog(fileName=nomFichier)
logger.debug("ESSAI 1 debug")      
logger.set_consoleLevel("DEBUG")
logger.debug("ESSAI 2 debug")      
