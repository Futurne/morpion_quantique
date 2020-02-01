"""
Contient l'objet representant un joueur dans le jeu du morpion.
Un joueur possede une couleur et un nom.
"""

class Joueur:
    def __init__(self, nom="Carlos", couleur="blue", is_croix=True):
        self.nom = nom
        self.couleur = couleur
        self.is_croix = is_croix

    def __str__(self):
        return self.nom
