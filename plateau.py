"""
Contient l'objet plateau du jeu, stockant les valeurs des coups joues.
"""

class Plateau:
    """Objet contenant les coups des joueurs."""
    def __init__(self, longueur=3, largeur=3):
        """
        Initialise les variables.
        La liste coups contiendra la liste de tout les coups joues par les joueurs.
        La liste des pions est la liste contenant les pions reellement places
        par les joueurs. Une case vide est representee par la valeur None.
        """
        self.longueur = longueur
        self.largeur = largeur
        self.coups = {(i, j):[] for i in range(longueur) for j in range(largeur)}
        self.pions = {(i, j):None for i in range(longueur) for j in range(largeur)}
        self.coup_id = 0
        self.coup_temporaire = []

    def ajouter_coup(self, joueur, case1, case2):
        """
        Ajoute un coup dans la liste des coups.
        Un coup est constitué des deux cases sur lesquelles le joueur joue, ainsi que le joueur lui-meme.
        La case doit etre un couple (x, y).
        Retourne l'id du coup.
        """
        self.coups[case1].append([joueur, case2, self.coup_id])
        self.coups[case2].append([joueur, case1, self.coup_id])
        self.coup_id += 1
        self.coup_temporaire = []
        return self.coup_id - 1

    def ajouter_pion(self, joueur, case):
        """
        Ajoute le pion dans la liste des pions.
        Un pion est juste represente par le joueur.
        La case doit etre un couple (x, y).
        """
        self.pions[case] = joueur

    def ajouter_coup_temporaire(self, joueur, case):
        """
        Ajoute un demi-coup, permettant de savoir a l'affichage
        et donc a l'utilisateur qu'il a un debut de coup a cet endroit.
        """
        self.coup_temporaire = [joueur, case]

    def parcourir_longueur(self):
        """Itere sur les pions en parcourant longueur par longueur."""
        for lon in range(self.longueur):
            for larg in range(self.largeur):
                yield self.pions[(lon, larg)]

    def parcourir_largeur(self):
        """Itere sur les pions en parcourant largeur par largeur."""
        for larg in range(self.largeur):
            for lon in range(self.longueur):
                yield self.pions[(lon, larg)]

    def __str__(self):
        """Affiche le jeu."""
        desc = ""
        for lon in range(self.longueur):
            desc += '||' + " | ".join(['({}, {}) : {} {}'.format(lon, larg, str(self.pions[(lon, larg)]), [coup[2] for coup in self.coups[(lon, larg)]]) for larg in range(self.largeur)]) + '||\n'
        return desc[:-1]
