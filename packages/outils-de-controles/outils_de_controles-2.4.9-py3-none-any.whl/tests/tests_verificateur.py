"""Ce module teste avec unittest la classe Verificateur (et son module)."""

import unittest
import os
import sys

#On change le dossier de travail (cwd) pour pouvoir appeler les fichiers via des chemins relatifs
os.chdir(os.path.dirname(__file__))#On change le dossier de travail en appellant le nom du dossier qui contient ce fichier (le dossier tests)
os.chdir("..")#On rechange le dossier de travail en prenant le dossier parent du dossier tests (le dossier outils_de_controles)
sys.path.append(os.getcwd())#ligne nécessaire à l'importation du module verificateur

from outils_de_controles.verificateur import *

class TestVerificateur(unittest.TestCase) :
    """Classe qui teste la classe Verificateur.

    Vérifie que la classe verificateur du package outils_de_controles soit conforme aux spécifications : création, affichage, vérification des objets, modification des attributs ...
    """

    def assertEqualVerificateur(self, verificateur, types=None, minimum=None, maximum=None) :
        """Cette méthode vérifie si deux objets Verificateur sont égaux.

        Cette methode compare chaque attribut à la valeur fournie.
        """
        if verificateur.types == types and verificateur.minimum == minimum and verificateur.maximum == maximum :
            return self.assertEqual(0,0)#l'objet verificateur est égal à la valeur théorique
        else :
            raise AssertionError(repr(verificateur) + " != " + repr(Verificateur(types, minimum, maximum)))

    def setUp(self) :
        """Cette méthode prépare l'exécution des tests.
        
        Cette méthode crée pour cela des objets Verificateur.
        """
        self.V1 = Verificateur(int, 0, 10)
        self.V2 = Verificateur((int, float), 0.5, 130)
        self.V3 = Verificateur(types=bool)
        self.V4 = Verificateur(types=int, maximum=60)

    def test_init(self) :
        """Méthode testant l'initialisation des objets Verificateur.

        Vérifie que l'objet créé est conforme aux arguments passés en paramètres.
        """
        self.assertEqualVerificateur(self.V1, int, 0, 10) 
        self.assertEqualVerificateur(self.V2, (int,float), 0.5, 130)
        self.assertEqualVerificateur(self.V3, bool)
        self.assertEqualVerificateur(self.V4, int, None, 60)
    
    def test_str(self) :
        """Cette méthode teste la méthode __str__ de la classe Verificateur.
        
        Cette méthode vérifie que __str__ renvoie bien une chaine avec le/les types valides, les valeurs minimale et maximale autorisées.
        """
        str_V1 = """◄types:<class 'int'>, minimum:0, maximum:10►"""
        self.assertEqual(str(self.V1),str_V1)
        str_V2 = """◄types:(<class 'int'>, <class 'float'>), minimum:0.5, maximum:130►"""
        self.assertEqual(str(self.V2), str_V2)
    
    def test_repr(self) :
        """Cette méthode teste la méthode __repr__ de la classe Verificateur.
        
        Cette méthode vérifie que __repr__ renvoie bien une chaine avec le nom du package, celui de la classe, et les attributs de l'objet.
        """
        repr_V1 = """outils_de_controles.Verificateur(types=<class 'int'>, minimum=0, maximum=10)"""
        self.assertEqual(repr(self.V1), repr_V1)
        repr_V2 = """outils_de_controles.Verificateur(types=(<class 'int'>, <class 'float'>), minimum=0.5, maximum=130)"""
        self.assertEqual(repr(self.V2), repr_V2)
    
    def test_eq(self) :
        """Cette méthode teste la rméthode __eq__ de la classe Verificateur."""
        autre_objet1 = Verificateur(int, 0, 10)
        self.assertEqual(self.V1 == autre_objet1, True)
        autre_objet2 = Verificateur((int, float), maximum=130)
        self.assertEqual(self.V2 == autre_objet2, False)


    def test_controle_types(self) :
        """Cette méthode teste la méthode controle_types de la classe testée.

        Dans une première partie, cette méthode vérifie que lorsque l'objet contrôlé est d'un type valide aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque le type n'est pas valide, une erreur est bien levée.
        """
        #objets valides
        obj_v1 = self.V1.controle_types(5)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, 5)
        obj_v2 = self.V2.controle_types(56)
        self.assertEqual(obj_v2, 56)
        self.V2.controle_types(0.75)
        self.V3.controle_types(True)
        self.V4.controle_types(-5)
        #la méthode doit lever des exceptions car les objets ne sont pas valides
        with self.assertRaises(TypeError) :
            self.V1.controle_types(1.5)
        with self.assertRaises(TypeError) :
            self.V2.controle_types("une chaine de caractères")
    
    def controle_types_conversion(self) :
        """Teste la méthode controle_types avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_types convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.V1.controle_types(5, conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, 5)
        obj_v2 = self.V2.controle_types("56", conversion=True)#conversion en int
        self.assertEqual(obj_v2, 56)
        with self.assertRaises(TypeError) :
            self.V1.controle_types("5.4", conversion=True)#impossible car 5.4 est un flottant donc la conversion possible est de str à float

    def test_controle_types_total(self) :
        """Cette méthode teste la méthode controle_types_total.

        Dans une première partie, cette méthode vérifie que lorsque l'objet contrôlé est d'un type valide aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque le type n'est pas valide, une erreur est bien levée.
        """
        #objets valides
        obj_v1 = self.V1.controle_types_total(5)
        self.assertEqual(obj_v1, 5)
        obj_v2 = self.V2.controle_types_total(56)
        self.assertEqual(obj_v2, 56)
        self.V2.controle_types_total(0.75)
        self.V3.controle_types_total(True)
        self.V4.controle_types_total(-5)
        #la méthode doit lever des exceptions car les objets ne sont pas valides
        with self.assertRaises(TypeError) :
            self.V1.controle_types_total(1.5)
        with self.assertRaises(TypeError) :
            self.V2.controle_types_total("une chaine de caractères")

    def test_controle_types_total_conversion(self) :
        """Teste controle_types_total avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_types_total convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.V1.controle_types_total(5, conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, 5)
        obj_v2 = self.V2.controle_types_total("56", conversion=True)#conversion en int
        self.assertEqual(obj_v2, 56)
        with self.assertRaises(TypeError) :
            self.V1.controle_types_total("5.4", conversion=True)#impossible car 5.4 est un flottant donc la conversion possible est de str à float

    def test_controle_minimum(self) :
        """Cette méthode teste la méthode controle_minimum de la classe testée.

        Dans une première partie, cette méthode vérifie que lorsque l'objet contrôlé est valide aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque l'objet est inférieur au minimum, une erreur est bien levée.
        """
        #objet valides
        obj_v1 = self.V1.controle_minimum(5)
        self.assertEqual(obj_v1, 5)
        obj_v2 = self.V2.controle_minimum(56)
        self.assertEqual(obj_v2, 56)
        self.V2.controle_minimum(0.75)
        self.V3.controle_minimum(True)
        self.V4.controle_minimum(-5)
        #la méthode doit lever des exceptions car les objets ne sont pas valides
        with self.assertRaises(ValueError) :
            self.V1.controle_minimum(-1)
        with self.assertRaises(ValueError) :
            self.V2.controle_minimum(0.25)
        
    def test_controle_maximum(self) :
        """Cette méthode teste la méthode controle_maximum de la classe testée.

        Dans une première partie, cette méthode vérifie que lorsque l'objet contrôlé est valide aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque l'objet est supérieur au maximum, une erreur est bien levée.
        """
        #objet valides
        obj_v1 = self.V1.controle_maximum(5)
        self.assertEqual(obj_v1, 5)
        obj_v2 = self.V2.controle_maximum(56)
        self.assertEqual(obj_v2, 56)
        self.V2.controle_maximum(0.75)
        self.V3.controle_maximum(True)
        self.V4.controle_maximum(-5)
        #la méthode doit lever des exceptions car les objets ne sont pas valides
        with self.assertRaises(ValueError) :
            self.V1.controle_maximum(11)
        with self.assertRaises(ValueError) :
            self.V2.controle_maximum(251)
    
    def test_controle_global(self) :
        """Cette méthode teste la méthode controle_global de la classe testée.

        Dans une première partie, cette méthode vérifie que lorsque l'objet contrôlé est valide aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque l'objet n'est pas valide, une erreur est bien levée.
        """
        #objets valides
        obj_v1 = self.V1.controle_global(5)
        self.assertEqual(obj_v1, 5)
        obj_v2 = self.V2.controle_global(56)
        self.assertEqual(obj_v2, 56)
        self.V2.controle_global(0.75)
        self.V3.controle_global(True)
        self.V4.controle_global(-5)
        #la méthode doit lever des exceptions car les objets ne sont pas valides
        with self.assertRaises(TypeError) :
            self.V1.controle_global(1.5)
        with self.assertRaises(TypeError) :
            self.V2.controle_global("une chaine de caractères")
        with self.assertRaises(ValueError) :
            self.V1.controle_global(-1)
        with self.assertRaises(ValueError) :
            self.V2.controle_global(251)
        with self.assertRaises(Exception) :
            self.V1.controle_global(142.3)
    
    def test_controle_global_conversion(self) :
        """Teste controle_global avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_global convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.V1.controle_global(5, conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, 5)
        obj_v2 = self.V2.controle_global("56", conversion=True)#conversion en int
        self.assertEqual(obj_v2, 56)
        with self.assertRaises(TypeError) :
            self.V1.controle_global("5.4", conversion=True)#impossible car 5.4 est un flottant donc la conversion possible est de str à float
        with self.assertRaises(ValueError) :
            self.V2.controle_global("251", conversion=True)

    def test_controle_total(self) :
        """Cette méthode teste la méthode controle_total de la classe testée.

        Dans une première partie, cette méthode vérifie que lorsque l'objet contrôlé est valide aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque l'objet n'est pas valide, une erreur est bien levée.
        """
        #objets valides
        obj_v1 = self.V1.controle_total(5)
        self.assertEqual(obj_v1, 5)
        obj_v2 = self.V2.controle_total(56)
        self.assertEqual(obj_v2, 56)
        self.V2.controle_total(0.75)
        self.V3.controle_total(True)
        self.V4.controle_total(-5)
        #la méthode doit lever des exceptions car les objets ne sont pas valides
        with self.assertRaises(TypeError) :
            self.V1.controle_total(1.5)
        with self.assertRaises(TypeError) :
            self.V2.controle_total("une chaine de caractères")
        with self.assertRaises(ValueError) :
            self.V1.controle_total(-1)
        with self.assertRaises(ValueError) :
            self.V2.controle_total(251)
        with self.assertRaises(Exception) :
            self.V1.controle_total(142.3)

    def test_controle_total_conversion(self) :
        """Teste controle_total avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_total convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.V1.controle_total(5, conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, 5)
        obj_v2 = self.V2.controle_total("56", conversion=True)#conversion en int
        self.assertEqual(obj_v2, 56)
        with self.assertRaises(TypeError) :
            self.V1.controle_total("5.4", conversion=True)#impossible car 5.4 est un flottant donc la conversion possible est de str à float
        with self.assertRaises(ValueError) :
            self.V2.controle_total("251", conversion=True)

    def test_get_types(self) :
        """Teste l'affichage de l'attribut types."""
        types = self.V1.types
        self.assertEqual(types, int)
    
    def test_set_types(self) :
        """Teste la modification de l'attribut types."""
        self.V4.types = float
        self.assertEqualVerificateur(self.V4, float, maximum=60)
    
    def test_del_types(self) :
        """Teste la suppression de l'attribut types."""
        del self.V2.types
        self.assertEqualVerificateur(self.V2, minimum=0.5, maximum=130)

    def test_get_minimum(self) :
        """Teste l'affichage de l'attribut minimum."""
        minimum = self.V2.minimum
        self.assertEqual(minimum, 0.5)
 
    def test_set_minimum(self) :
        """Teste la modification de l'attribut minimum."""
        self.V1.minimum = 2
        self.assertEqualVerificateur(self.V1, int, 2, 10)

    def test_del_minimum(self) :
        """Teste la suppression de l'attribut minimum."""
        del self.V1.minimum
        self.assertEqualVerificateur(self.V1, int, None, 10)

    def test_get_maximum(self) :
        """Teste l'affichage de l'attribut maximum."""
        maximum = self.V4.maximum
        self.assertEqual(maximum, 60)

    def test_set_maximum(self) :
        """Teste la modification de l'attribut maximum."""
        self.V2.maximum = 5.54
        self.assertEqualVerificateur(self.V2, (int, float), 0.5, 5.54)

    def test_del_maximum(self) :
        """Teste la suppression de l'attribut maximum."""
        del self.V4.maximum
        self.assertEqualVerificateur(self.V4, int)

    def test_conversion(self) :
        """Teste la méthode _conversion.
        
        Vérifie que la méthode convertit bien un objet de type invalide en un objet de type valide, lorsque c'est possible.
        """
        #conversion possibles
        obj_v1 = self.V1._conversion("5")
        self.assertEqual(obj_v1, 5)
        obj_v2 = self.V1._conversion(6.0)
        self.assertEqual(obj_v2, 6)
        obj_v3 = self.V2._conversion("5.4")
        self.assertEqual(obj_v3, 5.4)
        #conversion impossible
        with self.assertRaises(TypeError) :
            self.V1._conversion("5.4")#impossible car 5.4 est un flottant donc la conversion possible est de str à float

if __name__ == "__main__" :
    unittest.main()
