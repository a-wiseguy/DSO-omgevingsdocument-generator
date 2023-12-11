import hashlib


def compute_sha512(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        return hashlib.sha512(data).hexdigest()
