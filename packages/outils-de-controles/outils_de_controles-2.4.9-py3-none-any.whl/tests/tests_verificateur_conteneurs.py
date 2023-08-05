"""Ce module teste avec unittest la classe VerificateurConteneurs."""

import unittest
import os
import sys

#On change le dossier de travail (cwd) pour pouvoir appeler les fichiers via des chemins relatifs
os.chdir(os.path.dirname(__file__))#On change le dossier de travail en appellant le nom du dossier qui contient ce fichier (le dossier tests)
os.chdir("..")#On rechange le dossier de travail en prenant le dossier parent du dossier tests (le dossier outils_de_controles)
sys.path.append(os.getcwd())#ligne nécessaire à l'importation du module verificateur_conteneurs

from outils_de_controles.verificateur_conteneurs import *
from outils_de_controles.verificateur import *

class TestVerificateurConteneurs(unittest.TestCase) :
    """Classe qui teste la classe VerificateurConteneurs.

    Vérifie que la classe VerificateurConteneurs du package outils_de_controles soit conforme aux spécifications. (Création, affichage, vérification des conteneurs, ...).
    """

    def assertEqualVC(self, VC, types=None, minimum=0, maximum=None, liste_verificateurs=[]) :
        """Cette méthode vérifie si deux objets VerificateurConteneurs sont égaux.

        Cette methode compare chaque attribut à la valeur fournie.
        """
        if VC.types == types and VC.minimum == minimum and VC.maximum == maximum and VC._liste_verificateurs == liste_verificateurs :
            return self.assertEqual(0,0)#l'objet verificateur est égal à la valeur théorique
        else :
            VC_theorique = VerificateurConteneurs(types=types, minimum=minimum, maximum=maximum)
            for verif in liste_verificateurs :
                VC_theorique._append(verif)
            raise AssertionError(repr(VC) + " != " + repr(VC_theorique))

    def setUp(self) :
        """Cette méthode prépare l'exécution des tests.
        
        Cette méthode crée pour cela des objets VerificateurConteneurs.
        """
        #création d'un objet vide
        self.VC1 = VerificateurConteneurs()
        #création d'un objet avec une liste
        self.VC2 = VerificateurConteneurs([0, 4, Verificateur(int)], [5, None, VerificateurConteneurs(types=tuple, minimum=2, maximum=5)], types=list, minimum=1)
        #création d'un objet avec trois listes
        self.VC3 = VerificateurConteneurs([None,"Nombre de notes", Verificateur(int, 0)], [1,"Bon élève", Verificateur(bool)], [0, "Note maximale", Verificateur(float, 0, 20)], maximum=3)

    def test_init(self) :
        """Méthode testant l'initialisation des objets VerificateurConteneurs.

        Vérifie que l'objet créé est conforme aux arguments passés en paramètres.
        """
        #objet vide
        self.assertEqualVC(self.VC1)
        self.assertEqualVC(self.VC2, types=list, minimum=1, liste_verificateurs=[[0,4, Verificateur(int)], [5, None, VerificateurConteneurs(types=tuple, minimum=2, maximum=5)]])
        self.assertEqualVC(self.VC3, None, 0, 3, [[None,"Nombre de notes", Verificateur(int, 0)],[1,"Bon élève", Verificateur(bool)], [0, "Note maximale", Verificateur(float, 0, 20)]])

    def test_init_erreur(self) :
        """Méthode vérifiant que __init__ lève certaines erreurs.

        Vérifie notamment qu'il y a une erreur levée si un des arguments n'est pas une liste, si les deux indentifiants valent None, si un identifiant existe déjà dans la liste. Vérifie aussi que maximum est supérieur ou égal à minimum et que ces deux attributs soient des entiers positifs.
        """
        #l'argument non nommé n'est pas une liste
        with self.assertRaises(TypeError) :
            VCe = VerificateurConteneurs("c'est une blaque !")
        #le premier identifiant est identique à un autre argument de la liste
        with self.assertRaises(ValueError) :
            VCe = VerificateurConteneurs([0, "abc"], [0, "def"])
        #le deuxième identifiant est identique à celui d'un autre argument de la liste
        with self.assertRaises(ValueError) :
            VCe = VerificateurConteneurs([0, "deja_pris", Verificateur()], [1,"deja_pris", Verificateur()])
        #aucun identifiant n'est précisé
        with self.assertRaises(ValueError) :
            VCe = VerificateurConteneurs([None, None, Verificateur(int)])
        #minimum n'est pas un entier
        with self.assertRaises(TypeError) :
            VCe = VerificateurConteneurs(minimum=2.5)
        #maximum n'est pas un entier
        with self.assertRaises(TypeError) :
            VCe = VerificateurConteneurs(maximum="bla")
        #minimum n'est pas un nombre positif
        with self.assertRaises(ValueError) :
            VCe = VerificateurConteneurs(minimum=-2)
        #maximum est inférieur au minimum
        with self.assertRaises(ValueError) :
            VCe = VerificateurConteneurs(minimum=10, maximum=5)

    def test_str(self) :
        """Méthode qui teste la méthode spéciale __str__.
        
        Vérifie que l'affichage des objets de la classe VerificateurConteneurs est correct (présentation sous forme de tableau ...).
        """
        str_theorique = """◄types:None, minimum:0, maximum:3\n\n   Identifiant 1       Identifiant 2        Vérificateur    \n        None          Nombre de notes   ◄types:<class 'int'>, minimum:0, maximum:None►\n         1               Bon élève      ◄types:<class 'bool'>, minimum:None, maximum:None►\n         0             Note maximale    ◄types:<class 'float'>, minimum:0, maximum:20►\n►\n"""
        self.assertEqual(str(self.VC3), str_theorique)

    def test_repr(self) :
        """Cette méthode teste la méthode spéciale __repr__."""
        repr_theorique = """outils_de_controles.VerificateurConteneurs([None, 'Nombre de notes', outils_de_controles.Verificateur(types=<class 'int'>, minimum=0, maximum=None)], [1, 'Bon élève', outils_de_controles.Verificateur(types=<class 'bool'>, minimum=None, maximum=None)], [0, 'Note maximale', outils_de_controles.Verificateur(types=<class 'float'>, minimum=0, maximum=20)], types=None, minimum=0, maximum=3)"""
        self.assertEqual(repr(self.VC3), repr_theorique)

    def test__id_verificateur(self) :
        """Méthode vérifiant le bon fonctionnement de _id_verificateur.

        Vérifie que _id_verificateur renvoie bien le vérificateur correspondant à l'identifiant.
        """
        V1 = self.VC3._id_verificateur(1)
        V1_theorique = Verificateur(bool)
        self.assertEqual(V1, V1_theorique)
        V2 = self.VC3._id_verificateur("Note maximale")
        V2_theorique = Verificateur(float, 0, 20)
        self.assertEqual(V2, V2_theorique)
    
    def test_id_verificateur_error(self) :
        """Vérifie que _id_verificateur lève des erreurs.

        Vérifie que lorsque l'identifiant passé en paramètre n'existe pas, une erreur est levée.
        """
        with self.assertRaises(ValueError) :
            Ve = self.VC3._id_verificateur("blabla")

    def test_contains(self) :
        """Méthode vérifiant le bon fonctionnement de __contains__.

        Vérifie que la recherche d'argument dans la liste avec le mot clé in, s'effectue correctement. (recherche d'entiers, de chaines et d'autres types).
        """
        B = [False for i in range(7)]
        if 1 in self.VC1 :
            B[0] = True #booléen n°1
        if "prenom" in self.VC2 : 
            B[1] = True
        if list in self.VC3 :
            B[2] = True
        if "Bon élève" in self.VC3 :
            B[3] = True
        if 0 in self.VC2 :
            B[4] = True
        B[5] = self.VC1.__contains__("a")
        B[6] = self.VC2.__contains__(4)
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
        VC5 = VerificateurConteneurs([0, 4, Verificateur(int)], [5, None, VerificateurConteneurs(types=tuple, minimum=2, maximum=5)], types=list, minimum=1)#mêmes argumenst que self.VC2 
        eq1 = self.VC2.__eq__(VC5)
        self.assertEqual(eq1, True)
        VC6 = VerificateurConteneurs([None,"Nombre de notes", Verificateur(int, 0)], [1,"Bon élève", Verificateur(bool)], maximum=3)
        eq2 = self.VC3.__eq__(VC6)#il manque un vérificateur dans la liste des vérificateurs
        self.assertEqual(eq2, False)
        VC6.append(0, "Note maximale", Verificateur(float, 0, 20))#on ajoute le vérificateur manquant
        eq3 = False
        if VC6 == self.VC3 :
            eq3 = True
        self.assertEqual(eq3, True)
        del VC6.maximum
        eq4 = False
        if VC6 == self.VC3 :
            eq4 = True
        self.assertEqual(eq4, False)#le maximum n'est pas présent

    def test__append(self) :
        """Méthode testant la méthode _append de la classe.

        Vérifie notamment l'objet modifié est conforme aux arguments passés en paramètres.
        """
        #premier test
        self.VC1._append([0,"a", Verificateur(str)])
        self.assertEqual(self.VC1._liste_verificateurs, [[0,"a", Verificateur(str)]])
        #deuxième test 
        self.VC2._append([6,"abc", Verificateur()])
        liste_theorique = [[0, 4, Verificateur(int)],[5, None, VerificateurConteneurs(types=tuple, minimum=2, maximum=5)], [6,"abc", Verificateur()]]
        self.assertEqual(self.VC2._liste_verificateurs, liste_theorique)
        self.VC2._append([None, "année de naissance", Verificateur(int)])
        liste_theorique.append([None, "année de naissance", Verificateur(int)])
        self.assertEqual(self.VC2._liste_verificateurs, liste_theorique)

    def test__append_error(self) :
        """Méthode vérifiant que _append lève certaines erreurs.

        Vérifie notamment qu'il y a une erreur levée si l'argument n'est pas une liste, si les deux indentifiants valent None, si un identifiant existe déjà dans la liste, si la liste n'a pas trop d'éléments.
        """
        #l'argument n'est pas une liste
        with self.assertRaises(TypeError) :
            self.VC1._append("c'est une blaque !")
        with self.assertRaises(TypeError) :
            self.VC1._append(33)
        #le premier identifiant est identique à un autre argument de la liste
        with self.assertRaises(ValueError) :
            self.VC2._append([0, "abc", Verificateur()])
        #le deuxième identifiant est identique à celui d'un autre argument de la liste
        with self.assertRaises(ValueError) :
            self.VC3._append([2, "Bon élève", Verificateur()])
        #aucun identifiant n'est précisé
        with self.assertRaises(ValueError) :
            self.VC1._append([None, None, Verificateur(str)])
        #liste avec trop d'éléments
        with self.assertRaises(ValueError) :
            self.VC1._append([3,"miam", Verificateur(), True])
    
    def test_append(self) :
        """Méthode testant la méthode append de la classe.

        Vérifie notamment l'objet modifié est conforme aux arguments passés en paramètres.
        """
        self.VC1.append(id2="a", verificateur=Verificateur(str))
        liste_theorique = [[None,"a", Verificateur(str)]]
        self.assertEqual(self.VC1._liste_verificateurs, liste_theorique)
        self.VC1.append(0, verificateur=Verificateur(int))
        liste_theorique.append([0, None, Verificateur(int)])
        self.assertEqual(self.VC1._liste_verificateurs, liste_theorique)
        self.VC1.append(id1=3)
        liste_theorique.append([3, None, Verificateur()])
        self.assertEqual(self.VC1._liste_verificateurs, liste_theorique)

    def test_append_error(self) :
        """Méthode vérifiant que la méthode append lève certaines erreurs.

        Vérifie notamment qu'il y a une erreur levée si l'argument n'est pas une liste, si les deux indentifiants valent None, si un identifiant existe déjà dans la liste.
        """
        #le premier identifiant est identique à un autre argument de la liste
        with self.assertRaises(ValueError) :
            self.VC2.append(id1=0, id2="abc")
        #le deuxième identifiant est identique à celui d'un autre argument de la liste
        with self.assertRaises(ValueError) :
            self.VC3.append(2, "Bon élève")
        #aucun identifiant n'est précisé
        with self.assertRaises(ValueError) :
            self.VC1.append(verificateur=Verificateur(str))

    def test_sort(self) :
        """Cette méthode vérifie que sort trie bien liste_verificateurs.

        Vérifie notamment le tri par défaut, le tri par nom, celui par ordre de définition, et la réversibilité du tri.
        """
        #initialisation
        self.VC1.append(2,"a")
        self.VC1.append(0, "b")
        self.VC1.append(1, "zb")
        
        #tri par défaut
        self.VC1.sort()
        self.assertEqual(self.VC1._liste_verificateurs, [[0, "b", Verificateur()], [1, "zb", Verificateur()], [2,"a", Verificateur()]])

        #tri inversé
        self.VC1.sort(reverse=True)
        self.assertEqual(self.VC1._liste_verificateurs, [[2,"a", Verificateur()], [1, "zb", Verificateur()], [0, "b",Verificateur()]])

        self.VC4 = self.VC1
        self.VC4.append(3)
        self.VC4.append(id2="e")
        self.VC4.append(id2="c")

        #tri selon la première colonne
        self.VC4.sort(key= lambda colonne:self.VC1.clé(colonne,0, 500))
        self.assertEqual(self.VC4._liste_verificateurs, [[0, "b", Verificateur()], [1, "zb", Verificateur()], [2,"a", Verificateur()], [3, None, Verificateur()], [None, "e", Verificateur()], [None, "c", Verificateur()]])

        #tri selon la deuxième colonne
        self.VC4.sort(key= lambda colonne:self.VC1.clé(colonne, 1, ""))
        self.assertEqual(self.VC4._liste_verificateurs, [[3, None, Verificateur()], [2,"a", Verificateur()], [0, "b", Verificateur()], [None, "c", Verificateur()], [None, "e", Verificateur()], [1, "zb", Verificateur()]])
    
    def test_clé(self) :
        """Méthode qui teste la méthode clé utilisée afin de trier l'objet.
        
        Vérifie que clé renvoie bien les bonnes valeurs."""
        retour1 = []
        for i in range(len(self.VC3._liste_verificateurs)) :
            retour1.append(self.VC3.clé(self.VC3._liste_verificateurs[i], 0, -1))
        retour_theorique1 = [-1, 1, 0]
        self.assertEqual(retour1, retour_theorique1)
        retour2 = []
        for i in range(len(self.VC3._liste_verificateurs)) :
            retour2.append(self.VC3.clé(self.VC3._liste_verificateurs[i], 1))
        retour_theorique2 = ["Nombre de notes", "Bon élève", "Note maximale"]
        self.assertEqual(retour2, retour_theorique2)

    def test_controle_types(self) :
        """Cette méthode vérifie le fonctionnement de controle_types.

        Vérifie que lorsque le type du conteneur est correct la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque le type est incorrect une TypeError est levée.
        """
        obj_v = self.VC2.controle_types([2, 0])#obj_v pour objet valide
        self.assertEqual(obj_v, [2, 0])
        self.VC2.controle_types(["a"])#controle le type du conteneur
        with self.assertRaises(TypeError) :
            self.VC2.controle_types("blabla")

    def test_controle_types_item(self) :
        """Cette méthode vérifie le fonctionnement de controle_types_item.

        Vérifie d'abord que quand l'argument est correct, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque l'objet vérifié n'a pas le bon type une erreur TypeError soit levée.
        """
        #Le type est valide : pas de levée d'erreur
        obj_v = self.VC3.controle_types_item("Bon élève", True)#bon élève doit correspondre à un booléen
        self.assertEqual(obj_v, True)
        self.VC2.controle_types_item(0, 55)#le premier argument doit être un nombre entier
        #Le type n'est pas valide : on vérifie la levée d'erreur
        with self.assertRaises(TypeError) :
            self.VC3.controle_types_item("Note maximale", True)#la note doit être un flottant
        with self.assertRaises(TypeError) :
            self.VC3.controle_types_item(1, "abc")#le premier argument doit être un booléen

    def test_controle_types_item_erreur(self) :
        """Cette méthode vérifie que controle_types_item lève des erreurs.

        Vérifie que quand l'identifiant est incorrect (soit n'existe pas dans la liste des identifiants, soit vaut None), cette méthode lève bien une erreur.
        """
        #L'identifiant ne doit pas être None
        with self.assertRaises(ValueError) :
            self.VC2.controle_types_item(None, "abc")
        #L'identifiant doit être un nombre entier ou une chaine
        with self.assertRaises((ValueError, TypeError)) :
            self.VC2.controle_types_item([1], "abc")
        #L'identifant doit être dans la liste
        with self.assertRaises(ValueError) :
            self.VC2.controle_types_item(33, "abc")
        with self.assertRaises(ValueError) :
            self.VC3.controle_types_item("zrt", "abc")

    def test_controle_types_total(self) :
        """Cette méthode vérifie le fonctionnement de controle_types_total.

        Vérifie que lorsqu'on appele cette méthode une erreur soit levée.
        """
        with self.assertRaises(NotImplementedError) :
            self.VC3.controle_types_total([])

    def test_controle_minimum(self) :
        """Cette méthode vérifie le fonctionnement de controle_minimum.

        Vérifie que lorsque la longueur du conteneur est correcte la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque le conteneur ne contient pas assez d'éléments une ValueError est levée.
        """
        obj_v = self.VC2.controle_minimum([2, 0])
        self.assertEqual(obj_v, [2, 0])
        self.VC2.controle_minimum([2])#minimum=1 et ici il y a 1 élément dans la liste
        with self.assertRaises(ValueError) :
            self.VC2.controle_minimum([])#minimum=1 et ici il n'y a pas d'élément dans la liste
    
    def test_controle_maximum(self) :
        """Cette méthode vérifie le fonctionnement de controle_maximum.

        Vérifie que lorsque la longueur du conteneur est correcte la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque le conteneur contient trop d'éléments une ValueError est levée.
        """
        obj_v = self.VC3.controle_maximum([2, 0])
        self.assertEqual(obj_v, [2, 0])
        self.VC3.controle_maximum([15.5])#len de la liste = 1<3
        with self.assertRaises(ValueError) :
            self.VC3.controle_maximum([15.5, True, 3, "Travail régulier"])#4 éléments = 1 de trop

    def test_controle_global(self) :
        """Cette méthode teste la méthode controle_global de la classe testée.

        Dans une première partie, cette méthode vérifie que lorsque l'objet contrôlé est valide aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque l'objet n'est pas valide, une erreur est bien levée.
        """
        #conteneurs du bon type avec la bonne longueur
        obj_v = self.VC2.controle_global(["a", "b"])
        self.assertEqual(obj_v, ["a", "b"])
        self.VC3.controle_global([])
        #conteneur du mauvais type
        with self.assertRaises(TypeError) :
            self.VC2.controle_global("blabla")
        #conteneur trop court
        with self.assertRaises(ValueError) :
            self.VC2.controle_global([])
        #conteneur trop long
        with self.assertRaises(ValueError) :
            self.VC3.controle_global(["blabla","n", 3, 25])

    def test_controle_global_item(self) :
        """Cette méthode vérifie le fonctionnement de controle_global_item.

        Vérifie d'abord que quand l'argument est correct, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque l'objet vérifié n'est pas valide une erreur soit levée.
        """
        #objet valides
        obj_v = self.VC3.controle_global_item(0, 15.5)#la note (premier argument) doit être un flottant
        self.assertEqual(obj_v, 15.5)
        self.VC3.controle_global_item("Nombre de notes", 55)#le nombre de notes doit être un nombre entier positif
        #objets qui ne sont pas valides
        with self.assertRaises((TypeError, ValueError)) :
            self.VC3.controle_global_item("Nombre de notes", "bala")#le type est incorrect
        with self.assertRaises((TypeError, ValueError)) :
            self.VC3.controle_global_item("Nombre de notes", -3)#-3 est inférieur au minimum autorisé
        with self.assertRaises((TypeError, ValueError)) :
            self.VC3.controle_global_item(0, 36.0)#36 supérieur à 20 (maximum autorisé)

    def test_controle_global_item_erreur(self) :
        """Cette méthode vérifie que controle_global_item lève des erreurs.

        Vérifie que quand l'identifiant est incorrect (soit n'existe pas dans la liste des identifiants, soit vaut None), cette méthode lève bien une erreur.
        """
        #L'identifiant ne doit pas être None
        with self.assertRaises(ValueError) :
            self.VC2.controle_global_item(None, "abc")
        #L'identifiant doit être un nombre entier ou une chaine
        with self.assertRaises((ValueError, TypeError)) :
            self.VC2.controle_global_item([1], "abc")
        #L'identifant doit être dans la liste
        with self.assertRaises(ValueError) :
            self.VC2.controle_global_item(33, "abc")
        with self.assertRaises(ValueError) :
            self.VC3.controle_global_item("zrt", "abc")

    def test_controle_total(self) :
        """Cette méthode vérifie le fonctionnement de controle_total.

        Vérifie que lorsqu'on appele cette méthode une erreur soit levée.
        """
        with self.assertRaises(NotImplementedError) :
            self.VC3.controle_total([])
    
    def test_get_liste_verificateurs(self) :
        """Teste l'affichage de l'attribut liste_verificateurs."""
        get_theorique = """   Identifiant 1       Identifiant 2        Vérificateur    \n        None          Nombre de notes   ◄types:<class 'int'>, minimum:0, maximum:None►\n         1               Bon élève      ◄types:<class 'bool'>, minimum:None, maximum:None►\n         0             Note maximale    ◄types:<class 'float'>, minimum:0, maximum:20►\n"""
        self.assertEqual(self.VC3.liste_verificateurs, get_theorique)

    def test_get_types(self) :
        """Teste l'affichage de l'attribut types."""
        types = self.VC2.types
        self.assertEqual(types, list)
    
    def test_set_types(self) :
        """Teste la modification de l'attribut types."""
        self.VC2.types = tuple
        self.assertEqualVC(self.VC2, tuple,1, None, [[0, 4, Verificateur(int)],[5, None, VerificateurConteneurs(types=tuple, minimum=2, maximum=5)]])
    
    def test_del_types(self) :
        """Teste la suppression de l'attribut types."""
        del self.VC2.types
        self.assertEqualVC(self.VC2, None, 1, None, [[0, 4, Verificateur(int)],[5, None, VerificateurConteneurs(types=tuple, minimum=2, maximum=5)]])

    def test_get_minimum(self) :
        """Teste l'affichage de l'attribut minimum."""
        minimum = self.VC2.minimum
        self.assertEqual(minimum, 1)
 
    def test_set_minimum(self) :
        """Teste la modification de l'attribut minimum."""
        self.VC2.minimum = 2
        self.assertEqualVC(self.VC2, list, 2, None, [[0, 4, Verificateur(int)],[5, None, VerificateurConteneurs(types=tuple, minimum=2, maximum=5)]])
    
    def test_set_minimum_error(self) :
        """Vérifie que set_minimum lève certaines erreurs.

        Vérifie notamment que des erreurs sont levées lorsque nouveau_minimum n'est pas un nombre entier positif (ou nul) et qu'il est supérieur au maximum.
        """
        with self.assertRaises(TypeError) :
            self.VC1.minimum = "bla"#n'est pas un entier
            self.assertEqual(self.VC1, VerificateurConteneurs())
        with self.assertRaises(ValueError) :
            self.VC1.set_minimum(-2)#n'est pas un entier positif
            self.assertEqual(self.VC1, VerificateurConteneurs())
        with self.assertRaises(ValueError) :
            self.VC3.minimum = 5#minimum supérieur au maximum (3)
            self.assertEqualVC(self.VC3, None, 0, 3,[[None,"Nombre de notes", Verificateur(int, 0)], [1,"Bon élève", Verificateur(bool)], [0, "Note maximale", Verificateur(float, 0, 20)]])

    def test_del_minimum(self) :
        """Teste la suppression de l'attribut minimum."""
        del self.VC2.minimum
        self.assertEqualVC(self.VC2, list, 0, None, [[0, 4, Verificateur(int)],[5, None, VerificateurConteneurs(types=tuple, minimum=2, maximum=5)]])

    def test_get_maximum(self) :
        """Teste l'affichage de l'attribut maximum."""
        maximum = self.VC3.maximum
        self.assertEqual(maximum, 3)

    def test_set_maximum(self) :
        """Teste la modification de l'attribut maximum."""
        self.VC2.maximum = 6
        self.assertEqualVC(self.VC2, list, 1, 6, [[0, 4, Verificateur(int)],[5, None, VerificateurConteneurs(types=tuple, minimum=2, maximum=5)]])

    def test_set_maximum_error(self) :
        """Vérifie que set_maximum lève certaines erreurs.

        Vérifie notamment que des erreurs sont levées lorsque nouveau_maximum n'est pas un nombre entier positif (ou nul) et qu'il est inférieur au minimum.
        """
        with self.assertRaises(TypeError) :
            self.VC1.maximum = 0.3#n'est pas un entier
        self.assertEqual(self.VC1, VerificateurConteneurs())
        with self.assertRaises(ValueError) :
            self.VC1.set_maximum(-2)#n'est pas un entier positif
        self.assertEqual(self.VC1, VerificateurConteneurs())
        with self.assertRaises(ValueError) :
            self.VC2.maximum = 0#maximum inférieur au minimum (1)
        self.assertEqualVC(self.VC2, list, 1, None, [[0, 4, Verificateur(int)],[5, None, VerificateurConteneurs(types=tuple, minimum=2, maximum=5)]])

    def test_del_maximum(self) :
        """Teste la suppression de l'attribut maximum."""
        del self.VC3.maximum
        self.assertEqualVC(self.VC3, None, 0, None,[[None,"Nombre de notes", Verificateur(int, 0)], [1,"Bon élève", Verificateur(bool)], [0, "Note maximale", Verificateur(float, 0, 20)]])

if __name__ == "__main__" :
    unittest.main()