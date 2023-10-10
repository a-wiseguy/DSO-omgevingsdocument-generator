import os
import json
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader("."))


def load_template_and_write_file(template_name, output_file, **context):
    template = env.get_template(template_name)
    output = template.render(**context)
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
