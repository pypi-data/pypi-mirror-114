"""Ce module contient la classe VerificateurConteneurs."""

from outils_de_controles.verificateur import *

class VerificateurConteneurs(Verificateur) :
    """Cette classe vérifie la validité d'objets conteneurs.

    Cette classe a pour but de vérifier la validité d'objets conteneurs. (Par exemple, des objets list ou tuple). Cette classe enregistre, pour chaque élement contenu, deux identifiants ainsi qu'un objet vérifiant l'objet contenu (souvant un objet Verificateur). Cette classe dispose de méthodes qui vérifie qu'un objet est bien valide. De plus, cette vérifie la longueur du conteneur et son type (en héritant de Verificateur).
    Cette classe n'est pas destinée à être directement appelée, mais plutôt d'avoir des classes filles correspondant à un type de conteneur qui elles, seront appelées.
    """

    def __init__(self, *args, types=None, minimum=0, maximum=None) :
        """Cette méthode crée l'objet VerificateurConteneurs.

        Crée une liste avec tous les paramètres données : des listes de 3 éléments (id1, id2, vérificateur). Crée trois autres attributs :
        - types : le ou les types autorisés
        - minimum : longueur minimale autorisée du conteneur
        - maximum : longueur maximale autorisée.
        """
        #création des attributs (pour permettre le contrôle mutuel des valeurs de minimum et maximum)
        self._types = None
        self._minimum = 0
        self._maximum = None
        #initialisation des attributs
        self.set_types(types)
        self.set_minimum(minimum)
        self.set_maximum(maximum)

        self._liste_verificateurs = []
        for liste in args :
            self._append(liste)
        
    def __str__(self) :
        """Méthode spéciale appelé quand on cherche à afficher l'objet.
        
        Affiche une sorte de tableau avec trois colonnes : une pour le premier identifiant, une deuxième pour le deuxième identifiant et enfin une troisième pour le vérificateur.
        """
        chaine = """◄types:{obj._types}, minimum:{obj._minimum}, maximum:{obj._maximum}\n\n""".format(obj = self)#obj désigne l'objet vérificateur qu'il faut afficher
        chaine+= self.get_liste_verificateurs()
        return chaine+"►\n"
    
    def __repr__(self) :
        """Méthode représentant l'objet pour le débugage.

        Retourne une chaine avec le nom de la classe et l'attribut.
        """
        liste = repr(self._liste_verificateurs)
        liste = liste[1:-1]
        if liste :
            liste += ","
        chaine = """outils_de_controles.VerificateurConteneurs({} types={}, minimum={}, maximum={})""".format(liste, repr(self._types), repr(self._minimum), repr(self._maximum))
        return chaine

    def _id_verificateur(self, identifiant) :
        """Recherche le vérificateur correspondant à l'identifiant fourni.

        L'identifiant est recherché dans la liste des premiers identifiants et dans la liste des deuxièmes identifiants. Si l'identifiant n'est pas retrouvé dans la liste des identifiants, une ValueError est levée.
        """
        if identifiant is None :
            raise ValueError("L'identifiant None est invalide car plusieurs arguments peuvent correspondre à cet identifiant.")
        
        for liste in self._liste_verificateurs :
            if liste[0] == identifiant or liste[1] == identifiant :
                retour = liste[2]
                break
        try :
            return retour
        except (NameError, UnboundLocalError) : #si retour n'est pas défini = si on n'a pas trouvé l'identifiant
            raise ValueError("L'identifiant n'a pas été trouvé donc il n'est pas possible de fournir le vérificateur correspondant.")

    def __contains__(self, identifiant) :
        """Recherche un identifiant dans la liste de tous les identifiants.

        L'identifiant est recherché dans la liste des premiers identifiants et dans la liste des deuxièmes identifiants. On fait appel à la fonction _id_verificateur qui lève une erreur si l'identifiant n'est pas trouvé.
        """
        try :
            self._id_verificateur(identifiant)
        except ValueError :
            return False
        else :
            return True

    def __eq__(self, autre_objet) :
        """Méthode comparant deux objets VerificateurConteneurs.
        
        Si ces deux objets sont égaux (c'est-à-dire que tous leurs attributs sont égaux), cette méthode renvoie True.
        """
        if not isinstance(autre_objet, type(self)) :
            raise TypeError("""Le deuxième objet n'est pas un objet de la classe {}.""".format(type(self)))
        retour = False
        if self.types == autre_objet.types and self.minimum == autre_objet.minimum and self.maximum == autre_objet.maximum and self._liste_verificateurs == autre_objet._liste_verificateurs :
            retour = True
        return retour

    def _append(self, validation) :
        """Cette méthode ajoute une validation à la liste des vérificateurs.
        
        Une validation est une liste comportant trois éléments : 2 identifiants puis un vérificateur. Cette méthode ajoute une validation mais elle n'est pas destinée à être utilisée directement. Utilisez plutôt la méthode append.
        """
        if not isinstance(validation, list) :
            raise TypeError("L'argument validation doit être une liste.")
        if len(validation) != 3 :
            raise ValueError("La liste doit contenir 3 éléments.")
        if validation[0] is not None and validation[0] in self :
            raise ValueError("Une autre validation a déjà le même identifiant : {}.".format(validation[0]))
        if validation[1] is not None and validation[1] in self :
            raise ValueError("Une autre validation a déjà le même identifiant : {}.".format(validation[1]))
        if validation[0] == None and validation[1] == None :
            raise ValueError("Il faut préciser au moins un des identifiants.")
        
        #on ne teste pas forcément le type des autres éléments car c'est les fonctions de contrôle qui les lèvent
        #pas de vérification de types : c'est la fonction isinstance qui le fait lorsque l'on cherche à savoir si l'argument fourni est d'un type valide.
        self._liste_verificateurs.append(validation)

    def append(self, id1=None, id2=None, verificateur=None) :
        """Cette méthode ajoute un validateur à la liste des vérificateurs."""
        if not verificateur :
            verificateur = Verificateur()
        self._append([id1, id2, verificateur])#l'ajout de l'argument et les vérifications sont faites par _append.

    def controle_minimum(self, objet_controle) :
        """Vérifie que objet_controlé est plus long que le minimum autorisé.
        
        Retourne l'objet_controle si aucune erreur n'a été levée.
        """
        if len(objet_controle) < self._minimum :
            raise ValueError("L'objet {} est moins long que le minimum autorisé : {}.".format(objet_controle, self._minimum))
        return objet_controle
    
    def controle_maximum(self, objet_controle) :
        """Vérifie que objet_controlé est moins long que le maximum valide.
        
        Retourne l'objet_controle si aucune erreur n'a été levée.
        """
        if self._maximum is not None and len(objet_controle) > self._maximum :
            raise ValueError("L'objet {} est plus long que le maximum autorisé : {}.".format(objet_controle, self._maximum))
        return objet_controle

    def controle_types_item(self, identifiant, item_controlé, conversion=False) :
        """Vérifie que l'objet controlé a un type valide.
        
        Les critères de validité sont fourni par le vérificateur correspondant à l'id passé en paramètre. La vérification est faite par le vérificateur correspondnant à l'id (identifiant).
        Si aucune erreur est levée, cette méthode retourne l'item_controlé. (Si l'objet a été converti avec succès, l'objet renvoyé est différent de objet_controle.)
        """
        verificateur = self._id_verificateur(identifiant)
        return verificateur.controle_types_total(item_controlé, conversion=conversion)

    def controle_types_total(self, objet_controlé, conversion=False) :
        """Vérifie que les objets contenus ont des types valides.

        Cette méthode doit parcourir l'objet et associer à chaque objet contenu son identifiant pour le controler en appelant controle_types_item. Controle aussi le type de l'objet conteneur en appelant controle_types. Retourne l'objet valide si aucune erreur n'a été levée.
        Cette classe étant générique, elle ne connait pas la méthode de parcours à appliquer à l'objet et donc lève une erreur quand elle est appelée. Cette méthode doit être implémentée dans les classes filles. 
        """
        raise NotImplementedError("Méthode non implémentée car le parcours de l'objet n'est pas connu. Merci d'utiliser une classe fille pour exécuter cette méthode.")


    def controle_global_item(self, identifiant, item_controlé, conversion=False) :
        """Vérifie que l'objet controlé est valide.
        
        Les critères de validités sont fourni par le vérificateur correspondant à l'id passé en paramètre. La vérification est faite par le vérificateur correspondnant à l'id (identifiant).
        Si aucune erreur est levée, cette méthode retourne l'item_controlé. (Si l'objet a été converti avec succès, l'objet renvoyé est différent de objet_controle.)
        """
        verificateur = self._id_verificateur(identifiant)
        return verificateur.controle_total(item_controlé, conversion=conversion)

    def controle_total(self, objet_controlé, conversion=False) :
        """Vérifie que le conteneur controlé est valide.

        Cette méthode doit parcourir l'objet et associer à chaque objet contenu son identifiant pour le controler en appelant controle_global_item. Controle aussi le conteneur en appelant controle_global. Retourne l'objet valide si aucune erreur n'a été levée.
        Cette classe étant générique, elle ne connait pas la méthode de parcours à appliquer à l'objet et donc lève une erreur quand elle est appelée. Cette méthode doit être implémentée dans les classes filles. 
        """
        raise NotImplementedError("Méthode non implémentée car le parcours de l'objet n'est pas connu. Merci d'utiliser une classe fille pour exécuter cette méthode.")

    def get_liste_verificateurs(self) :
        """Retourne l'attribut liste_verificateur.
        
        Affiche une sorte de tableau avec trois colonnes : une pour le premier identifiant, une deuxième pour le deuxième identifiant et enfin une troisième pour le vérificateur.
        """
        l_colonne = 20
        chaine = "Identifiant 1".center(l_colonne)
        chaine += "Identifiant 2".center(l_colonne)
        chaine += "Vérificateur".center(l_colonne)
        chaine += "\n"

        for i in self._liste_verificateurs :
            for j in i :
                chaine += str(j).center(l_colonne)
            chaine += "\n"
        return chaine

    def clé(self, colonne, index_colonne, valeur_None = None) :
        """Fonction qui permet de trier les identifiants.
            
        Colonne indique la colonne à partir de laquelle il faut trier, valeur_None sert à dire par quelle valeur doit être remplacée None pour pouvoir être triée. (valeur_None doit être du même type que les objet des la colonne triée.)
        """
        data = colonne[index_colonne]
        if data is None :
            data = valeur_None
        return data

    def sort(self, key = None, reverse=False) :
        """Méthode qui trie cet objet en fonction des identifiants.
        
        Par défaut, les vérificateurs sont triés par ordre croissant dans l'ordre des premiers identifiants puis par les seconds identifiants.
        key doit être une fonction prenant en paramètre un seul argument.
        """
        if key :
            self._liste_verificateurs.sort(key=key, reverse=reverse)
        else :
            self._liste_verificateurs.sort(key=lambda colonne: self.clé(colonne, 1))
            self._liste_verificateurs.sort(key=lambda colonne: self.clé(colonne, 0))
            if reverse == True :
                self._liste_verificateurs.reverse()

    def set_minimum(self, nouveau_minimum) :
        """Modifie l'attribut minimum (longueur minimum du conteneur).
        
        Vérifie d'abord que minimum est un nombre entier positif (ou nul).
        """
        if not isinstance(nouveau_minimum, int) :
            raise TypeError("L'attribut minimum doit être un nombre entier positif (ou nul).")
        if nouveau_minimum < 0 :
                raise ValueError("L'attribut minimum doit être un nombre entier positif (ou nul).")
        if self._maximum is not None :
            if nouveau_minimum > self._maximum :
                raise ValueError("L'attribut minimum doit être un nombre entier positif inférieur ou égal au maximum.")
        self._minimum = nouveau_minimum

    def set_maximum(self, nouveau_maximum) :
        """Modifie l'attribut maximum (longueur maximum du conteneur).
        
        Vérifie d'abord que maximum est un nombre entier positif (ou nul), lorsqu'il ne vaut pas None. Vérifie ensuite qu'il est supérieur ou égal au minimum.
        """
        if nouveau_maximum is not None :
            if not isinstance(nouveau_maximum, int) :
                raise TypeError("L'attribut minimum doit être un nombre entier positif (ou nul).")
            if nouveau_maximum < 0 :
                raise ValueError("L'attribut maximum doit être un nombre entier positif (ou nul).")
            if nouveau_maximum < self._minimum :
                raise ValueError("L'attribut maximum doit être un nombre entier positif supérieur ou égal au minimum.")
        self._maximum = nouveau_maximum

    def del_minimum(self) :
        """Réinitialise l'attribut minimum. (minimum vaut alors 0)."""
        self._minimum = 0

    liste_verificateurs = property(get_liste_verificateurs)
    types = property(Verificateur.get_types, Verificateur.set_types, Verificateur.del_types, "Attribut représentant le (ou les) types du conteneur. (s'il y a plusieurs types, il faut les mettre dans un tuple).")
    minimum = property(Verificateur.get_minimum, set_minimum, del_minimum, "Attribut représentant la longueur minimum : longueur minimale autorisée (Le minimum doit être en nombre entier positif ou nul).")
    maximum = property(Verificateur.get_maximum, set_maximum, Verificateur.del_maximum, "Attribut représentant la longueur maximum : longueur maximale autorisée (Le maximum doit être un nombre entier positif supérieur ou égal au minimum).")