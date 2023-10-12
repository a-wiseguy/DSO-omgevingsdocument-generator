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

class InformatieObjectType(Enum):
    Geoinformatieobject = "/join/id/stop/informatieobject/gio_002"
    PDF_document = "/join/id/stop/informatieobject/doc_001"


# https://gitlab.com/koop/STOP/standaard/-/blob/1.3.0/waardelijsten/rechtsgebied.xml
class RechtsgebiedType(Enum):
    omgevingsrecht = "/tooi/def/concept/c_638d8062"


# https://gitlab.com/koop/STOP/standaard/-/blob/1.3.0/waardelijsten/onderwerp.xml
class OnderwerpType(Enum):
    zorg_en_gezondheid = "/tooi/def/concept/c_d0463fb7"
    wonen = "/tooi/def/concept/c_124eaf3a"
    werk = "/tooi/def/concept/c_9d1917e9"
    verkeer = "/tooi/def/concept/c_849842ac"
    sociale_zekerheid = "/tooi/def/concept/c_d4890526"
    ruimte_en_infrastructuur = "/tooi/def/concept/c_cfc7d5ab"
    recht = "/tooi/def/concept/c_f4679acc"
    overheidsfinanciën = "/tooi/def/concept/c_391585db"
    organisatie_en_bedrijfsvoering = "/tooi/def/concept/c_3eb6243b"
    openbare_orde_en_veiligheid = "/tooi/def/concept/c_d58b78ca"
    onderwijs_en_wetenschap = "/tooi/def/concept/c_c232ae4a"
    natuur_en_milieu = "/tooi/def/concept/c_afa30a11"
    migratie_en_integratie = "/tooi/def/concept/c_399f194b"
    internationaal = "/tooi/def/concept/c_f47ad6ca"
    economie = "/tooi/def/concept/c_d363776f"
    cultuur_en_recreatie = "/tooi/def/concept/c_0361ffb3"
    zorgverzekeringen = "/tooi/def/concept/c_341c5bef"
    ziekten_en_behandelingen = "/tooi/def/concept/c_9a574af9"
    ouderenzorg = "/tooi/def/concept/c_f02ce1b3"
    jeugdzorg = "/tooi/def/concept/c_0fe7c5e7"
    gezondheidsrisicos = "/tooi/def/concept/c_8b081a63"
    geneesmiddelen_en_medische_hulpmiddelen = "/tooi/def/concept/c_6b9627b5"
    ethiek = "/tooi/def/concept/c_218c52ee"
    woningmarkt = "/tooi/def/concept/c_17a86a17"
    bouwen_en_verbouwen = "/tooi/def/concept/c_a6a9eddd"
    werkgelegenheid = "/tooi/def/concept/c_7fe16af8"
    arbeidsverhoudingen = "/tooi/def/concept/c_1f37c612"
    arbeidsomstandigheden = "/tooi/def/concept/c_4e83eca7"
    scheepvaart = "/tooi/def/concept/c_d3b599f8"
    rail_en_wegverkeer = "/tooi/def/concept/c_f411e390"
    openbaar_vervoer = "/tooi/def/concept/c_319461d7"
    luchtvaart = "/tooi/def/concept/c_2835e395"
    ziekte_en_arbeidsongeschiktheid = "/tooi/def/concept/c_2ee165c4"
    arbeidsongeschiktheid_en_werkloosheid = "/tooi/def/concept/c_2ee165c4"
    ouderen = "/tooi/def/concept/c_1781ce20"
    gezin_en_kinderen = "/tooi/def/concept/c_76136c82"
    waterbeheer = "/tooi/def/concept/c_a71dc533"
    ruimtelijke_ordening = "/tooi/def/concept/c_9af4b880"
    netwerken = "/tooi/def/concept/c_85a72eb3"
    strafrecht = "/tooi/def/concept/c_98e03e32"
    staatsrecht = "/tooi/def/concept/c_1fe409d0"
    rechtspraak = "/tooi/def/concept/c_72138db9"
    rechten_en_vrijheden = "/tooi/def/concept/c_d2b1338a"
    privaatrecht = "/tooi/def/concept/c_824ce7ff"
    bezwaar_en_klachten = "/tooi/def/concept/c_e3d35361"
    bestuursrecht = "/tooi/def/concept/c_beb01b1c"
    subsidie = "/tooi/def/concept/c_01a4140b"
    inkomensbeleid = "/tooi/def/concept/c_68e408ff"
    financieel_toezicht = "/tooi/def/concept/c_1dd2bcc9"
    belasting = "/tooi/def/concept/c_25e30d03"
    begroting = "/tooi/def/concept/c_4348dad1"
    overheidspersoneel = "/tooi/def/concept/c_f2c9a613"
    koninkrijksrelaties = "/tooi/def/concept/c_f28344a5"
    interne_organisatie = "/tooi/def/concept/c_f6d7f591"
    inrichting_van_de_overheid = "/tooi/def/concept/c_f37fd49d"
    inkoop_en_beheer = "/tooi/def/concept/c_068da9fb"
    informatievoorziening_en_ICT = "/tooi/def/concept/c_ee06665e"
    dienstverlening = "/tooi/def/concept/c_cf421a08"
    veiligheid = "/tooi/def/concept/c_d772bf06"
    terrorisme = "/tooi/def/concept/c_4872b086"
    criminaliteit = "/tooi/def/concept/c_fcac43e4"
    voortgezet_onderwijs = "/tooi/def/concept/c_980b8db2"
    onderzoek_en_wetenschap = "/tooi/def/concept/c_08d12aef"
    onderwijsvoorzieningen = "/tooi/def/concept/c_4eb912c1"
    hoger_onderwijs = "/tooi/def/concept/c_516ec027"
    beroepsonderwijs = "/tooi/def/concept/c_b46b92e7"
    basisonderwijs = "/tooi/def/concept/c_7b01f260"
    water = "/tooi/def/concept/c_389a72e6"
    stoffen = "/tooi/def/concept/c_61d3e636"
    natuur_en_landschapsbeheer = "/tooi/def/concept/c_db2fbedb"
    lucht = "/tooi/def/concept/c_28ddcea5"
    geluid = "/tooi/def/concept/c_9f410ab6"
    flora_en_fauna = "/tooi/def/concept/c_a81687f1"
    energie = "/tooi/def/concept/c_f4f1867a"
    bodem = "/tooi/def/concept/c_7ce8a10c"
    afval = "/tooi/def/concept/c_d96f9cd3"
    migratie = "/tooi/def/concept/c_2e9944e7"
    integratie = "/tooi/def/concept/c_a94e1fa4"
    ontwikkelingssamenwerking = "/tooi/def/concept/c_8940ed07"
    internationale_betrekkingen = "/tooi/def/concept/c_576c2bd7"
    Europese_zaken = "/tooi/def/concept/c_68609e19"
    defensie = "/tooi/def/concept/c_daaa67b3"
    transport = "/tooi/def/concept/c_195b5b5e"
    ondernemen = "/tooi/def/concept/c_3afc269f"
    markttoezicht = "/tooi/def/concept/c_dc437d00"
    landbouw_visserij_voedselkwaliteit = "/tooi/def/concept/c_989e37d9"
    kenniseconomie = "/tooi/def/concept/c_87d3d66c"
    handel = "/tooi/def/concept/c_83db27fc"
    dienstensector = "/tooi/def/concept/c_4d1c84a7"
    religie = "/tooi/def/concept/c_e277e756"
    recreatie = "/tooi/def/concept/c_a6c5e5b8"
    media = "/tooi/def/concept/c_6b728132"
    horeca = "/tooi/def/concept/c_75809540"
    evenementen = "/tooi/def/concept/c_70e03904"
    cultuur = "/tooi/def/concept/c_f72b706a"
    cultureel_erfgoed = "/tooi/def/concept/c_2408fb5a"
    speciaal_onderwijs = "/tooi/def/concept/c_1f781691"
    zorginstellingen = "/tooi/def/concept/c_7a0f87d5"
    klimaatverandering = "/tooi/def/concept/c_79010191"