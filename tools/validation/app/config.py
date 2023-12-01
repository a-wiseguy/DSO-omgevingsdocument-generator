from typing import Dict, List

from helpers.models import Module


MODULES: List[Module] = [
    Module(
        file="data/schema/lvbb/versie.xml",
        nsmap={"ns": "https://standaarden.overheid.nl/stop/imop/schemata/"},
    ),
    Module(
        file="data/schema/stop/1.3.0/versiescompleet.xml",
        nsmap={"ns": "https://standaarden.overheid.nl/stop/imop/schemata/"},
    ),
    Module(
        file="data/schema/geostandaarden/versie.xml",
        nsmap={"ns": "https://standaarden.overheid.nl/stop/imop/schemata/"},
    ),
]


SAXON_JAR: str = "./saxon/saxon-he-11.6.jar"


SGML_CATALOG_FILES = " ".join([
    "./data/schema/extern/extern-catalog.xml",
    "./data/schema/stop/1.3.0/stop-catalog.xml",
    "./data/schema/lvbb/lvbb-catalog.xml",
    "./data/schema/geostandaarden/catalog.xml",
])


# @todo: This could be resolved from the catalogs
SCHEMATRON_MAP: Dict[str, str] = {
    # lvbb
    "https://standaarden.overheid.nl/lvbb/1.2.0/lvbb-aanlevering-io.sch": "lvbb/lvbb-aanlevering-io.sch",
    "https://standaarden.overheid.nl/lvbb/1.2.0/lvbb-aanlevering.sch": "lvbb/lvbb-aanlevering.sch",

    # stop
    "https://standaarden.overheid.nl/stop/1.3.0/imop-aknjoin.sch": "stop/1.3.0/imop-aknjoin.sch",
    "https://standaarden.overheid.nl/stop/1.3.0/imop-consolidatie.sch": "stop/1.3.0/imop-consolidatie.sch",
    "https://standaarden.overheid.nl/stop/1.3.0/imop-geo.sch": "stop/1.3.0/imop-geo.sch",
    "https://standaarden.overheid.nl/stop/1.3.0/imop-metadata.sch": "stop/1.3.0/imop-metadata.sch",
    "https://standaarden.overheid.nl/stop/1.3.0/imop-pakbon.sch": "stop/1.3.0/imop-pakbon.sch",
    "https://standaarden.overheid.nl/stop/1.3.0/imop-procedure.sch": "stop/1.3.0/imop-procedure.sch",
    "https://standaarden.overheid.nl/stop/1.3.0/imop-se.sch": "stop/1.3.0/imop-se.sch",
    "https://standaarden.overheid.nl/stop/1.3.0/imop-tekst.sch": "stop/1.3.0/imop-tekst.sch",
    "https://standaarden.overheid.nl/stop/1.3.0/imop-tekstmutaties.sch": "stop/1.3.0/imop-tekstmutaties.sch",
}

