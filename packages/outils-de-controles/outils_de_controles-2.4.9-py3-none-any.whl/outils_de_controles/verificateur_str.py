"""Ce module contient la classe Verificateur_str.

Cette classe a pour but de vérifier la validité d'objets du type str.
"""

from outils_de_controles.verificateur import *
from outils_de_controles.verificateur_conteneurs import *
import re

class VerificateurStr(Verificateur) :
    """Cette classe vérifie la validité de chaine de caractères (str).
    
    Pour cela, cette classe enregistre des critères de validité comme la longueur minimale de la chaine, sa longueur maximale et son expression régulière correspondante. Aucun critère n'est obligatoire : si aucun critère est enregistré, la classe ne vérifie rien. Cette classe dispose de méthodes qui vérifie qu'un objet est bien valide.
    """

    def __init__(self, minimum=0, maximum=None, regex=r"") :
        """Cette méthode crée l'objet VerificateurStr.

        L'attribut types est toujours str. Crée trois autres attributs : minimum : longueur minimale autorisée de la chaine, maximum : longueur maximale autorisée ainsi que regex : une expression régulière qui valide le contenu de la chaine.
        """
        #création des attributs (pour permettre le contrôle mutuel des valeurs de minimum et maximum)
        self._minimum = 0
        self._maximum = None
        #initialisation des attributs
        self._types = str
        VerificateurConteneurs.set_minimum(self, minimum)
        VerificateurConteneurs.set_maximum(self, maximum)
        self.set_regex(regex)

    def __str__(self) :
        """Renvoie une chaine pour afficher l'objet VerificateurStr."""
        return """◄minimum:{obj._minimum}, maximum:{obj._maximum}, regex:'{obj.regex}'►""".format(obj=self)#obj désigne l'objet vérificateur qu'il faut afficher

    def __repr__(self) :
        """Méthode représentant l'objet pour le débugage.

        Retourne une chaine avec le nom de la classe et chaque attribut.
        """
        chaine = """outils_de_controles.VerificateurStr(minimum={}, maximum={}, regex={})""".format(repr(self._minimum), repr(self._maximum), repr(self.regex))
        return chaine
    
    def __eq__(self, autre_objet) :
        """Méthode comparant deux objets VerificateurStr.
        
        Si ces deux objets sont égaux (c'est-à-dire que tous leurs attributs sont égaux), cette méthode renvoie True.
        """
        if not isinstance(autre_objet, VerificateurStr) :
            raise TypeError("""Le deuxième objet n'est pas un objet de la classe VerificateurStr.""")
        retour = False
        if self.types == autre_objet.types and self.minimum == autre_objet.minimum and self.maximum == autre_objet.maximum and self.regex == autre_objet.regex :
            retour = True
        return retour

    def set_minimum(self, nouveau_minimum) :
        """Modifie l'attribut minimum (longueur minimum de la chaine).
        
        Vérifie d'abord que minimum est un nombre entier positif (ou nul).
        """
        VerificateurConteneurs.set_minimum(self, nouveau_minimum)
    
    def set_maximum(self, nouveau_maximum) :
        """Modifie l'attribut maximum (longueur maximum de la chaine).
        
        Vérifie d'abord que maximum est un nombre entier positif (ou nul), lorsqu'il ne vaut pas None. Vérifie ensuite qu'il est supérieur ou égal au minimum.
        """
        VerificateurConteneurs.set_maximum(self, nouveau_maximum)

    def get_regex(self) :
        """Retourne l'attribut regex.
        
        Retourne l'expression régulière sous sa forme non compilée.
        """
        return self._regex.pattern#retourne la regex qui a été compilée
    
    def set_regex(self, nouvelle_regex) :
        """Modifie l'attribut regex.
        
        Si nouvelle_regex n'est pas compilée, on compile la regex. Cela accélère le controle de l'objet.
        """
        if not isinstance(nouvelle_regex, re.Pattern) :
            nouvelle_regex = re.compile(nouvelle_regex)
        self._regex = nouvelle_regex
    
    def del_regex(self) :
        """Réinitialise l'attribut regex. (regex vaut alors r"")."""
        self._regex = re.compile(r"")

    def controle_minimum(self, objet_controle) :
        """Vérifie que objet_controlé est plus long que le minimum autorisé.
        
        Renvoie l'objet controlé, s'il est valide.
        """
        return VerificateurConteneurs.controle_minimum(self, objet_controle)
    
    def controle_maximum(self, objet_controle) :
        """Vérifie que objet_controlé est moins long que le maximum valide.
        
        Renvoie l'objet controlé, s'il est valide."""
        return VerificateurConteneurs.controle_maximum(self, objet_controle)
    
    def controle_regex(self, objet_controle) :
        """Vérifie que objet_controlé correspond à regex.
        
        Vérifie que le contenu d'objet_controle correspond à l'expression régulière fournie par self.regex. Retourne l'objet controlé si l'objet est valide.
        """
        if self._regex.search(objet_controle) is None :
            raise ValueError("La chaine objet_controle passée en paramètre ne correspond pas à {}.".format(self.get_regex()))
        return objet_controle

    def controle_global(self, objet_controle, conversion=False) :
        """Vérifie que objet_controlé est valide et répond à tous les critères.

        Appelle les différentes méthodes de controle spécifiques (controle_types, controle_min...). Retourne l'objet controlé, si l'objet est valide.
        """
        objet_controle = self.controle_types(objet_controle, conversion=conversion)
        objet_controle = self.controle_minimum(objet_controle)
        objet_controle = self.controle_maximum(objet_controle)
        objet_controle = self.controle_regex(objet_controle)
        return objet_controle

    types = property(Verificateur.get_types)
    minimum = property(Verificateur.get_minimum, set_minimum, VerificateurConteneurs.del_minimum, "Attribut représentant la longueur minimum : longueur minimale autorisée (Le minimum doit être en nombre entier positif).")
    maximum = property(Verificateur.get_maximum, set_maximum, Verificateur.del_maximum, "Attribut représentant la longueur maximum : longueur maximale autorisée (Le maximum doit être un nombre entier positif supérieur ou égal au minimum).")
    regex = property(get_regex, set_regex, del_regex, "Attribut représentant l'expression régulière qui permet de controler le contenu de la chaine.")