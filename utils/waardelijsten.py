from enum import Enum

#
# Hardcoded waardelijsten
# Versions;
# - LVBB BHKV 1.2.0
#


# https://gitlab.com/koop/lvbb/bronhouderkoppelvlak/-/blob/1.2.0/waardelijsten/procedurestap_definitief.xml?ref_type=tags
class ProcedureStappenDefinitief(Enum):
    Vaststelling = "/join/id/stop/procedure/stap_002"
    Ondertekening = "/join/id/stop/procedure/stap_003"
    Publicatie = "/join/id/stop/procedure/stap_004"
    Einde_bezwaartermijn = "/join/id/stop/procedure/stap_015"
    Einde_beroepstermijn = "/join/id/stop/procedure/stap_016"
    Start_beroepsprocedure = "/join/id/stop/procedure/stap_018"
    Schorsing = "/join/id/stop/procedure/stap_019"
    Opheffing_schorsing = "/join/id/stop/procedure/stap_020"
    Einde_beroepsprocedures = "/join/id/stop/procedure/stap_021"


# https://gitlab.com/koop/lvbb/bronhouderkoppelvlak/-/blob/1.2.0/waardelijsten/procedurestap_ontwerp.xml?ref_type=tags
class ProcedureStappenOntwerp(Enum):
    Vaststelling = "/join/id/stop/procedure/stap_002"
    Ondertekening = "/join/id/stop/procedure/stap_003"
    Publicatie = "/join/id/stop/procedure/stap_004"
    Einde_inzagetermijn = "/join/id/stop/procedure/stap_005"
    Begin_inzagetermijn = "/join/id/stop/procedure/stap_014"


# https://gitlab.com/koop/lvbb/bronhouderkoppelvlak/-/blob/1.2.0/waardelijsten/provincie.xml?ref_type=tags
class Provincie(Enum):
    Drenthe = "/tooi/id/provincie/pv22"
    Flevoland = "/tooi/id/provincie/pv24"
    Fryslân = "/tooi/id/provincie/pv21"
    Gelderland = "/tooi/id/provincie/pv25"
    Groningen = "/tooi/id/provincie/pv20"
    Limburg = "/tooi/id/provincie/pv31"
    Noord_Brabant = "/tooi/id/provincie/pv30"
    Noord_Holland = "/tooi/id/provincie/pv27"
    Overijssel = "/tooi/id/provincie/pv23"
    Utrecht = "/tooi/id/provincie/pv26"
    Zeeland = "/tooi/id/provincie/pv29"
    Zuid_Holland = "/tooi/id/provincie/pv28"


# https://gitlab.com/koop/lvbb/bronhouderkoppelvlak/-/raw/1.2.0/waardelijsten/soortregeling.xml?ref_type=tags
class RegelingType(Enum):
    AMvB = "/join/id/stop/regelingtype_001"
    Ministeriele_Regeling = "/join/id/stop/regelingtype_002"
    Omgevingsplan = "/join/id/stop/regelingtype_003"
    Omgevingsverordening = "/join/id/stop/regelingtype_004"
    Waterschapsverordening = "/join/id/stop/regelingtype_005"
    Omgevingsvisie = "/join/id/stop/regelingtype_006"
    Projectbesluit = "/join/id/stop/regelingtype_007"
    Instructie = "/join/id/stop/regelingtype_008"
    Voorbeschermingsregels = "/join/id/stop/regelingtype_009"
    Programma = "/join/id/stop/regelingtype_010"
    Reactieve_interventie = "/join/id/stop/regelingtype_011"
    Aanwijzingsbesluit_N2000 = "/join/id/stop/regelingtype_012"
    Toegangsbeperkingsbesluit = "/join/id/stop/regelingtype_013"
    Omgevingsplanregels_uit_projectbesluit = "/join/id/stop/regelingtype_014"
    Voorbeschermingsregels_Omgevingsplan = "/join/id/stop/regelingtype_015"
    Voorbeschermingsregels_Omgevingsverordening = "/join/id/stop/regelingtype_016"


# https://gitlab.com/koop/lvbb/bronhouderkoppelvlak/-/raw/1.2.0/waardelijsten/soortprocedure.xml?ref_type=tags
class ProcedureType(Enum):
    Ontwerpbesluit = "/join/id/stop/proceduretype_ontwerp"
    Definitief_besluit = "/join/id/stop/proceduretype_definitief"


# https://gitlab.com/koop/lvbb/bronhouderkoppelvlak/-/blob/1.2.0/waardelijsten/soortpublicatie.xml?ref_type=tags
class PublicatieType(Enum):
    Bekendmaking = "/join/id/stop/soortpublicatie_001"
    Kennisgeving = "/join/id/stop/soortpublicatie_002"
    Rectificatie = "/join/id/stop/soortpublicatie_003"


# https://gitlab.com/koop/lvbb/bronhouderkoppelvlak/-/raw/1.2.0/waardelijsten/soortwork.xml?ref_type=tags
class WorkType(Enum):
    Besluit = "/join/id/stop/work_003"
    Geconsolideerd_informatieobject = "/join/id/stop/work_005"
    Geconsolideerde_regeling = "/join/id/stop/work_006"
    Informatieobject = "/join/id/stop/work_010"
    Officiële_Publicatie = "/join/id/stop/work_015"
    Rectificatie = "/join/id/stop/work_018"
    Regeling = "/join/id/stop/work_019"
    Tijdelijk_regelingdeel = "/join/id/stop/work_021"
    Consolidatie_tijdelijk_regelingdeel = "/join/id/stop/work_022"
    Kennisgeving = "/join/id/stop/work_023"
    Versieinformatie = "/join/id/stop/work_024"
