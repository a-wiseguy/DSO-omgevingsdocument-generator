from typing import Any


class PolicyObject:
    def __init__(self, data: dict):
        self.data: dict = data

    # @todo: maybe we should just give the html as a property to this api
    # instead of the Description, Explanation fields etc etc
    def html(self, context: dict = {}) -> str:
        match self.data["Object_Type"]:
            case "visie_algemeen":
                return f"""
                    {self._html_title(context)}
                    {self.data['Description']}
                    """
            case "ambitie":
                return f"""
                    {self._html_title(context)}
                    {self.data['Description']}
                    """
            case "beleidskeuze":
                return f"""
                    {self._html_title(context)}
                    <h2>Omschrijving</h2>
                    {self.data['Description']}
                    <h2>Redenering</h2>
                    {self.data['Cause']}
                    """
        raise NotImplementedError()

    def _html_title(self, context: dict = {}) -> str:
        heading_number = context.get("heading_number")
        heading_number_attr = f' data-nummer="{heading_number}"' if heading_number is not None else ""
        return f"<h1{heading_number_attr}>{self.data['Title']}</h1>"

    def get(self, key: str, default: Any = None):
        return self.data.get(key, default)
