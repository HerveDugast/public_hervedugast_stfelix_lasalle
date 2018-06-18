#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : s5_client_select.py      version 1.2
Date : 18-04-2018
Auteur : Hervé Dugast
Source : https://openclassrooms.com/courses/apprenez-a-programmer-en-python/le-reseau

s5_server_select.py
Création d'un serveur pouvant accepter plusieurs clients, réceptionner leurs messages et leur 
envoyer une confirmation à chaque réception.

s5_client_select.py
Client socket

------ Affichage console s5_server_select.py ------------------------------------------------------
Le serveur écoute à présent sur le port 12800
Reçu Je suis le client 1
Reçu Et moi le client 2
Reçu Client1: Coucou
Reçu Client2: Où est l'énergumène ?
Reçu fin
Fermeture des connexions
---------------------------------------------------------------------------------------------------

------ Affichage console s5_client_select.py (client 1) -------------------------------------------
H:\>python D:\prog\python\socket__initiation\s5_client_select.py
Connexion établie avec le serveur sur le port 12800
> Je suis le client 1
5 / 5
> Client1: Coucou
5 / 5
> fin
5 / 5
Fermeture de la connexion
---------------------------------------------------------------------------------------------------

------ Affichage console s5_client_select.py (client 2) -------------------------------------------
H:\>python D:\prog\python\socket__initiation\s5_client_select.py
Connexion établie avec le serveur sur le port 12800
> Et moi le client 2
5 / 5
> Client2: Où est l'énergumène ?
5 / 5
>
---------------------------------------------------------------------------------------------------
"""
import socket

hote = "localhost"
port = 12800

connexion_avec_serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_avec_serveur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

msg_a_envoyer = ""
while msg_a_envoyer != "fin":
   msg_a_envoyer = input("> ")
   # Peut planter si vous tapez des caractères spéciaux
   connexion_avec_serveur.send(msg_a_envoyer.encode('utf_8'))
   msg_recu = connexion_avec_serveur.recv(1024)
   print(msg_recu.decode('utf_8')) # Là encore, peut planter s'il y a des accents

print("Fermeture de la connexion")
connexion_avec_serveur.close()