from typing import List

from app.policy_objects import PolicyObject, PolicyObjects, html_to_xml_lichaam

#
# @note:
#   this is pretty much the template. but the name template is confusion because we use Jinja2 templates
#


def generate_regeling_vrijetekst_lichaam_visie(objects: PolicyObjects) -> str:
    ambities: List[PolicyObject] = objects.get_all("ambitie")

    html = f"""
        <div>
            {objects.get("visie_algemeen", 1).html({"heading_number": 1})}
        </div>
        <div>
            {objects.get("visie_algemeen", 2).html({"heading_number": 2})}
        </div>
        <div>
            {objects.get("visie_algemeen", 3).html({"heading_number": 3})}
        </div>
        <div>
            {objects.get("visie_algemeen", 4).html({"heading_number": 4})}

            {" ".join([f'<div data-hint-object-code="{ambitie.get("Code")}"' + 
                       (f' data-hint-location="{ambitie.get("Gebied_UUID")}"' if ambitie.get("Gebied_UUID") else '') + 
                       f'>{ambitie.html()}</div>' for ambitie in ambities])}

            <div>{objects.get("visie_algemeen", 5).html()}</div>
        </div>
        <div>
            {objects.get("visie_algemeen", 6).html({"heading_number": 5})}
        </div>
    """

    xml = html_to_xml_lichaam(html)
    return xml
