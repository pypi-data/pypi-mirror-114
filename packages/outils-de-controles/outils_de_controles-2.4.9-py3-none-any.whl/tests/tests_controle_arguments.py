"""Ce module teste avec unittest le module controle_arguments."""

import unittest
import os
import sys

#On change le dossier de travail (cwd) pour pouvoir appeler les fichiers via des chemins relatifs
os.chdir(os.path.dirname(__file__))#On change le dossier de travail en appellant le nom du dossier qui contient ce fichier (le dossier tests)
os.chdir("..")#On rechange le dossier de travail en prenant le dossier parent du dossier tests (le dossier outils_de_controles)
sys.path.append(os.getcwd())#ligne nécessaire à l'importation du module controle_arguments

from outils_de_controles.controle_arguments import *
from outils_de_controles.verificateur import *
from outils_de_controles.verificateur_str import *
from outils_de_controles.verificateur_arguments import *
from outils_de_controles.verificateur_listes import *

@controle_types(bool, int, nom=str, surnom=(str,int))
def F2TA(a,b, nom="", surnom=0) :
    """Fonction utile au test d'un décorateur.

    Fonction de tests n°2. Controle_types, grâce la syntaxe de l'Ancienne version, modifie la définition de cette fonction. (D'où le nom de F2TA).Ensuite les fonctions de tests appellent cette fonction, et vérifient que le décorateur fonctionne comme prévu.
    """
    return (2, a, b, nom, surnom)#cette méthode renvoie 2 car c'est la deuxième méthode/fonction, puis elle renvoie les arguments passés
    #Cette méthode d'indentification permet de vérifier que la fonction est bien exécutée (si aucune d'erreur est levée par le décorateur).

VA4 = VerificateurArguments([0, None, Verificateur(bool)], [1, 'b', Verificateur(int)], [2, "nom", VerificateurStr()], [3, "surnom", Verificateur((str, int))])
@controle_types(VA4)
def F4TN(a,b, nom="", surnom=0) :
    """Fonction utile au test d'un décorateur.

    Fonction de tests n°4. Controle_Types, grâce à la syntaxe de la Nouvelle version, modifie la définition de cette fonction. (D'où le nom de F4TN). Ensuite les fonctions de tests appellent cette fonction, et vérifient que le décorateur fonctionne comme prévu.
    """
    return (4, a, b, nom, surnom)#cette méthode renvoie 4 car c'est la quatrième méthode/fonction, puis elle renvoie les arguments passés
    #Cette méthode d'indentification permet de vérifier que la fonction est bien exécutée (si aucune d'erreur est levée par le décorateur).

@controle_arguments(VA4)
def F6A(a,b, nom="", surnom=0) :
    """Fonction utile au test d'un décorateur.

    Fonction de tests n°6. Controle_Arguments modifie la définition de cette fonction. (D'où le nom de F6A). Ensuite les fonctions de tests appellent cette fonction, et vérifient que le décorateur fonctionne comme prévu.
    """
    return (6, a, b, nom, surnom)#cette méthode renvoie 6 car c'est la sixième méthode/fonction, puis elle renvoie les arguments passés
    #Cette méthode d'indentification permet de vérifier que la fonction est bien exécutée (si aucune d'erreur est levée par le décorateur).

@controle_types(VA4, conversion=True)
def F8TNc(a,b, nom="", surnom=0) :
    """Fonction utile au test d'un décorateur.

    Fonction de tests n°8. Controle_Types, grâce à la syntaxe de la Nouvelle version, modifie la définition de cette fonction. On utilise la fonctionnalité Conversion. (D'où le nom de F8TNc). Ensuite les fonctions de tests appellent cette fonction, et vérifient que le décorateur fonctionne comme prévu.
    """
    return (8, a, b, nom, surnom)#cette méthode renvoie 8 car c'est la huitième méthode/fonction, puis elle renvoie les arguments passés
    #Cette méthode d'indentification permet de vérifier que la fonction est bien exécutée (si aucune d'erreur est levée par le décorateur).

