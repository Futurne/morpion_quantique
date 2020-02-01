"""
Permet la gestion du jeu.
Les regles s'appliquent ici.
"""

def is_win(plateau, joueur):
    """
    Retourne si oui ou non le joueur a gagne.
    On verifie uniquement certains axes, en sachant que les possibilites
    non verifiees seront de toutes facon verifiees lors du traitement d'autres pions.
    """
    pions = plateau.pions
    for case in pions:
        if pions[case] is not joueur:
            continue #on saute les cases qui ne sont pas des pions du joueur

        compteurs_alignement = [0, 0, 0, 0] #compte le nombre de cases alignees selon les 4 axes
        for decalage in range(1, 3): #parcourt toutes les cases voisines dans toutes les directions
            x, y = case[0], case[1]

            #axe longueur
            if x + decalage < plateau.longueur and pions[(x + decalage, y)] is joueur:
                compteurs_alignement[0] += 1
            #axe largeur
            if y + decalage < plateau.largeur and pions[(x, y + decalage)] is joueur:
                compteurs_alignement[1] += 1

            #diagonale 1
            if x + decalage < plateau.longueur and y + decalage < plateau.largeur and pions[(x+decalage, y+decalage)] is joueur:
                compteurs_alignement[2] += 1
            #diagonale 2
            if x + decalage < plateau.longueur and y - decalage > -1 and pions[(x+decalage, y-decalage)] is joueur:
                compteurs_alignement[3] += 1

        if 2 in compteurs_alignement: #Au moins 3 pions du meme joueur sont alignes
            return True
    return False

def is_coup_ferme(plateau, case_actuelle, case_depart, id_ancien_coup=None):
    """
    Fonction recursive donnant si oui ou non le coup jouer a la case de depart est un coup qui ferme
    un ensemble de coups.
    Pour le premier appel de la fonction, id_ancien_coup doit etre None
    """
    if case_actuelle == case_depart and id_ancien_coup is not None:
        return True

    for coup in plateau.coups[case_actuelle]:
        if coup[2] == id_ancien_coup:
            continue #deplacement precedent : ininteressant
        if is_coup_ferme(plateau, coup[1], case_depart, coup[2]): #se deplace d'un coup
            return True
    return False #aucun deplacement n'a marche

def placer_pion(plateau, case, coup_id, joueur, function_actualise=None):
    """
    Place recursivement tout les pions a partir du coup initial.
    Fait en sorte que lorsqu'un place est prise par un pion,
    tout les autres pions qui etait sur cette case et sur une autre
    sont definitivement places sur les autres cases.
    """
    if plateau.pions[case] is not None: #lorsqu'on a fini une boucle de deplacement : on s'arrete
        return

    plateau.ajouter_pion(joueur, case)
    if function_actualise is not None:
        function_actualise()

    for coup in plateau.coups[case]:
        if coup[2] != coup_id: #coup correspondant au deplacement du coup precedent : deja joue
            placer_pion(plateau, coup[1], coup[2], coup[0], function_actualise)

def purifier_coups(plateau):
    """Passe en revue la liste des coups du plateau, enleve ceux non valides."""
    for lon in range(plateau.longueur):
        for larg in range(plateau.largeur):
            case = (lon, larg)
            if plateau.pions[case] is not None:
                plateau.coups[case] = [] #reinitialise le dico lorsqu'il y a un pion

def tour(plateau, case1, case2, joueur, fonction_demander_case):
    """
    Effectue un tour de jeu.
    A besoin de la fonction qui demande si besoin, le choix d'une des deux cases.
    La fonction doit prendre en parametre les deux cases.
    """
    id_coup = plateau.ajouter_coup(joueur, case1, case2)
    if is_coup_ferme(plateau, case2, case2):
        case_choisie = fonction_demander_case(case1, case2) #demande la case sur laquelle placer le pion
        placer_pion(plateau, case_choisie, id_coup, joueur) #place les pions selon le choix du joueur
        purifier_coups(plateau) #enleve les coups qui sont devenus inutiles

def is_equal(plateau):
    """Retourne True si il n'y a plus de cases possiblent : si on ne peut plus jouer."""
    for lon in range(plateau.longueur):
        for larg in range(plateau.largeur):
            case = (lon, larg)
            if plateau.pions[case] is None:
                return False
    return True
