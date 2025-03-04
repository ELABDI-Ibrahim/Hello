import pandas as pd
import uuid

class Session:
    def __init__(self, list_organismes: list = None):
        self.list_organismes = list_organismes if list_organismes is not None else []
    
    def get_organisme_by_id(self, id_organisme):
        for org in self.list_organismes:
            if org.id_organisme == id_organisme:
                return org
        return None


class Organisme:
    def __init__(
        self,
        id_organisme: int = None,  # Generated
        nom_organisme: str = "",  # Input
        criteres_eligibilite_organisme: list = None,  # Input
        list_billets: list = None,  # Input
        code_mobilisation: str = "",  # Input
        colonne_mob_billet: str = "",  # Input
        permanence_creances: bool = True,  # Input
    ):
        self.id_organisme = id_organisme if id_organisme is not None else uuid.uuid4().int % 10000
        self.nom_organisme = nom_organisme
        self.criteres_eligibilite_organisme = (
            criteres_eligibilite_organisme
            if criteres_eligibilite_organisme is not None
            else []
        )
        self.list_billets = list_billets if list_billets is not None else []
        self.code_mobilisation = code_mobilisation
        self.colonne_mob_billet = colonne_mob_billet
        self.permanence_creances = permanence_creances

    def count_billet(self):
        return len(self.list_billets)
    
    def get_billet_by_id(self, id_billet):
        for billet in self.list_billets:
            if billet.id_billet == id_billet:
                return billet
        return None


class Billet:
    def __init__(
        self,
        id_billet: int = None,  # Generated when creating the object
        nom_billet: str = "",  # Input
        montant_cible_billet: float = 0.0,  # Input
        list_criteres_profilages: list = None,  # Input
        liste_prets_filtrer: pd.DataFrame = None,  # Generated from input data
    ):
        self.id_billet = id_billet if id_billet is not None else uuid.uuid4().int % 10000
        self.nom_billet = nom_billet
        self.montant_cible_billet = montant_cible_billet
        self.montant_mobilise_billet = None
        self.montant_mobilise_initial_billet = None
        self.montant_disponible_billet = None
        self.list_criteres_profilages = (
            list_criteres_profilages if list_criteres_profilages is not None else []
        )
        self.liste_prets_filtrer = (
            liste_prets_filtrer if liste_prets_filtrer is not None else pd.DataFrame()
        )
        self.tranches_remplies = False

    def count_critere(self):
        return len(self.list_criteres_profilages)
    
    def get_critere_by_id(self, id_critere_profilage):
        for critere in self.list_criteres_profilages:
            if critere.id_critere_profilage == id_critere_profilage:
                return critere
        return None


class CritereProfilage:
    def __init__(
        self,
        id_critere_profilage: int = None,  # Generated from input data
        nom_critere_profilage: str = "",  # Input
        list_tranches: list = None,  # Input
    ):
        self.id_critere_profilage = id_critere_profilage if id_critere_profilage is not None else uuid.uuid4().int % 10000
        self.nom_critere_profilage = nom_critere_profilage
        self.list_tranches = list_tranches if list_tranches is not None else []

    def count_tranche(self):
        return len(self.list_tranches)

    def sort_tranches_by_priority(self):
        if self.list_tranches:
            list_tranches_sorted = sorted(
                self.list_tranches, key=lambda x: x.priorite_tranche, reverse=False
            )
            return list_tranches_sorted
        return []
    
    def get_tranche_by_id(self, id_tranche):
        for tranche in self.list_tranches:
            if tranche.id_tranche == id_tranche:
                return tranche
        return None


class Tranche:
    def __init__(
        self,
        id_tranche: int = None,  # Generated from input data
        nom_tranche: str = "",  # Input
        condition_tranche: str = "",  # Input
        montant_disponible_tranche: float = None,  # Generated from input data
        montant_necessaire_tranche: float = None,  # Generated from input data
        montant_mobilise_tranche: float = None,  # Generated from input data
        montant_mobilise_initial_tranche: float = None,  # Generated from input data
        pourcentage_tranche: float = None,  # Default value Generated from input data Or Inputed in the platform
        priorite_tranche: int = None,  # Generated from input data
        condition_verifier_filtrage: bool = None,  # Generated from input data
        pret_not_mobilise_par_tranche: pd.DataFrame = None,  # Generated from input data
    ):
        self.id_tranche = id_tranche if id_tranche is not None else uuid.uuid4().int % 10000
        self.nom_tranche = nom_tranche
        self.condition_tranche = condition_tranche
        self.montant_disponible_tranche = montant_disponible_tranche
        self.montant_necessaire_tranche = montant_necessaire_tranche
        self.montant_mobilise_tranche = montant_mobilise_tranche
        self.montant_mobilise_initial_tranche = montant_mobilise_initial_tranche
        self.pourcentage_tranche = pourcentage_tranche
        self.priorite_tranche = priorite_tranche
        self.condition_verifier_filtrage = condition_verifier_filtrage
        self.pret_not_mobilise_par_tranche = pret_not_mobilise_par_tranche