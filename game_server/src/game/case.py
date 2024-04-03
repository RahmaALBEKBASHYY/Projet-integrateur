from categorie import *

class Case:

    """
    @brief: ajoute une voisin
    @input: self: l'objet case, value: id de la case, categorie: de la case, special: si elle rapporte un ingredient
    @output: none
    """
    def __init__(self, value, categorie, special=False):
        self.value = value
        self.categorie = categorie
        self.special = special
        self.voisins = []

    """
    @brief: ajoute une voisin
    @input: self: l'objet case, case: une case
    @output: none
    """
    def append_voisin(self, case):
        self.voisins.append(case)