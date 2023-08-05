"""Ce module teste avec unittest la classe VerificateurArguments."""

import unittest
import os
import sys

#On change le dossier de travail (cwd) pour pouvoir appeler les fichiers via des chemins relatifs
os.chdir(os.path.dirname(__file__))#On change le dossier de travail en appellant le nom du dossier qui contient ce fichier (le dossier tests)
os.chdir("..")#On rechange le dossier de travail en prenant le dossier parent du dossier tests (le dossier outils_de_controles)
sys.path.append(os.getcwd())#ligne nécessaire à l'importation du module verificateur_arguments

from outils_de_controles.verificateur_arguments import * 
from outils_de_controles.verificateur import *

class TestVerificateurArguments(unittest.TestCase) :
    """Classe qui teste la classe VerificateurArguments.

    Vérifie que la classe VerificateurArguments du package outils_de_controles soit conforme aux spécifications. (Création, affichage, vérification des arguments, ...).
    """

    def assertEqualVA(self, VA, types=(list, tuple, dict), minimum=0, maximum=None,liste_verificateurs=[]) :
        """Méthode vérifiant si deux objets VerificateurArguments sont égaux.

        Cette methode compare chaque attribut à la valeur fournie.
        """
        if VA.types == types and VA.minimum == minimum and VA.maximum == maximum and VA._liste_verificateurs == liste_verificateurs :
            return self.assertEqual(0,0)#l'objet verificateur est égal à la valeur théorique
        else :
            VA_theorique = VerificateurArguments(types=types, minimum=minimum, maximum=maximum)
            for verif in liste_verificateurs :
                VA_theorique._append(verif)
            raise AssertionError(repr(VA) + " != " + repr(VA_theorique))

    def setUp(self) :
        """Cette méthode prépare l'exécution des tests.
        
        Cette méthode crée pour cela des objets VerificateurArguments.
        """
        #création d'un objet vide
        self.VA1 = VerificateurArguments()
        #création d'un objet avec une liste
        self.VA2 = VerificateurArguments([0, "a", Verificateur(int)], types=(list, dict), minimum=1)
        #création d'un objet avec trois listes
        self.VA3 = VerificateurArguments([None,"Nombre de notes", Verificateur(int, 0)], [1,"Bon élève", Verificateur(bool)], [0, "Note maximale", Verificateur(float, 0, 20)], maximum=3)

    def test_init(self) :
        """Méthode testant l'initialisation des objets VerificateurArguments.

        Vérifie que l'objet créé est conforme aux arguments passés en paramètres.
        """
        #objet vide
        self.assertEqualVA(self.VA1)
        self.assertEqualVA(self.VA2, types=(list, dict), minimum=1, liste_verificateurs=[[0,"a", Verificateur(int)]])
        self.assertEqualVA(self.VA3, maximum=3, liste_verificateurs=[[None,"Nombre de notes", Verificateur(int, 0)],[1,"Bon élève", Verificateur(bool)], [0, "Note maximale", Verificateur(float, 0, 20)]])

    def test_init_erreur(self) :
        """Méthode vérifiant que __init__ lève certaines erreurs.

        Vérifie notamment qu'il y a une erreur levée si un des arguments n'est pas une liste, si le premier élément de la liste n'est pas un nombre entier positif (ou None), si le deuxième éléments de la liste n'est pas une chaine de caractère (ou None), si les deux indentifiants valent None, si un identifiant existe déjà dans la liste. Vérifie aussi que maximum est supérieur ou égal à minimum et que ces deux attributs soient des entiers positifs.
        """
        #l'argument non nommé n'est pas une liste
        with self.assertRaises(TypeError) :
            VAe = VerificateurArguments("c'est une blaque !")
        #l'ordre de définition n'est pas un nombre entier positif
        with self.assertRaises(TypeError) :
            VAe = VerificateurArguments(["a", None, Verificateur()])
        #l'ordre de définition n'est pas un nombre entier positif
        with self.assertRaises(ValueError) :
            VAe = VerificateurArguments([-2, None, Verificateur()])
        #l'ordre de définition est identique à un autre argument de la liste
        with self.assertRaises(ValueError) :
            VAe = VerificateurArguments([0, "abc"], [0, "def"])
        #le nom n'est pas une chaine
        with self.assertRaises(TypeError) :
            VAe = VerificateurArguments([1, "n", Verificateur(int)], [2, 23, Verificateur()])
            self.assertEqual(VAe._liste_verificateurs, [[1,"n", Verificateur(int)]])
        #le nom de l'argument est identique à celui d'un autre argument de la liste
        with self.assertRaises(ValueError) :
            VAe = VerificateurArguments([0, "deja_pris", Verificateur()], [1,"deja_pris", Verificateur()])
        #aucun identifiant n'est précisé
        with self.assertRaises(ValueError) :
            VAe = VerificateurArguments([None, None, Verificateur(int)])
        #minimum n'est pas un entier
        with self.assertRaises(TypeError) :
            VAe = VerificateurArguments(minimum=2.5)
        #maximum n'est pas un entier
        with self.assertRaises(TypeError) :
            VAe = VerificateurArguments(maximum="bla")
        #minimum n'est pas un nombre positif
        with self.assertRaises(ValueError) :
            VAe = VerificateurArguments(minimum=-2)
        #maximum est inférieur au minimum
        with self.assertRaises(ValueError) :
            VAe = VerificateurArguments(minimum=10, maximum=5)

    def test_str(self) :
        """Méthode qui teste la méthode spéciale __str__.
        
        Vérifie que l'affichage des objets de la classe VerificateurArguments est correct (présentation sous forme de tableau ...).
        """
        str_theorique = """◄types:(<class 'list'>, <class 'tuple'>, <class 'dict'>), minimum:0, maximum:3\n\n   Identifiant 1       Identifiant 2        Vérificateur    \n        None          Nombre de notes   ◄types:<class 'int'>, minimum:0, maximum:None►\n         1               Bon élève      ◄types:<class 'bool'>, minimum:None, maximum:None►\n         0             Note maximale    ◄types:<class 'float'>, minimum:0, maximum:20►\n►\n"""
        self.assertEqual(str(self.VA3), str_theorique)

    def test_repr(self) :
        """Cette méthode teste la méthode spéciale __repr__."""
        repr_theorique = """outils_de_controles.VerificateurArguments([None, 'Nombre de notes', outils_de_controles.Verificateur(types=<class 'int'>, minimum=0, maximum=None)], [1, 'Bon élève', outils_de_controles.Verificateur(types=<class 'bool'>, minimum=None, maximum=None)], [0, 'Note maximale', outils_de_controles.Verificateur(types=<class 'float'>, minimum=0, maximum=20)], types=(<class 'list'>, <class 'tuple'>, <class 'dict'>), minimum=0, maximum=3)"""
        self.assertEqual(repr(self.VA3), repr_theorique)

    def test__id_verificateur(self) :
        """Méthode vérifiant le bon fonctionnement de _id_verificateur.

        Vérifie que _id_verificateur renvoie bien le vérificateur correspondant à l'identifiant.
        """
        V1 = self.VA3._id_verificateur(1)
        V1_theorique = Verificateur(bool)
        self.assertEqual(V1, V1_theorique)
        V2 = self.VA3._id_verificateur("Note maximale")
        V2_theorique = Verificateur(float, 0, 20)
        self.assertEqual(V2, V2_theorique)

    def test_id_verificateur_error(self) :
        """Vérifie que _id_verificateur lève des erreurs.

        Vérifie que lorsque l'identifiant passé en paramètre n'existe pas, une erreur est levée.
        """
        with self.assertRaises(ValueError) :
            Ve = self.VA3._id_verificateur("blabla")
    
    def test_contains(self) :
        """Méthode vérifiant le bon fonctionnement de __contains__.

        Vérifie que la recherche d'argument dans la liste avec le mot clé in, s'effectue correctement. (recherche d'entiers ou de chaines).
        """
        B = [False for i in range(7)]
        if 1 in self.VA1 :
            B[0] = True #booléen n°1
        if "prenom" in self.VA2 : 
            B[1] = True
        if list in self.VA3 :
            B[2] = True
        if "Bon élève" in self.VA3 :
            B[3] = True
        if 0 in self.VA2 :
            B[4] = True
        B[5] = self.VA1.__contains__(3)
        B[6] = self.VA2.__contains__('a')
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
        VA5 = VerificateurArguments([0, "a", Verificateur(int)], types=(list, dict), minimum=1)#mêmes arguments que self.VA2 
        eq1 = self.VA2.__eq__(VA5)
        self.assertEqual(eq1, True)
        VA6 = VerificateurArguments([None,"Nombre de notes", Verificateur(int, 0)], [1,"Bon élève", Verificateur(bool)], maximum=3)
        eq2 = self.VA3.__eq__(VA6)#il manque un vérificateur dans la liste des vérificateurs
        self.assertEqual(eq2, False)
        VA6.append(0, "Note maximale", Verificateur(float, 0, 20))#on ajoute le vérificateur manquant
        eq3 = False
        if VA6 == self.VA3 :
            eq3 = True
        self.assertEqual(eq3, True)
        del VA6.maximum
        eq4 = False
        if VA6 == self.VA3 :
            eq4 = True
        self.assertEqual(eq4, False)#le maximum n'est pas présent

    def test__append(self) :
        """Méthode testant la méthode _append de la classe.

        Vérifie notamment l'objet modifié est conforme aux arguments passés en paramètres.
        """
        #premeier test
        self.VA1._append([0,"a", Verificateur(str)])
        self.assertEqual(self.VA1._liste_verificateurs, [[0,"a", Verificateur(str)]])
        #deuxième test 
        self.VA2._append([1,"abc", Verificateur()])
        liste_theorique = [[0, 'a', Verificateur(int)],[1,"abc", Verificateur()]]
        self.assertEqual(self.VA2._liste_verificateurs, liste_theorique)
        self.VA2._append([None, "année de naissance", Verificateur(int)])
        liste_theorique.append([None, "année de naissance", Verificateur(int)])
        self.assertEqual(self.VA2._liste_verificateurs, liste_theorique)

    def test__append_error(self) :
        """Méthode vérifiant que _append lève certaines erreurs.

        Vérifie notamment qu'il y a une erreur levée si l'argument n'est pas une liste, si le premier élément de la liste n'est pas un nombre entier positif, si le deuxième éléments de la liste n'est pas une chaine de caractère, si les deux indentifiants valent None, si un identifiant existe déjà dans la liste, si la liste n'a pas trop d'éléments.
        """
        #l'argument n'est pas une liste
        with self.assertRaises(TypeError) :
            self.VA1._append("c'est une blaque !")
        with self.assertRaises(TypeError) :
            self.VA1._append(33)
        #le premier élément de la liste n'est pas un nombre entier positif
        with self.assertRaises(TypeError) :
            self.VA1._append(["a","",Verificateur()])
        with self.assertRaises(TypeError) :
            self.VA1._append([3.75, "a", Verificateur()])
        with self.assertRaises(ValueError) :
            self.VA1._append([-2, "a", Verificateur()])
        #l'ordre de définition est identique à un autre argument de la liste
        with self.assertRaises(ValueError) :
            self.VA2._append([0, "abc", Verificateur()])
        #le deuxième élément de la liste n'est pas une chaine
        with self.assertRaises(TypeError) :
            self.VA1._append([1, 23, Verificateur()])
        #le nom de l'argument est identique à celui d'un autre argument de la liste
        with self.assertRaises(ValueError) :
            self.VA3._append([2, "Bon élève", Verificateur()])
        #aucun identifiant n'est précisé (-1 et "")
        with self.assertRaises(ValueError) :
            self.VA1._append([None, None, Verificateur(str)])
        with self.assertRaises(ValueError) :
            self.VA1._append([None, "", Verificateur(str)])
        #liste avec trop d'éléments
        with self.assertRaises(ValueError) :
            self.VA1._append([3,"miam", Verificateur(), True])
    
    def test_append(self) :
        """Méthode testant la méthode append de la classe.

        Vérifie notamment l'objet modifié est conforme aux arguments passés en paramètres.
        """
        self.VA1.append(id2="a", verificateur=Verificateur(str))
        liste_theorique = [[None,"a", Verificateur(str)]]
        self.assertEqual(self.VA1._liste_verificateurs, liste_theorique)
        self.VA1.append(0, verificateur=Verificateur(int))
        liste_theorique.append([0, None, Verificateur(int)])
        self.assertEqual(self.VA1._liste_verificateurs, liste_theorique)
        self.VA1.append(id1=3)
        liste_theorique.append([3, None, Verificateur()])
        self.assertEqual(self.VA1._liste_verificateurs, liste_theorique)

    def test_append_error(self) :
        """Méthode vérifiant que la méthode append lève certaines erreurs.

        Vérifie notamment qu'il y a une erreur levée si l'argument n'est pas une liste, si le premier élément de la liste n'est pas un nombre entier positif, si le deuxième éléments de la liste n'est pas une chaine de caractère, si les deux indentifiants valent None, si un identifiant existe déjà dans la liste.
        """
        #le premier élément de la liste n'est pas un nombre entier positif
        with self.assertRaises(TypeError) :
            self.VA1.append("a","")
        with self.assertRaises(TypeError) :
            self.VA1.append(id1=3.75, id2="a", verificateur=Verificateur())
        with self.assertRaises(ValueError) :
            self.VA1.append(-2, "a")
        #l'ordre de définition est identique à un autre argument de la liste
        with self.assertRaises(ValueError) :
            self.VA2.append(id1=0, id2="abc")
        #le deuxième élément de la liste n'est pas une chaine
        with self.assertRaises(TypeError) :
            self.VA1.append(id2 = True)
        #le nom de l'argument est identique à celui d'un autre argument de la liste
        with self.assertRaises(ValueError) :
            self.VA3.append(2, "Bon élève")
        #aucun identifiant n'est précisé (-1 et "")
        with self.assertRaises(ValueError) :
            self.VA1.append(verificateur=Verificateur(str))
        with self.assertRaises(ValueError) :
            self.VA1.append(id2="", verificateur=Verificateur(str))

    def test_sort(self) :
        """Cette méthode vérifie que la liste est bien triée.

        Vérifie notamment le tri par défaut, le tri par nom, celui par ordre de définition, et la réversibilité du tri.
        """
        #initialisation
        self.VA1.append(2,"a")
        self.VA1.append(0, "b")
        self.VA1.append(3)
        self.VA1.append(id2="e")
        self.VA1.append(id2="c")
        self.VA1.append(1, "zb")
        
        #tri par défaut
        self.VA1.sort()
        self.assertEqual(self.VA1._liste_verificateurs, [[None, "c", Verificateur()], [None, "e", Verificateur()], [0, "b", Verificateur()], [1, "zb", Verificateur()], [2,"a", Verificateur()], [3, None, Verificateur()]])

        #tri inversé
        self.VA1.sort(reverse=True)
        self.assertEqual(self.VA1._liste_verificateurs, [[3, None, Verificateur()],[2,"a", Verificateur()], [1, "zb", Verificateur()], [0, "b",Verificateur()], [None, "e", Verificateur()], [None, "c", Verificateur()]])

        #tri par ordre de définition, avec les arguments nommés (sans ordre de définition) à la fin
        self.VA1.sort(key= lambda colonne:self.VA1.clé(colonne,0, 500))
        self.assertEqual(self.VA1._liste_verificateurs, [[0, "b", Verificateur()], [1, "zb", Verificateur()], [2,"a", Verificateur()], [3, None, Verificateur()], [None, "e", Verificateur()], [None, "c", Verificateur()]])

        #tri par nom
        self.VA1.sort(key= lambda colonne:self.VA1.clé(colonne, 1, ""))
        self.assertEqual(self.VA1._liste_verificateurs, [[3, None, Verificateur()], [2,"a", Verificateur()], [0, "b", Verificateur()], [None, "c", Verificateur()], [None, "e", Verificateur()], [1, "zb", Verificateur()]])
    
    def test_clé(self) :
        """Méthode qui teste la méthode clé utilisée afin de trier l'objet.
        
        Vérifie que clé renvoie bien les bonnes valeurs."""
        retour1 = []
        for i in range(len(self.VA3._liste_verificateurs)) :
            retour1.append(self.VA3.clé(self.VA3._liste_verificateurs[i], 0, -1))
        retour_theorique1 = [-1, 1, 0]
        self.assertEqual(retour1, retour_theorique1)
        retour2 = []
        for i in range(len(self.VA3._liste_verificateurs)) :
            retour2.append(self.VA3.clé(self.VA3._liste_verificateurs[i], 1))
        retour_theorique2 = ["Nombre de notes", "Bon élève", "Note maximale"]
        self.assertEqual(retour2, retour_theorique2)

    def test_controle_types(self) :
        """Cette méthode vérifie le fonctionnement de controle_types.

        Vérifie que lorsque le type du conteneur est correct la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque le type est incorrect une TypeError est levée.
        """
        args_v, kwargs_v = self.VA2.controle_types(["a"],{})#controle le type du conteneur
        self.assertEqual(args_v, ["a"])
        self.assertEqual(kwargs_v, {})
        self.VA1.controle_types([],{"sep":"\n"})
        #args n'est pas du bon type
        with self.assertRaises(TypeError) :
            self.VA2.controle_types("blabla",{})
        #kwargs n'est pas du bon type
        with self.assertRaises(TypeError) :
            self.VA2.controle_types([], -2)

    def test_controle_types_conversion(self) :
        """Teste la méthode controle_types avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_types convertit au besoin les objets de types incorects.
        """
        #objets valides
        args_v1, kwargs_v1 = self.VA2.controle_types("56", conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(args_v1, ["5","6"])
        self.assertEqual(kwargs_v1, {})
        args_v2, kwargs_v2 = self.VA2.controle_types((5,6), [], conversion=True)#conversion en int
        self.assertEqual(args_v2, [5,6])
        self.assertEqual(kwargs_v2, {})
        with self.assertRaises(TypeError) :
            self.VA1.controle_types(5.4, conversion=True)#impossible car 5 est un flottant et donc n'est pas parcourable : la conversion en liste est impossible

    def test_controle_types_item(self) :
        """Cette méthode vérifie le fonctionnement de controle_types_item.

        Vérifie d'abord que quand l'argument est correct, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque l'objet vérifié n'a pas le bon type une erreur TypeError soit levée.
        """
        #Le type est valide : pas de levée d'erreur
        obj_v = self.VA3.controle_types_item("Bon élève", True)#le nom doit être une chaine
        self.assertEqual(obj_v, True)
        self.VA2.controle_types_item(0, 55)#le premier argument doit être un nombre entier
        #Le type n'est pas valide : on vérifie la levée d'erreur
        with self.assertRaises(TypeError) :
            self.VA3.controle_types_item("Note maximale", True)#la note doit être un flottant
        with self.assertRaises(TypeError) :
            self.VA3.controle_types_item(1, "abc")#le premier argument doit être un booléen

    def test_controle_types_item_erreur(self) :
        """Cette méthode vérifie que controle_types_item lève des erreurs.

        Vérifie que quand l'identifiant est incorrect (soit n'existe pas dans la liste des identifiants, soit vaut None), cette méthode lève bien une erreur.
        """
        #L'identifiant ne doit pas être None
        with self.assertRaises(ValueError) :
            self.VA2.controle_types_item(None, "abc")
        #L'identifiant doit être un nombre entier ou une chaine
        with self.assertRaises((ValueError, TypeError)) :
            self.VA2.controle_types_item([1], "abc")
        #L'identifant doit être dans la liste
        with self.assertRaises(ValueError) :
            self.VA2.controle_types_item(33, "abc")
        with self.assertRaises(ValueError) :
            self.VA3.controle_types_item("zrt", "abc")

    def test_controle_types_item_conversion(self) :
        """Teste controle_types_item avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_types_item convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VA2.controle_types_item(0, "4", conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, 4)
        obj_v2 = self.VA3.controle_types_item("Bon élève", 0, conversion=True)#conversion en bool
        self.assertEqual(obj_v2, False)
        with self.assertRaises(TypeError) :
            self.VA3.controle_types_item(0, "douze", conversion=True)#impossible car 'douze' est écrit en toute lettre donc n'est pas convertible en float

    def test_controle_types_total(self) :
        """Cette méthode vérifie le fonctionnement de controle_types_total.

        Vérifie d'abord que quand les arguments sont corrects, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque un des arguments n'est pas valide une erreur soit levée.
        """
        #arguments valides
        args1 = [19.2, True]
        kwargs1 = {}
        args_v, kwargs_v = self.VA3.controle_types_total(args1, kwargs1)
        self.assertEqual(args_v, args1)
        self.assertEqual(kwargs_v, kwargs1)

        args2 = [12.3]
        kwargs2 = {"Bon élève":False, "Nombre de notes":4}
        self.VA3.controle_types_total(args2, kwargs2)
        #un des arguments n'est pas valide
        args3 = ["bla"]
        with self.assertRaises(TypeError) :
            self.VA3.controle_types_total(args3, kwargs2)
        kwargs3 = {"Bon élève":"oui", "Nombre de notes":4}
        with self.assertRaises(TypeError) :
            self.VA3.controle_types_total(args2, kwargs3)
        #args et kwargs du mauvais type
        self.VA1.type = (list, dict)
        with self.assertRaises(TypeError) :
            self.VA2.controle_types_total("balbla",{})
        with self.assertRaises(TypeError) :
            self.VA2.controle_types_total([3], 2)

    def test_controle_types_total_conversion(self) :
        """Teste controle_types_total avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_types_total convertit au besoin les objets de types incorects.
        """
        #objets valides
        self.VA2.append(1, "b", Verificateur(int))
        args_v1, kwargs_v1 = self.VA2.controle_types_total("57", conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(args_v1, [5,7])
        self.assertEqual(kwargs_v1, {})
        args_v2, kwargs_v2 = self.VA3.controle_types_total((16, 1), {"Nombre de notes":2.0},  conversion=True)#conversion du tuple en liste, de 16 (int) en float et de 1 (int) en bool et de 2.0 (float) en int
        self.assertEqual(args_v2, [16.0, True])
        self.assertEqual(kwargs_v2, {"Nombre de notes":2})
        with self.assertRaises(TypeError) :
            self.VA1.controle_types_total(5.4, conversion=True)#impossible car 5.4 est un flottant pas de conversion en liste possible
        with self.assertRaises(TypeError) :
            self.VA3.controle_types_total(["douze"], conversion=True)#impossible car 'douze' est un nombre mais n'est pas écrit en chiffre donc il n'est pas convertible en int

    def test_controle_minimum(self) :
        """Cette méthode vérifie le fonctionnement de controle_minimum.

        Vérifie que lorsque la longueur du conteneur est correcte la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque le conteneur ne contient pas assez d'éléments une ValueError est levée.
        """
        args_v, kwargs_v = self.VA2.controle_minimum([2], {})#minimum=1 et ici il y a 1 élément dans la liste
        self.assertEqual(args_v, [2])
        self.assertEqual(kwargs_v, {})
        self.VA2.controle_minimum([], {"sep":"\n"})#minimum=1 et ici il y a 1 élément dans le dictionnaire
        with self.assertRaises(ValueError) :
            self.VA2.controle_minimum([])#minimum=1 et ici il n'y a pas d'élément dans la liste
    
    def test_controle_maximum(self) :
        """Cette méthode vérifie le fonctionnement de controle_maximum.

        Vérifie que lorsque la longueur du conteneur est correcte la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque le conteneur contient trop d'éléments une ValueError est levée.
        """
        args_v, kwargs_v = self.VA3.controle_maximum([15.5], {})#len de la liste = 1<3
        self.assertEqual(args_v, [15.5])
        self.assertEqual(kwargs_v, {})
        self.VA3.controle_maximum([15.5], {"sep":"\n"})#len de la liste = 1<3
        with self.assertRaises(ValueError) :
            self.VA3.controle_maximum([15.5, True, 3], {"appréciation": "Travail régulier"})#4 éléments = 1 de trop

    def test_controle_global(self) :
        """Cette méthode teste la méthode controle_global de la classe testée.

        Dans une première partie, cette méthode vérifie que lorsque args et kwargs sont valides aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque l'objet n'est pas valide, une erreur est bien levée.
        """
        #conteneurs du bon type avec la bonne longueur
        args_v, kwargs_v = self.VA2.controle_global(["a", "b"],{"sep":"\n"})
        self.assertEqual(args_v, ["a","b"])
        self.assertEqual(kwargs_v, {"sep":"\n"})
        self.VA3.controle_global([], {"Nombre de notes":5})
        #conteneur du mauvais type
        with self.assertRaises(TypeError) :
            self.VA2.controle_global("blabla")
        #conteneur trop court
        with self.assertRaises(ValueError) :
            self.VA2.controle_global([],{})
        #conteneur trop long
        with self.assertRaises(ValueError) :
            self.VA3.controle_global(["blabla","n", 3],{"appréciation":"Travail sérieux."})

    def test_controle_global_conversion(self) :
        """Teste la méthode controle_global avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_global convertit au besoin les objets de types incorects.
        """
        #objets valides
        args_v1, kwargs_v1 = self.VA2.controle_global("56", conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(args_v1, ["5","6"])
        self.assertEqual(kwargs_v1, {})
        args_v2, kwargs_v2 = self.VA2.controle_global((5,6), [], conversion=True)#conversion en int
        self.assertEqual(args_v2, [5,6])
        self.assertEqual(kwargs_v2, {})
        with self.assertRaises(TypeError) :
            self.VA1.controle_global(5.4, conversion=True)#impossible car 5 est un flottant et donc n'est pas parcourable : la conversion en liste est impossible

    def test_controle_global_item(self) :
        """Cette méthode vérifie le fonctionnement de controle_global_item.

        Vérifie d'abord que quand l'argument est correct, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque l'objet vérifié n'est pas valide une erreur soit levée.
        """
        #objet valides
        obj_v = self.VA3.controle_global_item(0, 15.5)#la note (premier argument) doit être un flottant
        self.assertEqual(obj_v, 15.5)
        self.VA3.controle_global_item("Nombre de notes", 55)#le nombre de notes doit être un nombre entier positif
        #objets qui ne sont pas valides
        with self.assertRaises((TypeError, ValueError)) :
            self.VA3.controle_global_item("Nombre de notes", "bala")#le type est incorrect
        with self.assertRaises((TypeError, ValueError)) :
            self.VA3.controle_global_item("Nombre de notes", -3)#-3 est inférieur au minimum autorisé
        with self.assertRaises((TypeError, ValueError)) :
            self.VA3.controle_global_item(0, 36.0)#36 supérieur à 20 (maximum autorisé)

    def test_controle_global_item_erreur(self) :
        """Cette méthode vérifie que controle_global lève des erreurs.

        Vérifie que quand l'identifiant est incorrect (soit n'existe pas dans la liste des identifiants, soit vaut None), cette méthode lève bien une erreur.
        """
        #L'identifiant ne doit pas être None
        with self.assertRaises(ValueError) :
            self.VA2.controle_global_item(None, "abc")
        #L'identifiant doit être un nombre entier ou une chaine
        with self.assertRaises((ValueError, TypeError)) :
            self.VA2.controle_global_item([1], "abc")
        #L'identifant doit être dans la liste
        with self.assertRaises(ValueError) :
            self.VA2.controle_global_item(33, "abc")
        with self.assertRaises(ValueError) :
            self.VA3.controle_global_item("zrt", "abc")

    def test_controle_global_item_conversion(self) :
        """Teste controle_global_item avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_global_item convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VA2.controle_global_item(0, "4", conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, 4)
        obj_v2 = self.VA3.controle_global_item("Bon élève", 0, conversion=True)#conversion en bool
        self.assertEqual(obj_v2, False)
        with self.assertRaises(TypeError) :
            self.VA3.controle_global_item(0, "douze", conversion=True)#impossible car 'douze' est écrit en toute lettre donc n'est pas convertible en float

    def test_controle_total(self) :
        """Cette méthode vérifie le fonctionnement de controle_total.

        Vérifie d'abord que quand les arguments sont corrects, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque un des arguments n'est pas valide une erreur soit levée.
        """
        #arguments valides
        args1 = [19.2, True]
        kwargs1 = {}
        args_v, kwargs_v = self.VA3.controle_total(args1, kwargs1)
        self.assertEqual(args_v, args1)
        self.assertEqual(kwargs_v, kwargs1)

        args2 = [12.3]
        kwargs2 = {"Bon élève":False, "Nombre de notes":4}
        self.VA3.controle_total(args2, kwargs2)
        args3 = [24.1]
        with self.assertRaises((TypeError, ValueError)) :
            self.VA3.controle_total(args3, kwargs2)
        kwargs3 = {"Bon élève":"oui", "Nombre de notes":4}
        with self.assertRaises((TypeError, ValueError)) :
            self.VA3.controle_total(args2, kwargs3)
        kwargs4 = {"Bon élève":"oui", "Nombre de notes":-5}
        with self.assertRaises((TypeError, ValueError)) :
            self.VA3.controle_total(args2, kwargs4)
        #args et kwargs du mauvais type
        self.VA1.type = (list, dict)
        with self.assertRaises(TypeError) :
            self.VA2.controle_total("balbla",{})
        with self.assertRaises(TypeError) :
            self.VA2.controle_total([3], 2)
        #conteneur trop court
        with self.assertRaises(ValueError) :
            self.VA2.controle_total([],{})
        #conteneur trop long
        with self.assertRaises(ValueError) :
            self.VA3.controle_total(["blabla","n", 3],{"appréciation":"Travail sérieux."})
    
    def test_controle_total_conversion(self) :
        """Teste la méthode controle_total avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_total convertit au besoin les objets de types incorects.
        """
        #objets valides
        self.VA2.append(1, "b", Verificateur(int))
        args_v1, kwargs_v1 = self.VA2.controle_total("57", conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(args_v1, [5,7])
        self.assertEqual(kwargs_v1, {})
        args_v2, kwargs_v2 = self.VA3.controle_total((16, 1), {"Nombre de notes":2.0},  conversion=True)#conversion du tuple en liste, de 16 (int) en float et de 1 (int) en bool et de 2.0 (float) en int
        self.assertEqual(args_v2, [16.0, True])
        self.assertEqual(kwargs_v2, {"Nombre de notes":2})
        with self.assertRaises(TypeError) :
            self.VA1.controle_total(5.4, conversion=True)#impossible car 5.4 est un flottant pas de conversion en liste possible
        with self.assertRaises(TypeError) :
            self.VA3.controle_total(["douze"], conversion=True)#impossible car 'douze' est un nombre mais n'est pas écrit en chiffre donc il n'est pas convertible en int

    def test_get_liste_verificateurs(self) :
        """Teste l'affichage de l'attribut liste_verificateurs."""
        get_theorique = """   Identifiant 1       Identifiant 2        Vérificateur    \n        None          Nombre de notes   ◄types:<class 'int'>, minimum:0, maximum:None►\n         1               Bon élève      ◄types:<class 'bool'>, minimum:None, maximum:None►\n         0             Note maximale    ◄types:<class 'float'>, minimum:0, maximum:20►\n"""
        self.assertEqual(self.VA3.liste_verificateurs, get_theorique)

    def test_get_types(self) :
        """Teste l'affichage de l'attribut types."""
        types = self.VA2.types
        self.assertEqual(types, (list, dict))
    
    def test_set_types(self) :
        """Teste la modification de l'attribut types."""
        self.VA2.types = tuple
        self.assertEqualVA(self.VA2, tuple,1, None, [[0, "a", Verificateur(int)]])
    
    def test_del_types(self) :
        """Teste la suppression de l'attribut types."""
        del self.VA2.types
        self.assertEqualVA(self.VA2, None, 1, None, [[0, "a", Verificateur(int)]])

    def test_get_minimum(self) :
        """Teste l'affichage de l'attribut minimum."""
        minimum = self.VA2.minimum
        self.assertEqual(minimum, 1)
 
    def test_set_minimum(self) :
        """Teste la modification de l'attribut minimum."""
        self.VA2.minimum = 2
        self.assertEqualVA(self.VA2, (list, dict), 2, None, [[0, "a", Verificateur(int)]])
    
    def test_set_minimum_error(self) :
        """Vérifie que set_minimum lève certaines erreurs.

        Vérifie notamment que des erreurs sont levées lorsque nouveau_minimum n'est pas un nombre entier positif (ou nul) et qu'il est supérieur au maximum.
        """
        with self.assertRaises(TypeError) :
            self.VA1.minimum = "bla"#n'est pas un entier
            self.assertEqual(self.VA1, VerificateurArguments())
        with self.assertRaises(ValueError) :
            self.VA1.set_minimum(-2)#n'est pas un entier positif
            self.assertEqual(self.VA1, VerificateurArguments())
        with self.assertRaises(ValueError) :
            self.VA3.minimum = 5#minimum supérieur au maximum (3)
            self.assertEqualVA(self.VC3, None, None, 3,[[None,"Nombre de notes", Verificateur(int, 0)], [1,"Bon élève", Verificateur(bool)], [0, "Note maximale", Verificateur(float, 0, 20)]])

    def test_del_minimum(self) :
        """Teste la suppression de l'attribut minimum."""
        del self.VA2.minimum
        self.assertEqualVA(self.VA2, (list, dict), 0, None, [[0, "a", Verificateur(int)]])

    def test_get_maximum(self) :
        """Teste l'affichage de l'attribut maximum."""
        maximum = self.VA3.maximum
        self.assertEqual(maximum, 3)

    def test_set_maximum(self) :
        """Teste la modification de l'attribut maximum."""
        self.VA2.maximum = 6
        self.assertEqualVA(self.VA2, (list, dict), 1, 6, [[0, "a", Verificateur(int)]])

    def test_set_maximum_error(self) :
        """Vérifie que set_maximum lève certaines erreurs.

        Vérifie notamment que des erreurs sont levées lorsque nouveau_maximum n'est pas un nombre entier positif (ou nul) et qu'il est inférieur au minimum.
        """
        with self.assertRaises(TypeError) :
            self.VA1.maximum = 0.3#n'est pas un entier
        self.assertEqual(self.VA1, VerificateurArguments())
        with self.assertRaises(ValueError) :
            self.VA1.set_maximum(-2)#n'est pas un entier positif
        self.assertEqual(self.VA1, VerificateurArguments())
        with self.assertRaises(ValueError) :
            self.VA2.maximum = 0#maximum inférieur au minimum (1)
        self.assertEqualVA(self.VA2, (list, dict), 1, None, [[0, "a", Verificateur(int)]])

    def test_del_maximum(self) :
        """Teste la suppression de l'attribut maximum."""
        del self.VA3.maximum
        self.assertEqualVA(self.VA3, (list, tuple, dict), 0, None,[[None,"Nombre de notes", Verificateur(int, 0)], [1,"Bon élève", Verificateur(bool)], [0, "Note maximale", Verificateur(float, 0, 20)]])

    def test_conversion(self) :
        """Teste la méthode _conversion.
        
        Vérifie que la méthode convertit bien un objet de type invalide en un objet de type valide, lorsque c'est possible.
        """
        #conversions possibles
        args_v1, kwargs_v1 = self.VA1._conversion("5")
        self.assertEqual(args_v1, ["5"])
        self.assertEqual(kwargs_v1, {})
        self.assertEqualVA(self.VA1)
        args_v2, kwargs_v2 = self.VA1._conversion("test",{"key":56})
        self.assertEqual(args_v2, ["t","e","s","t"])
        self.assertEqual(kwargs_v2, {"key":56})
        self.assertEqualVA(self.VA1)
        args_v3, kwargs_v3 = self.VA2._conversion((),{"a":2})
        self.assertEqual(args_v3, [])
        self.assertEqual(kwargs_v3, {"a":2})
        self.assertEqualVA(self.VA2, types=(list, dict), minimum=1, liste_verificateurs=[[0,"a", Verificateur(int)]])


if __name__ == "__main__" :
    unittest.main()