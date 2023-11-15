import os
import json
from jinja2 import Environment, FileSystemLoader
from lxml import etree

from app.exceptions import TemplateError, FileWriteError

env = Environment(loader=FileSystemLoader("."))


def load_template(template_name: str, pretty_print: bool = False, **context) -> str:
    template = env.get_template(template_name)

    try:
        output = template.render(**context)
    except Exception as e:
        raise TemplateError(template_name, f"Error rendering template: {str(e)}")

    if pretty_print:
        try:
            if output.startswith("<?xml"):
                parser = etree.XMLParser(remove_blank_text=True)
                tree = etree.fromstring(output.encode("utf-8"), parser=parser)
            else:
                tree = etree.fromstring(output)
            output = etree.tostring(
                tree, pretty_print=True, xml_declaration=True, encoding="utf-8"
            ).decode("utf-8")
        except Exception as e:
            raise TemplateError(template_name, f"Error pretty printing: {str(e)}")

    return output


def load_template_and_write_file(template_name, output_file, pretty_print=False, **context):
    output = load_template(template_name, pretty_print=pretty_print, **context)
    try:
        with open(output_file, "w") as f:
            f.write(output)
    except Exception as e:
        raise FileWriteError(output_file, str(e))


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
