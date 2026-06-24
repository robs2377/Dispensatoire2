# vehicule.py - À COMPLÉTER (épreuve flotte)
#
# Hiérarchie Vehicule / VoitureElectrique / Camion, à transposer de la
# hiérarchie Livre / LivreNumerique / LivreAudio (S11-S18).
# Pour cette épreuve, aucune docstring n'est demandée : les indices «#»
# donnent le RÔLE (et parfois le cas analogue à transposer), et les
# tests (test_vehicule.py) fixent les valeurs et exceptions exactes.
# Complétez les corps « ... ».


class Vehicule:
    # ENTITE largement immuable. Identité métier : le numéro de châssis
    # (qui ne change jamais, contrairement à la plaque). Seule la
    # disponibilité évolue. Transposé de Livre (identité par ISBN).

    def __init__(self, marque, modele, numero_chassis, nb_places, annee):
        # Valider chaque caractéristique avant de la stocker :
        #   - marque, modèle : chaînes non vides ;
        #   - châssis : utiliser la méthode de validation dédiée ;
        #   - nb_places, année : entiers, bornes exactes dans les tests.
        # Distinguer TypeError (mauvais type) et ValueError (mauvaise valeur).
        # À la création, le véhicule est disponible.
        if not isinstance(marque, str) or not isinstance(modele, str):
            raise TypeError("la marque et le modele doivent etre des chaine de caractere")
        if marque.strip() =="" or modele.strip()== "" :
            raise ValueError("la marque et le modele ne peuvent pas etre des chaines vides ")
        if not isinstance (numero_chassis, str):
            raise TypeError("le numero de chassis doit etre une chaine de caractere..")
        if not self.chassis_valide(numero_chassis):
            raise ValueError("le numero de chassis '{numero_chassis}' est invalide ")
        if  isinstance(nb_places, bool) or not isinstance(nb_places, int):
            raise TypeError("le nombre de place doit etre un entier")
        if not (1<= nb_places <= 80):
            raise ValueError("le nombre de place doit se trouver entre 1 et 80")
        if not isinstance(annee, int) or isinstance(annee, bool):
            raise TypeError("l'annee doit etre un entier")
        if annee < 1886 :
            raise ValueError("l'annee doit etre superieur ou egal a 1886")
                             
        self._marque = marque
        self._modele= modele
        self._numero_chassis = numero_chassis
        self._nb_places= nb_places
        self._annee = annee
        self._disponible = True


        

    # --- Propriétés en lecture seule ---

    @property
    def marque(self):
        return self._marque

    @property
    def modele(self):
        return self._modele

    @property
    def numero_chassis(self):
        return self._numero_chassis

    @property
    def nb_places(self):
        return self._nb_places

    @property
    def annee(self):
        return self._annee

    @property
    def disponible(self):
        return self._disponible 

    # --- Méthode statique ---

    @staticmethod
    def chassis_valide(chaine):
        # Vrai si la chaîne a exactement la bonne longueur et n'est faite
        # que de caractères alphanumériques. Longueur et nature exactes :
        # déductibles des tests. Une entrée non-str renvoie False.
        if not isinstance(chaine, str) :
            return False
        return len(chaine) == 17 and chaine.isalnum()

    # --- Constructeur alternatif ---

    @classmethod
    def depuis_csv(cls, ligne):
        # Découper la ligne, vérifier le nombre de champs, construire via
        # cls(...). Même rôle que Livre.depuis_chaine_csv : utiliser cls
        # (et non Vehicule) est ce qui donnera le TYPE EXACT dans les
        # sous-classes.
        if not isinstance(ligne, str):
            raise TypeError("La ligne CSV doit être une chaîne.")
        
        champs = [c.strip() for c in ligne.split(";")]
        
        if len(champs) != 5:
            raise ValueError(f"Nombre de champs incorrect pour un Vehicule de base. Reçu : {len(champs)}")

        marque, modele, numero_chassis = champs[0], champs[1], champs[2]
        
        try:
            nb_places = int(champs[3])
            annee = int(champs[4])
        except ValueError:
            raise TypeError("Les champs numériques doivent être des entiers.")

        return cls(marque, modele, numero_chassis, nb_places, annee)

    # --- Sérialisation JSON ---

    def to_dict(self):
        # Produire un dict marqué d'un champ « type » (le discriminateur
        # qui guidera la reconstruction). Clés attendues : voir les tests.
        return {
            "type": self.__class__.__name__,
            "marque": self.marque,
            "modele": self.modele,
            "numero_chassis": self.numero_chassis,
            "nb_places": self.nb_places,
            "annee": self.annee,
            "disponible": self.disponible
        }

    @classmethod
    def from_dict(cls, donnees):
        # Pendant de to_dict : reconstruire via cls(...), puis restaurer la
        # disponibilité par l'API publique (jamais en écrivant l'attribut
        # privé). Même logique que Livre.from_dict.
        if not isinstance(donnees, dict):
            raise TypeError("Les données doivent être un dictionnaire.")
            
        obj = cls(
            donnees["marque"],
            donnees["modele"],
            donnees["numero_chassis"],
            donnees["nb_places"],
            donnees["annee"]
        )
        
        if not donnees.get("disponible", True):
            obj.louer()
        return obj


    @staticmethod
    def _restaurer_disponibilite(vehicule, donnees):
        # Si l'objet était loué, le replacer dans cet état via la méthode
        # métier. Factorisé : toutes les sous-classes restaurent pareil.
        if not donnees.get("disponible", True):
            vehicule.louer()

    # --- Méthodes métier ---

    def louer(self):
        # Bascule vers « loué » ; refuser si déjà loué.
        if not self._disponible:
            raise ValueError("Le véhicule est déjà loué.")
        self._disponible = False

    def restituer(self):
        # Bascule vers « disponible » ; refuser si déjà disponible.
        if self._disponible:
            raise ValueError("Le véhicule est déjà disponible.")
        self._disponible = True

    def fiche_resume(self):
        # Description de la capacité d'un véhicule générique. Format exact :
        # voir les tests. (Transposé de Livre.taille_estimee.)
        return f"{self.nb_places} places"

    # --- Représentations ---

    def __str__(self):
         etat = "disponible" if self.disponible else "loué"
         return f"{self.marque} {self.modele} ({self.numero_chassis}) - {etat}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.marque}', '{self.modele}', '{self.numero_chassis}', {self.nb_places}, {self.annee})"

    # --- Identité (entité) ---

    def __eq__(self, autre):
        # Vehicule est une ENTITE : égalité par numéro de châssis (comme
        # Livre par ISBN). NotImplemented si « autre » n'est pas un Vehicule.
        if not isinstance(autre, Vehicule):
            return NotImplemented
        return self.numero_chassis == autre.numero_chassis

    def __hash__(self):
        # Cohérent avec __eq__ : fondé sur le châssis.
        return hash(self.numero_chassis)


