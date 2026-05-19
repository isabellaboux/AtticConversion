from lxml import etree


def load_builgings_from_file(lod2_file, ns) -> list:
    '''Load building elements from a CityGML file and return them in the form of a list of building objects.'''

    # parse the CityGML file
    tree = etree.parse(lod2_file)
    # find the XML root
    root = tree.getroot()
    # extract building elements
    buildings = root.findall(".//bldg:Building", namespaces=ns)
    return buildings


LOD2_FILE = "data/raw/LoD2/LoD2_33_394_5819_1_BE.xml"

NS = {
    "core": "http://www.opengis.net/citygml/1.0",
    "bldg": "http://www.opengis.net/citygml/building/1.0",
    "gml": "http://www.opengis.net/gml",
    "gen": "http://www.opengis.net/citygml/generics/1.0",
}

buildings = load_builgings_from_file(LOD2_FILE, NS)


print(f"Found {len(buildings)} buildings in the CityGML file.")

building = buildings[1]

print(type(building))
print(building.tag)
print(building.attrib)


for building in buildings:
    building_id = building.get("{http://www.opengis.net/gml}id")
    roof_type_elem = building.find("bldg:roofType", namespaces=NS)
    roof_type_code = roof_type_elem.text if roof_type_elem is not None else None
    grundriss_elem = building.find("gen:stringAttribute[@name='Grundrissaktualitaet']/gen:value", namespaces=NS)

    grundriss_code = grundriss_elem.text if grundriss_elem is not None else None

    print(building_id, roof_type_code, grundriss_code)