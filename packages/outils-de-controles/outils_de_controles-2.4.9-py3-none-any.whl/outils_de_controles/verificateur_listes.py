"""Ce module contient la classe VerificateurListes."""

from outils_de_controles.verificateur_conteneurs import *

class VerificateurListes(VerificateurConteneurs) :
    """Cette classe vérifie la validité d'objet de type liste.
    
    Cette classe a pour but de vérifier la validité d'objets contenus dans une liste. Cette classe enregistre, pour chaque élement passé en paramètre, deux identifiants : l'index (de début) et l'index de fin, ainsi qu'un objet vérifiant l'objet contenu (souvant un objet Verificateur). Cette classe dispose de méthodes qui vérifie qu'un objet est bien valide.
    Cette classe hérite de VerificateurConteneurs.
    """

    def __init__(self, *args, types=list, minimum=0, maximum=None) :
        """Cette méthode crée l'objet VerificateurListes.

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
            liste += ","
        chaine = """outils_de_controles.VerificateurListes({} types={}, minimum={}, maximum={})""".format(liste, repr(self._types), repr(self._minimum), repr(self._maximum))
        return chaine
    
    def _id_verificateur(self, identifiant) :
        """Recherche le vérificateur correspondant à l'identifiant fourni.

        L'identifiant est recherché dans la liste des premiers identifiants et s'il y a deux identifiants, parmi les entiers compris dans l'intervalle entre le premier et le deuxième identifiant. Si l'identifiant n'est pas retrouvé dans la liste des identifiants, une ValueError est levée.
        """
        if identifiant is None :
            raise ValueError("L'identifiant None est invalide car plusieurs arguments peuvent correspondre à cet identifiant.")
        
        if isinstance(identifiant, int) :
            for liste in self._liste_verificateurs :
                if liste[1] is None :#il n'y a pas de deuxième identifiant
                    if liste[0] == identifiant :
                        retour = liste[2]
                        break
                elif liste[0] <= identifiant and liste[1] >= identifiant : # s'il y a deux identifiants, et que valeur est compris entre les deux identifiants
                    retour = liste[2]
                    break

        try :
            return retour
        except (NameError, UnboundLocalError) : #si retour n'est pas défini = si on n'a pas trouvé l'identifiant
            raise ValueError("L'identifiant n'a pas été trouvé donc il n'est pas possible de fournir le vérificateur correspondant.")


    def _append(self, validation) :
        """Cette méthode ajoute une validation à la liste des vérificateurs.
        
        Une validation est une liste comportant trois éléments : 2 identifiants (un index ou les borne d'un intervalle d'index) puis un vérificateur. Cette méthode ajoute une validation mais elle n'est pas destinée à être utilisée directement. Utilisez plutôt la méthode append.
        """
        if not isinstance(validation, list) :
            raise TypeError("L'argument validation doit être une liste.")
        for id in range(2) : #on vérifie juste validation[0] et validation[1]
            if validation[id] is not None :
                if not isinstance(validation[id], int) :
                    raise TypeError("Les identifiants doivent être des nombres entiers positifs (ou None).")
                if validation[id] < 0 :
                    raise ValueError("Les identifiants sont des index et doivent donc être des nombres entiers positifs (supérieur ou égal à 0).")
        if validation[0] is None :#si le premier identifiant ne vaux pas None (= dans tous les cas car si les deux id vallent None, la méthode de VerificateurConteneurs lève une erreur), on échange la position des identifiants
            validation[0], validation[1] = validation[1], validation[0]
        if validation[1] is not None :#si aucun des identifiants est None (voir lignes précédentes)
            if validation[1] < validation[0] :#le premier identifiant doit être plus petit que le deuxième
                validation[0], validation[1] = validation[1], validation[0]
        VerificateurConteneurs._append(self, validation)
    
    def controle_types_total(self, objet_controlé, conversion=False) :
        """Vérifie que les objets contenus ont des types valides.

        Cette méthode parcourt la liste à controler et associe à chaque objet contenu son identifiant pour le controler en appelant controle_types.
        Retourne objet_controlé si aucune erreur est levée.
        """
        objet_controlé = self.controle_types(objet_controlé, conversion=conversion)#on controle/convertit l'objet controlé
        if conversion and isinstance(objet_controlé, tuple) :
            objet_controlé = list(objet_controlé)#on transforme en liste pour modifier le tuple
        for i, objet_contenu in enumerate(objet_controlé) :
            if i in self :
                if conversion == True :
                    objet_controlé[i] = self.controle_types_item(i, objet_contenu, conversion=True)
                else :
                    self.controle_types_item(i, objet_contenu)
        objet_controlé = self.controle_types(objet_controlé, conversion=conversion)#on recontrole/convertit en type valide l'objet controlé (utile si on a transformer le tuple en liste)
        return objet_controlé
    
    def controle_total(self, objet_controlé, conversion=False) :
        """Vérifie que la liste controlée est valide.

        Cette méthode d'une part parcourt la liste et associe à chaque objet contenu son identifiant pour le controler en appelant controle_global.
        D'autre part, cette méthode vérifie que la longueur de la liste est comprise entre len_min et len_max. Retourne objet_controlé si aucune erreur est levée.
        """
        objet_controlé = self.controle_global(objet_controlé, conversion=conversion)
        if conversion and isinstance(objet_controlé, tuple) :
            objet_controlé = list(objet_controlé)#on transforme en liste pour modifier le tuple
        for i, objet_contenu in enumerate(objet_controlé) :
            if i in self :
                if conversion == True :
                    objet_controlé[i] = self.controle_global_item(i, objet_contenu, conversion=True)
                else :
                    self.controle_global_item(i, objet_contenu)
        objet_controlé = self.controle_types(objet_controlé, conversion=conversion)#on recontrole/convertit en type valide l'objet controlé (utile si on a transformer le tuple en liste)
        return objet_controlé

    def sort(self, key = None, reverse=False) :
        """Méthode qui trie cet objet en fonction des identifiants.
        
        Par défaut, les vérificateurs sont triés par ordre croissant des premiers identifiants.
        """
        if key :
            self._liste_verificateurs.sort(key=key, reverse=reverse)
        else :
            self._liste_verificateurs.sort(key=lambda colonne: colonne[0])
            if reverse == True :
                self._liste_verificateurs.reverse()


    liste_verificateurs = property(VerificateurConteneurs.get_liste_verificateurs)
    types = property(VerificateurConteneurs.get_types, VerificateurConteneurs.set_types, VerificateurConteneurs.del_types, "Attribut représentant le (ou les) types du conteneur. (S'il y a plusieurs types, il faut les mettre dans un tuple).")
    minimum = property(VerificateurConteneurs.get_minimum, VerificateurConteneurs.set_minimum, VerificateurConteneurs.del_minimum, "Attribut représentant la longueur minimum : longueur minimale autorisée (Le minimum doit être en nombre entier positif).")
    maximum = property(VerificateurConteneurs.get_maximum, VerificateurConteneurs.set_maximum, VerificateurConteneurs.del_maximum, "Attribut représentant la longueur maximum : longueur maximale autorisée (Le maximum doit être un nombre entier positif supérieur ou égal au minimum).")