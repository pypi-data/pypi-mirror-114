"""Ce module permet de contrôler les types et les arguments.

Ce module grâce à des décorateurs et à des classes permet de vérifier la validité des arguments fournis à des fonctions/méthodes. Vérifie notamment les types de ces objets.
"""

from outils_de_controles.verificateur_arguments import *


def controle_types(*args_attendus,**kwargs_attendus) :
    """Fonction qui contrôle les types des arguments de fonctions.
    
    On attend en paramètres du décorateur soit un objet ArgumentsAttendus, soit les types souhaités, attendus par la fonction/méthode à exécuter (un argument = un type). On accepte une liste de paramètres indéterminés, étant donné que notre fonction définie pourra être appelée avec un nombre variable de paramètres et que chacun doit être contrôlé. Cette fonction transmet ces paramètres au décorateur.
    """
    def decorateur_types(fonction) :
        """C'est le décorateur. Il renvoie la fonction vérifiée."""
        def fonction_vérifiée_types(*args, **kwargs) :
            """Fonction qui se charge de contrôler les types.
        
            Cette fonction renvoie la fonction exécutée, lorsque les types sont corrects (aucune erreur levée).
            """
            if isinstance(args_attendus[0], VerificateurArguments) :#si les types sont dans un objet VerificateurArguments
                try :
                    if isinstance(args_attendus[1], bool) :#si le deuxième argument non nommé est un booléen, on modifie conversion
                        conversion = args_attendus[1]
                except IndexError :
                    try :
                        if isinstance(kwargs_attendus["conversion"], bool) : #si un argument nommé "conversion" est un booléen, on modifie conversion
                            conversion = kwargs_attendus["conversion"]
                    except KeyError :
                        conversion = False
                v_args, v_kwargs = args_attendus[0].controle_types_total(args, kwargs, conversion=conversion)

            else :#si les types sont en arguments dans l'appel de la fonction controle_types
                if len(args_attendus) != len(args) : #on vérifie le nombre d'arguments reçus (en revanche, on ne fait pas cette vérification si on a un objet argumentsAttendus, car si un argument ne correspond à aucun argument attendu, lors de l'appel de controle_type, une erreur est levée)
                    raise TypeError("{} arguments sont attendus mais {} sont passées en paramètres.".format(len(args_attendus), len(args)))
                for i, arg in enumerate(args) : #on parcours la listes des paramètres non nommés
                    if not isinstance(arg, args_attendus[i]) :
                        raise TypeError("L'argument {} n'est pas du type {}.".format(i, args_attendus[i]))
                for cle in kwargs : #on parcours la listes des paramètres nommés
                    if cle not in kwargs_attendus :
                        raise TypeError("L'argument {} n'est pas valide (son type n'est pas précisé).".format(repr(cle)))
                    if not isinstance(kwargs[cle], kwargs_attendus[cle]) :
                        raise TypeError("L'argument {} n'est pas du type {}.".format(repr(cle), kwargs_attendus[cle]))
                v_args, v_kwargs = args, kwargs
            return fonction(*v_args, **v_kwargs)
        return fonction_vérifiée_types
    return decorateur_types


def controle_arguments(verificateur_arguments, conversion=False) :
    """Fonction qui contrôle les arguments de fonctions/méthodes.
    
    On attend en paramètres du décorateur un objet VerificateurArguments, qui précise les critères de validités des arguments. Conversion est un booléen qui précise si l'on doit tenter de convertir un objet lorsque son type est invalide.
    """
    def decorateur(fonction) :
        """C'est le décorateur. Il renvoie la fonction vérifiée."""
        def fonction_vérifiée(*args, **kwargs) :
            """Fonction qui se charge de contrôler les arguments.
        
            Cette fonction renvoie la fonction exécutée, lorsque les arguments sont valides (aucune erreur levée).
            """
            if not isinstance(verificateur_arguments, VerificateurArguments) :#si les types ne sont pas dans un objet VerificateurArguments
                raise TypeError("""L'argument "verificateur_arguments" doit être un objet de la classe VerificateurArguments.""")
            if not isinstance(conversion, bool) :#si conversion n'est pas un booléen
                raise TypeError("""L'argument "conversion" doit être un booléen.""")
            v_args, v_kwargs = verificateur_arguments.controle_total(args, kwargs, conversion=conversion)
            
            return fonction(*v_args, **v_kwargs)
        return fonction_vérifiée
    return decorateur
