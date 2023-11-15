from hashlib import sha512
from typing import List
from uuid import UUID

from shapely import wkt

from app.gio.models import Werkingsgebied
from app.helpers import compute_sha512
from app.models import Bestand, ContentType, FRBR, Regeling, PublicationSettings, DocumentType, AKN
from utils.helpers import load_template, load_template_and_write_file


class GMLGeometryGenerator:
    def __init__(self, gml_id: str, geometry: str):
        self._gml_id: str = gml_id
        self._geom = wkt.loads(geometry)

    def generate_xml(self):
        if self._geom.geom_type == "Polygon":
            return self._polygon_to_xml()
        elif self._geom.geom_type == "MultiPolygon":
            return self._multipolygon_to_xml()

    def _polygon_to_xml(self):
        xml_string = f'<gml:Polygon srsName="urn:ogc:def:crs:EPSG::28992">'
        xml_string += self._ring_gml(self._geom.exterior, "exterior")
        for interior in self._geom.interiors:
            xml_string += self._ring_gml(interior, "interior")
        xml_string += "</gml:Polygon>"
        return xml_string

    def _multipolygon_to_xml(self):
        xml_string = (
            f'<gml:MultiSurface srsName="urn:ogc:def:crs:EPSG::28992" gml:id="{self._gml_id}-0">'
        )
        for idx, polygon in enumerate(self._geom.geoms):
            xml_string += "<gml:surfaceMember>"
            xml_string += self._polygon_gml(polygon, f"{self._gml_id}-{idx}")
            xml_string += "</gml:surfaceMember>"
        xml_string += "</gml:MultiSurface>"
        return xml_string

    def _polygon_gml(self, polygon, gml_id):
        xml_string = f"<gml:Polygon>"
        xml_string += self._ring_gml(polygon.exterior, "exterior")
        for interior in polygon.interiors:
            xml_string += self._ring_gml(interior, "interior")
        xml_string += "</gml:Polygon>"
        return xml_string

    def _ring_gml(self, ring, type):
        coords = " ".join([f"{coord[0]} {coord[1]}" for coord in ring.coords])
        xml_string = f"<gml:{type}><gml:LinearRing><gml:posList>{coords}</gml:posList></gml:LinearRing></gml:{type}>"
        return xml_string


class GioService:
    def __init__(self, act_akn, publication_settings, pretty_print: bool = True):
        self._act_akn: FRBR = act_akn
        self._publication_settings: PublicationSettings = publication_settings
        self._pretty_print: bool = pretty_print
        self._werkingsgebieden: List[Werkingsgebied] = []

    def add_werkingsgebied(self, werkingsgebied: Werkingsgebied):
        self._werkingsgebieden.append(werkingsgebied)

    def get_refs(self) -> List[str]:
        refs: List[str] = [w.get_FRBR().expression for w in self._werkingsgebieden]
        return refs

    def generate_files(self) -> List[Bestand]:
        files: List[Bestand] = []
        for werkingsgebied in self._werkingsgebieden:
            files.append(self._generate_glm_for(werkingsgebied))
            files.append(self._generate_gio_for(werkingsgebied))

        return files

    def _generate_glm_for(self, werkingsgebied: Werkingsgebied) -> Bestand:
        locaties: List[dict] = []
        for location in werkingsgebied.Locaties:
            gml_id: str = f"gml-{location.UUID}"
            generator = GMLGeometryGenerator(
                gml_id,
                location.Geometry,
            )
            geometry_xml = generator.generate_xml()
            locaties.append(
                {
                    "gml_id": gml_id,
                    "groep_id": f"groep-{str(location.UUID)}",
                    "basis_id": f"basis-{str(location.UUID)}",
                    "naam": location.Title,
                    "geometry_xml": geometry_xml,
                }
            )

        output_file: str = werkingsgebied.get_gml_filepath()
        load_template_and_write_file(
            "templates/geo/GeoInformatieObjectVaststelling.xml",
            output_file,
            pretty_print=True,
            achtergrondVerwijzing=werkingsgebied.Achtergrond_Verwijzing,
            achtergrondActualiteit=werkingsgebied.Achtergrond_Actualiteit,
            frbr=werkingsgebied.get_FRBR(),
            locaties=locaties,
        )

        return Bestand(
            bestandsnaam=werkingsgebied.get_gml_filename(),
            content_type=ContentType.GML,
        )

    def _generate_gio_for(self, werkingsgebied: Werkingsgebied) -> Bestand:
        gml_file: str = werkingsgebied.get_gml_filepath()
        gio_file: str = werkingsgebied.get_gio_filepath()

        gml_hash: str = compute_sha512(gml_file)

        load_template_and_write_file(
            "templates/geo/AanleveringInformatieObject.xml",
            gio_file,
            pretty_print=True,
            werkingsgebied_frbr=werkingsgebied.get_FRBR(),
            bestandsnaam=werkingsgebied.get_gml_filename(),
            gml_hash=gml_hash,
            regeling_akn=self._act_akn,
            eindverantwoordelijke=self._publication_settings.provincie_id,
            maker=self._publication_settings.provincie_ref,
            naamInformatie_object=werkingsgebied.Title,
        )

        return Bestand(
            bestandsnaam=werkingsgebied.get_gio_filename(),
            content_type=ContentType.XML,
        )