class VoitureElectrique(Vehicule):
    # Enrichit Vehicule d'une autonomie. Transposé de LivreNumerique.

    def __init__(self, marque, modele, numero_chassis, nb_places, annee,
                 autonomie_km):
        # Déléguer la validation héritée au parent, puis valider l'attribut
        # propre (autonomie : entier strictement positif).
        super().__init__(marque, modele, numero_chassis, nb_places, annee)
        
        if not isinstance(autonomie_km, int) or isinstance(autonomie_km, bool):
            raise TypeError("L'autonomie doit être un entier.")
        if autonomie_km <= 0:
            raise ValueError("L'autonomie doit être strictement positive.")
            
        self._autonomie_km = autonomie_km

    @property
    def autonomie_km(self):
         return self._autonomie_km

    @classmethod
    def depuis_csv(cls, ligne):
        # Comme Vehicule.depuis_csv, mais un champ de plus (l'autonomie).
        if not isinstance(ligne, str):
            raise TypeError("La ligne CSV doit être une chaîne.")
        
        champs = [c.strip() for c in ligne.split(";")]
        
        if len(champs) != 6:
            raise ValueError(f"Nombre de champs incorrect pour une Voiture Électrique. Reçu : {len(champs)}")

        marque, modele, numero_chassis = champs[0], champs[1], champs[2]
        
        try:
            nb_places = int(champs[3])
            annee = int(champs[4])
            autonomie_km = int(champs[5])  
        except ValueError:
            raise TypeError("Les champs numériques (places, année, autonomie) doivent être des entiers.")

        return cls(marque, modele, numero_chassis, nb_places, annee, autonomie_km)

    def to_dict(self):
        # ENRICHIR le dictionnaire hérité du parent (ne pas le réécrire) :
        # corriger « type » et ajouter l'attribut propre. (Geste de
        # LivreNumerique.to_dict.)
        d = super().to_dict()
        d["autonomie_km"] = self.autonomie_km
        return d

    @classmethod
    def from_dict(cls, donnees):
        if not isinstance(donnees, dict):
            raise TypeError("Les données doivent être un dictionnaire.")
            

        obj = cls(
            donnees["marque"],
            donnees["modele"],
            donnees["numero_chassis"],
            donnees["nb_places"],
            donnees["annee"],
            donnees["autonomie_km"] 
        )
        
        if not donnees.get("disponible", True):
            obj.louer()
        return obj


    def fiche_resume(self):
        # On REPREND la fiche de base et on la complète : la capacité reste
        # un préfixe (ENRICHISSEMENT). Format exact : voir les tests.
         return f"{super().fiche_resume()} [électrique, {self.autonomie_km} km]"

    def __str__(self):
        etat = "disponible" if self.disponible else "loué"
        return f"{self.marque} {self.modele} ({self.numero_chassis}) - {etat}"

    def __repr__(self):
         return (f"{self.__class__.__name__}('{self.marque}', '{self.modele}', "
                f"'{self.numero_chassis}', {self.nb_places}, {self.annee}, {self.autonomie_km})")


