import base64
import re

from app.assets.assets_service import Asset


def create_image(asset: Asset, path: str):
    match = re.match(r"data:image/(.*?);base64,(.*)", asset.Content)
    if not match:
        raise RuntimeError("Invalid asset content")
    _, base64_data = match.groups()

    image_data = base64.b64decode(base64_data)
    with open(path, "wb") as file:
        file.write(image_data)
