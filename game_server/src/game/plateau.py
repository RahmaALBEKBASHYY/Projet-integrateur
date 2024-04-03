from random import *
from case import *


class Plateau:
         
    """
    @brief: initialise l'objet plateau
    @input: self: l'objet, catgegories: les categories du jeu
    @output: none
    """
    def __init__(self, categories):
        self.cases = []
        self.categories = categories
        self.generate_nodes()
        self.generate_edges()
    
    """
    @brief: genere les noeuds 
    @input: self: l'objet
    @output: none
    """
    def generate_nodes(self):

        #case 0 particuliere
        self.cases.append(Case(0, self.categories[5]))

        #genere les autres cases de maniere rapide 
        for i in range(5):
            #genere les cases faisant remporter un aliment
            self.cases.append(Case(((5-i)*7)%35 +26, self.categories[i], True))

            #genere les 2 cases autour           
            self.cases.append(Case((5-i)*7 +20, self.categories[i]))#suivante ok           
            self.cases.append(Case(60 - 7*((i+1)%5), self.categories[i]))#precedente

            #ajoute les 2 cases du thèmes
            self.cases.append(Case(((5-i)*7 +11)%35 +26, self.categories[i]))
            self.cases.append(Case(((5-i)*7 +17)%35 +26, self.categories[i]))

            #ajoute les des
            self.cases.append(Case(((5-i)*7)%35 +28, Categorie(6, 'b','d', '')))
            self.cases.append(Case(((5-i)*7)%35 +31, Categorie(6, 'b','d', '')))
            for j in range(5):
                self.cases.append(Case(j*5+(j+i)%5+1, self.categories[i]))
        self.cases.sort(key=lambda x: x.value)

    """
    @brief: genere les aretes 
    @input: self: l'objet
    @output: none
    """
    def generate_edges(self):
        k=0
        for i in range(1,61):
            #prec
            if i%5 == 1 and i <=25:
                self.cases[i].append_voisin(0)
                self.cases[0].append_voisin(i)
            elif i == 26:
                self.cases[i].append_voisin(60)
            else:
                self.cases[i].append_voisin(i-1)

            #suivant
            if i%5 == 0 and i <=25:
                self.cases[i].append_voisin(i+21+ k*2)
                self.cases[i+21+ k*2].append_voisin(i)
                k+=1
            elif i == 60:
                self.cases[i].append_voisin(26)
            else:
                self.cases[i].append_voisin(i+1)

    """
    @brief: genere le retour d'un theme
    @input: self: l'objet
    @output: none
    """
    def print_theme(self):
        retour = '['
        for i in range (len(self.cases)):
            retour += '\'' + str(self.cases[i].categorie.color)+ '\'' + ','
        return retour[:-1] + ']'

    """
    @brief: genere le lancer d'un de
    @input: self: l'objet
    @output: none
    """
    def lancer_des(self):
        x = randint(1,6)
        return x

    """
    @brief: genere la liste des cases atteignables
    @input: self: l'objet
    @output: none
    """
    def liste_case(self, num, de):
        case_prec = []
        case_suiv = [num]
        case_iter_suiv = []
        while de >0:
            for c in case_suiv:
                case_prec.append(c)
                for i in range(len(self.cases[c].voisins)):
                    voisin = self.cases[c].voisins[i]
                    if voisin not in case_prec:
                        case_iter_suiv.append(voisin)
            case_suiv = case_iter_suiv
            case_iter_suiv = []
            print(case_prec)
            print((de,case_suiv))
            de -=1
        return case_suiv
        
