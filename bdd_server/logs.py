import os
import datetime

# creation du dossier logs s'il n'existe pas
if not os.path.exists('logs'):
    print("make")
    os.makedirs('logs')

# @brief: permet d'écrire un nouveau log de message reçu
#        dans le fichier du jour
# @input: le numero de processus recevant le message,
#       le type de demande,
#       les parametres
def write_log_recv(numprocess, type, params):
    # creation/ouverture du fichier du jour
    today = datetime.date.today()
    file = open("logs/"+str(today.day)+"_"+str(today.month)+"_"+str(today.year)+".txt", "w")
    msg = "--> "+str(numprocess)+" "+str(datetime.datetime.today())+" "+type+" "+str(params)+"\n"
    file.write(msg)
    file.close()

# @brief: permet d'écrire un nouveau log de message renvoye
#        dans le fichier du jour
# @input: le numero de processus envoyant le message,
#       les parametres
def write_log_send(numprocess, params):
    # creation/ouverture du fichier du jour
    today = datetime.date.today()
    file = open("logs/"+str(today.day)+"_"+str(today.month)+"_"+str(today.year)+".txt", "w")
    msg = "<-- "+str(numprocess)+" "+str(datetime.datetime.today())+" return "+str(params)+"\n"
    file.write(msg)
    file.close()
