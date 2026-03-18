# Roof Conversion Project

## 1. Overview
The DachAusbau project focuses on identifying buildings with potential for rooftop (attic) conversion using data-driven methods. By leveraging geospatial data, 3D building models, and algorithmic analysis, the project aims to streamline the detection of underutilized roof spaces in urban environments.

### Objectives
- Automatically identify buildings suitable for attic conversion
- Analyze physical building characteristics (e.g., roof shape, height, volume)
- Support urban development and housing expansion strategies
- Reduce manual effort compared to traditional property assessment

### Methodology
The project integrates:
- 3D building data (e.g., LoD2 models)
- Geographic Information Systems (GIS)
- Algorithmic filtering based on predefined criteria (roof geometry, zoning, etc.)

### Benefits
- **Efficiency**: Faster identification of viable buildings compared to manual search
- **Scalability**: Ability to analyze entire cities like Berlin
- **Decision Support**: Useful for urban planners, investors, and architects
- **Housing Impact**: Helps unlock additional living space in dense urban areas

### Use Case
In cities like Berlin, where housing demand is high, the project enables stakeholders to quickly pinpoint buildings with rooftop conversion potential, accelerating development processes.

### Technologies
- GIS platforms (e.g., Geoportal Berlin)
- 3D building datasets (LoD2)
- Data processing and analysis algorithms

### Future Work
- Integration of legal and zoning constraints
- Automation of feasibility scoring
- Visualization tools for identified buildings


## Data souces

- **3D Building data (LoD2)**: this data is provided by the *Senatsverwaltung für Stadtentwicklung, Bauen und Wohnen Berlin* (https://daten.berlin.de/datensaetze/3d-gebaudemodelle-im-level-of-detail-2-lod-2-3c7c49af). Clicking on the "Resource link leads to the download of the r9Ul3STr, an ATOM feed. Inside this file there is the link http://inspire.ec.europa.eu/schemas/inspire_dls/1.0, which leads to another file download (0.atom) which also contains a list of further links: one link containing the tiling of the state of Berlin and one link for each of the tiles.**License**: Für die Nutzung der Daten ist die Datenlizenz Deutschland - Zero - Version 2.0 anzuwenden. Die Lizenz ist über https://www.govdata.de/dl-de/zero-2-0 abrufbar.
