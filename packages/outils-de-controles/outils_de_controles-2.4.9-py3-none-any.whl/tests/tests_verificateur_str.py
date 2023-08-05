"""Ce module teste avec unittest la classe VerificateurStr (et son module)."""

import os
import sys
import unittest
import re

#On change le dossier de travail (cwd) pour pouvoir appeler les fichiers via des chemins relatifs
os.chdir(os.path.dirname(__file__))#On change le dossier de travail en appellant le nom du dossier qui contient ce fichier (le dossier tests)
os.chdir("..")#On rechange le dossier de travail en prenant le dossier parent du dossier tests (le dossier outils_de_controles)
sys.path.append(os.getcwd())#ligne nécessaire à l'importation du module verificateur

from outils_de_controles.verificateur_str import *

class TestVerificateur(unittest.TestCase) :
    """Classe qui teste la classe VerificateurStr.

    Vérifie que la classe verificateur du package outils_de_controles soit conforme aux spécifications : création, affichage, vérification des objets, modification des attributs ...
    """

    def assertEqualVS(self, VS, minimum=0, maximum=None, regex=r"") :
        """Cette méthode vérifie si deux objets VerificateurStr sont égaux.

        Cette methode compare chaque attribut à la valeur fournie.
        """
        if VS.minimum == minimum and VS.maximum == maximum and VS.regex == regex :
            return self.assertEqual(0,0)#l'objet verificateur est égal à la valeur théorique
        else :
            raise AssertionError(repr(VS) + " != " + repr(VerificateurStr(minimum, maximum, regex)))

    def setUp(self) :
        """Cette méthode prépare l'exécution des tests.
        
        Cette méthode crée pour cela des objets VerificateurStr.
        """
        self.VS1 = VerificateurStr()
        self.VS2 = VerificateurStr(10, 17, r"^((\+33[ -]?)|0)[1-9]([ -]?[0-9]{2}){4}$")#pour vérifier un numéro de téléphone
        self.VS3 = VerificateurStr(7, 7, re.compile(r"[a-z-]{7}"))#pour vérifier que c'est un nom commun à 7 lettres
        self.VS4 = VerificateurStr(regex=r"^[A-Za-z0-9\.-]+\@[A-Za-z0-9-]+\.[a-z]{2,3}$")#vérifie que l'on a saisi une adresse e-mail
        self.VS5 = VerificateurStr(minimum=1, regex=r"^[0-9]+[A-B]?$")#vérifie qu'il n'y a que des chiffres et a ou b à la fin (ex. code d'entré pour un imeuble)

    def test_init(self) :
        """Méthode testant l'initialisation des objets VerificateurStr.

        Vérifie que l'objet créé est conforme aux arguments passés en paramètres.
        """
        self.assertEqualVS(self.VS1) 
        self.assertEqualVS(self.VS2, 10, 17,  r"^((\+33[ -]?)|0)[1-9]([ -]?[0-9]{2}){4}$")
        self.assertEqualVS(self.VS3, 7, 7, r"[a-z-]{7}")
        self.assertEqualVS(self.VS4, 0, None, r"^[A-Za-z0-9\.-]+\@[A-Za-z0-9-]+\.[a-z]{2,3}$")
        self.assertEqualVS(self.VS5, 1, None, r"^[0-9]+[A-B]?$")
    
    def test_str(self) :
        """Cette méthode teste la méthode __str__ de la classe VerificateurStr.
        
        Cette méthode vérifie que __str__ renvoie bien une chaine avec le/les types valides, les valeurs minimale et maximale autorisées.
        """
        str_VS1 = """◄minimum:0, maximum:None, regex:''►"""
        self.assertEqual(str(self.VS1),str_VS1)
        str_VS2 = """◄minimum:10, maximum:17, regex:'^((\\+33[ -]?)|0)[1-9]([ -]?[0-9]{2}){4}$'►"""
        self.assertEqual(str(self.VS2), str_VS2)
    
    def test_repr(self) :
        """Cette méthode teste la méthode __repr__ de VerificateurStr.
        
        Cette méthode vérifie que __repr__ renvoie bien une chaine avec le nom du package, celui de la classe, et les attributs de l'objet.
        """
        repr_VS1 = """outils_de_controles.VerificateurStr(minimum=0, maximum=None, regex='')"""
        self.assertEqual(repr(self.VS1), repr_VS1)
        repr_VS2 = """outils_de_controles.VerificateurStr(minimum=10, maximum=17, regex='^((\\\\+33[ -]?)|0)[1-9]([ -]?[0-9]{2}){4}$')"""
        self.assertEqual(repr(self.VS2), repr_VS2)
    
    def test_eq(self) :
        """Cette méthode teste la méthode __eq__ de la classe Verificateur."""
        autre_objet2 = VerificateurStr(10, 17, r"^((\+33[ -]?)|0)[1-9]([ -]?[0-9]{2}){4}$")
        self.assertEqual(self.VS2 == autre_objet2, True)
        autre_objet3 = VerificateurStr(7, 7, r"[a-z-]{7}")
        self.assertEqual(self.VS3 == autre_objet3, True)
        autre_objet3b = VerificateurStr(7, 8, r"[a-z-]{7}")
        self.assertEqual(self.VS3 == autre_objet3b, False)
        autre_objet3c = VerificateurStr(7, 7, r"[a-z]{7}")
        self.assertEqual(self.VS3 == autre_objet3c, False)

    def test_controle_types(self) :
        """Cette méthode teste la méthode controle_types de la classe testée.

        Dans une première partie, cette méthode vérifie que lorsque l'objet contrôlé est d'un type valide, c'est-à-dire un str aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque le type n'est pas valide, une erreur est bien levée.
        """
        #objets valides
        obj_v1 = self.VS1.controle_types("5")#obj_v1 pour objet valide n°1
        self.assertEqual(obj_v1, "5")
        obj_v2 = self.VS2.controle_types("04 71 45 56 30")#idem mais n°2 ...
        self.assertEqual(obj_v2, "04 71 45 56 30")
        obj_v3 = self.VS2.controle_types("+33-6-54-88-59-70")
        self.assertEqual(obj_v3, "+33-6-54-88-59-70")
        obj_v4 = self.VS3.controle_types("canette")
        self.assertEqual(obj_v4, "canette")
        self.VS4.controle_types("c.b.e.python@gmail.com")#cette ligne teste la rétro compatibilité avec les versions antérieures à la v2.4.0
        #la méthode doit lever des exceptions car les objets ne sont pas valides
        with self.assertRaises(TypeError) :
            self.VS1.controle_types(1.5)
        with self.assertRaises(TypeError) :
            self.VS2.controle_types(True)
    
    def test_controle_types_conversion(self) :
        """Teste la méthode controle_types avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_types convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VS1.controle_types("5", conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, "5")
        obj_v2 = self.VS1.controle_types(5, conversion=True)#conversion en int
        self.assertEqual(obj_v2, "5")
        obj_v3 = self.VS5.controle_types(1459, conversion=True)
        self.assertEqual(obj_v3, "1459")

    def test_controle_types_total(self) :
        """Cette méthode teste la méthode controle_types_total.

        Dans une première partie, cette méthode vérifie que lorsque l'objet contrôlé est d'un type valide, c'est-à-dire du type str, aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque le type n'est pas valide, une erreur est bien levée.
        """
        #objets valides
        obj_v1= self.VS1.controle_types_total("5")#obj_v1 pour objet valide n°1
        self.assertEqual(obj_v1, "5")
        obj_v2 = self.VS2.controle_types_total("04 71 45 56 30")
        self.assertEqual(obj_v2, "04 71 45 56 30")
        self.VS2.controle_types_total("+33-6-54-88-59-70")
        self.VS3.controle_types_total("canette")
        self.VS4.controle_types_total("c.b.e.python@gmail.com")
        #la méthode doit lever des exceptions car les objets ne sont pas valides
        with self.assertRaises(TypeError) :
            self.VS1.controle_types_total(1.5)
        with self.assertRaises(TypeError) :
            self.VS2.controle_types_total(False)

    def test_controle_types_total_conversion(self) :
        """Teste controle_types_total avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_types_total convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VS1.controle_types_total("5", conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, "5")
        obj_v2 = self.VS1.controle_types_total(5, conversion=True)#conversion en int
        self.assertEqual(obj_v2, "5")
        obj_v3 = self.VS5.controle_types_total(1459, conversion=True)
        self.assertEqual(obj_v3, "1459")

    def test_controle_minimum(self) :
        """Cette méthode teste la méthode controle_minimum de la classe testée.

        Vérifie que lorsque la longueur de la chaine est correcte la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque la chaine est trop courte une ValueError est levée.
        """
        #objet valides
        obj_v1 = self.VS1.controle_minimum("5")#obj_v1 pour objet valide n°1
        self.assertEqual(obj_v1, "5")
        obj_v2 = self.VS2.controle_minimum("04 71 45 56 30")
        self.assertEqual(obj_v2, "04 71 45 56 30")
        self.VS2.controle_minimum("+33-6-54-88-59-70")
        self.VS3.controle_minimum("canette")
        self.VS4.controle_minimum("c.b.e.python@gmail.com")
        #la méthode doit lever des exceptions car les objets ne sont pas valides
        with self.assertRaises(ValueError) :
            self.VS2.controle_minimum("31")
        with self.assertRaises(ValueError) :
            self.VS3.controle_minimum("canard")
        
    def test_controle_maximum(self) :
        """Cette méthode teste la méthode controle_maximum de la classe testée.

        Vérifie que lorsque la longueur de la chaine est correcte la méthode testée ne lève pas d'erreurs. Vérifie ensuite que lorsque la chaine  est trop longue une ValueError est levée.
        """
        #objet valides
        obj_v1 = self.VS1.controle_maximum("5")#obj_v1 pour objet valide n°1
        self.assertEqual(obj_v1, "5")
        obj_v2 = self.VS2.controle_maximum("04 71 45 56 30")
        self.assertEqual(obj_v2, "04 71 45 56 30")
        self.VS2.controle_maximum("+33-6-54-88-59-70")
        self.VS3.controle_maximum("canette")
        self.VS4.controle_maximum("c.b.e.python@gmail.com")
        #la méthode doit lever des exceptions car les objets ne sont pas valides
        with self.assertRaises(ValueError) :
            self.VS2.controle_maximum("+33 6 54 88 59 70 84")
        with self.assertRaises(ValueError) :
            self.VS3.controle_maximum("canetons")
    
    def test_controle_regex(self) :
        """Cette méthode testse la méthode controle_regex de la classe testée.
        
        Vérifie que lorsque la chaine correspond à l'expression régulière la méthode testée ne lève pas d'erreurs. Vérifie que lorsque la chaine est incorecte, une erreur est levée.
        """
        #objet valides
        obj_v1 = self.VS1.controle_regex("5")
        self.assertEqual(obj_v1, "5")
        obj_v2 = self.VS2.controle_regex("04 71 45 56 30")
        self.assertEqual(obj_v2, "04 71 45 56 30")
        self.VS2.controle_regex("+33-6-54-88-59-70")
        self.VS3.controle_regex("canette")
        self.VS4.controle_regex("c.b.e.python@gmail.com")
        #la méthode doit lever des exceptions car les objets ne sont pas valides
        with self.assertRaises(ValueError) :
            self.VS2.controle_regex("065 488597084")#espace en trop entre le 5 et le 4
        with self.assertRaises(ValueError) :
            self.VS4.controle_regex("canetons.du.bled.gmail.com")#il n'y a pas de @
        
    def test_controle_global(self) :
        """Cette méthode teste la méthode controle_global de la classe testée.

        Dans une première partie, cette méthode vérifie que lorsque l'objet contrôlé est valide aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque l'objet n'est pas valide, une erreur est bien levée.
        """
        #objet valides
        obj_v1 = self.VS1.controle_global("5")
        self.assertEqual(obj_v1, "5")
        obj_v2 = self.VS2.controle_global("04 71 45 56 30")
        self.assertEqual(obj_v2, "04 71 45 56 30")
        self.VS2.controle_global("+33-6-54-88-59-70")
        self.VS3.controle_global("canette")
        self.VS4.controle_global("c.b.e.python@gmail.com")
        #la méthode doit lever des exceptions car les objets ne sont pas valides
        with self.assertRaises(TypeError) :
            self.VS1.controle_global(1.5)#type incorrect
        with self.assertRaises(TypeError) :
            self.VS2.controle_global(True)#idem
        with self.assertRaises(ValueError) :
            self.VS3.controle_global("canard")#chaine trop courte
        with self.assertRaises(ValueError) :
            self.VS2.controle_global("+33 6 54 88 59 70 84")#chaine trop longue
        with self.assertRaises(ValueError) :
            self.VS4.controle_global("canetons.du.bled.gmail.com")#chaine ne correspondant pas à la regex : il n'y a pas de @

    def test_controle_global_conversion(self) :
        """Teste controle_global avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_global convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VS1.controle_global("5948A", conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, "5948A")
        obj_v2 = self.VS1.controle_types_total(5, conversion=True)#conversion en int
        self.assertEqual(obj_v2, "5")
        obj_v3 = self.VS5.controle_global(1459, conversion=True)
        self.assertEqual(obj_v3, "1459")

    def test_controle_total(self) :
        """Cette méthode teste la méthode controle_total de la classe testée.

        Dans une première partie, cette méthode vérifie que lorsque l'objet contrôlé est valide aucune erreur n'est levée. Dans un deuxième temps, on vérifie que lorsque l'objet n'est pas valide, une erreur est bien levée.
        """
        #objet valides
        obj_v1 = self.VS1.controle_total("5")
        self.assertEqual(obj_v1, "5")
        obj_v2 = self.VS2.controle_total("04 71 45 56 30")
        self.assertEqual(obj_v2, "04 71 45 56 30")
        self.VS2.controle_total("+33-6-54-88-59-70")
        self.VS3.controle_total("canette")
        self.VS4.controle_total("c.b.e.python@gmail.com")
        #la méthode doit lever des exceptions car les objets ne sont pas valides
        with self.assertRaises(TypeError) :
            self.VS1.controle_total(1.5)#type incorrect
        with self.assertRaises(TypeError) :
            self.VS2.controle_total(True)#idem
        with self.assertRaises(ValueError) :
            self.VS3.controle_total("canard")#chaine trop courte
        with self.assertRaises(ValueError) :
            self.VS2.controle_total("+33 6 54 88 59 70 84")#chaine trop longue
        with self.assertRaises(ValueError) :
            self.VS4.controle_total("canetons.du.bled.gmail.com")#chaine ne correspondant pas à la regex : il n'y a pas de @

    def test_controle_total_conversion(self) :
        """Teste controle_total avec utilisation de la conversion.
        
        Vérifie que quand conversion est vrai, controle_total convertit au besoin les objets de types incorects.
        """
        #objets valides
        obj_v1 = self.VS1.controle_total("5948A", conversion=True)#obj_v1 pour objet_valide n°1
        self.assertEqual(obj_v1, "5948A")
        obj_v2 = self.VS1.controle_total(5, conversion=True)#conversion en int
        self.assertEqual(obj_v2, "5")
        obj_v3 = self.VS5.controle_total(1459, conversion=True)
        self.assertEqual(obj_v3, "1459")

    def test_get_types(self) :
        """Teste l'affichage de l'attribut types."""
        types = self.VS1.types
        self.assertEqual(types, str)

    def test_get_minimum(self) :
        """Teste l'affichage de l'attribut minimum."""
        minimum = self.VS2.minimum
        self.assertEqual(minimum, 10)
 
    def test_set_minimum(self) :
        """Teste la modification de l'attribut minimum."""
        self.VS1.minimum = 2
        self.assertEqualVS(self.VS1, 2)
    
    def test_set_minimum_error(self) :
        """Vérifie que set_minimum lève certaines erreurs.

        Vérifie notamment que des erreurs sont levées lorsque nouveau_minimum n'est pas un nombre entier positif (ou nul) et qu'il est supérieur au maximum.
        """
        with self.assertRaises(TypeError) :
            self.VS1.minimum = "bla"#n'est pas un entier
            self.assertEqual(self.VS1, VerificateurStr())
        with self.assertRaises(ValueError) :
            self.VS1.set_minimum(-2)#n'est pas un entier positif
            self.assertEqual(self.VS1, VerificateurStr())
        with self.assertRaises(ValueError) :
            self.VS3.minimum = 10#minimum supérieur au maximum (3)
            self.assertEqualVS(self.VS3, 7, 7, r"[a-z-]{7}")

    def test_del_minimum(self) :
        """Teste la suppression de l'attribut minimum."""
        del self.VS2.minimum
        self.assertEqualVS(self.VS2, 0, 17, r"^((\+33[ -]?)|0)[1-9]([ -]?[0-9]{2}){4}$")

    def test_get_maximum(self) :
        """Teste l'affichage de l'attribut maximum."""
        maximum = self.VS2.maximum
        self.assertEqual(maximum, 17)

    def test_set_maximum(self) :
        """Teste la modification de l'attribut maximum."""
        self.VS1.maximum = 5
        self.assertEqualVS(self.VS1, 0, 5)
    
    def test_set_maximum_error(self) :
        """Vérifie que set_maximum lève certaines erreurs.

        Vérifie notamment que des erreurs sont levées lorsque nouveau_maximum n'est pas un nombre entier positif (ou nul) et qu'il est inférieur au minimum.
        """
        with self.assertRaises(TypeError) :
            self.VS1.maximum = 0.3#n'est pas un entier
        self.assertEqual(self.VS1, VerificateurStr())
        with self.assertRaises(ValueError) :
            self.VS1.set_maximum(-2)#n'est pas un entier positif
        self.assertEqual(self.VS1, VerificateurStr())
        with self.assertRaises(ValueError) :
            self.VS2.maximum = 0#maximum inférieur au minimum (1)
        self.assertEqualVS(self.VS2, 10, 17, r"^((\+33[ -]?)|0)[1-9]([ -]?[0-9]{2}){4}$")

    def test_del_maximum(self) :
        """Teste la suppression de l'attribut maximum."""
        del self.VS3.maximum
        self.assertEqualVS(self.VS3, 7, None, r"[a-z-]{7}")

    def test_get_regex(self) :
        """Teste l'affichage de l'attribut regex."""
        regex = self.VS4.regex
        self.assertEqual(regex, r"^[A-Za-z0-9\.-]+\@[A-Za-z0-9-]+\.[a-z]{2,3}$")
    
    def test_set_regex(self) :
        """Teste la modification de l'attribut regex."""
        self.VS1.regex = r"[0-9]+"
        self.assertEqualVS(self.VS1, 0, None, r"[0-9]+")
    
    def test_del_regex(self) :
        """Teste la suppression de l'attribut regex."""
        del self.VS3.regex
        self.assertEqualVS(self.VS3, 7, 7, r"")

    def test_conversion(self) :
        """Teste la méthode _conversion.
        
        Vérifie que la méthode convertit bien un objet de type invalide enun objet de type valide, lorsque c'est possible.
        """
        #conversion possibles
        obj_v1 = self.VS5._conversion(5948)
        self.assertEqual(obj_v1, "5948")
        obj_v2 = self.VS1._conversion(True)
        self.assertEqual(obj_v2, "True")
        obj_v3 = self.VS1._conversion(5.4)
        self.assertEqual(obj_v3, "5.4")

if __name__ == "__main__" :
    unittest.main()
