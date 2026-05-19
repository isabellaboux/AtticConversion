from dataclasses import dataclass

from lxml import etree


def load_buildings_from_file(lod2_file, ns) -> list:
    """Load building elements from a CityGML file."""

    tree = etree.parse(lod2_file)
    root = tree.getroot()
    return root.findall(".//bldg:Building", namespaces=ns)


def xml_element_to_dict(element) -> dict:
    """Convert an XML element into a recursive Python dict without dropping data."""

    return {
        "tag": element.tag,
        "attributes": dict(element.attrib),
        "text": element.text.strip() if element.text and element.text.strip() else None,
        "tail": element.tail.strip() if element.tail and element.tail.strip() else None,
        "children": [xml_element_to_dict(child) for child in element],
    }


@dataclass
class LoD2Building:
    """Lossless Python representation of a CityGML building."""

    element: etree._Element

    def __post_init__(self):
        self.id = self.element.get("{http://www.opengis.net/gml}id")
        self.data = xml_element_to_dict(self.element)

    def roof_type(self, ns):
        roof_type_elem = self.element.find("bldg:roofType", namespaces=ns)
        return roof_type_elem.text if roof_type_elem is not None else None

    def grundrissaktualitaet(self, ns):
        grundriss_elem = self.element.find(
            "gen:stringAttribute[@name='Grundrissaktualitaet']/gen:value",
            namespaces=ns,
        )
        return grundriss_elem.text if grundriss_elem is not None else None
    
    def roof_geometries(self, ns):
        roof_surfaces = self.element.findall(".//bldg:RoofSurface", namespaces=ns)
        geometries = []

        for roof in roof_surfaces:
            pos_lists = roof.findall(".//gml:posList", namespaces=ns)
            roof_polygons = []

            for pos_list in pos_lists:
                coords = list(map(float, pos_list.text.split()))
                points_3d = [coords[i:i+3] for i in range(0, len(coords), 3)]
                roof_polygons.append(points_3d)

            geometries.append(roof_polygons)

        return geometries


LOD2_FILE = "data/raw/LoD2/LoD2_33_394_5820_1_BE.xml"

NS = {
    "core": "http://www.opengis.net/citygml/1.0",
    "bldg": "http://www.opengis.net/citygml/building/1.0",
    "gml": "http://www.opengis.net/gml",
    "gen": "http://www.opengis.net/citygml/generics/1.0",
}

building_elements = load_buildings_from_file(LOD2_FILE, NS)
buildings = [LoD2Building(element) for element in building_elements]

print(f"Found {len(buildings)} buildings in the CityGML file.")

first_building = buildings[0]
print(first_building.id)
print(first_building.roof_type(NS))
print(first_building.grundrissaktualitaet(NS))
print(first_building.data["tag"])
print(first_building.data["attributes"])
print(f"Direct child count: {len(first_building.data['children'])}")


print(buildings[0].roof_geometries(NS))