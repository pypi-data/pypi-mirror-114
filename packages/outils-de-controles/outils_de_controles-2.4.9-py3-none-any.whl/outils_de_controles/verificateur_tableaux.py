"""Ce module contient la classe VerificateurTableaux."""

from outils_de_controles.verificateur import *
from outils_de_controles.verificateur_listes import *

class VerificateurTableaux(VerificateurListes) :
    """Cette classe vérifie la validité d'objet tableaux.
    
    Cette classe a pour but de vérifier la validité d'objets contenus dans un tableau, c'est à dire une liste contenant d'autres listes, qui forme un tableau bi-dimensionnel.

    Remarque : ce "type" d'objet n'est pas vraiment un type résultant d'une classe mais une structure d'objets composés de listes. Cependant, cette structure est utilisé afin de définir des classes (exemple : la classe Tableau a un attribut utilisant cette structure.) Néanmoins l'objet vérifié n'est pas du type Tableau.

    Cette classe permet de paramétrer des objets verificateurs pour le nom du tableau, les en-têtes verticales et horizontalesainsi que pour chaque colonne. De plus, cette classe définit un nombre minimal et maximal de lignes et de colonnes.
    """

    def __init__(self, *args, minimum=(2,2), maximum=(2**10,2**20),nom_tableau=Verificateur(str), en_tete_h=Verificateur(), en_tete_v=Verificateur()) :
        """Initialise l'objet VerificateurTableaux.

        Enregistre les différents paramètres dans les attributs.
        """
        self._types = list
        self._maximum = (None,None)
        self.set_minimum(minimum)
        self.set_maximum(maximum)

        self._nom_tableau = nom_tableau
        self._en_tete_h = en_tete_h
        self._en_tete_v = en_tete_v  

        self._liste_verificateurs = []
        for liste in args :
            self._append(liste)

    
    def __str__(self) :
        """Méthode spéciale appelé quand on cherche à afficher l'objet.
        
        Affiche les attributs de l'objet. Affiche une sorte de tableau avec trois colonnes : une pour le premier identifiant, une deuxième pour le deuxième identifiant et enfin une troisième pour le vérificateur.
        """
        chaine = """◄minimum:{obj._minimum}, maximum:{obj._maximum}, nom_tableau:{obj._nom_tableau}, en_tete_h:{obj._en_tete_h}, en_tete_v:{obj._en_tete_v}\n\n""".format(obj = self)#obj désigne l'objet vérificateur qu'il faut afficher
        chaine += self.get_liste_verificateurs()
        return chaine + """►\n"""
    
    def __repr__(self) :
        """Méthode représentant l'objet pour le débugage.

        Retourne une chaine avec le nom de la classe et les attributs (sauf _verificateurTableau).
        """
        liste = repr(self._liste_verificateurs)
        liste = liste[1:-1]
        if liste :
            liste += ","
        chaine = """outils_de_controles.VerificateurTableaux({} minimum={}, maximum={}, nom_tableau={}, en_tete_h={}, en_tete_v={})""".format(liste, repr(self.minimum), repr(self.maximum), repr(self.nom_tableau), repr(self.en_tete_h), repr(self.en_tete_v))
        return chaine

    def __eq__(self, aVT) : #aVT pour autre VerificateurTableaux
        """Méthode comparant deux objets VerificateurConteneurs.
        
        Si ces deux objets sont égaux (c'est-à-dire que tous leurs attributs sont égaux), cette méthode renvoie True.
        """
        if not isinstance(aVT, type(self)) :
            raise TypeError("""Le deuxième objet n'est pas un objet de la classe {}.""".format(type(self)))
        retour = False
        if self._liste_verificateurs == aVT._liste_verificateurs \
        and self._types == aVT._types \
        and self.minimum == aVT.minimum \
        and self.maximum == aVT.maximum \
        and self._nom_tableau == aVT._nom_tableau \
        and self.en_tete_h == aVT.en_tete_h \
        and self.en_tete_v == aVT.en_tete_v :
            retour = True
        return retour

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
                if validation[id] <= 0 :
                    raise ValueError("Les identifiants sont des index et doivent donc être des nombres entiers positifs (strictement supérieur à 0).")
        VerificateurListes._append(self, validation)

    def controle_types(self, objet_controlé, conversion=False) :
        """Vérifie que le type du conteneur est correct.

        Vérifie que le tableau est une liste dans laquelle sont imbriquées d'autres listes. Si le type est incorrect et que conversion est vrai, cette méthode tente de convertir l'objet controlé en un objet du bon type. Si la conversion a lieu avec succès, l'objet renvoyé est différent de l'objet fourni en paramètre.
        """
        if conversion :
            objet_controlé = self._conversion(objet_controlé)
        else :
            objet_controlé = VerificateurListes.controle_types(self, objet_controlé)
            for i, ligne in enumerate(objet_controlé) :#on vérifie que les objets contenus sont bien des listes
                try :
                    objet_controlé[i] = VerificateurListes.controle_types(self, ligne, conversion=conversion)
                except TypeError :
                    raise TypeError("""Un tableau doit être une liste contenant d'autres listes.""")
        return objet_controlé

    def controle_minimum(self, objet_controlé) :
        """Vérifie que objet_controlé est plus long que le minimum autorisé.
        
        Vérifie que le tableau a une dimension suppérieure aux dimension minimales, définies par self.minimum. Retourne objet_controlé si aucune erreur est levée.
        """
        if self._minimum[1] and len(objet_controlé) < self._minimum[1] :#controle pour le nombre de lignes
            raise ValueError("Le tableau n'a pas assez de lignes.")
        
        for i in objet_controlé :#controle pour le nombre de colonnes
            if self._minimum[0] and len(i) < self._minimum[0] :
                raise ValueError("Le tableau n'a pas assez de colonnes.")
        return objet_controlé
    
    def controle_maximum(self, objet_controlé) :
        """Vérifie que objet_controlé est moins long que le maximum valide.
        
        Vérifie que le tableau n'a ni trop de lignes ni trop de colonnes. Retourne objet_controlé si aucune erreur est levée.
        """
        if self._maximum[1] and len(objet_controlé) > self._maximum[1] :#controle pour le nombre de lignes
            raise ValueError("Le tableau a trop de lignes.")
        
        for i in objet_controlé :#controle pour le nombre de colonnes
            if self._maximum[0] and len(i) > self._maximum[0] :
                raise ValueError("Le tableau a trop de colonnes.")
        return objet_controlé

    def controle_nom_tableau(self, objet_controlé, conversion=False) :
        """Vérifie que objet_controlé comporte un nom de tableau valide.

        Le nom du tableau est en position [0][0] du tableau est doit être valide selon les critères du vérificateur contenu par self.nom_tableau.
        Retourne l'objet controlé si aucune erreur est levée.
        """
        objet_controlé[0][0] = self._nom_tableau.controle_total(objet_controlé[0][0], conversion=conversion)
        return objet_controlé

    def controle_en_tete_h(self, objet_controlé, conversion=False) :
        """Vérifie que objet_controlé a des en-têtes horizontales valides.

        Vérifie que chaque en-tête horizontale est valide selon les critères du vérificateur défini dans self.en_tete_h. Retourne l'objet controlé si aucune erreur est levée.
        """
        for i in range(1, len(objet_controlé[0])) :#on ne vérifie pas la position [0][0], qui comporte le nom du tableau
            objet_controlé[0][i] = self._en_tete_h.controle_total(objet_controlé[0][i], conversion=conversion)
        return objet_controlé

    def controle_en_tete_v(self, objet_controlé, conversion=False) :
        """Vérifie que objet_controlé a des en-têtes verticales valides.

        Vérifie que chaque en-tête verticale est valide selon les critères du vérificateur défini dans self.en_tete_v. Retourne l'objet controlé si aucune erreur est levée.
        """
        for i in range(1, len(objet_controlé)) :#on ne vérifie pas la position [0][0], qui comporte le nom du tableau
            objet_controlé[i][0] = self._en_tete_v.controle_total(objet_controlé[i][0], conversion = conversion)
        return objet_controlé

    def controle_taille_lignes(self, objet_controlé) :
        """Vérifie que toutes les lignes sont de tailles égales.
        
        Retourne l'objet controlé si aucune erreur est levée.
        """
        for i in objet_controlé :
            if len(i) != len(objet_controlé[0]) :
                raise ValueError("""Le tableau n'est pas valide car toutes les lignes n'ont pas la même longueur.""")
        return objet_controlé

    def controle_global(self, objet_controlé, conversion=False) :
        """Vérifie que objet_controlé est globalement valide.
        
        Vérifie que l'object controlé est du bon type et a une longueur valide.Vérifie également que le nom du tableau, les en-têtes horizontales et verticales soient valides. Les objets contenus ne sont pas vérifiés. Retourne l'objet controlé si aucune erreur est lévée.
        """
        objet_controlé = self.controle_types(objet_controlé, conversion=conversion)
        objet_controlé = self.controle_minimum(objet_controlé)
        objet_controlé = self.controle_maximum(objet_controlé)
        objet_controlé = self.controle_nom_tableau(objet_controlé, conversion=conversion)
        objet_controlé = self.controle_en_tete_h(objet_controlé, conversion=conversion)
        objet_controlé = self.controle_en_tete_v(objet_controlé, conversion=conversion)
        objet_controlé = self.controle_taille_lignes(objet_controlé)
        if conversion :
            self.controle_global(objet_controlé)#on recontrole l'objet controlé car il a pu changer entre le début et la fin de la méthode
        return objet_controlé

    def controle_types_total(self, objet_controlé, conversion=False):
        """Vérifie que les objets contenus ont des types valides.
        
        Vérifie d'abord que le tableau est une liste dans laquelle sont imbriquées d'autres listes (appel de controle_types). Vérifie ensuite que le nom du tableaux et tous les en-têtes sont du bon type. Enfin, vérifie que les objets contenus dans les cases "normales" sont du bon types (grâce à controle_types_item).
        Retourne l'objet controlé s'il est valide.
        """
        objet_controlé = self.controle_types(objet_controlé, conversion=conversion)

        for i in range(len(objet_controlé)) :#i est le numéro de ligne
            for j in range(len(objet_controlé[i])) :#j est le numéro de colonne
                if i == 0 and j == 0 :
                    objet_controlé[0][0] = self._nom_tableau.controle_types_total(objet_controlé[0][0], conversion=conversion)#controle du type du nom du tableau
                elif i == 0 :#si i==0 et j!=0
                    objet_controlé[0][j] = self._en_tete_h.controle_types_total(objet_controlé[0][j], conversion=conversion)#controle des types des en-têtes horizontaux
                elif j==0 :#si j==0 et i!=0
                    objet_controlé[i][0] = self._en_tete_v.controle_types_total(objet_controlé[i][0], conversion=conversion)#controle du type des en-têtes verticaux
                else :
                    objet_controlé[i][j] = self.controle_types_item(j, objet_controlé[i][j], conversion=conversion)#controle du type des objets contenus dans les cases normales
        return objet_controlé
       

    def controle_total(self, objet_controlé, conversion=False) :
        """Vérifie que le tableau controlé est valide.
        
        Appelle d'abord controle_global pour vérifier que le tableaux est du bon type, de la bonne dimension, qu'il a un nom valide et que ces en-têtes sont elles aussi valides. Ensuite, vérifie à l'aide de controle_global_item que tous les objets contenus dans les cases "normales" sont valides.
        """
        objet_controlé = self.controle_global(objet_controlé, conversion=conversion)
        #controle des cases "normales"
        for i in range(1,len(objet_controlé)) :#i est le numéro de ligne
            for j in range(1,len(objet_controlé[i])) :#j est le numéro de colonne
                objet_controlé[i][j] = self.controle_global_item(j, objet_controlé[i][j], conversion=conversion)
        return objet_controlé

    def get_nom_tableau(self) :
        """Retourne l'attribut nomTableau."""
        return self._nom_tableau

    def get_en_tete_h(self) :
        """Retourne l'attribut en_tete_h."""
        return self._en_tete_h
    
    def get_en_tete_v(self) :
        """Retourne l'attribut en_tete_v."""
        return self._en_tete_v

    def set_minimum(self, nouvelle_valeur) :
        """Modifie l'attribut minimum.

        Vérifie d'abord que minimum est une liste ou un tuple de deux éléments. Ces deux éléments doivent être deux nombres entiers supérieurs à 1. De plus, le nombre minimal de colonnes doit être inférieur au nombre maximal de colonnes et le nombre minimal de lignes doit être inférieur au nombre maximal de lignes.
        """
        if not isinstance(nouvelle_valeur, (tuple, list)) :
            raise TypeError("L'attribut minimum doit être un tuple ou une liste de deux éléments : le premier est le nombre minimal de colonnes et le second est le nombre minimal de lignes.")
        if len(nouvelle_valeur) != 2 :
            raise ValueError("L'attribut minimum doit être un tuple ou une liste de deux éléments : le premier est le nombre minimal de colonnes et le second est le nombre minimal de lignes.")
        for i,min in enumerate(nouvelle_valeur) :
            if not isinstance(min, int) :
                raise TypeError("L'attribut minimum doit être un tuple ou une liste de deux éléments : le premier est le nombre minimal de colonnes et le second est le nombre minimal de lignes. Ces deux éléments doivent être du type int.")
            if min < 2 :
                raise ValueError("L'attribut minimum doit être un tuple ou une liste de deux éléments : le premier est le nombre minimal de colonnes et le second est le nombre minimal de lignes. Ces deux éléments doivent être du type int et supérieur à 1.")
            if self._maximum[i] is not None and min > self._maximum[i] :
                raise ValueError("Le nombre minimal de colonnes doit être inférieur au nombre maximal de colonnes et le nombre minimal de lignes doit être inférieur au nombre maximal de lignes.")
        self._minimum = nouvelle_valeur    
    
    def set_maximum(self, nouvelle_valeur) :
        """Modifie l'attribut maximum.

        Vérifie d'abord que maximum est une liste ou un tuple de deux éléments. Ces deux éléments doivent être deux nombres entiers (ou valent None). De plus, le nombre maximal de colonnes doit être supérieur au nombre minimal de colonnes et le nombre maximal de lignes doit être supérieur au nombre minimal de lignes.
        """
        if not isinstance(nouvelle_valeur, (tuple, list)) :
            raise TypeError("L'attribut maximum doit être un tuple ou une liste de deux éléments : le premier est le nombre maximal de colonnes et le second est le nombre maximal de lignes.")
        if len(nouvelle_valeur) != 2 :
            raise ValueError("L'attribut maximum doit être un tuple ou une liste de deux éléments : le premier est le nombre maximal de colonnes et le second est le nombre maximal de lignes.")
        for i,max in enumerate(nouvelle_valeur) :
            if max is not None :
                if not isinstance(max, int) :
                    raise TypeError("L'attribut maximum doit être un tuple ou une liste de deux éléments : le premier est le nombre maximal de colonnes et le second est le nombre maximal de lignes. Ces deux éléments doivent être du type int ou valoir None.")
                if max < self._minimum[i] :
                    raise ValueError("Le nombre maximal de colonnes doit être supérieur au nombre minimal de colonnes et le nombre maximal de lignes doit être supérieur au nombre minimal de lignes.")                
        self._maximum = nouvelle_valeur

    def set_nom_tableau(self, nouvelle_valeur) :
        """Modifie l'attribut nomTableau."""
        self._nom_tableau = nouvelle_valeur

    def set_en_tete_h(self, nouvelle_valeur) :
        """Modifie l'attribut en_tete_h."""
        self._en_tete_h = nouvelle_valeur
    
    def set_en_tete_v(self, nouvelle_valeur) :
        """Modifie l'attribut en_tete_v."""
        self._en_tete_v = nouvelle_valeur
    
    def del_minimum(self) :
        """Supprime l'attribut minimum."""
        self._minimum = (2,2)

    def del_maximum(self) :
        """Supprime l'attribut maximum."""
        self._maximum = (None, None)

    def del_nom_tableau(self) :
        """Supprime l'attribut nomTableau.
        
        L'attribut est mis à la valeur Verificateur() car cet objet verificateur considère comme valide tous les objets.
        """
        self._nom_tableau = Verificateur()    

    def del_en_tete_h(self) :
        """Supprime l'attribut en_tete_h.
        
        L'attribut est mis à la valeur Verificateur() car cet objet verificateur considère comme valide tous les objets.
        """
        self._en_tete_h = Verificateur()
    
    def del_en_tete_v(self) :
        """Supprime l'attribut en_tete_v.
        
        L'attribut est mis à la valeur Verificateur() car cet objet verificateur considère comme valide tous les objets.
        """
        self._en_tete_v = Verificateur()

    def _conversion(self, objet_controlé) :
        """Converti l'objet controlé en type valide.
        
        Cette méthode tente de convertir objet _controlé en objet du bon type.Retourne l'objet s'il a été converti avec succès.
        """
        if not isinstance(objet_controlé, self._types) :
            objet_controlé = VerificateurListes._conversion(self, objet_controlé)
        for i, sous_liste in enumerate(objet_controlé) :#on vérifie que les objets contenus sont bien des listes
            objet_controlé[i] = VerificateurListes._conversion(self, sous_liste)
        return self.controle_types(objet_controlé)

    liste_verificateurs = property(VerificateurListes.get_liste_verificateurs)
    types = property(VerificateurListes.get_types)
    minimum = property(VerificateurListes.get_minimum, set_minimum, del_minimum, "Tuple représentant les dimensions minimales du tableau.")
    maximum = property(VerificateurListes.get_maximum, set_maximum, del_maximum, "Tuple représentant les dimensions maximales du tableau.")
    nom_tableau = property(get_nom_tableau, set_nom_tableau, del_nom_tableau, "Attribut représentant l'objet qui vérifie la validité du nom du tableau.")
    en_tete_h = property(get_en_tete_h, set_en_tete_h, del_en_tete_h, "Attribut représentant l'objet qui vérifie la validité des en-têtes horizontaux.")
    en_tete_v = property(get_en_tete_v, set_en_tete_v, del_en_tete_v, "Attribut représentant l'objet qui vérifie la validité des en-têtes verticaux.")
    