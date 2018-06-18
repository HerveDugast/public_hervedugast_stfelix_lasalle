#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : s5_server_select.py      version 1.2
Date : 18-04-2018
Auteur : Hervé Dugast
Source : https://openclassrooms.com/courses/apprenez-a-programmer-en-python/le-reseau

s5_server_select.py
Création d'un serveur pouvant accepter plusieurs clients, réceptionner leurs messages et leur 
envoyer une confirmation à chaque réception.

s5_client_select.py
Client socket

------ Affichage console s5_server_select.py ------------------------------------------------------
C:\>python D:\prog\python\socket__initiation\s5_server_select.py
Le serveur écoute à présent sur le port 12800
Message reçu : Je suis le client futé n°1
Message reçu : Et moi je suis le client bête n°2
Message reçu : fin
Fermeture des connexions
---------------------------------------------------------------------------------------------------

------ Affichage console s5_client_select.py (client 1) -------------------------------------------
C:\>python D:\prog\python\socket__initiation\s5_client_select.py
Connexion établie avec le serveur sur le port 12800
> Je suis le client futé n°1
5/5
>
---------------------------------------------------------------------------------------------------

------ Affichage console s5_client_select.py (client 2) -------------------------------------------
C:\>python D:\prog\python\socket__initiation\s5_client_select.py
Connexion établie avec le serveur sur le port 12800
> Et moi je suis le client bête n°2
5/5
> fin
5/5
Fermeture de la connexion
---------------------------------------------------------------------------------------------------
"""
import socket
import select

hote = ''
port = 12800

connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexion_principale.bind((hote, port))
connexion_principale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

serveur_lance = True
clients_connectes = []
while serveur_lance:
   # On va vérifier que de nouveaux clients ne demandent pas à se connecter
   # Pour cela, on écoute la connexion_principale en lecture. On attend maximum 50ms
   connexions_demandees, wlist, xlist = select.select([connexion_principale], [], [], 0.05)

   for connexion in connexions_demandees:
      connexion_avec_client, infos_connexion = connexion.accept()
      # On ajoute le socket connecté à la liste des clients
      clients_connectes.append(connexion_avec_client)

   # Maintenant, on écoute la liste des clients connectés. Les clients renvoyés par select sont 
   # ceux devant être lus (recv). On attend là encore 50ms maximum
   # On enferme l'appel à select.select dans un bloc try
   # En effet, si la liste de clients connectés est vide, une exception peut être levée
   clients_a_lire = []
   try:
      clients_a_lire, wlist, xlist = select.select(clients_connectes, [], [], 0.05)
   except select.error:
      pass
   else:
      # On parcourt la liste des clients à lire
      for client in clients_a_lire:
         # Client est de type socket
         msg_recu = client.recv(1024)
         # Peut planter si le message contient des caractères spéciaux
         print("Message reçu : {}".format(msg_recu.decode('utf_8')))
         client.send("5/5".encode('utf_8'))
         if msg_recu.decode('utf_8') == "fin":
            serveur_lance = False

print("Fermeture des connexions")
for client in clients_connectes:
   client.close()

connexion_principale.close()