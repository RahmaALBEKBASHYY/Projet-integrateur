class Choucroute():

    """
    @brief: initialise la choucroute
    @input: self: l'objet choucroute
    @output: none
    """
    def __init__(self):
        self.choux = False
        self.knack = False
        self.pdt = False
        self.lard = False
        self.vin = False

    """
    @brief: prepare la string de la choucroute
    @input: self: l'objet choucroute
    @output: string
    """
    def to_str(self):
        return str(self.choux) + ";" + str(self.knack) + ";" + str(self.pdt) + ";" + str(self.lard) + ";" + str(self.vin) + ";"
    
    """
    @brief: changes l'etat de la choucroute
    @input: self: l'objet choucroute, letter: le theme
    @output: none
    """
    def setIngredient(self, letter):
        if letter =='h':
            self.choux = True
        elif letter == 's':
            self.knack = True
        elif letter == 'n':
            self.pdt = True
        elif letter == 'c':
            self.lard = True
        elif letter == 'g':
            self.vin = True

    """
    @brief: prepare la string de la choucroute
    @input: self: l'objet choucroute
    @output: string
    """
    def win(self):
        return self.choux and self.knack and self.pdt and self.lard and self.vin

    """
    @brief: donne le nombre d'ingredient
    @input: self: l'objet choucroute
    @output: int
    """
    def nbIngredient(self):
        ret = 0
        if self.choux:
            ret +=1
        if self.knack:
            ret +=1
        if self.pdt:
            ret +=1
        if self.lard:
            ret +=1
        if self.vin:
            ret +=1
        return ret