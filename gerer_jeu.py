"""
Lance et gere le jeu dans son ensemble.
"""

import jeu
from plateau import Plateau
from afficher_jeu import AfficherJeu
from joueur import Joueur

class GererJeu:
    """Lance le jeu et permet de gerer le jeu dans son ensemble."""
    def __init__(self, joueur1, joueur2):
        self.joueur1 = joueur1
        self.joueur2 = joueur2

        self.is_in_coup = False #True lorsqu'on a clicke sur une case et qu'on doit en choisir une deuxieme
        self.is_in_pion = False #True lorsqu'on doit choisir entre deux cases pour placer un pion
        self.joueur_en_cours = self.joueur1 #premier a jouer est le joueur1

    def gerer_click(self, case):
        """Fonction appelee à chaque clics sur une case du morpion."""
        if self.is_in_coup:
            self.case2 = case
            self.clic_in_coup()
        elif self.is_in_pion:
            self.case_choisie = case
            self.case1, self.case2 = None, None
            self.clic_in_pion()
            j1, j2 = self.is_win()
            if j1 is not None or j2 is not None:
                self.afficher_jeu.end_game(j1, j2)
            elif jeu.is_equal(self.plateau):
                self.afficher_jeu.end_game(None, None)
        else:
            self.case1 = case
            self.clic_debut_coup()

    def clic_debut_coup(self):
        self.plateau.ajouter_coup_temporaire(self.joueur_en_cours, self.case1)
        self.is_in_coup = True
        self.afficher_jeu.actualiser_affichage()

    def clic_in_coup(self):
        """
        Lorsqu'on a clicke et qu'on vient donc de finir un coup.
        Verifie que le coup est valide, sinon annule le coup et reset les variables.
        Si le coup est valide : ajoute le coup dans la liste des coups, et verifie si le coup est ferme.
        Dans le cas ou le coup est ferme, agit en consequence.
        """
        #si le coup n'est pas valide, on annule le coup et on recommence
        if self.plateau.pions[self.case1] is not None or self.plateau.pions[self.case2] is not None or self.case1 == self.case2:
            self.case1, self.case2 = None, None
            self.is_in_coup = False
            self.afficher_jeu.changer_title("Coup invalide, recommencez", None)
            self.plateau.ajouter_coup_temporaire(None, None) #annule le debut du coup
            self.afficher_jeu.actualiser_affichage()
            return

        self.id_coup = self.plateau.ajouter_coup(self.joueur_en_cours, self.case1, self.case2)
        self.afficher_jeu.actualiser_affichage()
        self.is_in_coup = False
        if jeu.is_coup_ferme(self.plateau, self.case1, self.case1, None): #ce coup vient de ferme un chemin
            self.afficher_jeu.dessiner_symboles_possibles(self.case1, self.case2, self.joueur_en_cours)
            self.is_in_pion = True #signal que le prochain clic doit etre pour placer un pion
            if self.joueur_en_cours is self.joueur1:
                joueur_adverse = self.joueur2
            else:
                joueur_adverse = self.joueur1
            self.afficher_jeu.changer_title("{} choisi où placer le symbole.".format(joueur_adverse.nom), joueur_adverse.couleur)
            return #attend le clic sur une des deux cases

        #fin du tour de jeu : c'est a l'autre joueur de jouer
        if self.joueur_en_cours is self.joueur1:
            self.joueur_en_cours = self.joueur2
        else:
            self.joueur_en_cours = self.joueur1
        self.afficher_jeu.changer_title("A {} de jouer !".format(self.joueur_en_cours.nom), self.joueur_en_cours.couleur)

    def clic_in_pion(self):
        """Lorsqu'on a choisi un pion a placer."""
        jeu.placer_pion(self.plateau, self.case_choisie, self.id_coup, self.joueur_en_cours, self.actualiser_pause)
        jeu.purifier_coups(self.plateau)
        self.afficher_jeu.actualiser_affichage()
        self.afficher_jeu.changer_title("A {} de jouer !".format(self.joueur_en_cours.nom), self.joueur_en_cours.couleur)
        self.is_in_pion = False

    def actualiser_pause(self, temps=1):
        """Actualise puis effectue une pause du programme."""
        self.afficher_jeu.actualiser_affichage()

    def is_win(self):
        """
        Check si la partie est finie pour un des joueurs.
        Retourne un joueur si il a gagne, sinon retourne None.
        """
        j1, j2 = None, None
        if jeu.is_win(self.plateau, self.joueur1):
            j1 = self.joueur1
        if jeu.is_win(self.plateau, self.joueur2):
            j2 = self.joueur2
        return j1, j2

    def lancer_jeu(self, longueur=3, largeur=3):
        self.plateau = Plateau(longueur, largeur)
        self.afficher_jeu = AfficherJeu(self.plateau, self.gerer_click)
        self.afficher_jeu.actualiser_affichage()
        self.afficher_jeu.changer_title("A {} de jouer !".format(self.joueur_en_cours.nom), self.joueur_en_cours.couleur)

        self.afficher_jeu.mainloop() #lance le jeu ! Ne s'arrete pas tant que le jeu n'est pas fini
        self.afficher_jeu.quit()

if __name__ == "__main__":
    joueur1 = Joueur("Pierrot", "blue", True)
    joueur2 = Joueur("Alex", "red", False)

    g = GererJeu(joueur1, joueur2)
    g.lancer_jeu()
