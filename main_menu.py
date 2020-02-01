#! /usr/bin/ python3
"""
Affiche le menu principal.
Menu permettant de choisir le nom des joueurs, puis de lancer la partie.
"""

from tkinter import *

class MainMenu(Tk):
    """Affiche le menu principal en utilisant le module Tkinter."""
    def __init__(self):
        Tk.__init__(self)
        self.width = 300
        self.height = 300

        self.resizable(width=False, height=False)
        self.minsize(width=self.width, height=self.height)

        self.create_north_frame()
        self.create_main_frame()

    def create_north_frame(self):
        self.north_frame = Frame(self, bd=2, width=self.width, height=100, relief=GROOVE)
        self.north_frame.pack(padx=10, pady=10)
        Label(self.north_frame, text="Morpion quantique", fg="black").pack()

    def create_main_frame(self):
        self.main_frame = Frame(self, bd=2, width=self.width, height=200, relief=GROOVE)
        self.main_frame.pack(side=TOP)

        temp1 = Frame(self.main_frame, width=self.width)
        temp1.pack()
        self.pseudos = []
        for i in range(1, 3):
            temp = Frame(temp1, width=self.width)
            temp.pack()
            s = StringVar()
            s.set("")
            self.pseudos.append(s)
            Label(temp, text="Pseudo joueur {}".format(i)).pack(side=LEFT)
            Entry(temp, textvariable=s, width=10).pack(side=RIGHT)

        temp2 = Frame(self.main_frame, width=self.width)
        temp2.pack(side=BOTTOM)
        Button(temp2, text="OK", command=self.ok_button).pack()
        self.pressed_ok = False

    def ok_button(self):
        """Ferme la fenetre et met la valeur de la variable a True pour que l'on sache que on a appuye sur le bouton."""
        self.pressed_ok = True
        return self.destroy()

if __name__ == "__main__":
    from joueur import Joueur
    from gerer_jeu import GererJeu

    menu = MainMenu()
    menu.mainloop()
    menu.quit()

    if menu.pressed_ok:
        joueur1 = Joueur(menu.pseudos[0].get(), "blue", True)
        joueur2 = Joueur(menu.pseudos[1].get(), "red", False)
        g = GererJeu(joueur1, joueur2)
        g.lancer_jeu()
