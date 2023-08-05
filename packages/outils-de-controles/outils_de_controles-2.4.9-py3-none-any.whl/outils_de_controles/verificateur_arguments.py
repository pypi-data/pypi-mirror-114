"""Ce module contient la classe VerificateurArguments."""

from outils_de_controles.verificateur_conteneurs import *

class VerificateurArguments(VerificateurConteneurs) :
    """Cette classe vérifie la validité d'arguments passés en paramètres.
    
    Cette classe a pour but de vérifier la validité d'arguments passés en paramètre d'une fonction ou d'une méthode. Cette classe enregistre, pour chaque élement passé en paramètre, deux identifiants (l'ordre de définition et le nom du paramètre) ainsi qu'un objet vérifiant l'objet contenu (souvant un objet Verificateur). Cette classe dispose de méthodes qui vérifie qu'un objet est bien valide.
    Cette classe hérite de VerificateurConteneurs.
    """

    def __init__(self, *args, types=(list, tuple, dict), minimum=0, maximum=None) :
        """Cette méthode crée l'objet VerificateurArguments.

        Crée une liste avec tous les paramètres données : des listes de 3 éléments (id1, id2, vérificateur). Crée trois autres attributs :
        - types : le ou les types autorisés
        - minimum : longueur minimale autorisée du conteneur
        - maximum : longueur maximale autorisée.
        """
        VerificateurConteneurs.__init__(self, *args, types=types, minimum=minimum, maximum=maximum)#L'objet est initialisé par la méthode __init__() de VerificateurConteneurs.

    def __repr__(self) :
        """Méthode représentant l'objet pour le débugage.

        Retourne une chaine avec le nom de la classe et l'attribut.
        """
        liste = repr(self._liste_verificateurs)
        liste = liste[1:-1]
        if liste :
            liste += ", "
        chaine = """outils_de_controles.VerificateurArguments({}types={}, minimum={}, maximum={})""".format(liste, repr(self._types), repr(self._minimum), repr(self._maximum))
        return chaine

    def _append(self, validation) :
        """Cette méthode ajoute une validation à la liste des vérificateurs.
        
        Une validation est une liste comportant trois éléments : 2 identifiants (l'ordre de définition et le nom du paramètre) puis un vérificateur. Cette méthode ajoute une validation mais elle n'est pas destinée à être utilisée directement. Utilisez plutôt la méthode append.
        """
        if not isinstance(validation, list) :
            raise TypeError("L'argument validation doit être une liste.")
        if validation[0] is not None :
            if not isinstance(validation[0], int) :
                raise TypeError("Le premier identifiant doit être un nombre entier.")
            if validation[0] < 0 :
                raise ValueError("Le premier identifiant doit être un nombre entier positif (supérieur ou égal à 0 ; représentant l'ordre de définition).")
        if validation[1] is not None :
            if not isinstance(validation[1],str) :
                raise TypeError("Le deuxième identifiant doit être une chaîne qui est le nom de l'argument. (S'il n'y a pas de nom, mettre None.)")
            if validation[1] == "" :
                validation[1] = None
        VerificateurConteneurs._append(self, validation)
    
    def sort(self, key = None, reverse=False) :
        """Méthode qui trie cet objet en fonction des identifiants.
        
        Par défaut, les vérificateurs sont triés par ordre croissant dans l'ordre des premiers identifiants puis par les seconds identifiants.
        key doit être une fonction prenant en paramètre un seul argument.
        """
        if key :
            self._liste_verificateurs.sort(key=key, reverse=reverse)
        else :
            self._liste_verificateurs.sort(key=lambda colonne: self.clé(colonne, 1,""))
            self._liste_verificateurs.sort(key=lambda colonne: self.clé(colonne, 0,-1))
            if reverse == True :
                self._liste_verificateurs.reverse()
    
    def controle_types(self,args=[], kwargs={}, conversion=False) :
        """Vérifie que args et kwargs sont d'un type valide.
        
        Appelle la méthode controle_types de la classe mère (VerificateurConteneurs) sur args et kwargs. Retourne les args et kwargs valides.
        """
        if self._types is not None :
            if not isinstance(args, self._types) or not isinstance(kwargs, self._types) :#le type n'est pas correct
                if conversion :#si conversion est activé
                    args, kwargs = self._conversion(args, kwargs)#on tente de convertir args et kwargs
                else :#si la conversion est interdite, on lève une erreur
                    raise TypeError("Les arguments ne sont pas fourni avec un conteneur du bon type. Les types valides sont {}.".format(self._types))
        return args, kwargs

    def controle_types_total(self, args=[], kwargs={}, conversion=False) :
        """Vérifie que les arguments ont des types valides.

        Cette méthode parcourt les arguments et associe à chaque argument son identifiant pour controler son type en appelant controle_types.
        Cette méthode prend en paramètre la liste de tous les arguments non nommés passés en paramètres (args) et les dictionnaires des arguments nommés (kwargs). Retourne les args et kwargs valides.
        """
        args, kwargs = self.controle_types(args, kwargs, conversion=conversion)
        if conversion and isinstance(args, tuple) :
            args = list(args)#on transforme en liste pour modifier le tuple
        for i, arg in enumerate(args) :#on parcours la listes des paramètres non nommés
            try :
                if conversion == True :
                    args[i] = self.controle_types_item(i, arg, conversion=True)
                else :
                    self.controle_types_item(i, arg)
            except ValueError as e :
                raise TypeError(e)
        for cle in kwargs : #on parcours la listes des paramètres nommés
            try :
                if conversion == True :
                    kwargs[cle] = self.controle_types_item(cle, kwargs[cle], conversion=True)
                else :
                    self.controle_types_item(cle, kwargs[cle])
            except ValueError as e :
                raise TypeError(e)
        args, kwargs = self.controle_types(args, kwargs, conversion=conversion)#utile si on a convertit args en liste et que le type valide est tuple
        return args, kwargs
    
    def controle_minimum(self, args=[], kwargs={}) :
        """Vérifie qu'il y a plus de self.minimum arguments.
        
        On additionne la longueur (len) de args et kwargs et on vérifie que cette valeur est supérieure au minimum autorisé. Retourne args et kwargs, si aucune erreur a été levée.
        """
        longueur = len(args)+len(kwargs)
        if longueur < self._minimum :
            raise ValueError("Il y a {} arguments alors que le minimum autorisé est {} arguments.".format(longueur, self._minimum))
        return args, kwargs
    
    def controle_maximum(self, args=[], kwargs={}) :
        """Vérifie qu'il y a moins de self.maximum arguments.
        
        On additionne la longueur (len) de args et kwargs et on vérifie que cette valeur est inférieure au maximum autorisé. Retourne args et kwargs, si aucune erreur a été levée.
        """
        longueur = len(args)+len(kwargs)
        if self._maximum is not None and longueur > self._maximum :
            raise ValueError("Il y a {} arguments alors que le maximum autorisé est {} arguments.".format(longueur, self._maximum))
        return args, kwargs

    def controle_global(self, args=[], kwargs={}, conversion=False) :
        """Vérifie que args et kwargs sont valides.

        Appelle les différentes méthodes de controle spécifiques (controle_types, controle_min...). Retourne args et kwargs, si aucune erreur a été levée.
        """
        args, kwargs = self.controle_types(args, kwargs, conversion=conversion)
        args, kwargs = self.controle_minimum(args, kwargs)
        args, kwargs = self.controle_maximum(args, kwargs)
        return args, kwargs

    def controle_total(self, args=[], kwargs={}, conversion=False) :
        """Vérifie que les arguments sont valides.

        Cette méthode parcourt les arguments et associe à chaque argument son identifiant pour le controler en appelant controle_global.
        Cette méthode prend en paramètre la liste de tous les arguments non nommés passés en paramètres (args) et les dictionnaires des arguments nommés (kwargs). Retourne args et kwargs, si aucune erreur a été levée.
        """
        args, kwargs = self.controle_global(args, kwargs, conversion=conversion)
        if conversion and isinstance(args, tuple) :
            args = list(args)#on transforme en liste pour modifier le tuple
        for i, arg in enumerate(args) :#on parcours la listes des paramètres non nommés
            if conversion == True :
                args[i] = self.controle_global_item(i, arg, conversion=True)
            else :
                self.controle_global_item(i, arg)
        for cle in kwargs : #on parcours la listes des paramètres nommés
            if conversion == True :
                kwargs[cle] = self.controle_global_item(cle, kwargs[cle], conversion=True)
            else :
                self.controle_global_item(cle, kwargs[cle])
        args, kwargs = self.controle_types(args, kwargs, conversion=conversion)#utile si on a convertit args en liste et que le type valide est tuple
        return args, kwargs

    def _conversion(self, args=[], kwargs={}) :
        """Converti args et kwargs en objets de type valide.
        
        Cette méthode tente de convertir args et kwargs en objet du bon type.Retourne args et kwargs s'ils ont été converti avec succès.
        N.B. : Ne convertit pas les objets contenus.
        """
        if self._types is not None :
            #on convertit args en objet du premier type valide possible (en général, le premier type valide doit être list ou tuple).
            args = VerificateurConteneurs._conversion(self, args)
            if dict in self._types :#si on peut convertir en dict
                types = self._types
                self._types = dict#on convertit kwargs en dict
                kwargs = VerificateurConteneurs._conversion(self, kwargs)
                self._types = types
            else :#sinon on convertit kwargs en objet du premier type valide possible (attention, cette conversion peut poser des problèmes par la suite, lors du passage en paramètre de v_kwargs)
                kwargs = VerificateurConteneurs._conversion(self, kwargs)
        return self.controle_types(args, kwargs)

    liste_verificateurs = property(VerificateurConteneurs.get_liste_verificateurs)
    types = property(VerificateurConteneurs.get_types, VerificateurConteneurs.set_types, VerificateurConteneurs.del_types, "Attribut représentant le (ou les) types du conteneur. (s'il y a plusieurs types, il faut les mettre dans un tuple).")
    minimum = property(VerificateurConteneurs.get_minimum, VerificateurConteneurs.set_minimum, VerificateurConteneurs.del_minimum, "Attribut représentant la longueur minimum : longueur minimale autorisée (Le minimum doit être en nombre entier positif).")
    maximum = property(VerificateurConteneurs.get_maximum, VerificateurConteneurs.set_maximum, VerificateurConteneurs.del_maximum, "Attribut représentant la longueur maximum : longueur maximale autorisée (Le maximum doit être un nombre entier positif supérieur ou égal au minimum).")