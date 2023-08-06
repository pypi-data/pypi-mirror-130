from math import *
import math

# Variables
verif = True


# Fonctions EncodageUser


def EncodageUser(msg, dataType):
    while verif:
        dataTemp = input("\n" + msg + "\n>>> ")
        try:
            dataTemp = dataType(dataTemp)
            return dataTemp
        except:
            print("\nVeuillez entrer une valeur valide.")


# Fonctions Calcul


def CalcAdd(nb1, nb2):
    try:
        return nb1 + nb2
    except ValueError:
        print("\nLa valeur rentrer n'est pas un nombre ")


def CalcDiv(nb1, nb2):
    try:
        return nb1 / nb2
    except ValueError:
        print("\nLa valeur rentrer n'est pas un nombre ")


def CalcDeff(nb1, nb2):
    try:
        return nb1 - nb2
    except ValueError:
        print("\nLa valeur rentrer n'est pas un nombre ")


def CalcSin(nb):
    try:
        return math.sin(nb)
    except ValueError:
        print("\nLa valeur rentrer n'est pas un nombre ")


def CalcCos(nb):
    try:
        return math.cos(nb)
    except ValueError:
        print("\nLa valeur rentrer n'est pas un nombre ")


def CalcSqrt(nb):
    try:
        return math.sqrt(nb)
    except ValueError:
        print("\nLa valeur rentrer n'est pas un nombre ")


def CalcPow(nb1, power):
    try:
        return nb1 ** power
    except ValueError:
        print("\nLa valeur rentrer n'est pas un nombre ")


def CalcLog(nb):
    try:
        return math.log(nb)
    except ValueError:
        print("\nLa valeur rentrer n'est pas un nombre ")


def CalcExp(nb):
    try:
        return math.exp(nb)
    except ValueError:
        print("\nLa valeur rentrer n'est pas un nombre ")


def CalcTan(nb):
    try:
        return math.tan(nb)
    except ValueError:
        print("\nLa valeur rentrer n'est pas un nombre ")


def CalcCotan(nb):
    try:
        return 1 / math.tan(nb)
    except ValueError:
        print("\nLa valeur rentrer n'est pas un nombre ")


# Fonction qui calcule l'air d'un objet entré


def CalcAir(objet):
    # Calcul de l'aire d'un carré
    if objet == "carre":
        while verif:
            carreLongueur = EncodageUser(
                "Entrez la longueur du côté du carré", float)
            if carreLongueur > 0:
                return carreLongueur * carreLongueur
            else:
                print("\nLa valeur rentrer n'est pas un nombre ")
    # Calcul de l'aire d'un rectangle
    elif objet == "rectangle":
        while verif:
            rectangleLongueur = EncodageUser(
                "Entrez la longueur d'un côté du rectangle", float)
            if rectangleLongueur > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        while verif:
            rectangleLargeur = EncodageUser(
                "Entrez la largeur d'un côté du rectangle", float)
            if rectangleLargeur > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        return rectangleLongueur * rectangleLargeur
    # Calcul de l'aire d'un triangle
    elif objet == "triangle":
        while verif:
            triangleBase = EncodageUser(
                "Entrez la base du triangle", float)
            if triangleBase > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        while verif:
            triangleHauteur = EncodageUser(
                "Entrez la hauteur du triangle", float)
            if triangleHauteur > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        return triangleBase * triangleHauteur / 2
    # Calcul de l'aire d'un cercle
    elif objet == "cercle":
        while verif:
            cercleRayon = EncodageUser(
                "Entrez le rayon du cercle", float)
            if cercleRayon > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        return cercleRayon * cercleRayon * pi
    # Calcul de l'aire d'un losange
    elif objet == "losange":
        while verif:
            losangeDiagonale = EncodageUser(
                "Entrez la diagonale du losange", float)
            if losangeDiagonale > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        return losangeDiagonale * losangeDiagonale / 2
    # Calcul de l'aire d'un parallélogramme
    elif objet == "parallelogramme":
        while verif:
            parallelogrammeDiagonale = EncodageUser(
                "Entrez la diagonale du parallélogramme", float)
            if parallelogrammeDiagonale > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        return parallelogrammeDiagonale * parallelogrammeDiagonale / 2
    # Calcul de l'aire d'un trapèze
    elif objet == "trapeze":
        while verif:
            trapezeBase = EncodageUser(
                "Entrez la base du trapèze", float)
            if trapezeBase > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        while verif:
            trapezeHauteur = EncodageUser(
                "Entrez la hauteur du trapèze", float)
            if trapezeHauteur > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        return trapezeBase * trapezeHauteur / 2


# Fonction qui calcule le périmètre d'un objet entré


def CalcPerimetre(objet):
    # Calcul du périmètre d'un carré
    if objet == "carre":
        while verif:
            carreLongueur = EncodageUser(
                "Entrez la longueur du côté du carré", float)
            if carreLongueur > 0:
                return carreLongueur * 4
            else:
                print("\nLa valeur rentrer n'est pas un nombre ")
    # Calcul du périmètre d'un rectangle
    elif objet == "rectangle":
        while verif:
            rectangleLongueur = EncodageUser(
                "Entrez la longueur d'un côté du rectangle", float)
            if rectangleLongueur > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        while verif:
            rectangleLargeur = EncodageUser(
                "Entrez la largeur d'un côté du rectangle", float)
            if rectangleLargeur > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        return rectangleLongueur * 2 + rectangleLargeur * 2
    # Calcul du périmètre d'un cercle
    elif objet == "cercle":
        while verif:
            cercleRayon = EncodageUser(
                "Entrez le rayon du cercle", float)
            if cercleRayon > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        return cercleRayon * 2 * pi
    # Calcul du périmètre d'un losange
    elif objet == "losange":
        while verif:
            losangeDiagonale = EncodageUser(
                "Entrez la diagonale du losange", float)
            if losangeDiagonale > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        return losangeDiagonale * 4
    # Calcul du périmètre d'un parallelogramme
    elif objet == "parallelogramme":
        while verif:
            parallelogrammeDiagonale = EncodageUser(
                "Entrez la diagonale du parallélogramme", float)
            if parallelogrammeDiagonale > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        return parallelogrammeDiagonale * 4
    # Calcul du périmètre d'un trapèze
    elif objet == "trapeze":
        while verif:
            trapezeBase = EncodageUser(
                "Entrez la base du trapèze", float)
            if trapezeBase > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        while verif:
            trapezeHauteur = EncodageUser(
                "Entrez la hauteur du trapèze", float)
            if trapezeHauteur > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        return trapezeBase * 2 + trapezeHauteur
    # Calcul du périmètre d'un triangle
    elif objet == "triangle":
        while verif:
            triangle1 = EncodageUser(
                "Veuillez entrer la longueur du premier côté du triangle", float)
            if triangle1 > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        while verif:
            triangle2 = EncodageUser(
                "Veuillez entrer la longueur du deuxième côté du triangle", float)
            if triangle2 > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        while verif:
            triangle3 = EncodageUser(
                "Veuillez entrer la longueur du troisième côté du triangle", float)
            if triangle3 > 0:
                break
            else:
                print("\nLa valeur rentrer n'est pas un nombre")
        return triangle1 + triangle2 + triangle3
