class Categorie:

    """
    @brief: init les categories
    @input: self: l'objet categorie, id: id de la cat, color: couleur liee, theme: nom du theme, aliment: alim remporte
    @output: none
    """
    def __init__(self, id, color, theme, aliment):
        self.id = id
        self.color = color
        self.theme = theme
        self.aliment = aliment