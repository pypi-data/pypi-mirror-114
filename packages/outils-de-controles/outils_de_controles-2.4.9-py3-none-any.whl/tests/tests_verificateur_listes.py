"""Ce module teste avec unittest la classe VerificateurListes."""

import unittest
import os
import sys

#On change le dossier de travail (cwd) pour pouvoir appeler les fichiers via des chemins relatifs
os.chdir(os.path.dirname(__file__))#On change le dossier de travail en appellant le nom du dossier qui contient ce fichier (le dossier tests)
os.chdir("..")#On rechange le dossier de travail en prenant le dossier parent du dossier tests (le dossier outils_de_controles)
sys.path.append(os.getcwd())#ligne nécessaire à l'importation du module verificateur_listes

from outils_de_controles.verificateur_listes import * 
from outils_de_controles.verificateur import *
from outils_de_controles.verificateur_str import *

class TestVerificateurListes(unittest.TestCase) :
    """Classe qui teste la classe VerificateurListes.

    Vérifie que la classe VerificateurListes du package outils_de_controles soit conforme aux spécifications. (Création, affichage, vérification des listes, ...).
    """

    def assertEqualVL(self, VL, types=list, minimum=0, maximum=None, liste_verificateurs=[]) :
        """Cette méthode vérifie si deux objets VerificateurListes sont égaux.

        Cette methode compare chaque attribut à la valeur fournie.
        """
        if VL.types == types and VL.minimum == minimum and VL.maximum == maximum and VL._liste_verificateurs == liste_verificateurs :
            return self.assertEqual(0,0)#l'objet verificateur est égal à la valeur théorique
        else :
            VL_theorique = VerificateurListes(types=types, minimum=minimum, maximum=maximum)
            for verif in liste_verificateurs :
                VL_theorique._append(verif)
            raise AssertionError(repr(VL) + " != " + repr(VL_theorique))

    def setUp(self) :
        """Cette méthode prépare l'exécution des tests.
        
        Cette méthode crée pour cela des objets VerificateurListes.
        """
        #création d'un objet vide
        self.VL1 = VerificateurListes()
        #création d'un objet avec une liste
        self.VL2 = VerificateurListes([0, 4, Verificateur(float)], types=list, minimum=1)
        #création d'un objet avec trois listes
        self.VL3 = VerificateurListes([3, None, VerificateurStr(1)], [0,None, Verificateur(int, 0, 23)], [1,2, Verificateur(int, 0, 59)], types=tuple, maximum=4)#exemple avec un tuple à 4 champs : heure, minute seconde et nom du fuseau horaire

    def test_init(self) :
        """Méthode testant l'initialisation des objets VerificateurListes.

        Vérifie que l'objet créé est conforme aux arguments passés en paramètres.
        """
        #objet vide
        self.assertEqualVL(self.VL1)
        self.assertEqualVL(self.VL2, types=list, minimum=1, liste_verificateurs=[[0,4, Verificateur(float)]])
        self.assertEqualVL(self.VL3, types=tuple, maximum=4, liste_verificateurs=[[3, None, VerificateurStr(1)], [0,None, Verificateur(int, 0, 23)], [1,2, Verificateur(int, 0, 59)]])

    def test_init_erreur(self) :
        """Méthode vérifiant que __init__ lève certaines erreurs.

        Vérifie notamment qu'il y a une erreur levée si un des arguments n'est pas une liste, si un des deux identifiants (index) n'est pas un nombre entier positif (ou None), si les deux indentifiants valent None, si un identifiant existe déjà dans la liste. Vérifie aussi que maximum est supérieur ou égal à minimum et que ces deux attributs soient des entiers positifs.
        """
        #l'argument non nommé n'est pas une liste
        with self.assertRaises(TypeError) :
            VLe = VerificateurListes("c'est une blaque !")
        #l'index 1 n'est pas un nombre entier positif
        with self.assertRaises(TypeError) :
            VLe = VerificateurListes(["a", None, Verificateur()])
        #l'index 1 n'est pas un nombre entier positif
        with self.assertRaises(ValueError) :
            VLe = VerificateurListes([-2, None, Verificateur()])
        #l'index est identique à un autre argument de la liste
        with self.assertRaises(ValueError) :
            VLe = VerificateurListes([0, None], [0, 3])
        with self.assertRaises(ValueError) :
            VLe = VerificateurListes([1, None], [0, 3])
        #l'index 2 n'est pas un entier positif
        with self.assertRaises(TypeError) :
            VLe = VerificateurListes([1, 3, Verificateur(int)], [4, "a", Verificateur()])
            self.assertEqual(VLe._liste_verificateurs, [[1, 3, Verificateur(int)]])
        #aucun identifiant n'est précisé
        with self.assertRaises(ValueError) :
            VLe = VerificateurListes([None, None, Verificateur(int)])
        #minimum n'est pas un entier
        with self.assertRaises(TypeError) :
            VLe = VerificateurListes(minimum=2.5)
        #maximum n'est pas un entier
        with self.assertRaises(TypeError) :
            VLe = VerificateurListes(maximum="bla")
        #minimum n'est pas un nombre positif
        with self.assertRaises(ValueError) :
            VLe = VerificateurListes(minimum=-2)
        #maximum est inférieur au minimum
        with self.assertRaises(ValueError) :
            VLe = VerificateurListes(minimum=10, maximum=5)

    def test_str(self) :
        """Méthode qui teste la méthode spéciale __str__.
        
        Vérifie que l'affichage des objets de la classe VerificateurArguments est correct (présentation sous forme de tableau ...).
        """
        str_theorique = """◄types:<class 'tuple'>, minimum:0, maximum:4\n\n   Identifiant 1       Identifiant 2        Vérificateur    \n         3                  None        ◄minimum:1, maximum:None, regex:''►\n         0                  None        ◄types:<class 'int'>, minimum:0, maximum:23►\n         1                   2          ◄types:<class 'int'>, minimum:0, maximum:59►\n►\n"""
        self.assertEqual(str(self.VL3), str_theorique)

    def test_repr(self) :
        """Cette méthode teste la méthode spéciale __repr__."""
        repr_theorique = """outils_de_controles.VerificateurListes([3, None, outils_de_controles.VerificateurStr(minimum=1, maximum=None, regex='')], [0, None, outils_de_controles.Verificateur(types=<class 'int'>, minimum=0, maximum=23)], [1, 2, outils_de_controles.Verificateur(types=<class 'int'>, minimum=0, maximum=59)], types=<class 'tuple'>, minimum=0, maximum=4)"""
        self.maxDiff = None
        self.assertEqual(repr(self.VL3), repr_theorique)

    def test__id_verificateur(self) :
        """Méthode vérifiant le bon fonctionnement de _id_verificateur.

        Vérifie que _id_verificateur renvoie bien le vérificateur correspondant à l'identifiant.
        """
        V1 = self.VL3._id_verificateur(1)
        V1_theorique = Verificateur(int, 0, 59)
        self.assertEqual(V1, V1_theorique)
        V2 = self.VL2._id_verificateur(3)
        V2_theorique = Verificateur(float, None, None)
        self.assertEqual(V2, V2_theorique)

    def test__id_verificateur_error(self) :
        """Vérifie que _id_verificateur lève des erreurs.

        Vérifie que lorsque l'identifiant passé en paramètre n'existe pas, une erreur est levée.
        """
        with self.assertRaises(ValueError) :
            Ve = self.VL3._id_verificateur("blabla")

    def test_contains(self) :
        """Méthode vérifiant le bon fonctionnement de __contains__.

        Vérifie que la recherche d'argument dans la liste avec le mot clé in, s'effectue correctement.
        """
        B = [False for i in range(7)]
        if 1 in self.VL1 :
            B[0] = True #booléen n°1
        if "prenom" in self.VL2 : 
            B[1] = True
        if list in self.VL3 :
            B[2] = True
        if 3 in self.VL2 :#0<=3<=4 donc 3 est dans VL2
            B[3] = True
        if 0 in self.VL3 :
            B[4] = True
        B[5] = self.VL1.__contains__(3)
        B[6] = self.VL3.__contains__(2)
        self.assertEqual(B[0], False)
        self.assertEqual(B[1], False)
        self.assertEqual(B[2], False)
        self.assertEqual(B[3], True)
        self.assertEqual(B[4], True)
        self.assertEqual(B[5], False)
        self.assertEqual(B[6], True)

    def test_eq(self) :
        """Méthode testant la méthode spéciale __eq__.

        Teste d'abord que si deux objets sont construits avec les mêmes arguments, ils sont égaux. Puis verifie que si un des arguments n'est pas identique __eq__ renvoie bien False.
        """
        VL5 = VerificateurListes([0, 4, Verificateur(float)], types=list, minimum=1)#mêmes arguments que self.VL2 
        eq1 = self.VL2.__eq__(VL5)
        self.assertEqual(eq1, True)
        VL6 = VerificateurListes([0, None, Verificateur(int, 0, 23)], [1, 2, Verificateur(int, 0,59)], types=tuple, maximum=4)
        eq2 = self.VL3.__eq__(VL6)#il manque un vérificateur dans la liste des vérificateurs
        self.assertEqual(eq2, False)
        VL6.append(3, None, VerificateurStr(1))#on ajoute le vérificateur manquant
        eq3 = False
        if VL6 == self.VL3 :
            eq3 = True
        self.assertEqual(eq3, False)#l'ordre des vérificateurs n'est pas le même
        self.VL3.sort()
        eq4 = False
        if VL6 == self.VL3 :
            eq4 = True
        self.assertEqual(eq4, True)#l'ordre est identique
        del VL6.maximum
        eq5 = False
        if VL6 == self.VL3 :
            eq5 = True
        self.assertEqual(eq5, False)#le maximum n'est pas présent

    def test__append(self) :
        """Méthode testant la méthode _append de la classe.

        Vérifie notamment l'objet modifié est conforme aux arguments passés en paramètres.
        """
        #premeier test
        self.VL1._append([0,10, Verificateur(bool)])
        self.assertEqualVL(self.VL1, liste_verificateurs=[[0,10, Verificateur(bool)]])
        #deuxième test 
        self.VL2._append([5, None, Verificateur()])
        liste_theorique = [[0, 4, Verificateur(float)],[5, None, Verificateur()]]
        self.assertEqual(self.VL2._liste_verificateurs, liste_theorique)

    def test__append_error(self) :
        """Méthode vérifiant que _append lève certaines erreurs.

        Vérifie notamment qu'il y a une erreur levée si l'argument n'est pas une liste, si l'un des deux identifiants n'est pas un nombre entier positif, si les deux indentifiants valent None, si un identifiant existe déjà dans la liste, si la liste n'a pas trop d'éléments.
        """
        #l'argument n'est pas une liste
        with self.assertRaises(TypeError) :
            self.VL1._append("c'est une blaque !")
        with self.assertRaises(TypeError) :
            self.VL1._append(33)
        #le premier élément de la liste n'est pas un nombre entier positif
        with self.assertRaises(TypeError) :
            self.VL1._append(["a",None,Verificateur()])
        with self.assertRaises(TypeError) :
            self.VL1._append([3.75, 3, Verificateur()])
        with self.assertRaises(ValueError) :
            self.VL1._append([-2, None, Verificateur()])
        #l'index 1 est identique à un autre argument de la liste
        with self.assertRaises(ValueError) :
            self.VL3._append([3, 5, Verificateur()])
        with self.assertRaises(ValueError) :
            self.VL2._append([3, None, Verificateur()])
        #le deuxième index n'est pas un nombre entier positif
        with self.assertRaises(TypeError) :
            self.VL1._append([1, "blaz", Verificateur()])
        #le deuxième index est identique à celui d'un autre argument de la liste
        self.VL2.append(50,60)
        with self.assertRaises(ValueError) :
            self.VL2._append([45, 51, Verificateur()])
        #aucun identifiant n'est précisé
        with self.assertRaises(ValueError) :
            self.VL1._append([None, None, Verificateur(str)])
        #liste avec trop d'éléments
        with self.assertRaises(ValueError) :
            self.VL1._append([3,4, Verificateur(), True])
    
    def test_append(self) :
        """Méthode testant la méthode append de la classe.

        Vérifie notamment l'objet modifié est conforme aux arguments passés en paramètres.
        """
        self.VL1.append(id2=3, verificateur=Verificateur(str))
        liste_theorique = [[3,None, Verificateur(str)]]
        self.assertEqual(self.VL1._liste_verificateurs, liste_theorique)
        self.VL1.append(0, verificateur=Verificateur(int))
        liste_theorique.append([0, None, Verificateur(int)])
        self.assertEqual(self.VL1._liste_verificateurs, liste_theorique)
        self.VL1.append(id1=4, id2=6)
        liste_theorique.append([4, 6, Verificateur()])
        self.assertEqual(self.VL1._liste_verificateurs, liste_theorique)

    def test_append_error(self) :
        """Méthode vérifiant que la méthode append lève certaines erreurs.

        Vérifie notamment qu'il y a une erreur levée si l'argument n'est pas une liste, si l'un des deux identifiants n'est pas un nombre entier positif, si les deux indentifiants valent None, si un identifiant existe déjà dans la liste.
        """
        #le premier index de la liste n'est pas un nombre entier positif
        with self.assertRaises(TypeError) :
            self.VL1.append("a", 3)
        with self.assertRaises(TypeError) :
            self.VL1.append(id1=3.75, verificateur=Verificateur())
        with self.assertRaises(ValueError) :
            self.VL1.append(-2, 2)
        #l'index 1 est identique à un autre argument de la liste
        with self.assertRaises(ValueError) :
            self.VL2.append(id1=0)
        #l'index 2 n'est pas un nombre entier positif
        with self.assertRaises(TypeError) :
            self.VL1.append(id2 = float)
        #l'index 2 est identique à celui d'un autre argument de la liste
        self.VL2.append(50,60)
        with self.assertRaises(ValueError) :
            self.VL2.append(45, 51, Verificateur())
        #aucun identifiant n'est précisé
        with self.assertRaises(ValueError) :
            self.VL1.append(verificateur=Verificateur(str))

    def test_sort(self) :
        """Cette méthode vérifie que la liste est bien triée.

        Vérifie notamment le tri par défaut, le tri par le deuxième index, et la réversibilité du tri.
        """
        #initialisation
        self.VL1.append(2,None)
        self.VL1.append(0, None)
        self.VL1.append(8, 20)
        self.VL1.append(7)
        self.VL1.append(3,5)
        self.VL1.append(1)
        
        #tri par défaut
        self.VL1.sort()
        self.assertEqual(self.VL1._liste_verificateurs, [[0, None, Verificateur()], [1, None, Verificateur()], [2, None, Verificateur()], [3, 5, Verificateur()], [7,None, Verificateur()], [8, 20, Verificateur()]])

        #tri inversé
        self.VL1.sort(reverse=True)
        self.assertEqual(self.VL1._liste_verificateurs, [[8, 20, Verificateur()],[7, None, Verificateur()], [3, 5, Verificateur()], [2, None,Verificateur()], [1, None, Verificateur()], [0, None, Verificateur()]])
    
    def test_clé(self) :
        """Méthode qui teste la méthode clé utilisée afin de trier l'objet.
        
        Vérifie que clé renvoie bien les bonnes valeurs.
        """
        retour1 = []
        for i in range(len(self.VL3._liste_verificateurs)) :
            retour1.append(self.VL3.clé(self.VL3._liste_verificateurs[i], 1, 0))
        retour_theorique1 = [0, 0, 2]
        self.assertEqual(retour1, retour_theorique1)
        retour2 = []
        for i in range(len(self.VL3._liste_verificateurs)) :
            retour2.append(self.VL3.clé(self.VL3._liste_verificateurs[i], 0))
        retour_theorique2 = [3, 0, 1]
        self.assertEqual(retour2, retour_theorique2)

    def test_controle_types(self) :
        """Cette méthode vérifie le fonctionnement de controle_types.

        Vérifie que lorsque le type du conteneur est correct la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque le type est incorrect une TypeError est levée.
        """
        obj_v = self.VL3.controle_types((20,14,23))#controle le type du conteneur
        self.assertEqual(obj_v, (20,14,23))
        self.VL2.controle_types([19, 30])
        #le conteneur n'est pas du bon type
        with self.assertRaises(TypeError) :
            self.VL2.controle_types({})

    def test_controle_types_conversion(self) :
        """Teste la méthode controle_types avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_types convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VL1.controle_types((5,7), conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, [5,7])
        obj_v2 = self.VL2.controle_types({"clé1":56, "clé2":78}, conversion=True)
        self.assertEqual(obj_v2, ["clé1", "clé2"])
        with self.assertRaises(TypeError) :
            self.VL1.controle_types(54, conversion=True)#impossible car 54 est un entier et donc on ne peut pas le convertir en liste (car non parcourable)

    def test_controle_types_item(self) :
        """Cette méthode vérifie le fonctionnement de controle_types_item.

        Vérifie d'abord que quand l'argument est correct, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque l'objet vérifié n'a pas le bon type une erreur TypeError soit levée.
        """
        #Le type est valide : pas de levée d'erreur
        obj_v = self.VL3.controle_types_item(0, 22)#l'heure doit être un entier entre 0 et 23
        self.assertEqual(obj_v, 22)
        self.VL2.controle_types_item(3, 55.2)#les éléments d'indice 0 à 4 doivent être des flottants
        #Le type n'est pas valide : on vérifie la levée d'erreur
        with self.assertRaises(TypeError) :
            self.VL3.controle_types_item(3, True)#les secondes doivent êtres des entiers
        with self.assertRaises(TypeError) :
            self.VL2.controle_types_item(0, "abc")#le premier éléments de la liste doit être un flottant

    def test_controle_types_item_erreur(self) :
        """Cette méthode vérifie que controle_types_item lève des erreurs.

        Vérifie que quand l'identifiant est incorrect (soit n'existe pas dans la liste des identifiants, soit vaut None), cette méthode lève bien une erreur.
        """
        #L'identifiant ne doit pas être None
        with self.assertRaises(ValueError) :
            self.VL2.controle_types_item(None, "abc")
        #L'identifiant doit être un nombre entier
        with self.assertRaises((ValueError, TypeError)) :
            self.VL2.controle_types_item([1], "abc")
        #L'identifant doit être dans la liste
        with self.assertRaises(ValueError) :
            self.VL2.controle_types_item(33, 25.1)

    def test_controle_types_item_conversion(self) :
        """Teste controle_types_item avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_types_item convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VL2.controle_types_item(1, 4, conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, 4.0)
        obj_v2 = self.VL2.controle_types_item(2, "56", conversion=True)#conversion en int
        self.assertEqual(obj_v2, 56)
        with self.assertRaises(TypeError) :
            self.VL3.controle_types_item(1, "douze", conversion=True)#impossible car 'douze' est écrit en toute lettre donc n'est pas convertible en int

    def test_controle_types_total(self) :
        """Cette méthode vérifie le fonctionnement de controle_types_total.

        Vérifie d'abord que quand les arguments sont corrects, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque un des arguments n'est pas valide une erreur soit levée.
        """
        #objets valides
        obj_v = self.VL3.controle_types_total((20,14,33))
        self.assertEqual(obj_v, (20, 14, 33))
        self.VL2.controle_types_total([12.5,15.6,11.33])
        #un des contenus n'est pas valide
        with self.assertRaises(TypeError) :
            self.VL3.controle_types_total((20,"14",33))
        with self.assertRaises(TypeError) :
            self.VL2.controle_types_total([12.5, 14.0,None])
        #le conteneur a un type invalide
        with self.assertRaises(TypeError) :
            self.VL2.controle_types_total((12.5, 14.0))
        with self.assertRaises(TypeError) :
            self.VL3.controle_types_total({"h":20,"min":25,"sec":36})

    def test_controle_types_total_conversion(self) :
        """Teste controle_types_total avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_types_total convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VL1.controle_types_total((5,7), conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, [5,7])
        obj_v2 = self.VL3.controle_types_total(["5", 56, "12", "GMT"], conversion=True)#conversion en int
        self.assertEqual(obj_v2, (5, 56, 12, "GMT"))
        with self.assertRaises(TypeError) :
            self.VL1.controle_types_total(5.4, conversion=True)#impossible car 5.4 est un flottant pas de conversion en liste possible
        with self.assertRaises(TypeError) :
            self.VL3.controle_types_total([5, 56,"douze"], conversion=True)#impossible car 'douze' est un nombre mais n'est pas écrit en chiffre donc il n'est pas convertible en int

    def test_controle_minimum(self) :
        """Cette méthode vérifie le fonctionnement de controle_minimum.

        Vérifie que lorsque la longueur du conteneur est correcte la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque le conteneur ne contient pas assez d'éléments une ValueError est levée.
        """
        obj_v = self.VL2.controle_minimum([12.25])#minimum=1 et ici il y a 1 élément dans la liste
        self.assertEqual(obj_v, [12.25])
        self.VL2.controle_minimum([12.25, 15.5])
        with self.assertRaises(ValueError) :
            self.VL2.controle_minimum([])#minimum=1 et ici il n'y a pas d'élément dans la liste
    
    def test_controle_maximum(self) :
        """Cette méthode vérifie le fonctionnement de controle_maximum.

        Vérifie que lorsque la longueur du conteneur est correcte la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque le conteneur contient trop d'éléments une ValueError est levée.
        """
        obj_v = self.VL3.controle_maximum((15,32))#len du tuple = 2<4
        self.assertEqual(obj_v, (15,32))
        self.VL3.controle_maximum((15, 33, 26))
        with self.assertRaises(ValueError) :
            self.VL3.controle_maximum((15, 56, 13, "GTM+1", True))#5 éléments = 1 de trop

    def test_controle_global(self) :
        """Cette méthode teste la méthode controle_global de la classe testée.

        Dans une première partie, cette méthode vérifie que lorsque args et kwargs sont valides aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque l'objet n'est pas valide, une erreur est bien levée.
        """
        #conteneurs du bon type avec la bonne longueur
        obj_v = self.VL2.controle_global(["a", "b"])
        self.assertEqual(obj_v, ["a", "b"])
        self.VL3.controle_global((5,12))
        #conteneur du mauvais type
        with self.assertRaises(TypeError) :
            self.VL2.controle_global("blabla")
        #conteneur trop court
        with self.assertRaises(ValueError) :
            self.VL2.controle_global([])
        #conteneur trop long
        with self.assertRaises(ValueError) :
            self.VL3.controle_global((15, 56, 13, "GTM+1", True))#5 éléments = 1 de trop

    def test_controle_global_conversion(self) :
        """Teste la méthode controle_global avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_global convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VL1.controle_global((5,7), conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, [5,7])
        obj_v2 = self.VL2.controle_global({"clé1":56, "clé2":78}, conversion=True)
        self.assertEqual(obj_v2, ["clé1", "clé2"])
        with self.assertRaises(TypeError) :
            self.VL1.controle_global(54, conversion=True)#impossible car 54 est un entier et donc on ne peut pas le convertir en liste (car non parcourable)

    def test_controle_global_item(self) :
        """Cette méthode vérifie le fonctionnement de controle_global_item.

        Vérifie d'abord que quand l'argument est correct, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque l'objet vérifié n'est pas valide une erreur soit levée.
        """
        #objet valides
        obj_v = self.VL3.controle_global_item(0, 9)#l'heure doit être un entier entre 0 et 23
        self.assertEqual(obj_v, 9)
        self.VL3.controle_global_item(3, "GTM+1")#lefuseau horaire doit être une chaine de caractères
        #objets qui ne sont pas valides
        with self.assertRaises((TypeError, ValueError)) :
            self.VL3.controle_global_item(1, "bala")#le type est incorrect
        with self.assertRaises((TypeError, ValueError)) :
            self.VL3.controle_global_item(2, -3)#-3 est inférieur au minimum autorisé
        with self.assertRaises((TypeError, ValueError)) :
            self.VL3.controle_global_item(0, 50)#50 supérieur à 23 (maximum autorisé)
        with self.assertRaises((TypeError, ValueError)) :
            self.VL2.controle_global_item(3, 50)#50 n'est pas un flottant (maximum autorisé)

    def test_controle_global_item_erreur(self) :
        """Cette méthode vérifie que controle_global lève des erreurs.

        Vérifie que quand l'identifiant est incorrect (soit n'existe pas dans la liste des identifiants, soit vaut None), cette méthode lève bien une erreur.
        """
        #L'identifiant ne doit pas être None
        with self.assertRaises(ValueError) :
            self.VL2.controle_global_item(None, "abc")
        #L'identifiant doit être un nombre entier
        with self.assertRaises((ValueError, TypeError)) :
            self.VL2.controle_global_item([1], "abc")
        #L'identifant doit être dans la liste
        with self.assertRaises(ValueError) :
            self.VL2.controle_global_item(33, "abc")

    def test_controle_global_item_conversion(self) :
        """Teste controle_global_item avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_global_item convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VL2.controle_global_item(1, 4, conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, 4.0)
        obj_v2 = self.VL2.controle_global_item(2, "56", conversion=True)#conversion en int
        self.assertEqual(obj_v2, 56)
        with self.assertRaises(TypeError) :
            self.VL3.controle_global_item(1, "douze", conversion=True)#impossible car 'douze' est écrit en toute lettre donc n'est pas convertible en int

    def test_controle_total(self) :
        """Cette méthode vérifie le fonctionnement de controle_total.

        Vérifie d'abord que quand les arguments sont corrects, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque un des arguments n'est pas valide une erreur soit levée.
        """
        #objets valides
        obj_v1 = self.VL3.controle_types_total((20,14,33))#obj_v1 pour objet valide n°1
        self.assertEqual(obj_v1, (20,14,33))
        self.VL3.controle_types_total((9, 25, 56))
        obj_v2 = self.VL2.controle_types_total([12.5,15.6,11.33])
        self.assertEqual(obj_v2, [12.5, 15.6,11.33])
        #conteneur du mauvais type
        with self.assertRaises(TypeError) :
            self.VL2.controle_total([20,14,33])#le conteneur doit être un tuple
        #conteneur trop court
        with self.assertRaises(ValueError) :
            self.VL2.controle_total([])
        #conteneur trop long
        with self.assertRaises(ValueError) :
            self.VL3.controle_total((15, 56, 13, "GTM+1", True))
        #un des éléments contenus est d'un type incorrect
        with self.assertRaises((TypeError, ValueError)) :
            self.VL2.controle_total([15.0,14])#les éléments contenus doivent être des flottants
        #un des éléments contenus est inférieur au minimum
        with self.assertRaises((TypeError, ValueError)) :
            self.VL3.controle_total((2, -1,14))#-1 est inférieur à 0 (le minimum)
        #un des éléments contenus est supérieur au maximum
        with self.assertRaises((TypeError, ValueError)) :
            self.VL3.controle_total((25, 1,14))#25 est supérieur à 23 (le maximum)

    def test_controle_total_conversion(self) :
        """Teste la méthode controle_total avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_total convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VL1.controle_total((5,7), conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, [5,7])
        obj_v2 = self.VL3.controle_total(["5", 56, "12", "GMT"], conversion=True)#conversion en int
        self.assertEqual(obj_v2, (5, 56, 12, "GMT"))
        with self.assertRaises(TypeError) :
            self.VL1.controle_total(5.4, conversion=True)#impossible car 54 est un flottant pas de conversion en liste possible
        with self.assertRaises(TypeError) :
            self.VL3.controle_total([5, 56,"douze"], conversion=True)#impossible car 'douze' est un nombre mais n'est pas écrit en chiffre donc il n'est pas convertible en int

    def test_get_liste_verificateurs(self) :
        """Teste l'affichage de l'attribut liste_verificateurs."""
        get_theorique = """   Identifiant 1       Identifiant 2        Vérificateur    \n         3                  None        ◄minimum:1, maximum:None, regex:''►\n         0                  None        ◄types:<class 'int'>, minimum:0, maximum:23►\n         1                   2          ◄types:<class 'int'>, minimum:0, maximum:59►\n"""
        self.assertEqual(self.VL3.liste_verificateurs, get_theorique)

    def test_get_types(self) :
        """Teste l'affichage de l'attribut types."""
        types = self.VL2.types
        self.assertEqual(types, list)
    
    def test_set_types(self) :
        """Teste la modification de l'attribut types."""
        self.VL2.types = tuple
        self.assertEqualVL(self.VL2, tuple,1, None, [[0, 4, Verificateur(float)]])
    
    def test_del_types(self) :
        """Teste la suppression de l'attribut types."""
        del self.VL2.types
        self.assertEqualVL(self.VL2, None, 1, None, [[0, 4, Verificateur(float)]])

    def test_get_minimum(self) :
        """Teste l'affichage de l'attribut minimum."""
        minimum = self.VL2.minimum
        self.assertEqual(minimum, 1)
 
    def test_set_minimum(self) :
        """Teste la modification de l'attribut minimum."""
        self.VL2.minimum = 2
        self.assertEqualVL(self.VL2, list, 2, None, [[0, 4, Verificateur(float)]])
    
    def test_set_minimum_error(self) :
        """Vérifie que set_minimum lève certaines erreurs.

        Vérifie notamment que des erreurs sont levées lorsque nouveau_minimum n'est pas un nombre entier positif (ou nul) et qu'il est supérieur au maximum.
        """
        with self.assertRaises(TypeError) :
            self.VL1.minimum = "bla"#n'est pas un entier
            self.assertEqual(self.VL1, VerificateurListes())
        with self.assertRaises(ValueError) :
            self.VL1.set_minimum(-2)#n'est pas un entier positif
            self.assertEqual(self.VL1, VerificateurListes())
        with self.assertRaises(ValueError) :
            self.VL3.minimum = 5#minimum supérieur au maximum (4)
            self.assertEqualVL(self.VL3, tuple, None, 3, [[3, None, Verificateur(str)], [0, None, Verificateur(int, 0, 23)], [1, 2, Verificateur(int, 0, 59)]])

    def test_del_minimum(self) :
        """Teste la suppression de l'attribut minimum."""
        del self.VL2.minimum
        self.assertEqualVL(self.VL2, list, 0, None, [[0, 4, Verificateur(float)]])

    def test_get_maximum(self) :
        """Teste l'affichage de l'attribut maximum."""
        maximum = self.VL3.maximum
        self.assertEqual(maximum, 4)

    def test_set_maximum(self) :
        """Teste la modification de l'attribut maximum."""
        self.VL2.maximum = 4
        self.assertEqualVL(self.VL2, list, 1, 4, [[0, 4, Verificateur(float)]])

    def test_set_maximum_error(self) :
        """Vérifie que set_maximum lève certaines erreurs.

        Vérifie notamment que des erreurs sont levées lorsque nouveau_maximum n'est pas un nombre entier positif (ou nul) et qu'il est inférieur au minimum.
        """
        with self.assertRaises(TypeError) :
            self.VL1.maximum = 0.3#n'est pas un entier
        self.assertEqual(self.VL1, VerificateurListes())
        with self.assertRaises(ValueError) :
            self.VL1.set_maximum(-2)#n'est pas un entier positif
        self.assertEqual(self.VL1, VerificateurListes())
        with self.assertRaises(ValueError) :
            self.VL2.maximum = 0#maximum inférieur au minimum (1)
        self.assertEqualVL(self.VL2, list, 1, None, [[0, 4, Verificateur(float)]])

    def test_del_maximum(self) :
        """Teste la suppression de l'attribut maximum."""
        del self.VL3.maximum
        self.assertEqualVL(self.VL3, tuple, 0, None, [[3, None, VerificateurStr(1)], [0, None, Verificateur(int, 0, 23)], [1, 2, Verificateur(int, 0, 59)]])
    
    def test_conversion(self) :
        """Teste la méthode _conversion.
         
        Vérifie que la méthode convertit bien un objet de type invalide en un objet de type valide, lorsque c'est possible.
        """
        obj_v1 = self.VL3._conversion([5, '15', 36, "GMT"])
        self.assertEqual(obj_v1, (5, '15', 36, "GMT"))
        obj_v2 = self.VL1._conversion("abcde")
        self.assertEqual(obj_v2, ["a","b","c","d","e"])

if __name__ == "__main__" :
    unittest.main()