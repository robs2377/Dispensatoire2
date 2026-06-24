# flotte.py - À COMPLÉTER (épreuve flotte)
#
# Conteneur Flotte, à transposer de Bibliotheque (S12) : enveloppe
# encapsulée d'une liste de Vehicule, exposant len(), in et for.
# Aucune docstring demandée ; les tests (test_flotte.py) fixent le
# comportement exact. Complétez les corps « ... ».

from vehicule import Vehicule


class Flotte:
    # Garde l'ordre d'ajout, refuse les doublons par châssis, et expose
    # les protocoles de conteneur. La hiérarchie Vehicule la traverse
    # sans aucune modification (polymorphisme) : ni isinstance ni cas
    # particulier par sous-type.

    def __init__(self):
        # Collection interne : une liste (préserve l'ordre d'ajout).
          self._vehicules = {}

    # --- ajouter, retirer ---

    def ajouter(self, vehicule):
        # Refuser un objet qui n'est pas un Vehicule (TypeError) et un
        # doublon de châssis déjà présent (ValueError). Indice : « déjà
        # présent ? » se teste élégamment avec l'opérateur « in » sur self.
        if not isinstance(vehicule, Vehicule):
            raise TypeError("Seuls les objets de type Vehicule peuvent être ajoutés.")
        if vehicule.numero_chassis in self._vehicules:
            raise ValueError("Un véhicule avec ce numero de châssis existe déjà dans la flotte.")
        self._vehicules[vehicule.numero_chassis] = vehicule

    def retirer(self, vehicule):
        # Refuser un non-Vehicule (TypeError) ; absent -> KeyError.
        # __eq__ de Vehicule (par châssis) localise l'élément à retirer.
        if not isinstance(vehicule, Vehicule):
            raise TypeError("Le paramètre doit être une instance de Vehicule.")
        if vehicule.numero_chassis not in self._vehicules:
            raise KeyError("Véhicule absent de la flotte.")
        del self._vehicules[vehicule.numero_chassis]


    # --- Protocole de conteneur ---

    def __len__(self):
        return len(self._vehicules)

    def __contains__(self, item):
        # Accepter soit un Vehicule (comparé par châssis via __eq__), soit
        # une chaîne de châssis. Tout autre type -> False (sans lever).
        if isinstance(item, Vehicule):
            return item.numero_chassis in self._vehicules
        if isinstance(item, str):
            return item in self._vehicules
        return False

    def __iter__(self):
        # Itérer dans l'ordre d'ajout.
        return iter(self._vehicules.values())


    # --- Méthodes métier ---

    def trouver_par_chassis(self, numero_chassis):
        # Renvoyer le véhicule de ce châssis ; absent -> KeyError.
        if numero_chassis not in self._vehicules:
            raise KeyError(f"Aucun véhicule trouvé avec le châssis {numero_chassis}.")
        return self._vehicules[numero_chassis]

    def vehicules_disponibles(self):
        # Liste des véhicules dont disponible vaut True, dans l'ordre d'ajout.
        return [v for v in self._vehicules.values() if v.disponible]

    @property
    def nombre_disponibles(self):
        return sum(1 for v in self._vehicules.values() if v.disponible)

    # --- Représentation ---

    def __repr__(self):
        liste_vehicules = list(self._vehicules.values())
        return f"Flotte({liste_vehicules})"
