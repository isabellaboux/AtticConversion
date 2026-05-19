import csv
from dataclasses import dataclass
from pathlib import Path

from lxml import etree
from tqdm import tqdm


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
class AlkisBuilding:
    """Lossless Python representation of one ALKIS building element."""

    element: etree._Element

    def __post_init__(self):
        self.id = self.element.get("{http://www.opengis.net/gml/3.2}id")
        self.data = xml_element_to_dict(self.element)


@dataclass
class AlkisAddressRecord:
    """Minimal ALKIS export record for linking a building to its address."""

    building_id: str | None
    street_name: str | None
    street_number: str | None

    @property
    def street_address(self) -> str | None:
        if self.street_name and self.street_number:
            return f"{self.street_name} {self.street_number}"
        return self.street_name or self.street_number


def _clean_text(value: str | None) -> str | None:
    """Normalize XML text values and map empty strings to None."""

    if value is None:
        return None

    value = value.strip()
    return value or None


def load_building_elements_from_file(alkis_file, ns) -> list:
    """Parse the ALKIS XML file and return all building XML elements."""

    tree = etree.parse(str(alkis_file))
    root = tree.getroot()
    return root.findall(".//alkis_gebaeude:gebaeude", namespaces=ns)


def load_buildings_from_file(alkis_file, ns) -> list[AlkisBuilding]:
    """Parse the ALKIS XML file and return all AX_Gebaeude objects."""

    building_elements = load_building_elements_from_file(alkis_file, ns)
    buildings = []

    for element in building_elements:
        building_type = element.findtext("alkis_gebaeude:bezeich", namespaces=ns)
        if building_type == "AX_Gebaeude":
            buildings.append(AlkisBuilding(element))

    return buildings


def _find_text(element: etree._Element, field_name: str, ns: dict) -> str | None:
    """Return the stripped text content of an ALKIS field if present."""

    return _clean_text(element.findtext(f"alkis_gebaeude:{field_name}", namespaces=ns))


def _extract_building_id(element: etree._Element, ns: dict) -> str | None:
    """Return the most reliable building ID available for one ALKIS element."""

    return (
        _clean_text(element.get(f"{{{ns['gml']}}}id"))
        or _find_text(element, "uuid", ns)
        or _find_text(element, "gkn", ns)
    )


def _estimate_total_buildings(alkis_file: Path) -> int | None:
    """Read the WFS feature count from the XML header if available."""

    with alkis_file.open("rb") as xml_file:
        for _, element in etree.iterparse(xml_file, events=("start",), huge_tree=True):
            value = element.get("numberReturned")
            element.clear()

            if value and value.isdigit():
                return int(value)
            return None

    return None


def iter_building_address_records(alkis_file, ns, progress_bar: tqdm | None = None):
    """Yield ALKIS building IDs and address fields for AX_Gebaeude entries."""

    building_tag = f"{{{ns['alkis_gebaeude']}}}gebaeude"
    context = etree.iterparse(
        str(alkis_file),
        events=("end",),
        tag=building_tag,
        huge_tree=True,
        remove_comments=True,
    )

    for _, element in context:
        if progress_bar is not None:
            progress_bar.update()

        if _find_text(element, "bezeich", ns) == "AX_Gebaeude":
            street_address = _find_text(element, "namlag", ns)
            street_number = _find_text(element, "hnr", ns)

            yield AlkisAddressRecord(
                building_id=_extract_building_id(element, ns),
                street_name=street_address,
                street_number=street_number,
            )

        element.clear()
        while element.getprevious() is not None:
            del element.getparent()[0]


def extract_building_address_records(alkis_file, ns) -> list[AlkisAddressRecord]:
    """Extract ALKIS building IDs and address fields for AX_Gebaeude entries."""

    return list(iter_building_address_records(alkis_file, ns))


def save_building_address_csv(
    alkis_file=Path("data/raw/alkis/gebaeude.xml"),
    output_file=Path("data/intermediate/alkis_building_addresses.csv"),
    ns=None,
) -> Path:
    """Save a CSV with building ID, street fields, and combined street address."""

    namespaces = ns or NS
    total_buildings = _estimate_total_buildings(alkis_file)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["building_id", "street_name", "street_number", "street_address"],
        )
        writer.writeheader()

        with tqdm(
            total=total_buildings,
            desc="Processing ALKIS buildings",
            unit="building",
        ) as progress_bar:
            written_count = 0

            for record in iter_building_address_records(alkis_file, namespaces, progress_bar):
                writer.writerow(
                    {
                        "building_id": record.building_id,
                        "street_name": record.street_name,
                        "street_number": record.street_number,
                        "street_address": record.street_address,
                    }
                )
                written_count += 1
                progress_bar.set_postfix(written=written_count)

    return output_file


ALKIS_FILE = Path("data/raw/alkis/gebaeude.xml")
OUTPUT_CSV = Path("data/intermediate/alkis_building_addresses.csv")

NS = {
    "gml": "http://www.opengis.net/gml/3.2",
    "alkis_gebaeude": "alkis_gebaeude",
}


if __name__ == "__main__":
    output_file = save_building_address_csv(ALKIS_FILE, OUTPUT_CSV, NS)
    print(f"Saved ALKIS building addresses to {output_file}.")
