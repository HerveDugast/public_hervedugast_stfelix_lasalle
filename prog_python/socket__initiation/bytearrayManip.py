#!/usr/bin/python3.4
# coding: utf-8
"""
Programme : bytearrayManip.py      version 1.0
Date : 18-04-2018
Auteur : Hervé Dugast

------ Affichage console --------------------------------------------------------------------------
Hello world!
b'Hello world!'
Hello world!

b'Bonjour le monde !'
Bonjour le monde !
b'Bonjour le monde !'
---------------------------------------------------------------------------------------------------
"""

msgStr = "Hello world!"
print(msgStr)
msgStr_to_bytearray = msgStr.encode('utf8')
print(msgStr_to_bytearray)
msgStr2 = msgStr_to_bytearray.decode('utf8')
print(msgStr2)


print("")
msgBytearray = b'Bonjour le monde !'
print(msgBytearray)
msgBytearray_to_str = msgBytearray.decode('utf8')
print(msgBytearray_to_str)
msgBytearray2 = msgBytearray_to_str.encode('utf8')
print(msgBytearray2)