@controle_arguments(VA4, conversion=True)
def F10Ac(a,b, nom="", surnom=0) :
    """Fonction utile au test d'un décorateur.

    Fonction de tests n°10. Controle_Arguments modifie la définition de cette fonction. On utilise la fonctionnalité Conversion. (D'où le nom de F10Ac). Ensuite les fonctions de tests appellent cette fonction, et vérifient que le décorateur fonctionne comme prévu.
    """
    return (10, a, b, nom, surnom)#cette méthode renvoie 10 car c'est la dixième méthode/fonction, puis elle renvoie les arguments passés
    #Cette méthode d'indentification permet de vérifier que la fonction est bien exécutée (si aucune d'erreur est levée par le décorateur).


class TestsControleArguments(unittest.TestCase) :
    """Cette classe teste des décorateurs grâce à Unittest.
    
    Teste les décorateurs du module controle_arguments.
    """
    
    def setUp(self) :
        """Méthode vide pour l'insant."""
        pass

    def test_controle_typesAE(self) :#AE pour Ancienne version et Erreurs
        """Cette méthode teste le décorateur controle_types.

        Cette méthode teste en particulier que l'utilisation de ce décorateur est toujours compatible la syntaxe utilisée pour la version 1 (l'Ancienne version), qui consiste à passer les types attendus en arguments. Teste que certaines erreurs sont bien levées. Teste que si le nombre d'arguments non nommés et nommées sont différents, une erreur soit levée. On vérifie qu'il n'y ait pas de paramètres nommés qui ne soit pas valide. On contrôle aussi la levée d'erreur si un type n'est pas correct.
        """
        with self.assertRaises(TypeError) :
            F2TA()#on ne passe pas de paramètres non nommés alors qu'il en faut 2
        with self.assertRaises(TypeError) :
            self.M1TA()#il manque un paramètre non nommé
        with self.assertRaises(TypeError) :
            self.M1TA(1,"",1)#il y a trop d'arguments
        with self.assertRaises(TypeError) :
            self.M1TA(1,c=3)#c n'est pas un paramètre nommé valide
        with self.assertRaises(TypeError) :
            self.M1TA(a="")#a doit être un int
        with self.assertRaises(TypeError) :
            self.M1TA(a=2,b=3)#b doit être un str
        with self.assertRaises(TypeError) :
            F2TA(True, 2, surnom={})#surnom doit être une liste
    
    def test_controle_typesA(self) :#A pour Ancienne version
        """Cette méthode teste le décorateur controle_types.

        Cette méthode teste en particulier que l'utilisation de ce décorateur est toujours compatible la syntaxe utilisée pour la version 1 (l'Ancienne version), qui consiste à passer les types attendus en arguments. Vérifie que dans certaines situations, la fonction/méthode appellée est bien exécutée.
        """
        a = F2TA(True, 0)
        self.assertEqual(a, (2, True, 0, '', 0))
        b = self.M1TA(3)
        self.assertEqual(b, (1,3,""))
        c = self.M1TA(1, b="az")
        self.assertEqual(c, (1, 1, "az"))
        d = F2TA(True, 2, nom="moi")
        self.assertEqual(d, (2, True, 2, "moi", 0))
        e = F2TA(False, 17, nom="mon nom", surnom="me")
        self.assertEqual(e, (2, False, 17,"mon nom", "me"))
        f = F2TA(True, 0, surnom=32)
        self.assertEqual(f, (2, True, 0, "", 32))

    def test_controle_typesNE(self) :#NE pour Nouvelles versions et Erreurs
        """Cette méthode teste le décorateur controle_types.

        Cette méthode vérifie que controle_types lève des erreurs lorsque les arguments ne correspondent pas à l'objet VerificateurArguments passé en paramètre de ce décorateur. Teste que si le nombre d'arguments non nommés et nommées sont différents, une erreur soit levée. On vérifie qu'il n'y ait pas de paramètres nommés qui ne soit pas valide. On contrôle aussi la levée d'erreur si un type n'est pas correct.
        """
        with self.assertRaises(TypeError) :
            F4TN()#on ne passe pas de paramètres non nommés alors qu'il en faut 2
        with self.assertRaises(TypeError) :
            self.M3TN()#il manque un paramètre non nommé
        with self.assertRaises(TypeError) :
            self.M3TN(1,"",1)#il y a trop d'arguments
        with self.assertRaises(TypeError) :
            self.M3TN(1,c=3)#c n'est pas un paramètre nommé valide
        with self.assertRaises(TypeError) :
            self.M3TN(a="")#a doit être un int
        with self.assertRaises(TypeError) :
            self.M3TN(a=2,b=3)#b doit être un str
        with self.assertRaises(TypeError) :
            F4TN(True, 2, surnom={})#surnom doit être une liste

    def test_controle_typesN(self) :#N pour Nouvelles versions
        """Cette méthode teste le décorateur controle_types.

        Cette méthode teste en particulier que l'utilisation de ce décorateur peut se faire grace au passage en argument d'un objet VerificateurArguments.Vérifie que dans certaines situations, la fonction/méthode appellée est bien exécutée.
        """
        a = F4TN(True, 0)
        self.assertEqual(a, (4, True, 0, "", 0))
        b = self.M3TN(3)
        self.assertEqual(b, (3, 3, "", []))
        c = self.M3TN(1, b="az")
        self.assertEqual(c, (3, 1, "az", []))
        d = F4TN(True, 2, nom="moi")
        self.assertEqual(d, (4, True, 2, "moi", 0))
        e = F4TN(False, 17, nom="mon nom", surnom="me")
        self.assertEqual(e, (4, False, 17, "mon nom", "me"))
        f = F4TN(True, 0, surnom=32)
        self.assertEqual(f, (4, True, 0, "", 32))
        g = F4TN(False, b=33)
        self.assertEqual(g, (4, False, 33, "", 0))
        h = F4TN(False, 25, "Mon prénom")
        self.assertEqual(h, (4, False, 25, "Mon prénom", 0))
        i = self.M3TN(a=25, b="BB", liste=[3,5,4])
        self.assertEqual(i, (3, 25, "BB", [3,5,4]))
        j = self.M3TN(5587, "bd", liste=["z"])
        self.assertEqual(j, (3, 5587, "bd", ["z"]))

    def test_controle_typesNc(self) :#Nc pour Nouvelles versions et Conversion
        """Teste controle_types avec l'utilisation de la conversion.

        Cette méthode teste en particulier que l'utilisation de ce décorateur peut se faire grace au passage en argument d'un objet VerificateurArguments.Vérifie que dans certaines situations, la fonction/méthode appellée est bien exécutée.
        """
        a = F8TNc(1, "0")#conversion de 1 en bool et de '0' en int
        self.assertEqual(a, (8, True, 0, "", 0))
        b = self.M7TNc(3.8)#conversion de 3.8 en int
        self.assertEqual(b, (7, 3, "", []))
        c = self.M7TNc(1, b="az")
        self.assertEqual(c, (7, 1, "az", []))
        d = F8TNc(1, 2, nom="moi")#conversion de 0 en bool
        self.assertEqual(d, (8, True, 2, "moi", 0))
        e = F8TNc(0, 17, nom="mon nom", surnom="me")
        self.assertEqual(e, (8, False, 17, "mon nom", "me"))
        f = F8TNc(True, 0, surnom=32)
        self.assertEqual(f, (8, True, 0, "", 32))
        g = F8TNc(False, b=33)
        self.assertEqual(g, (8, False, 33, "", 0))
        h = F8TNc(False, 25, "Mon prénom")
        self.assertEqual(h, (8, False, 25, "Mon prénom", 0))
        i = self.M7TNc(a=25, b="BB", liste=[3,5,4])
        self.assertEqual(i, (7, 25, "BB", [3,5,4]))
        j = self.M7TNc(5587, "bd", liste=("z"))#conversion de la liste en tuple
        self.assertEqual(j, (7, 5587, "bd", ["z"]))

    def test_controle_argumentsE(self) :#E pour Erreur
        """Cette méthode teste le décorateur controle_types.

        Teste que certaines erreurs sont bien levées. Teste que si le nombre d'arguments non nommés et nommées sont différents, une erreur soit levée. On vérifie qu'il n'y ait pas de paramètres nommés qui ne soit pas valide. On contrôle aussi la levée d'erreur si un type n'est pas correct.
        """
        with self.assertRaises(TypeError) :
            F6A()#on ne passe pas de paramètres non nommés alors qu'il en faut 2
        with self.assertRaises(TypeError) :
            self.M5A()#il manque un paramètre non nommé
        with self.assertRaises(ValueError) :
            self.M5A(1,"",1)#il y a trop d'arguments
        with self.assertRaises(ValueError) :
            self.M5A(1,c=3)#c n'est pas un paramètre nommé valide
        with self.assertRaises(TypeError) :
            self.M5A(a="")#a doit être un int
        with self.assertRaises(TypeError) :
            self.M5A(a=2,b=3)#b doit être un str
        with self.assertRaises(TypeError) :
            F6A(True, 2, surnom={})#surnom doit être une liste

    def test_controle_arguments(self) :
        """Cette méthode teste le décorateur controle_arguments.

        Cette méthode teste en particulier que l'utilisation de ce décorateur peut se faire grace au passage en argument d'un objet VerificateurArguments. Vérifie que lorsque les arguments sont valides, la fonction/méthode appellée est bien exécutée.
        """
        a = F6A(True, 0)
        self.assertEqual(a, (6, True, 0, "", 0))
        b = self.M5A(3)
        self.assertEqual(b, (5, 3, "", []))
        c = self.M5A(1, b="az")
        self.assertEqual(c, (5, 1, "az", []))
        d = F6A(True, 2, nom="moi")
        self.assertEqual(d, (6, True, 2, "moi", 0))
        e = F6A(False, 17, nom="mon nom", surnom="me")
        self.assertEqual(e, (6, False, 17, "mon nom", "me"))
        f = F6A(True, 0, surnom=32)
        self.assertEqual(f, (6, True, 0, "", 32))
        g = F6A(False, b=33)
        self.assertEqual(g, (6, False, 33, "", 0))
        h = F6A(False, 25, "Mon prénom")
        self.assertEqual(h, (6, False, 25, "Mon prénom", 0))
        i = self.M5A(a=25, b="BB", liste=[3,5,4])
        self.assertEqual(i, (5, 25, "BB", [3,5,4]))
        j = self.M5A(5587, "bd", liste=["z"])
        self.assertEqual(j, (5, 5587, "bd", ["z"]))
    
    def test_controle_arguments_c(self) :#c pour conversion
        """Teste controle_arguments avec l'utilisation de la conversion.

        Cette méthode teste en particulier que l'utilisation de ce décorateur peut se faire grace au passage en argument d'un objet VerificateurArguments. Vérifie que dans certaines situations, la fonction/méthode appellée est bien exécutée.
        """
        a = F10Ac(1, "0")
        self.assertEqual(a, (10, True, 0, "", 0))
        b = self.M9Ac(3.8)
        self.assertEqual(b, (9, 3, "", []))
        c = self.M9Ac(1, b="az")
        self.assertEqual(c, (9, 1, "az", []))
        d = F10Ac(True, 2, nom="moi")
        self.assertEqual(d, (10, True, 2, "moi", 0))
        e = F10Ac(0, 17, nom="mon nom", surnom="me")
        self.assertEqual(e, (10, False, 17, "mon nom", "me"))
        f = F10Ac(True, 0, surnom=32)
        self.assertEqual(f, (10, True, 0, "", 32))
        g = F10Ac(False, b=33)
        self.assertEqual(g, (10, False, 33, "", 0))
        h = F10Ac(False, 25, "Mon prénom")
        self.assertEqual(h, (10, False, 25, "Mon prénom", 0))
        i = self.M9Ac(a=25, b="BB", liste=(3,5,4))
        self.assertEqual(i, (9, 25, "BB", [3,5,4]))
        j = self.M9Ac(5587, "bd", liste=["z"])
        self.assertEqual(j, (9, 5587, "bd", ["z"]))

    @controle_types(unittest.TestCase, int, b=str)
    def M1TA(self, a, b="") :
        """Méthode utile au test d'un décorateur.

        Méthode de tests n°1. Controle_Type, grâce à la syntaxe de l'Ancienne version, modifie la définition de cette méthode. (D'où le nom M1TA). Ensuite les fonctions de tests appellent cette méthode, et vérifient que le décorateur fonctionne comme prévu.
        """
        return (1, a, b)#cette méthode renvoie 1 car c'est la première méthode/fonction, puis retourne les arguments passés en paramètres
        #Cette méthode d'indentification permet de vérifier que la fonction est bien exécutée (si aucune d'erreur est levée par le décorateur).
    
    VA3 = VerificateurArguments()
    VA3.append(0,'self')
    VA3.append(1, 'a', Verificateur(int))
    VA3.append(2, 'b', VerificateurStr())
    VA3.append(None, 'liste', VerificateurListes(types=(list, tuple)))
    @controle_types(VA3)
    def M3TN(self, a, b="", liste=[]) :
        """Méthode utile au test d'un décorateur.

        Méthode de test n°3. Controle_Types, grâce à la syntaxe de la Nouvelle version, modifie la définition de cette méthode. (D'où le nom M3TN). Ensuite les fonctions de tests appellent cette méthode, et vérifient que le décorateur fonctionne comme prévu.
        """
        return (3, a, b, liste)#cette méthode renvoie 3 car c'est la troisième méthode/fonction, puis retourne les arguments passés en paramètres
        #Cette méthode d'indentification permet de vérifier que la fonction est bien exécutée (si aucune d'erreur est levée par le décorateur).

    @controle_arguments(VA3)
    def M5A(self, a, b="", liste=[]) :
        """Méthode utile au test d'un décorateur.

        Méthode de test n°5. Controle_Arguments modifie la définition de cette méthode. (D'où le nom M6A). Ensuite les fonctions de tests appellent cette méthode, et vérifient que le décorateur fonctionne comme prévu.
        """
        return (5, a, b, liste)#cette méthode renvoie 5 car c'est la cinquième méthode/fonction, puis retourne les arguments passés en paramètres
        #Cette méthode d'indentification permet de vérifier que la fonction est bien exécutée (si aucune d'erreur est levée par le décorateur).
    
    @controle_types(VA3, conversion=True)
    def M7TNc(self, a, b="", liste=[]) :
        """Méthode utile au test d'un décorateur.

        Méthode de test n°7. Controle_Types, grâce à la syntaxe de la Nouvelle version, modifie la définition de cette méthode. On utilise la fonctionnalité de Conversion. (D'où le nom M7TNc). Ensuite les fonctions de tests appellent cette méthode, et vérifient que le décorateur fonctionne comme prévu.
        """
        return (7, a, b, liste)#cette méthode renvoie 7 car c'est la septième méthode/fonction, puis retourne les arguments passés en paramètres
        #Cette méthode d'indentification permet de vérifier que la fonction est bien exécutée (si aucune d'erreur est levée par le décorateur).
    
    @controle_arguments(VA3, conversion=True)
    def M9Ac(self, a, b="", liste=[]) :
        """Méthode utile au test d'un décorateur.

        Méthode de test n°9. Controle_Arguments modifie la définition de cette méthode. On utilise la fonctionnalité de Conversion. (D'où le nom M9Ac). Ensuite les fonctions de tests appellent cette méthode, et vérifient que le décorateur fonctionne comme prévu.
        """
        return (9, a, b, liste)#cette méthode renvoie 9 car c'est la neuvième méthode/fonction, puis retourne les arguments passés en paramètres
        #Cette méthode d'indentification permet de vérifier que la fonction est bien exécutée (si aucune d'erreur est levée par le décorateur).


if __name__ == "__main__" :
    unittest.main()