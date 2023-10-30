import os
import json
from jinja2 import Environment, FileSystemLoader
from lxml import etree

env = Environment(loader=FileSystemLoader("."))


def load_template(template_name, pretty_print=False, **context):
    template = env.get_template(template_name)
    output = template.render(**context)

    if pretty_print:
        # Convert the string to bytes if it has an XML declaration
        if output.startswith("<?xml"):
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.fromstring(output.encode('utf-8'), parser=parser)
        else:
            tree = etree.fromstring(output)

        # Convert back to string, retaining the XML declaration and with pretty-printing
        output = etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding="utf-8").decode("utf-8")

    return output


def load_template_and_write_file(template_name, output_file, pretty_print=False, **context):
    output = load_template(template_name, pretty_print=pretty_print, **context)
    with open(output_file, "w") as f:
        f.write(output)


def get_file_entries(folder_path, content_type_map):
    file_entries = []
    for filename in os.listdir(folder_path):
        extension = filename.split(".")[-1]
        content_type = content_type_map.get(extension)
        file_entries.append({"filename": filename, "contentType": content_type})
    return file_entries


def load_json_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)
