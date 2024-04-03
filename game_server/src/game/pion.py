from choucroute import Choucroute

#class du joueur
class Pion():

    """
    @brief: initialise l'objet pion
    @input: self: l'objet, sock_j: la socket du joueur,
    @output: none
    """
    def __init__(self,sock_j, login):
        self.socket = sock_j #socket
        self.ready = False #etat pret ou non
        self.login = login #login
        self.last_de = -1 #derniere valeur du de
        self.color = "" #couleur
        self.Choucroute = Choucroute() #etat de la choucroute
        self.num_case = 0 #numero de la case
        self.joueur = True #ia ou joueur
        
        self.nbpoint = 0 #nombre de points
        self.classement = 1 #classement courant
        self.nbGoodAnswer = 0 #nombre de bonne rep
        self.nbBadAnswer = 0 #nombre de mauvaises rep


    """
    @brief: etat du joueur
    @input: self: l'objet
    @output: boolean
    """
    def is_not_ready(self):
        return self.ready

    """
    @brief: crée la string pour une requete 
    @input: self: l'objet
    @output: string
    """
    def toStr(self):
        return self.login + ";" + self.color + ';' + str(self.nbpoint) + ';' + str(self.classement) + ';' + str(self.nbGoodAnswer) + ';'+ str(self.nbBadAnswer) + ';' +self.Choucroute.to_str()

    

