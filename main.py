from dataclasses import dataclass
from pathlib import Path

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

    def _surface_polygons(self, surface_xpath, ns):
        """Return one list of 3D polygons for each matching surface element."""

        surfaces = self.element.findall(surface_xpath, namespaces=ns)
        polygons = []

        for surface in surfaces:
            for pos_list in surface.findall(".//gml:posList", namespaces=ns):
                coords = list(map(float, pos_list.text.split()))
                points_3d = [tuple(coords[i:i + 3]) for i in range(0, len(coords), 3)]
                polygons.append(points_3d)

        return polygons

    def roof_geometries(self, ns):
        return self._surface_polygons(".//bldg:RoofSurface", ns)

    def wall_geometries(self, ns):
        return self._surface_polygons(".//bldg:WallSurface", ns)

    def ground_geometries(self, ns):
        return self._surface_polygons(".//bldg:GroundSurface", ns)

    def all_surface_geometries(self, ns):
        return {
            "ground": self.ground_geometries(ns),
            "wall": self.wall_geometries(ns),
            "roof": self.roof_geometries(ns),
        }


def plot_building_surfaces_3d(building, ns):
    """Plot roof, wall, and ground polygons of one building in 3D."""

    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    surface_colors = {
        "ground": "#c49a6c",
        "wall": "#7aa6c2",
        "roof": "#c85c5c",
    }

    surfaces = building.all_surface_geometries(ns)
    figure = plt.figure(figsize=(10, 8))
    axis = figure.add_subplot(111, projection="3d")

    all_points = []

    for surface_type, polygons in surfaces.items():
        for polygon in polygons:
            if len(polygon) < 3:
                continue

            patch = Poly3DCollection(
                [polygon],
                facecolors=surface_colors[surface_type],
                edgecolors="black",
                linewidths=0.7,
                alpha=0.6,
            )
            axis.add_collection3d(patch)
            all_points.extend(polygon)

    if not all_points:
        raise ValueError(f"Building {building.id} does not contain plottable surface geometry.")

    xs = [point[0] for point in all_points]
    ys = [point[1] for point in all_points]
    zs = [point[2] for point in all_points]

    axis.set_xlim(min(xs), max(xs))
    axis.set_ylim(min(ys), max(ys))
    axis.set_zlim(min(zs), max(zs))
    axis.set_box_aspect((
        max(xs) - min(xs),
        max(ys) - min(ys),
        max(zs) - min(zs) or 1.0,
    ))

    axis.set_title(f"LoD2 building surfaces: {building.id}")
    axis.set_xlabel("X")
    axis.set_ylabel("Y")
    axis.set_zlabel("Z")
    axis.legend(
        handles=[
            Patch(facecolor=surface_colors["roof"], edgecolor="black", label="Roof"),
            Patch(facecolor=surface_colors["wall"], edgecolor="black", label="Wall"),
            Patch(facecolor=surface_colors["ground"], edgecolor="black", label="Grundriss"),
        ]
    )
    plt.tight_layout()
    return figure, axis


LOD2_FILE = Path("data/ATOM_CityGLM/raw/LoD2_33_394_5820_1_BE.xml")

NS = {
    "core": "http://www.opengis.net/citygml/1.0",
    "bldg": "http://www.opengis.net/citygml/building/1.0",
    "gml": "http://www.opengis.net/gml",
    "gen": "http://www.opengis.net/citygml/generics/1.0",
}

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    building_elements = load_buildings_from_file(LOD2_FILE, NS)
    buildings = [LoD2Building(element) for element in building_elements]

    print(f"Found {len(buildings)} buildings in the CityGML file.")

    first_building = buildings[281]
    print(first_building.id)
    print(first_building.roof_type(NS))
    print(first_building.grundrissaktualitaet(NS))
    print(first_building.data["tag"])
    print(first_building.data["attributes"])
    print(f"Direct child count: {len(first_building.data['children'])}")
    print(f"Ground polygons: {len(first_building.ground_geometries(NS))}")
    print(f"Wall polygons: {len(first_building.wall_geometries(NS))}")
    print(f"Roof polygons: {len(first_building.roof_geometries(NS))}")

    plot_building_surfaces_3d(first_building, NS)
    plt.show()
