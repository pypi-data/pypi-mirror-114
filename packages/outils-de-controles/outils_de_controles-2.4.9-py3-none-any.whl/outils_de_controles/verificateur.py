"""Ce module contient la classe Verificateur.

Cette classe a pour but de vérifier la validité d'objets non conteneurs. (Par exemple, des objets int, bool ou float).
"""

class Verificateur() :
    """Cette classe vérifie la validité d'objets non conteneurs.

    Pour cela, cette classe enregistre des critères de validité comme le type de l'objet, son minimum ou son maximum. Aucun critère n'est obligatoire : si aucun critère est enregistré, la classe ne vérifie rien. Cette classe dispose de méthodes qui vérifie qu'un objet est bien valide.
    """

    def __init__(self, types=None, minimum=None, maximum=None) :
        """Cette méthode initialise l'objet Verificateur et crée ses attributs.

        Cette méthode prend en paramètre plusieurs critères de vérification :
        - le (ou les) types de l'objet (s'il y a plusieurs types, il faut les mettre dans un tuple). Vérifique l'objet est du type (ou d'un des types) précisé.
        - le minimum : valeur minimale autorisée (ne fonctionne que si l'objet à tester supporte l'opérateur < avec l'objet qui est le minimum.)
        - le maximum : valeur maximale autorisée (ne fonctionne que si l'objet à tester supporte l'opérateur > avec l'objet qui est le maximum.)
        """
        self._types = types
        self._minimum = minimum
        self._maximum = maximum
    
    def __str__(self) :
        """Méthode revoyant une chaine pour afficher l'objet Verificateur."""
        return """◄types:{obj._types}, minimum:{obj._minimum}, maximum:{obj._maximum}►""".format(obj = self)#obj désigne l'objet vérificateur qu'il faut afficher
    
    def __repr__(self) :
        """Méthode représentant l'objet pour le débugage.

        Retourne une chaine avec le nom de la classe et chaque attribut.
        """
        chaine = """outils_de_controles.Verificateur(types={}, minimum={}, maximum={})""".format(repr(self._types), repr(self._minimum), repr(self._maximum))
        return chaine

    def __eq__(self, autre_objet) :
        """Méthode comparant deux objets Verificateur.
        
        Si ces deux objets sont égaux (c'est-à-dire que tous leurs attributs sont égaux), cette méthode renvoie True.
        """
        if not isinstance(autre_objet, Verificateur) :
            raise TypeError("""Le deuxième objet n'est pas un objet de la classe Verificateur.""")
        retour = False
        if self.types == autre_objet.types and self.minimum == autre_objet.minimum and self.maximum == autre_objet.maximum :
            retour = True
        return retour

    def get_types(self) :
        """Retourne l'attribut types."""
        return self._types
    
    def get_minimum(self) :
        """Retourne l'attribut min (minimum)."""
        return self._minimum

    def get_maximum(self) :
        """Retourne l'attribut max (maximum)."""
        return self._maximum

    def set_types(self, nouveaux_types) :
        """Modifie l'attribut types."""
        self._types = nouveaux_types
    
    def set_minimum(self, nouveau_minimum) :
        """Modifie l'attribut minimum."""
        self._minimum= nouveau_minimum
    
    def set_maximum(self, nouveau_maximum) :
        """Modifie l'attribut maximum."""
        self._maximum = nouveau_maximum
    
    def del_types(self) :
        """Réinitialise l'attribut types. (types vaut alors None)."""
        self._types = None
    
    def del_minimum(self) :
        """Réinitialise l'attribut minimum. (minimum vaut alors None)."""
        self._minimum = None

    def del_maximum(self) :
        """Réinitialise l'attribut maximum. (maximum vaut alors None)."""
        self._maximum = None

    def controle_types(self, objet_controle, conversion=False) :
        """Vérifie que le type de objet_controlé est valide.
        
        Si objet_controlé n'est pas du bon type et que conversion est vrai, cette méthode tente de convertir objet _controlé en objet du bon type.
        Cette méthode renvoie l'objet valide, si elle n'a pas émise d'erreur (Si l'objet a été converti avec succès, l'objet renvoyé est différent de objet_controle.)
        """
        if self._types is not None and not isinstance(objet_controle, self._types) :#le type n'est pas correct
            if conversion :#si conversion est activé
                objet_controle = self._conversion(objet_controle)#on tente de convertir l'objet_controlé
            else :#si la conversion est interdite, on lève une erreur
                raise TypeError("L'objet {} n'est pas du/des types {}.".format(objet_controle, self._types))
        return objet_controle

    def controle_types_total(self, objet_controle, conversion=False) :
        """Vérifie que le type de objet_controlé est valide.
        
        Effectue les mêmes taches que controle_types car les objets controlés par cette classe ne sont pas des conteneurs. Il n'y a donc pas de vérification supplémentaire sur les objets contenus.
        """
        return self.controle_types(objet_controle, conversion=conversion)

    def controle_minimum(self, objet_controle) :
        """Vérifie que objet_controlé est supérieur au minimum autorisé.
        
        Retourne l'objet_controle si aucune erreur n'a été levée.
        """
        if self._minimum is not None and objet_controle < self._minimum :
            raise ValueError("L'objet {} est inférieur au minimum autorisé : {}.".format(objet_controle, self._minimum))
        return objet_controle
    
    def controle_maximum(self, objet_controle) :
        """Vérifie que objet_controlé est inférieur au maximum autorisé.
        
        Retourne l'objet_controle si aucune erreur n'a été levée.
        """
        if self._maximum is not None and objet_controle > self._maximum :
            raise ValueError("L'objet {} est supérieur au maximum autorisé : {}.".format(objet_controle, self._maximum))
        return objet_controle

    def controle_global(self, objet_controle, conversion=False) :
        """Vérifie que objet_controlé est valide et répond à tous les critères.

        Appelle les différentes méthodes de controle spécifiques (controle_types, controle_min...). Si aucune erreur est levée, renvoie l'objet valide. (Si l'objet a été converti avec succès, l'objet renvoyé est différent de objet_controle.)
        """
        objet_controle = self.controle_types(objet_controle, conversion=conversion)
        objet_controle = self.controle_minimum(objet_controle)
        objet_controle = self.controle_maximum(objet_controle)
        return objet_controle

    def controle_total(self, objet_controle, conversion=False) :
        """Vérifie que objet_controlé est valide et répond à tous les critères.
        
        Effectue les même taches que controle_global car les objets controlés par cette classe ne sont pas des conteneurs. Il n'y a donc pas de vérification supplémentaire sur les objets contenus.
        """
        return self.controle_global(objet_controle, conversion = conversion)

    def _conversion(self, objet_controle) :
        """Converti l'objet controlé en type valide.
        
        Cette méthode tente de convertir objet _controlé en objet du bon type.Retourne l'objet s'il a été converti avec succès.
        N.B. : Pour les objets conteneurs, ne convertit que le conteneur ; pas les objets contenus.
        """
        if self._types is not None :#si des types valides sont précisés
            #on crée une liste des types valides
            if isinstance(self._types, type) :
                liste_type = [self._types]
            else :
                liste_type = list(self._types)#à partir du tuple self._types, on cére une liste
            for i, type_valide in enumerate(liste_type) :
                chaine_type = str(type_valide)
                chaine_type = chaine_type[8:-2]#enlève les caractères :<class ' et '>
                try :
                    objet_controle = eval(chaine_type+"("+"objet_controle"+")")
                except ValueError as e :
                    if i == len(liste_type)-1 :
                        raise TypeError("L'objet {0} n'est pas du/des types {1} et n'est pas convertible en {1} car :\n{2}.".format(objet_controle, self._types, e))
                    else :
                        continue
                else :#si aucune erreur n'est levé
                    break
        return Verificateur.controle_types(self, objet_controle)#on controle le type de l'objet sans conversion et on renvoie l'objet_controlé converti


    types = property(get_types, set_types, del_types, "Attribut représentant le (ou les) types de l'objet. (s'il y a plusieurs types, il faut les mettre dans un tuple).")
    minimum = property(get_minimum, set_minimum, del_minimum, "Attribut représentant le minimum : valeur minimale autorisée (ne fonctionne que si l'objet à tester supporte l'opérateur < avec l'objet qui est le minimum.)")
    maximum = property(get_maximum, set_maximum, del_maximum, "Attribut représentant le maximum : valeur maximale autorisée (ne fonctionne que si l'objet à tester supporte l'opérateur > avec l'objet qui est le maximum.)")

