import os


def create_normalized_path(base_dir, resource_file):
    normalized_base_dir = os.path.normpath(base_dir)
    normalized_resource_file = os.path.normpath(resource_file)

    path = os.path.join(normalized_base_dir, normalized_resource_file)
    return path
