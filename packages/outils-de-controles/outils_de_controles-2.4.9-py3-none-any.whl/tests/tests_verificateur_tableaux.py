"""Ce module teste avec unittest la classe VerificateurTableaux."""

import unittest
import os
import sys

#On change le dossier de travail (cwd) pour pouvoir appeler les fichiers via des chemins relatifs
os.chdir(os.path.dirname(__file__))#On change le dossier de travail en appellant le nom du dossier qui contient ce fichier (le dossier tests)
os.chdir("..")#On rechange le dossier de travail en prenant le dossier parent du dossier tests (le dossier outils_de_controles)
sys.path.append(os.getcwd())#ligne nécessaire à l'importation du module verificateur_tableaux

from outils_de_controles.verificateur_tableaux import *
from outils_de_controles.verificateur import *

class TestVerificateurTableaux(unittest.TestCase) :
    """Classe qui teste la classe Verificateurtableaux.

    Vérifie que la classe VerificateurTableaux du package outils_de_controles soit conforme aux spécifications. (Création, affichage, vérification des tableaux, ...).
    """
    
    def assertEqualVT(self, VT, liste_verificateurs=[], minimum=(2,2), maximum=(2**10, 2**20), nom_tableau=Verificateur(str), en_tete_h=Verificateur(), en_tete_v=Verificateur()) :
        """Cette méthode vérifie si deux objets VerificateurListes sont égaux.

        Cette methode compare chaque attribut à la valeur fournie.
        """
        if VT._liste_verificateurs == liste_verificateurs \
        and VT.minimum == minimum \
        and VT.maximum == maximum \
        and VT.nom_tableau == nom_tableau \
        and VT.en_tete_h == en_tete_h \
        and VT.en_tete_v == en_tete_v :
            return self.assertEqual(0,0)#l'objet verificateur est égal à la valeur théorique
        else :
            VT_theorique = VerificateurTableaux(minimum=minimum, maximum=maximum, nom_tableau=nom_tableau, en_tete_h=en_tete_h, en_tete_v=en_tete_v)
            for verif in liste_verificateurs :
                VT_theorique._append(verif)
            raise AssertionError(repr(VT) + " != " + repr(VT_theorique))
    
    def setUp(self) :
        """Cette méthode prépare l'exécution des tests.
        
        Cette méthode crée pour cela des objets VerificateurTableaux.
        """
        #création d'un objet vide
        self.VT1 = VerificateurTableaux()
        self.VT2 = VerificateurTableaux([1,3,Verificateur((int, float),minimum=0, maximum=100)], nom_tableau = Verificateur(str),  maximum=(4,5))#un petit tableau avec des pourcentages (cases avec nombres entre 0 et 100) avec comme nom un str
        self.VT3 = VerificateurTableaux([7, 8, Verificateur(int, 0, 59)], [2, None, Verificateur(str)], [4, None, Verificateur(int, 1,12)], [3, None, Verificateur(int, 1, 31)], [1, None, Verificateur(str)], [5, None, Verificateur(int, 2000, 2100)], [6, None, Verificateur(int, 0, 23)], minimum=(4,7), maximum = (9, None), nom_tableau=Verificateur(int, 0), en_tete_h=Verificateur(str), en_tete_v=Verificateur(int, 1))

        self.VT2_correct = [["", "% de bon élèves"],["Classe A",12.25]]
        self.VT3_correct = [[287, "Nom erreur", "Type d'erreur", "Jour", "Mois", "Année", "Heure"],[54, "Le tableau n'est pas une liste", "TypeError", 17,1,2021,15], [381, "Le tableau est trop petit", "ValueError", 19,1,2021,10], [215, "Cette méthode n'est pas définie pour cette classe (classe virtuelle).", "NotImplementedError", 20,1,2021,8], [382, "Le tableau a trop de colonnes", "ValueError", 22,1,2021,19], [383, "Le tableau a trop de lignes", "ValueError", 22,1,2021,20], [380, "Le tableau n'a pas assez de colonnes", "ValueError", 23,1,2021,7]]#représente un  tableau sensé être valides selon les critère de VT2
    
    def test_init(self) :
        """Méthode testant l'initialisation des objets VerificateurTableaux.

        Vérifie que l'objet créé est conforme aux arguments passés en paramètres.
        """
        #objet vide
        self.assertEqualVT(self.VT1)
        self.assertEqualVT(self.VT2, liste_verificateurs = [[1,3,Verificateur((int, float),minimum=0, maximum=100)]], nom_tableau = Verificateur(str), maximum=(4, 5))
        self.assertEqualVT(self.VT3, [[7, 8, Verificateur(int, 0, 59)], [2, None, Verificateur(str)], [4, None, Verificateur(int, 1,12)], [3, None, Verificateur(int, 1, 31)], [1, None, Verificateur(str)], [5, None, Verificateur(int, 2000, 2100)], [6, None, Verificateur(int, 0, 23)]], minimum=(4,7), maximum = (9, None), nom_tableau=Verificateur(int, 0), en_tete_h=Verificateur(str), en_tete_v=Verificateur(int, 1))

    def test_init_erreur(self) :
        """Méthode vérifiant que __init__ lève certaines erreurs.

        Vérifie notamment qu'il y a une erreur levée si un des arguments n'est pas une liste, si un des deux identifiants (index) n'est pas un nombre entier positif strictement supérieur à 0 (ou None), si les deux indentifiants valent None, si un identifiant existe déjà dans la liste. Vérifie que minimum et maximum sont bien des tuples à deux éléments : deux nombres entiers positif.Vérifie également que chaque élément du typle du minimum est bien supérieur à 1. Vérifie aussi que maximum est supérieur ou égal à minimum.
        """
        #l'argument non nommé n'est pas une liste
        with self.assertRaises(TypeError) :
            VTe = VerificateurTableaux("c'est une blaque !")
        #l'index 1 n'est pas un nombre entier positif
        with self.assertRaises(TypeError) :
            VTe = VerificateurTableaux(["a", None, Verificateur()])
        #l'index 1 n'est pas un nombre entier positif (>0)
        with self.assertRaises(ValueError) :
            VTe = VerificateurTableaux([-2, None, Verificateur()])
        with self.assertRaises(ValueError) :
            VTe = VerificateurTableaux([0, None, Verificateur()])
        #l'index est identique à un autre argument de la liste
        with self.assertRaises(ValueError) :
            VTe = VerificateurTableaux([1, None], [1, 3])
        with self.assertRaises(ValueError) :
            VTe = VerificateurTableaux([2, None], [1, 3])
        #l'index 2 n'est pas un entier positif
        with self.assertRaises(TypeError) :
            VTe = VerificateurTableaux([1, 3, Verificateur(int)], [4, "a", Verificateur()])
            self.assertEqual(VTe._liste_verificateurs, [[1, 3, Verificateur(int)]])
        #aucun identifiant n'est précisé
        with self.assertRaises(ValueError) :
            VTe = VerificateurTableaux([None, None, Verificateur(int)])
        #minimum n'est pas un tuple
        with self.assertRaises(TypeError) :
            VTe = VerificateurTableaux(minimum=2.5)
        #maximum n'est pas un tuple
        with self.assertRaises(TypeError) :
            VTe = VerificateurTableaux(maximum="bla")
        #minimum n'est pas un tuple à deux éléments
        with self.assertRaises(ValueError) :
            VTe = VerificateurTableaux(minimum=(3,3,2))
        #maximum n'est pas un tuple à deux éléments
        with self.assertRaises(ValueError) :
            VTe = VerificateurTableaux(maximum=(5,25,125))
        #minimum n'est pas un tuple d'entier
        with self.assertRaises(TypeError) :
            VTe = VerificateurTableaux(minimum=(3.5, 6.2))
        #maximum n'est pas un tuple d'entier
        with self.assertRaises(TypeError) :
            VTe = VerificateurTableaux(maximum=("rien", None))
        #minimum n'est pas composé de deux nombres entiers supérieur à 1
        with self.assertRaises(ValueError) :
            VTe = VerificateurTableaux(minimum=(1, 3))
        #minimum n'est pas composé de deux nombres entiers positifs
        with self.assertRaises(ValueError) :
            VTe = VerificateurTableaux(maximum=(-2, 6))
        #maximum est inférieur au minimum
        with self.assertRaises(ValueError) :
            VTe = VerificateurTableaux(minimum=(10, 15), maximum=(5, 100))

    def test_str(self) :
        """Méthode qui teste la méthode spéciale __str__.
        
        Vérifie que l'affichage des objets de la classe VerificateurArguments est correct (présentation sous forme de tableau ...).
        """
        str_theorique = """◄minimum:(4, 7), maximum:(9, None), nom_tableau:◄types:<class 'int'>, minimum:0, maximum:None►, en_tete_h:◄types:<class 'str'>, minimum:None, maximum:None►, en_tete_v:◄types:<class 'int'>, minimum:1, maximum:None►\n\n   Identifiant 1       Identifiant 2        Vérificateur    \n         7                   8          ◄types:<class 'int'>, minimum:0, maximum:59►\n         2                  None        ◄types:<class 'str'>, minimum:None, maximum:None►\n         4                  None        ◄types:<class 'int'>, minimum:1, maximum:12►\n         3                  None        ◄types:<class 'int'>, minimum:1, maximum:31►\n         1                  None        ◄types:<class 'str'>, minimum:None, maximum:None►\n         5                  None        ◄types:<class 'int'>, minimum:2000, maximum:2100►\n         6                  None        ◄types:<class 'int'>, minimum:0, maximum:23►\n►\n"""
        self.assertEqual(str(self.VT3), str_theorique)

    def test_repr(self) :
        """Cette méthode teste la méthode spéciale __repr__."""
        self.maxDiff = None#provisoire
        repr_theorique = """outils_de_controles.VerificateurTableaux([7, 8, outils_de_controles.Verificateur(types=<class 'int'>, minimum=0, maximum=59)], [2, None, outils_de_controles.Verificateur(types=<class 'str'>, minimum=None, maximum=None)], [4, None, outils_de_controles.Verificateur(types=<class 'int'>, minimum=1, maximum=12)], [3, None, outils_de_controles.Verificateur(types=<class 'int'>, minimum=1, maximum=31)], [1, None, outils_de_controles.Verificateur(types=<class 'str'>, minimum=None, maximum=None)], [5, None, outils_de_controles.Verificateur(types=<class 'int'>, minimum=2000, maximum=2100)], [6, None, outils_de_controles.Verificateur(types=<class 'int'>, minimum=0, maximum=23)], minimum=(4, 7), maximum=(9, None), nom_tableau=outils_de_controles.Verificateur(types=<class 'int'>, minimum=0, maximum=None), en_tete_h=outils_de_controles.Verificateur(types=<class 'str'>, minimum=None, maximum=None), en_tete_v=outils_de_controles.Verificateur(types=<class 'int'>, minimum=1, maximum=None))"""
        self.assertEqual(repr(self.VT3), repr_theorique)
    
    def test__id_verificateur(self) :
        """Méthode vérifiant le bon fonctionnement de _id_verificateur.

        Vérifie que _id_verificateur renvoie bien le vérificateur correspondant à l'identifiant.
        """
        V1 = self.VT3._id_verificateur(1)
        V1_theorique = Verificateur(str, None, None)
        self.assertEqual(V1, V1_theorique)
        V2 = self.VT2._id_verificateur(2)
        V2_theorique = Verificateur((int, float), 0, 100)
        self.assertEqual(V2, V2_theorique)
    
    def test__id_verificateur_error(self) :
        """Vérifie que _id_verificateur lève des erreurs.

        Vérifie que lorsque l'identifiant passé en paramètre n'existe pas, une erreur est levée.
        """
        with self.assertRaises(ValueError) :
            Ve = self.VT2._id_verificateur("blabla")
        with self.assertRaises(ValueError) :
            Ve = self.VT3._id_verificateur(9)

    def test_contains(self) :
        """Méthode vérifiant le bon fonctionnement de __contains__.

        Vérifie que la recherche d'argument dans la liste avec le mot clé in, s'effectue correctement.
        """
        B = [False for i in range(7)]
        if 1 in self.VT1 :
            B[0] = True #booléen n°1
        if "prenom" in self.VT2 : 
            B[1] = True
        if list in self.VT3 :
            B[2] = True
        if 2 in self.VT2 :#1<=2<=3 donc 2 est dans VT2
            B[3] = True
        if 5 in self.VT3 :
            B[4] = True
        B[5] = self.VT1.__contains__(3)
        B[6] = self.VT3.__contains__(2)
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
        VT5 = VerificateurTableaux([1,3,Verificateur((int, float),minimum=0, maximum=100)], nom_tableau = Verificateur(str),  maximum=(4,5))#mêmes arguments que self.VT2 
        eq1 = self.VT2.__eq__(VT5)
        self.assertEqual(eq1, True)
        VT6 = VerificateurTableaux([7, 8, Verificateur(int, 0, 59)], [2, None, Verificateur(str)], [4, None, Verificateur(int, 1,12)], [3, None, Verificateur(int, 1, 31)], [1, None, Verificateur(str)], [5, None, Verificateur(int, 2000, 2100)], [6, None, Verificateur(int, 0, 23)], minimum=(4,11), maximum = (None, None), nom_tableau=Verificateur(int, 0), en_tete_h=Verificateur(str), en_tete_v=Verificateur(int, 1))
        eq2 = self.VT3.__eq__(VT6)#il manque le maximum
        self.assertEqual(eq2, False)
        VT6.maximum=(8,None)#on ajoute le maximum manquant
        VT6.sort(reverse=True)
        eq3 = False
        if VT6 == self.VT3 :
            eq3 = True
        self.assertEqual(eq3, False)#l'ordre des vérificateurs n'est pas le même

    def test__append(self) :
        """Méthode testant la méthode _append de la classe.

        Vérifie notamment l'objet modifié est conforme aux arguments passés en paramètres.
        """
        #premeier test
        self.VT1._append([1,10, Verificateur(bool)])
        self.assertEqualVT(self.VT1, liste_verificateurs=[[1,10, Verificateur(bool)]])
        #deuxième test 
        self.VT2._append([4, None, Verificateur()])
        liste_theorique = [[1, 3, Verificateur((int,float),0,100)],[4, None, Verificateur()]]
        self.assertEqual(self.VT2._liste_verificateurs, liste_theorique)

    def test__append_error(self) :
        """Méthode vérifiant que _append lève certaines erreurs.

        Vérifie notamment qu'il y a une erreur levée si l'argument n'est pas une liste, si l'un des deux identifiants n'est pas un nombre entier positif (>0), si les deux indentifiants valent None, si un identifiant existe déjà dans la liste, si la liste n'a pas trop d'éléments.
        """
        #l'argument n'est pas une liste
        with self.assertRaises(TypeError) :
            self.VT1._append("c'est une blaque !")
        with self.assertRaises(TypeError) :
            self.VT1._append(33)
        #le premier élément de la liste n'est pas un nombre entier positif (>0)
        with self.assertRaises(TypeError) :
            self.VT1._append(["a",None,Verificateur()])
        with self.assertRaises(TypeError) :
            self.VT1._append([3.75, 3, Verificateur()])
        with self.assertRaises(ValueError) :
            self.VT1._append([0, None, Verificateur()])
        #l'index 1 est identique à un autre argument de la liste
        with self.assertRaises(ValueError) :
            self.VT3._append([3, 5, Verificateur()])
        with self.assertRaises(ValueError) :
            self.VT2._append([3, None, Verificateur()])
        #le deuxième index n'est pas un nombre entier positif
        with self.assertRaises(TypeError) :
            self.VT1._append([1, "blaz", Verificateur()])
        #le deuxième index est identique à celui d'un autre argument de la liste
        self.VT2.append(50,60)
        with self.assertRaises(ValueError) :
            self.VT2._append([45, 51, Verificateur()])
        #aucun identifiant n'est précisé
        with self.assertRaises(ValueError) :
            self.VT1._append([None, None, Verificateur(str)])
        #liste avec trop d'éléments
        with self.assertRaises(ValueError) :
            self.VT1._append([3,4, Verificateur(), True])
    
    def test_append(self) :
        """Méthode testant la méthode append de la classe.

        Vérifie notamment l'objet modifié est conforme aux arguments passés en paramètres.
        """
        self.VT1.append(id2=3, verificateur=Verificateur(str))
        liste_theorique = [[3,None, Verificateur(str)]]
        self.assertEqual(self.VT1._liste_verificateurs, liste_theorique)
        self.VT1.append(1, verificateur=Verificateur(int))
        liste_theorique.append([1, None, Verificateur(int)])
        self.assertEqual(self.VT1._liste_verificateurs, liste_theorique)
        self.VT1.append(id1=4, id2=6)
        liste_theorique.append([4, 6, Verificateur()])
        self.assertEqual(self.VT1._liste_verificateurs, liste_theorique)

    def test_append_error(self) :
        """Méthode vérifiant que la méthode append lève certaines erreurs.

        Vérifie notamment qu'il y a une erreur levée si l'argument n'est pas une liste, si l'un des deux identifiants n'est pas un nombre entier positif (>0), si les deux indentifiants valent None, si un identifiant existe déjà dans la liste.
        """
        #le premier index de la liste n'est pas un nombre entier positif (>0)
        with self.assertRaises(TypeError) :
            self.VT1.append("a", 3)
        with self.assertRaises(TypeError) :
            self.VT1.append(id1=3.75, verificateur=Verificateur())
        with self.assertRaises(ValueError) :
            self.VT1.append(0, 2)
        #l'index 1 est identique à un autre argument de la liste
        with self.assertRaises(ValueError) :
            self.VT2.append(id1=1)
        #l'index 2 n'est pas un nombre entier positif (>0)
        with self.assertRaises(TypeError) :
            self.VT1.append(id2 = float)
        #l'index 2 est identique à celui d'un autre argument de la liste
        self.VT2.append(50,60)
        with self.assertRaises(ValueError) :
            self.VT2.append(45, 51, Verificateur())
        #aucun identifiant n'est précisé
        with self.assertRaises(ValueError) :
            self.VT1.append(verificateur=Verificateur(str))

    def test_sort(self) :
        """Cette méthode vérifie que la liste est bien triée.

        Vérifie notamment le tri par défaut, le tri par le deuxième index, et la réversibilité du tri.
        """
        #initialisation
        self.VT1.append(2,None)
        self.VT1.append(21, None)
        self.VT1.append(8, 20)
        self.VT1.append(7)
        self.VT1.append(3,5)
        self.VT1.append(1)
        
        #tri par défaut
        self.VT1.sort()
        self.assertEqual(self.VT1._liste_verificateurs, [[1, None, Verificateur()], [2, None, Verificateur()], [3, 5, Verificateur()], [7,None, Verificateur()], [8, 20, Verificateur()], [21, None, Verificateur()]])

        #tri inversé
        self.VT1.sort(reverse=True)
        self.assertEqual(self.VT1._liste_verificateurs, [[21, None, Verificateur()], [8, 20, Verificateur()],[7, None, Verificateur()], [3, 5, Verificateur()], [2, None,Verificateur()], [1, None, Verificateur()]])
    
    def test_clé(self) :
        """Méthode qui teste la méthode clé utilisée afin de trier l'objet.
        
        Vérifie que clé renvoie bien les bonnes valeurs.
        """
        retour1 = []
        for i in range(len(self.VT3._liste_verificateurs)) :
            retour1.append(self.VT3.clé(self.VT3._liste_verificateurs[i], 1, 0))
        retour_theorique1 = [8, 0, 0, 0, 0, 0, 0]
        self.assertEqual(retour1, retour_theorique1)
        retour2 = []
        for i in range(len(self.VT3._liste_verificateurs)) :
            retour2.append(self.VT3.clé(self.VT3._liste_verificateurs[i], 0))
        retour_theorique2 = [7, 2, 4, 3, 1, 5, 6]
        self.assertEqual(retour2, retour_theorique2)

    def test_controle_types(self) :
        """Cette méthode vérifie le fonctionnement de controle_types.

        Vérifie que lorsque le type du conteneur est correct la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque le type est incorrect une TypeError est levée.
        """
        obj_v = self.VT3.controle_types([["Tableau","Pourcentage"],["de chomeur", 12.08],["de débiles", 47]])#obj_v pour objet valide
        self.assertEqual(obj_v, [["Tableau","Pourcentage"],["de chomeur", 12.08],["de débiles", 47]])
        self.VT3.controle_types([[],[],[]])#controle le type du conteneur
        #le tableau n'est pas une liste
        with self.assertRaises(TypeError) :
            self.VT2.controle_types({})

    def test_controle_types_conversion(self) :
        """Teste la méthode controle_types avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_types convertit au besoin les objets de types incorects.
        """
        #conversion possibles
        obj_v1 = self.VT2.controle_types((["", "% de bon élèves"],["Classe A",12.25]), conversion=True)#conversion du tuple en liste
        self.assertEqual(obj_v1, self.VT2_correct)
        obj_v2 = self.VT2.controle_types([["", "% de bon élèves"],("Classe A",12.25)], conversion=True)
        self.assertEqual(obj_v2, self.VT2_correct)
        obj_v3 = self.VT1.controle_types(["test", (5.4, 6.9)], conversion=True)
        self.assertEqual(obj_v3, [["t","e","s","t"], [5.4, 6.9]])
        #conversion impossible
        with self.assertRaises(TypeError) :
            self.VT1.controle_types(5.4, conversion=True)#impossible car 5.4 est un flottant donc n'est pas parcourable : la conversion en liste est impossible
        with self.assertRaises(TypeError) :
            self.VT1.controle_types(["test", 5.4], conversion=True)#impossible car 5.4 est un flottant donc n'est pas parcourable : la conversion en liste est impossible

    def test_controle_types_item(self) :
        """Cette méthode vérifie le fonctionnement de controle_types_item.

        Vérifie d'abord que quand l'argument est correct, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque l'objet vérifié n'a pas le bon type une erreur TypeError soit levée.
        """
        #Le type est valide : pas de levée d'erreur
        obj_v = self.VT3.controle_types_item(6, 22)#l'heure doit être un entier entre 0 et 23
        self.assertEqual(obj_v, 22)
        self.VT2.controle_types_item(3, 55.2)#les éléments d'indice 1 à 3 doivent être des flottants/ de s entiers compris entre 0 et 100
        #Le type n'est pas valide : on vérifie la levée d'erreur
        with self.assertRaises(TypeError) :
            self.VT3.controle_types_item(2, True)#True n'est pas un str
        with self.assertRaises(TypeError) :
            self.VT2.controle_types_item(1, "abc")#le premier élément de la liste doit être un flottant

    def test_controle_types_item_erreur(self) :
        """Cette méthode vérifie que controle_types_item lève des erreurs.

        Vérifie que quand l'identifiant est incorrect (soit n'existe pas dans la liste des identifiants, soit vaut None), cette méthode lève bien une erreur.
        """
        #L'identifiant ne doit pas être None
        with self.assertRaises(ValueError) :
            self.VT2.controle_types_item(None, "abc")
        #L'identifiant doit être un nombre entier
        with self.assertRaises((ValueError, TypeError)) :
            self.VT2.controle_types_item([1], "abc")
        #L'identifant doit être dans la liste
        with self.assertRaises(ValueError) :
            self.VT2.controle_types_item(33, 25.1)

    def test_controle_types_item_conversion(self) :
        """Teste controle_types_item avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_types_item convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VT2.controle_types_item(2, "4", conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, 4)
        obj_v2 = self.VT3.controle_types_item(4, 11.0, conversion=True)#conversion en int
        self.assertEqual(obj_v2, 11)
        with self.assertRaises(TypeError) :
            self.VT3.controle_types_item(4, "douze", conversion=True)#impossible car 'douze' est écrit en toute lettre donc n'est pas convertible en int

    def test_controle_types_total(self) :
        """Cette méthode vérifie le fonctionnement de controle_types_total.

        Vérifie d'abord que quand les arguments sont corrects, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque un des arguments n'est pas valide une erreur soit levée.
        """
        #objets valides
        self.VT3.controle_types_total(self.VT3_correct)
        obj_v = self.VT2.controle_types_total([["Pourcentages", "% de bons élèves"],["Classe A", 12.5],["Classe B", 15],["Classe C",11.33]])
        self.assertEqual(obj_v, [["Pourcentages", "% de bons élèves"],["Classe A", 12.5],["Classe B", 15],["Classe C",11.33]])
        #un des contenus n'est pas valide
        with self.assertRaises(TypeError) :
            VT3_erroné = self.VT3_correct
            VT3_erroné[0][0] = "287"
            self.VT3.controle_types_total(VT3_erroné)#nom du tableau n'est pas un int
        with self.assertRaises(TypeError) :
            self.VT2.controle_types_total([["Pourcentages", "% de bons élèves"],["Classe A", 12.5],["Classe B", "15"],["Classe C",11.33]])#un nombre est dans une chaine de caractères
        #le conteneur a un type invalide
        with self.assertRaises(TypeError) :
            self.VT2.controle_types_total((["Pourcentages", "% de bons élèves"],["Classe A", 12.5],["Classe B", "15"],["Classe C",11.33]))#tuple
        with self.assertRaises(TypeError) :
            self.VT3.controle_types_total({"h":20,"min":25,"sec":36})#dict

    def test_controle_types_total_conversion(self) :
        """Teste controle_types_total avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_types_total convertit au besoin les objets de types incorects.
        """
        #conversion possibles
        obj_v1 = self.VT2.controle_types_total((["", "% de bon élèves"],["Classe A",12.25]), conversion=True)#conversion du tuple en liste
        self.assertEqual(obj_v1, self.VT2_correct)
        obj_v2 = self.VT2.controle_types_total([["", "% de bon élèves"],("Classe A","12.25")], conversion=True)#conversion du tuple en liste et de '12.25' en float
        self.assertEqual(obj_v2, self.VT2_correct)
        #conversion impossible
        with self.assertRaises(TypeError) :
            self.VT1.controle_types_total(5.4, conversion=True)#impossible car 5.4 est un flottant donc n'est pas parcourable : la conversion en liste est impossible
        with self.assertRaises(TypeError) :
            self.VT1.controle_types_total(["test", 5.4], conversion=True)#impossible car 5.4 est un flottant donc n'est pas parcourable : la conversion en liste est impossible

    def test_controle_minimum(self) :
        """Cette méthode vérifie le fonctionnement de controle_minimum.

        Vérifie que lorsque le tableau a les bonnes dimensions, la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque le tableau n'a pas assez de lignes ou de colonnes une ValueError est levée.
        """
        obj_v = self.VT2.controle_minimum(self.VT2_correct)#minimum : deux lignes et deux colonnes
        self.assertEqual(obj_v, self.VT2_correct)
        self.VT3.controle_minimum(self.VT3_correct)
        with self.assertRaises(ValueError) :
            self.VT3.controle_minimum([[287, "Nom erreur", "Type d'erreur", "Jour", "Mois", "Année"],[54, "Le tableau n'est pas une liste", "TypeError", 17,1,2021], [381, "Le tableau est trop petit", "ValueError", 19,1,2021]])#minimum : 4 colonnes et 7 lignes
        with self.assertRaises(ValueError) :
            self.VT2.controle_minimum([["", "% de bon élèves"]])#minimum : deux lignes et deux colonnes et ici il n'y a qu'une seule ligne
        with self.assertRaises(ValueError) :
            self.VT2.controle_minimum([[""],["Classe A"]])#minimum : deux lignes et deux colonnes et ici il n'y a qu'une seule colonne

    def test_controle_maximum(self) :
        """Cette méthode vérifie le fonctionnement de controle_maximum.

        Vérifie que lorsque le tableau a les bonnes dimensions, la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque le tableau contient trop de lignes ou de colonnes une ValueError est levée.
        """
        obj_v = self.VT2.controle_maximum(self.VT2_correct)
        self.assertEqual(obj_v, self.VT2_correct)
        self.VT2.controle_maximum([["", "% de bon élèves"],["Classe A",12.25],["Classe B", 25.4]])
        with self.assertRaises(ValueError) :
            self.VT2.controle_maximum([["", "% de bon élèves", "% de cancres", "% d'élèves moyens", "% d'élèves bavards"],["Classe A",12.25, 5, 45.6, 55.3]])#5 colonnes = une de trop
        with self.assertRaises(ValueError) :
            self.VT2.controle_maximum([["", "% de bon élèves"],["Classe A",12.25],["Classe B",15], ["Classe C",17.2], ["Classe D",5.95], ["Classe E", 45.22]])#6 lignes = une de trop

    def test_controle_nom_tableau(self) :
        """Cette méthode vérifie le fonctionnement de controle_nom_tableau.

        Vérifie d'abord que quand le nom du tableau est correct, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque le nom du tableau n'est pas valide une erreur soit levée.
        """
        obj_v = self.VT3.controle_nom_tableau(self.VT3_correct)
        self.assertEqual(obj_v, self.VT3_correct)
        self.VT2.controle_nom_tableau(self.VT2_correct)
        with self.assertRaises(TypeError) :
            VT3_erroné = self.VT3_correct
            VT3_erroné[0][0] = 287.3
            self.VT3.controle_nom_tableau(VT3_erroné)#le nom du tableau n'est pas un entier
        with self.assertRaises(ValueError) :
            VT3_erroné[0][0] = -28
            self.VT3.controle_nom_tableau(VT3_erroné)#le nom du tableau n'est pas un entier positif
    
    def test_controle_nom_tableau_conversion(self) :
        """Teste controle_nom_tableau avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_nom_tableau convertit au besoin les objets de types incorects.
        """
        VT3_erroné = self.VT3_correct
        VT3_erroné[0][0] = 287.3
        obj_v = self.VT3.controle_nom_tableau(VT3_erroné, conversion=True)#le nom du tableau n'est pas un entier
        self.assertEqual(obj_v, self.VT3_correct)

    def test_controle_en_tete_h(self) :
        """Vérifie le fonctionnement de controle_en_tete_h.

        Vérifie d'abord que quand les en-têtes horizontales sont correctes, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque une des en-têtes horizontales n'est pas valide une erreur soit levée.
        """
        obj_v = self.VT3.controle_en_tete_h(self.VT3_correct)
        self.assertEqual(obj_v, self.VT3_correct)
        self.VT3.controle_en_tete_h(self.VT3_correct)
        with self.assertRaises(TypeError) :
            VT3_erroné = self.VT3_correct
            VT3_erroné[0][1] = True
            self.VT3.controle_en_tete_h(VT3_erroné)#le nom de la première colonne n'est pas un str mais un bool

    def test_controle_en_tete_h_conversion(self) :
        """Teste controle_en_tete_h avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_en_tete_h convertit au besoin les objets de types incorects.
        """
        VT3_erroné = self.VT3_correct
        VT3_erroné[0][1] = True
        obj_v = self.VT3.controle_en_tete_h(VT3_erroné, conversion=True)#le nom de la première colonne n'est pas un str mais un bool
        self.assertEqual(obj_v, self.VT3_correct)

    def test_controle_en_tete_v(self) :
        """Vérifie le fonctionnement de controle_en_tete_v.

        Vérifie d'abord que quand les en-têtes verticales sont correctes, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque une des en-têtes verticales n'est pas valide une erreur soit levée.
        """
        obj_v = self.VT3.controle_en_tete_v(self.VT3_correct)
        self.assertEqual(obj_v, self.VT3_correct)
        self.VT3.controle_en_tete_v(self.VT3_correct)
        with self.assertRaises(TypeError) :
            VT3_erroné = self.VT3_correct
            VT3_erroné[1][0] = "54"
            self.VT3.controle_en_tete_v(VT3_erroné)#le nom de la première ligne n'est pas un int mais un str
        with self.assertRaises(ValueError) :
            VT3_erroné[1][0] = 54#on remplace l'ancienne valeur incorrecte par une valeur correcte
            VT3_erroné[2][0] = -381
            self.VT3.controle_en_tete_v(VT3_erroné)#le nom de la deuxième ligne n'est pas un nombre entier positif mais négatif

    def test_controle_en_tete_v_conversion(self) :
        """Teste controle_en_tete_v avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_en_tete_v convertit au besoin les objets de types incorects.
        """
        VT3_erroné = self.VT3_correct
        VT3_erroné[1][0] = "54"
        obj_v = self.VT3.controle_en_tete_v(VT3_erroné, conversion=True)#le nom de la première ligne n'est pas un int mais un str
        self.assertEqual(obj_v, self.VT3_correct)

    def test_controle_taille_lignes(self) :
        """Vérifie le fonctionnement de controle_taille_lignes.

        Vérifie d'abord que quand les lignes sont toutes de la même taille, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque une des lignes n'a pas la même taille que les autres une erreur soit levée.
        """
        obj_v = self.VT3.controle_taille_lignes(self.VT3_correct)
        self.assertEqual(obj_v, self.VT3_correct)
        self.VT3.controle_taille_lignes(self.VT3_correct)
        with self.assertRaises(ValueError) :
            VT3_erroné = self.VT3_correct
            del VT3_erroné[3][5]
            self.VT3.controle_taille_lignes(VT3_erroné)#ligne 215 : il manque l'heure

    def test_controle_global(self) :
        """Cette méthode teste la méthode controle_global de la classe testée.

        Dans une première partie, cette méthode vérifie que lorsque le tableau est valide aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque l'objet n'est pas valide, une erreur est bien levée.
        """
        #tableaux valides
        obj_v = self.VT2.controle_global(self.VT2_correct)
        self.assertEqual(obj_v, self.VT2_correct)
        self.VT3.controle_global(self.VT3_correct)

        #tableau du mauvais type
        with self.assertRaises(TypeError) :
            self.VT2.controle_global(["blabla", "trois"])

        #tableau n'ayant pas assez de lignes
        with self.assertRaises(ValueError) :
            self.VT2.controle_global([["", "% de bon élèves"]])
        
        #tableau ayant trop de colonnes
        with self.assertRaises(ValueError) :
            VT3_erroné = self.VT3_correct
            VT3_erroné[0].append("Secondes")
            VT3_erroné[0].append("Milisecondes")
            VT3_erroné[1].append(37)
            VT3_erroné[1].append(505)
            self.VT3.controle_global(VT3_erroné)#10 colonnes = 1 de trop
        
        #nom du tableau invalide
        with self.assertRaises(TypeError) :
            del VT3_erroné[0][8]#on supprime l'ancienne valeur incorrecte
            del VT3_erroné[1][8]#on supprime l'ancienne valeur incorrecte
            del VT3_erroné[0][7]#on supprime l'ancienne valeur incorrecte
            del VT3_erroné[1][7]#on supprime l'ancienne valeur incorrecte
            VT3_erroné[0][0] = 287.3
            self.VT3.controle_nom_tableau(VT3_erroné)#le nom du tableau n'est pas un entier
        with self.assertRaises(ValueError) :
            VT3_erroné[0][0] = -28
            self.VT3.controle_nom_tableau(VT3_erroné)#le nom du tableau n'est pas un entier positif
        
        #en-têtes invalides
        with self.assertRaises(TypeError) :
            VT3_erroné[0][0] = 287
            VT3_erroné[0][1] = True
            self.VT3.controle_global(VT3_erroné)#le nom de la première colonne n'est pas un str mais un bool
        with self.assertRaises(TypeError) :
            VT3_erroné[0][1] = "Nom erreur"
            VT3_erroné[1][0] = "54"
            self.VT3.controle_global(VT3_erroné)#le nom de la première ligne n'est pas un int mais un str
        with self.assertRaises(ValueError) :
            VT3_erroné[1][0] = 54#on remplace l'ancienne valeur incorrecte par une valeur correcte
            VT3_erroné[2][0] = -381
            self.VT3.controle_global(VT3_erroné)#le nom de la deuxième ligne n'est pas un nombre entier positif mais négatif
        
        #lignes de longueur différentes
        with self.assertRaises(ValueError) :
            VT3_erroné = self.VT3_correct
            del VT3_erroné[3][5]
            self.VT3.controle_global(VT3_erroné)#ligne 215 : il manque l'heure

    def test_controle_global_conversion(self) :
        """Teste la méthode controle_global avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_global convertit au besoin les objets de types incorects.
        """
        #conversion possibles
        obj_v1 = self.VT2.controle_global((["", "% de bon élèves"],["Classe A",12.25]), conversion=True)#conversion du tuple en liste
        self.assertEqual(obj_v1, self.VT2_correct)
        obj_v2 = self.VT2.controle_global([["", "% de bon élèves"],("Classe A",12.25)], conversion=True)
        self.assertEqual(obj_v2, self.VT2_correct)
        VT3_erroné = self.VT3_correct
        VT3_erroné[0][0] = 287.3
        obj_v3 = self.VT3.controle_global(VT3_erroné, conversion=True)#le nom du tableau n'est pas un entier
        self.assertEqual(obj_v3, self.VT3_correct)
        VT3_erroné[0][1] = True
        obj_v4 = self.VT3.controle_global(VT3_erroné, conversion=True)#le nom de la première colonne n'est pas un str mais un bool
        self.assertEqual(obj_v4, self.VT3_correct)
        VT3_erroné[1][0] = "54"
        obj_v5 = self.VT3.controle_global(VT3_erroné, conversion=True)#le nom de la première ligne n'est pas un int mais un str
        self.assertEqual(obj_v5, self.VT3_correct)
        #conversion impossible
        with self.assertRaises(TypeError) :
            self.VT1.controle_global(5.4, conversion=True)#impossible car 5.4 est un flottant donc n'est pas parcourable : la conversion en liste est impossible
        with self.assertRaises(TypeError) :
            self.VT1.controle_global(["test", 5.4], conversion=True)#impossible car 5.4 est un flottant donc n'est pas parcourable : la conversion en liste est impossible

    def test_controle_global_item(self) :
        """Cette méthode vérifie le fonctionnement de controle_global_item.

        Vérifie d'abord que quand l'argument est correct, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque l'objet vérifié n'est pas valide une erreur soit levée.
        """
        #Le type est valide : pas de levée d'erreur
        obj_v = self.VT3.controle_global_item(6, 22)#l'heure doit être un entier entre 0 et 23
        self.assertEqual(obj_v, 22)
        self.VT2.controle_global_item(3, 55.2)#les éléments d'indice 1 à 3 doivent être des flottants/ de s entiers compris entre 0 et 100
        #Le type n'est pas valide : on vérifie la levée d'erreur
        with self.assertRaises(TypeError) :
            self.VT3.controle_global_item(2, True)#True n'est pas un str
        with self.assertRaises(TypeError) :
            self.VT2.controle_global_item(1, "abc")#le premier élément de la liste doit être un flottant
    
    def test_controle_global_item_erreur(self) :
        """Cette méthode vérifie que controle_global lève des erreurs.

        Vérifie que quand l'identifiant est incorrect (soit n'existe pas dans la liste des identifiants, soit vaut None), cette méthode lève bien une erreur.
        """
        #L'identifiant ne doit pas être None
        with self.assertRaises(ValueError) :
            self.VT2.controle_global_item(None, "abc")
        #L'identifiant doit être un nombre entier
        with self.assertRaises((ValueError, TypeError)) :
            self.VT2.controle_global_item([1], "abc")
        #L'identifant doit être dans la liste
        with self.assertRaises(ValueError) :
            self.VT2.controle_global_item(33, "abc")

    def test_controle_global_item_conversion(self) :
        """Teste controle_global_item avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_global_item convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VT2.controle_global_item(1, 4, conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, 4.0)
        obj_v2 = self.VT2.controle_global_item(2, "56", conversion=True)#conversion en int
        self.assertEqual(obj_v2, 56)
        with self.assertRaises(TypeError) :
            self.VT3.controle_global_item(4, "douze", conversion=True)#impossible car 'douze' est écrit en toute lettre donc n'est pas convertible en int

    def test_controle_total(self) :
        """Cette méthode vérifie le fonctionnement de controle_total.

        Vérifie d'abord que quand le tableau est valide, cette méthode ne lève pas d'erreur. Puis vérifie que lorsque le tableau n'est pas valide une erreur soit levée.
        """
        #objets valides
        obj_v = self.VT2.controle_types_total(self.VT2_correct)
        self.assertEqual(obj_v, self.VT2_correct)
        self.VT3.controle_global(self.VT3_correct)

        #tableau du mauvais type
        with self.assertRaises(TypeError) :
            self.VT2.controle_global(["blabla", "trois"])

        #tableau n'ayant pas assez de lignes
        with self.assertRaises(ValueError) :
            self.VT2.controle_global([["", "% de bon élèves"]])
        
        #tableau ayant trop de colonnes
        with self.assertRaises(ValueError) :
            VT3_erroné = self.VT3_correct
            VT3_erroné[0].append("Secondes")
            VT3_erroné[0].append("Milisecondes")
            VT3_erroné[1].append(37)
            VT3_erroné[1].append(505)
            self.VT3.controle_global(VT3_erroné)#10 colonnes = 1 de trop
        
        #nom du tableau invalide
        with self.assertRaises(TypeError) :
            del VT3_erroné[0][8]#on supprime l'ancienne valeur incorrecte
            del VT3_erroné[1][8]#on supprime l'ancienne valeur incorrecte
            del VT3_erroné[0][7]#on supprime l'ancienne valeur incorrecte
            del VT3_erroné[1][7]#on supprime l'ancienne valeur incorrecte
            VT3_erroné[0][0] = 287.3
            self.VT3.controle_nom_tableau(VT3_erroné)#le nom du tableau n'est pas un entier
        with self.assertRaises(ValueError) :
            VT3_erroné[0][0] = -28
            self.VT3.controle_nom_tableau(VT3_erroné)#le nom du tableau n'est pas un entier positif
        
        #en-têtes invalides
        with self.assertRaises(TypeError) :
            VT3_erroné[0][0] = 287
            VT3_erroné[0][1] = True
            self.VT3.controle_total(VT3_erroné)#le nom de la première colonne n'est pas un str mais un bool
        with self.assertRaises(TypeError) :
            VT3_erroné[0][1] = "Nom erreur"
            VT3_erroné[1][0] = "54"
            self.VT3.controle_total(VT3_erroné)#le nom de la première ligne n'est pas un int mais un str
        with self.assertRaises(ValueError) :
            VT3_erroné[1][0] = 54#on remplace l'ancienne valeur incorrecte par une valeur correcte
            VT3_erroné[2][0] = -381
            self.VT3.controle_total(VT3_erroné)#le nom de la deuxième ligne n'est pas un nombre entier positif mais négatif
        
        #lignes de longueur différentes
        with self.assertRaises(ValueError) :
            VT3_erroné = self.VT3_correct
            del VT3_erroné[3][5]
            self.VT3.controle_total(VT3_erroné)#ligne 215 : il manque l'heure
        
        #un des éléments contenus est d'un type incorrect
        with self.assertRaises((TypeError, ValueError)) :
            self.VT2.controle_total([["", "% de bon élèves"],["Classe A","12"]])#les éléments contenus doivent être des nombres
        
        #un des éléments contenus est inférieur au minimum
        with self.assertRaises((TypeError, ValueError)) :
            self.VT2.controle_total([["", "% de bon élèves"],["Classe A",-12]])#-12 est inférieur à 0 (le minimum)
        
        #un des éléments contenus est supérieur au maximum
        with self.assertRaises((TypeError, ValueError)) :
            self.VT2.controle_total([["", "% de bon élèves"],["Classe A",102.5]])#102.5 est supérieur à 100 (le maximum)

    def test_controle_total_conversion(self) :
        """Teste la méthode controle_total avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_total convertit au besoin les objets de types incorects.
        """
        #conversion possibles
        obj_v1 = self.VT2.controle_total((["", "% de bon élèves"],["Classe A",12.25]), conversion=True)#conversion du tuple en liste
        self.assertEqual(obj_v1, self.VT2_correct)
        obj_v2 = self.VT2.controle_total([["", "% de bon élèves"],("Classe A","12.25")], conversion=True)
        self.assertEqual(obj_v2, self.VT2_correct)
        VT3_erroné = self.VT3_correct
        VT3_erroné[0][0] = 287.3
        obj_v3 = self.VT3.controle_total(VT3_erroné, conversion=True)#le nom du tableau n'est pas un entier
        self.assertEqual(obj_v3, self.VT3_correct)
        VT3_erroné[0][1] = True
        obj_v4 = self.VT3.controle_total(VT3_erroné, conversion=True)#le nom de la première colonne n'est pas un str mais un bool
        self.assertEqual(obj_v4, self.VT3_correct)
        VT3_erroné[1][0] = "54"
        obj_v5 = self.VT3.controle_total(VT3_erroné, conversion=True)#le nom de la première ligne n'est pas un int mais un str
        self.assertEqual(obj_v5, self.VT3_correct)
        with self.assertRaises(TypeError) :
            self.VT1.controle_total(5.4, conversion=True)#impossible car 5.4 est un flottant donc n'est pas parcourable : la conversion en liste est impossible
        with self.assertRaises(TypeError) :
            self.VT1.controle_total(["test", 5.4], conversion=True)#impossible car 5.4 est un flottant donc n'est pas parcourable : la conversion en liste est impossible

    def test_get_liste_verificateurs(self) :
        """Teste l'affichage de l'attribut liste_verificateurs."""
        get_theorique = """   Identifiant 1       Identifiant 2        Vérificateur    \n         7                   8          ◄types:<class 'int'>, minimum:0, maximum:59►\n         2                  None        ◄types:<class 'str'>, minimum:None, maximum:None►\n         4                  None        ◄types:<class 'int'>, minimum:1, maximum:12►\n         3                  None        ◄types:<class 'int'>, minimum:1, maximum:31►\n         1                  None        ◄types:<class 'str'>, minimum:None, maximum:None►\n         5                  None        ◄types:<class 'int'>, minimum:2000, maximum:2100►\n         6                  None        ◄types:<class 'int'>, minimum:0, maximum:23►\n"""
        self.assertEqual(self.VT3.liste_verificateurs, get_theorique)

    def test_get_types(self) :
        """Teste l'affichage de l'attribut types."""
        types = self.VT2.types
        self.assertEqual(types, list)

    def test_get_minimum(self) :
        """Teste l'affichage de l'attribut minimum."""
        minimum = self.VT3.minimum
        self.assertEqual(minimum, (4,7))

    def test_set_minimum(self) :
        """Teste la modification de l'attribut minimum."""
        self.VT3.minimum = (4,5)
        self.assertEqualVT(self.VT3, [[7, 8, Verificateur(int, 0, 59)], [2, None, Verificateur(str)], [4, None, Verificateur(int, 1,12)], [3, None, Verificateur(int, 1, 31)], [1, None, Verificateur(str)], [5, None, Verificateur(int, 2000, 2100)], [6, None, Verificateur(int, 0, 23)]], minimum=(4,5), maximum = (9, None), nom_tableau=Verificateur(int, 0), en_tete_h=Verificateur(str), en_tete_v=Verificateur(int, 1))
        self.VT3.minimum = (4, 2)
        self.assertEqualVT(self.VT3, [[7, 8, Verificateur(int, 0, 59)], [2, None, Verificateur(str)], [4, None, Verificateur(int, 1,12)], [3, None, Verificateur(int, 1, 31)], [1, None, Verificateur(str)], [5, None, Verificateur(int, 2000, 2100)], [6, None, Verificateur(int, 0, 23)]], minimum=(4,2), maximum = (9, None), nom_tableau=Verificateur(int, 0), en_tete_h=Verificateur(str), en_tete_v=Verificateur(int, 1))
    
    def test_set_minimum_error(self) :
        """Vérifie que set_minimum lève certaines erreurs.

        Vérifie notamment que des erreurs sont levées lorsque nouveau_minimum n'est pas un tuple avec deux nombres entiers positifs supérieurs à 1 et qu'un des deux minima (colonnes ou lignes)est supérieur au maximum.
        """
        with self.assertRaises(TypeError) :
            self.VT1.minimum = "bla"#n'est pas un tuple
            self.assertEqual(self.VT1, VerificateurTableaux())
        with self.assertRaises((TypeError, ValueError)) :
            self.VT1.set_minimum((3))#n'a qu'un seul élément
            self.assertEqual(self.VT1, VerificateurTableaux())
        with self.assertRaises((TypeError, ValueError)) :
            self.VT1.set_minimum((2,3,5,55))#a trop d'éléments
            self.assertEqual(self.VT1, VerificateurTableaux())
        with self.assertRaises(TypeError) :
            self.VT1.set_minimum(("bal",3))#"bal" n'est pas un entier
            self.assertEqual(self.VT1, VerificateurTableaux())
        with self.assertRaises(TypeError) :
            self.VT1.set_minimum((20,None))#None n'est pas un entier
            self.assertEqual(self.VT1, VerificateurTableaux())
        with self.assertRaises(ValueError) :
            self.VT1.set_minimum((-2,3))#-2 est inférieur à 1
            self.assertEqual(self.VT1, VerificateurTableaux())
        with self.assertRaises(ValueError) :
            self.VT1.set_minimum((5,1))#1 est inférieur (strictement) à 1
            self.assertEqual(self.VT1, VerificateurTableaux())
        with self.assertRaises(ValueError) :
            self.VT3.minimum = (120, None)#minimum des colonnes supérieur au maximum (8)
            self.assertEqualVT(self.VT3, [[7, 8, Verificateur(int, 0, 59)], [2, None, Verificateur(str)], [4, None, Verificateur(int, 1,12)], [3, None, Verificateur(int, 1, 31)], [1, None, Verificateur(str)], [5, None, Verificateur(int, 2000, 2100)], [6, None, Verificateur(int, 0, 23)]], minimum=(4,5), maximum = (7, None), nom_tableau=Verificateur(int, 0), en_tete_h=Verificateur(str), en_tete_v=Verificateur(int, 1))
        with self.assertRaises(ValueError) :
            self.VT2.minimum = (2,6)#minimum des lignes supérieur au maximum (5)
            self.assertEqualVT(self.VT2, liste_verificateurs = [[1,3,Verificateur((int, float),minimum=0, maximum=100)]], nom_tableau = Verificateur(str), maximum=(4, 5))

    def test_del_minimum(self) :
        """Teste la suppression de l'attribut minimum."""
        del self.VT3.minimum
        self.assertEqualVT(self.VT3, [[7, 8, Verificateur(int, 0, 59)], [2, None, Verificateur(str)], [4, None, Verificateur(int, 1,12)], [3, None, Verificateur(int, 1, 31)], [1, None, Verificateur(str)], [5, None, Verificateur(int, 2000, 2100)], [6, None, Verificateur(int, 0, 23)]], minimum=(2,2), maximum = (9, None), nom_tableau=Verificateur(int, 0), en_tete_h=Verificateur(str), en_tete_v=Verificateur(int, 1))

    def test_get_maximum(self) :
        """Teste l'affichage de l'attribut maximum."""
        maximum = self.VT3.maximum
        self.assertEqual(maximum, (9, None))

    def test_set_maximum(self) :
        """Teste la modification de l'attribut maximum."""
        self.VT2.maximum = (7, 25)
        self.assertEqualVT(self.VT2, liste_verificateurs = [[1,3,Verificateur((int, float),minimum=0, maximum=100)]], nom_tableau = Verificateur(str), maximum=(7, 25))
        self.VT1.maximum = (None, 2*20)
        self.assertEqualVT(self.VT1, maximum=(None, 2*20))

    def test_set_maximum_error(self) :
        """Vérifie que set_maximum lève certaines erreurs.

        Vérifie notamment que des erreurs sont levées lorsque nouveau_maximum n'est pas un tuple avec deux nombres entiers positifs supérieurs à 1 (ou valent None) et qu'un des deux maxima (colonnes ou lignes) est au minimum lui correspondant.
        """
        with self.assertRaises(TypeError) :
            self.VT1.maximum = "bla"#n'est pas un tuple
            self.assertEqual(self.VT1, VerificateurTableaux())
        with self.assertRaises((TypeError, ValueError)) :
            self.VT1.set_maximum((3))#n'a qu'un seul élément
            self.assertEqual(self.VT1, VerificateurTableaux())
        with self.assertRaises((TypeError, ValueError)) :
            self.VT1.set_maximum((2,3,5,55))#a trop d'éléments
            self.assertEqual(self.VT1, VerificateurTableaux())
        with self.assertRaises(TypeError) :
            self.VT1.set_maximum(("bal",3))#"bal" n'est pas un entier
            self.assertEqual(self.VT1, VerificateurTableaux())
        with self.assertRaises(ValueError) :
            self.VT1.set_maximum((-2,3))#-2 est inférieur à 1
            self.assertEqual(self.VT1, VerificateurTableaux())
        with self.assertRaises(ValueError) :
            self.VT1.set_maximum((5,1))#1 est inférieur (strictement) à 1
            self.assertEqual(self.VT1, VerificateurTableaux())
        with self.assertRaises(ValueError) :
            self.VT3.maximum = (3, None)#maximum colonnes inférieur au minimum (4)
            self.assertEqualVT(self.VT3, [[7, 8, Verificateur(int, 0, 59)], [2, None, Verificateur(str)], [4, None, Verificateur(int, 1,12)], [3, None, Verificateur(int, 1, 31)], [1, None, Verificateur(str)], [5, None, Verificateur(int, 2000, 2100)], [6, None, Verificateur(int, 0, 23)]], minimum=(2,2), maximum = (9, None), nom_tableau=Verificateur(int, 0), en_tete_h=Verificateur(str), en_tete_v=Verificateur(int, 1))

    def test_del_maximum(self) :
        """Teste la suppression de l'attribut maximum."""
        del self.VT2.maximum
        self.assertEqualVT(self.VT2, liste_verificateurs = [[1,3,Verificateur((int, float),minimum=0, maximum=100)]], nom_tableau = Verificateur(str), maximum=(None, None))
    
    def test_get_nom_tableau(self) :
        """Vérifie que get_nom_tableau renvoie l'attribut nom_tableau."""
        nom_tableau = self.VT2.get_nom_tableau()
        self.assertEqual(nom_tableau, Verificateur(str))
    
    def test_set_nom_tableau(self) :
        """Vérifie que set_nom_tableau modifie bien l'attribut nom_tableau."""
        self.VT3.nom_tableau = Verificateur(str)
        self.assertEqualVT(self.VT3, [[7, 8, Verificateur(int, 0, 59)], [2, None, Verificateur(str)], [4, None, Verificateur(int, 1,12)], [3, None, Verificateur(int, 1, 31)], [1, None, Verificateur(str)], [5, None, Verificateur(int, 2000, 2100)], [6, None, Verificateur(int, 0, 23)]], minimum=(4,7), maximum = (9, None), nom_tableau=Verificateur(str), en_tete_h=Verificateur(str), en_tete_v=Verificateur(int, 1))

    def test_del_nom_tableau(self) :
        """Vérife que del_nom_tableau supprime bien l'attribut nom_tableau."""
        del self.VT2.nom_tableau
        self.assertEqualVT(self.VT2, liste_verificateurs = [[1,3,Verificateur((int, float),minimum=0, maximum=100)]], nom_tableau = Verificateur(), maximum=(4, 5))

    def test_get_en_tete_h(self) :
        """Vérifie que get_en_tete_h renvoie bien l'attribut en_tete_h."""
        en_tete_h = self.VT3.get_en_tete_h()
        self.assertEqual(en_tete_h, Verificateur(str))

    def test_set_en_tete_h(self) :
        """Vérifie que set_en_tete_h modifie bien l'attribut en_tete_h."""
        self.VT2.en_tete_h = Verificateur(str)
        self.assertEqualVT(self.VT2, liste_verificateurs = [[1,3,Verificateur((int, float),minimum=0, maximum=100)]], nom_tableau = Verificateur(str), en_tete_h=Verificateur(str), maximum=(4, 5))
        self.VT3.en_tete_h = Verificateur(float, 0, 10)
        self.assertEqualVT(self.VT3, [[7, 8, Verificateur(int, 0, 59)], [2, None, Verificateur(str)], [4, None, Verificateur(int, 1,12)], [3, None, Verificateur(int, 1, 31)], [1, None, Verificateur(str)], [5, None, Verificateur(int, 2000, 2100)], [6, None, Verificateur(int, 0, 23)]], minimum=(4,7), maximum = (9, None), nom_tableau=Verificateur(int,0), en_tete_h=Verificateur(float, 0, 10), en_tete_v=Verificateur(int, 1))
    
    def test_del_en_tete_h(self) :
        """Vérifie que del_en_tete_h supprime bien l'attribut en_tete_h."""
        del self.VT3.en_tete_h
        self.assertEqualVT(self.VT3, [[7, 8, Verificateur(int, 0, 59)], [2, None, Verificateur(str)], [4, None, Verificateur(int, 1,12)], [3, None, Verificateur(int, 1, 31)], [1, None, Verificateur(str)], [5, None, Verificateur(int, 2000, 2100)], [6, None, Verificateur(int, 0, 23)]], minimum=(4,7), maximum = (9, None), nom_tableau=Verificateur(int,0), en_tete_h=Verificateur(), en_tete_v=Verificateur(int, 1))

    def test_get_en_tete_v(self) :
        """Vérifie que get_en_tete_v renvoie bien l'attribut en_tet_v."""
        en_tete_v = self.VT3.get_en_tete_v()
        self.assertEqual(en_tete_v, Verificateur(int, 1))
    
    def test_set_en_tete_v(self) :
        """Vérifie que set_en_tete_v modifie bien l'attribut en_tete_v."""
        self.VT2.en_tete_v = Verificateur(int, 0)
        self.assertEqualVT(self.VT2, liste_verificateurs = [[1,3,Verificateur((int, float),minimum=0, maximum=100)]], nom_tableau = Verificateur(str), en_tete_v=Verificateur(int, 0), maximum=(4, 5))
        import datetime as dt
        self.VT3.en_tete_v = Verificateur(dt.datetime)
        self.assertEqualVT(self.VT3, [[7, 8, Verificateur(int, 0, 59)], [2, None, Verificateur(str)], [4, None, Verificateur(int, 1,12)], [3, None, Verificateur(int, 1, 31)], [1, None, Verificateur(str)], [5, None, Verificateur(int, 2000, 2100)], [6, None, Verificateur(int, 0, 23)]], minimum=(4,7), maximum = (9, None), nom_tableau=Verificateur(int,0), en_tete_h=Verificateur(str), en_tete_v=Verificateur(dt.datetime))
    
    def test_del_en_tete_v(self) :
        """Vérifie que del_en_tete_v supprime bien l'attribut en_tete_v."""
        del self.VT3.en_tete_v
        self.assertEqualVT(self.VT3, [[7, 8, Verificateur(int, 0, 59)], [2, None, Verificateur(str)], [4, None, Verificateur(int, 1,12)], [3, None, Verificateur(int, 1, 31)], [1, None, Verificateur(str)], [5, None, Verificateur(int, 2000, 2100)], [6, None, Verificateur(int, 0, 23)]], minimum=(4,7), maximum = (9, None), nom_tableau=Verificateur(int,0), en_tete_h=Verificateur(str), en_tete_v=Verificateur())

    def test_conversion(self) :
        """Teste la méthode _conversion.
        
        Vérifie que la méthode convertit bien un objet de type invalide en un objet de type valide, lorsque c'est possible.
        """
        #conversion possibles
        obj_v1 = self.VT2._conversion((["", "% de bon élèves"],["Classe A",12.25]))#conversion du tuple en liste
        self.assertEqual(obj_v1, self.VT2_correct)
        obj_v2 = self.VT2._conversion([["", "% de bon élèves"],("Classe A",12.25)])
        self.assertEqual(obj_v2, self.VT2_correct)
        obj_v3 = self.VT1._conversion(["test", (5.4, 6.9)])
        self.assertEqual(obj_v3, [["t","e","s","t"], [5.4, 6.9]])
        #conversion impossible
        with self.assertRaises(TypeError) :
            self.VT1._conversion(5.4)#impossible car 5.4 est un flottant donc n'est pas parcourable : la conversion en liste est impossible
        with self.assertRaises(TypeError) :
            self.VT1._conversion(["test", 5.4])#impossible car 5.4 est un flottant donc n'est pas parcourable : la conversion en liste est impossible


if __name__ == "__main__" :
    unittest.main()