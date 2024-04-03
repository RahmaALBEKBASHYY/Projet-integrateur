import os
from select import select
import sys
import inspect
from random import *
import socket
from unittest import case
from pion import Pion
from plateau import Plateau
from categorie import Categorie
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
gparentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, gparentdir)
import treatement.treatement_request_error as tre
import treatement.treatement_request_game as trg
import treatement.treatement_request_lobby as trl
from src.GSNetwork import GSNetwork
from src.ClientThread import *

network = GSNetwork(10001)

network.send_msg_DBS(str(102) + ';aaaa;1')
retour = network.recv_msg_DBS()
split = retour.split(';')
code_request = split.pop(0)
question = split.pop(0)
tab_string = []
tab_bool = []
for i in range(len(split)):
    if i%2 == 0:
        tab_string.append(split[i])
    else:
        tab_bool.append(split[i])

print("code =" + code_request)
print("question =" + question)
print("reponses =" + ','.join(t for t in tab_string))
print("bool =" + ','.join(str(t) for t in tab_bool))
    
