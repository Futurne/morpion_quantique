"""
Affiche le jeu.
Possibilite d'actualiser la partie et le titre.
"""

from tkinter import *

class AfficherJeu(Tk):
    """Gere l'affichage du jeu."""
    def __init__(self, plateau, function_on_click):
        """
        A besoin du plateau sur lequel s'appuye pour l'affichage,
        et d'une fonction qui prend en parametre une case, qui est appelee a chaque clique sur une case.
        """
        Tk.__init__(self)
        self.width = 600
        self.height = 700

        self.resizable(width=False, height=False)
        self.minsize(width=self.width, height=self.height)

        self.plateau = plateau
        #enleve 20 aux dimensions car il y a un padx et pady de 10
        self.longueur_case = (self.width-20)/self.plateau.longueur
        self.largeur_case = (self.height-100-20)/self.plateau.largeur

        self.function_on_click = function_on_click

        self.create_title_frame()
        self.create_main_frame()

    def create_title_frame(self):
        """Le title permet de montrer aux joueurs l'etat du jeu."""
        self.title_frame = Frame(self, bd=2, width=self.width, height=100, relief=GROOVE)
        self.title_frame.pack(side=TOP, padx=10, pady=10)

        self.label_title = Label(self.title_frame, text="Morption quantique !")
        self.label_title.pack()

    def create_main_frame(self):
        """Contient le jeu lui-meme."""
        self.main_frame = Frame(self, width=self.width, height=self.height-100)
        self.main_frame.pack(side=BOTTOM)

        self.canvas = Canvas(self.main_frame, width=self.width, height=self.height-100)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.callback)

    def end_game(self, joueur1, joueur2):
        """Fait apparaitre un pop-up pour signaler qui a gagne."""
        toplevel = Toplevel(self)
        if joueur1 is None and joueur2 is None:
            desc = "Egalité !"
        elif joueur1 is None:
            desc = "{} a gagné !".format(joueur2.nom)
        elif joueur2 is None:
            desc = "{} a gagné !".format(joueur1.nom)
        else:
            desc = "Les deux joueurs ont gagné."
        toplevel.wm_title("Partie finie !")
        toplevel.tkraise(self)
        Label(toplevel, text=desc, height=0, width=50).pack()
        Button(toplevel, text="Okay", command=self.destroy).pack()
        toplevel.focus_force()

    def callback(self, event):
        """Fonction declanchee lors d'un click sur le canvas."""
        if event.x > self.width-10 or event.y > self.height-110 or event.x < 10 or event.y < 10: #hors des cases
            return

        case = (int((event.x-10)/self.longueur_case), int((event.y-10)/self.largeur_case)) #determine la case clickee en fonction des coordonnees du click
        self.function_on_click(case)

    def changer_title(self, texte, couleur):
        """Modifie le title pour afficher l'etat du jeu. None a couleur permet de ne pas la changer."""
        if couleur is not None:
            self.label_title.config(text=texte, fg=couleur)
        else:
            self.label_title.config(text=texte)

    def dessiner_symboles_possibles(self, case1, case2, joueur):
        """
        Fonction appellee lorsqu'un chemin a ete ferme et qu'il faut selectionner
        entre deux cases pour placer un pion. Affiche donc deux symboles en mode dash
        pour inviter le joueur a selectionner une case.
        """
        self.dessiner_symbole(case1, None, joueur.is_croix, "yellow", True)
        self.dessiner_symbole(case2, None, joueur.is_croix, "yellow", True)

    def actualiser_affichage(self):
        """
        Acutalise l'affichage du canvas.
        Efface tout le canvas puis redessine tout en utilisant le plateau.
        """
        coups_a_relier = dict() #dictionnaire contenant pour chaque coup_id les coord des symboles (pour dessiner les traits)
        longueur_case, largeur_case = self.longueur_case, self.largeur_case

        #efface le plateau totalement puis le redessine en blanc
        self.canvas.delete(ALL)
        for lon in range(self.plateau.longueur):
            for larg in range(self.plateau.largeur):
                self.blanchir_case((lon, larg))

        for lon in range(self.plateau.longueur): #ajoute les symboles case par case
            for larg in range(self.plateau.largeur):
                case = (lon, larg)
                coord_case = self.coord_case(case)
                joueur = self.plateau.pions[case]
                if joueur is not None:
                    self.dessiner_symbole(case, None, joueur.is_croix, joueur.couleur) #dessine d'abord le pion de la case

                cpt = 0
                for coup in self.plateau.coups[case]: #puis les coups sur la case
                    joueur = coup[0]
                    coord_symb = [0, 0]
                    coord_symb[0] = 10 + (cpt%4)*(longueur_case/5+10)
                    coord_symb[1] = 10 + int(cpt/4)*(longueur_case/5+10)
                    self.dessiner_symbole(case, coord_symb, joueur.is_croix, joueur.couleur)

                    coord_symb[0] += coord_case[0] #decale les coordonnes pour qu'elles match la realite
                    coord_symb[1] += coord_case[1]
                    if coup[2] in coups_a_relier: #si l'autre partie du coup a deja ete affichee : trace un trait qui les relie
                        self.canvas.create_line(coord_symb[0], coord_symb[1], coups_a_relier[coup[2]][0], coups_a_relier[coup[2]][1], fill=joueur.couleur, width=3)
                    else:
                        coups_a_relier[coup[2]] = coord_symb #enregistre les coordonnees du symbole pour pouvoir ensuite trace un trait

                    cpt += 1 #permet de decaler les petits symboles dans une meme case d'un cran

                if case in self.plateau.coup_temporaire: #dessine le debut d'un coup qui a ete fait par un joueur
                    coord_symb = [0, 0]
                    coord_symb[0] = 10 + (cpt%4)*(longueur_case/5+10)
                    coord_symb[1] = 10 + int(cpt/4)*(longueur_case/5+10)
                    self.dessiner_symbole(case, coord_symb, self.plateau.coup_temporaire[0].is_croix, self.plateau.coup_temporaire[0].couleur, True)

    def coord_case(self, case):
        """Retourne les coordonnees de la case donnees (dans le canvas)."""
        debut_plateau = (10, 10) #padx et pady de 10
        debut_case = (debut_plateau[0]+case[0]*self.longueur_case, debut_plateau[1]+case[1]*self.largeur_case)
        return debut_case

    def blanchir_case(self, case):
        """Efface et redessine la case donnee en blanc."""
        debut_case = self.coord_case(case)
        #dessine une case blanche
        self.canvas.create_rectangle(debut_case[0], debut_case[1], debut_case[0]+self.longueur_case, debut_case[1]+self.largeur_case, fill="white")

    def dessiner_symbole(self, case, coord_symbole, is_croix, couleur, is_dashed=False):
        """
        Dessine le symbole croix (si is_croix=True) ou cercle (sinon) dans la case donnee.
        Si coord_symbole n'est pas None, alors c'est qu'il faut dessiner un petit symbole (un coup)
        et non un grand symbole (un pion). Les coord_symbole sont relatives a la case.
        """
        longueur_case, largeur_case = self.longueur_case, self.largeur_case
        debut_case = self.coord_case(case)
        if coord_symbole is not None: #petit symbole
            debut_symbole = (debut_case[0] + coord_symbole[0], debut_case[1] + coord_symbole[1])
            fin_symbole = (debut_symbole[0] + longueur_case/5, debut_symbole[1] + longueur_case/5)
        else:
            debut_symbole = (debut_case[0] + 10, debut_case[1] + 10)
            fin_symbole = (debut_case[0] + longueur_case - 10, debut_case[1] + largeur_case - 10)

        dash = None
        if is_dashed: #pour dessiner des symboles en tirets pour proposer les cases pour placer des pions
            if coord_symbole is None:
                dash = (10, 10, 10, 10)
            else:
                dash = (8, 8, 8, 8)

        if is_croix:#dessine une croix
            self.canvas.create_line(debut_symbole[0], debut_symbole[1], fin_symbole[0], fin_symbole[1], fill=couleur, width=4, dash=dash)
            self.canvas.create_line(debut_symbole[0], fin_symbole[1], fin_symbole[0], debut_symbole[1], fill=couleur, width=4, dash=dash)
        else:
            self.canvas.create_oval(debut_symbole[0], debut_symbole[1], fin_symbole[0], fin_symbole[1], outline=couleur, width=4, dash=dash)
