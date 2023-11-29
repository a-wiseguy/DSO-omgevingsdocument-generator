import fnmatch
import os

from bs4 import BeautifulSoup


def generate_files(prefix: str):
    module_json_data = {}
    catalog_data = {}

    schema_dir = "data/schema/geostandaarden/"
    for root_dir, dirs, files in os.walk(schema_dir):
        for file in files:
            if fnmatch.fnmatch(file, '*.xsd'):
                xsd_file_path = os.path.join(root_dir, file)
                with open(xsd_file_path, 'r') as content:
                    soup = BeautifulSoup(content, 'xml')
                    root_element = soup.find()
                    target_namespace = root_element.get('targetNamespace')

                    local_path: str = xsd_file_path[len(schema_dir):]
                    official_url = f"{prefix}/{local_path}"

                    if target_namespace not in module_json_data:
                        module_json_data[target_namespace] = set()
                    module_json_data[target_namespace].add(official_url)
                    catalog_data[official_url] = local_path

    # Generate the module
    module_xmls = []
    for namespace, schemas in module_json_data.items():
        for schema in list(schemas):
            module_xmls.append(f"""
                <Module>
                    <namespace>{namespace}</namespace>
                    <schema>{schema}</schema>
                </Module>
            """)
    module_final_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Versieoverzicht xmlns="https://standaarden.overheid.nl/stop/imop/schemata/"
                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                 schemaversie="1.2.0"
                 xsi:schemaLocation="https://standaarden.overheid.nl/stop/imop/schemata/   https://standaarden.overheid.nl/stop/1.3.0/imop-schemata.xsd">
  <versie>1.2.0</versie>
    {" ".join(module_xmls)}
</Versieoverzicht>"""

    with open(f"{schema_dir}versie.xml", "w") as file:
        file.write(module_final_xml)
    
    # Generate catalog
    catalog_xmls = []
    for name, uri in catalog_data.items():
        catalog_xmls.append(f"""
            <uri name="{name}" uri="{uri}" />
        """)
    catalog_final_xml = f"""<?xml version='1.0' encoding='UTF-8'?>
<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">
    {" ".join(catalog_xmls)}
</catalog>"""

    with open(f"{schema_dir}catalog.xml", "w") as file:
        file.write(catalog_final_xml)