class Camion(Vehicule):
    # La mesure pertinente est la charge utile, pas le nombre de places.
    # Transposé de LivreAudio (durée d'écoute plutôt que pages).

    def __init__(self, marque, modele, numero_chassis, nb_places, annee,
                 charge_utile_t):
        # Déléguer au parent, puis valider l'attribut propre (charge :
        # nombre strictement positif, stocké en float).
        super().__init__(marque, modele, numero_chassis, nb_places, annee)
        
        if not isinstance(charge_utile_t, (int, float)) or isinstance(charge_utile_t, bool):
            raise TypeError("La charge utile doit être un nombre réel (float).")
        if float(charge_utile_t) <= 0:
            raise ValueError("La charge utile doit être strictement positive.")
            
        self._charge_utile_t = float(charge_utile_t)

    @property
    def charge_utile_t(self):
        return self._charge_utile_t

    @classmethod
    def depuis_csv(cls, ligne):
        if not isinstance(ligne, str):
            raise TypeError("La ligne CSV doit être une chaîne.")
        
        champs = [c.strip() for c in ligne.split(";")]
        
        if len(champs) != 6:
            raise ValueError(f"Nombre de champs incorrect pour un Camion. Reçu : {len(champs)}")

        marque, modele, numero_chassis = champs[0], champs[1], champs[2]
        
        try:
            nb_places = int(champs[3])
            annee = int(champs[4])
        except ValueError:
            raise TypeError("Le nombre de places et l'année doivent être des entiers.")
            
        try:
            charge_utile_t = float(champs[5])  
        except ValueError:
            raise TypeError("La charge utile doit être un nombre réel (float).")

        return cls(marque, modele, numero_chassis, nb_places, annee, charge_utile_t)


    def to_dict(self):
        d = super().to_dict()
        d["charge_utile_t"] = self.charge_utile_t
        return d

    @classmethod
    def from_dict(cls, donnees):
        if not isinstance(donnees, dict):
            raise TypeError("Les données doivent être un dictionnaire.")

        obj = cls(
            donnees["marque"],
            donnees["modele"],
            donnees["numero_chassis"],
            donnees["nb_places"],
            donnees["annee"],
            donnees["charge_utile_t"]  
        )
        if not donnees.get("disponible", True):
            obj.louer()
        return obj


    def fiche_resume(self):
        # Ici la mesure pertinente n'est PAS le nombre de places : on ne
        # réutilise donc PAS la fiche de base (REMPLACEMENT). Format exact :
        # voir les tests.
        return f"{self.charge_utile_t} t de charge"

    def __str__(self):
         etat = "disponible" if self.disponible else "loué"
         return f"{self.marque} {self.modele} ({self.numero_chassis}) - {etat}"

    def __repr__(self):
         return (f"{self.__class__.__name__}('{self.marque}', '{self.modele}', "
                f"'{self.numero_chassis}', {self.nb_places}, {self.annee}, {self.charge_utile_t})")
