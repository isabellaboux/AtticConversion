# Attic Conversion Project

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

### 3D Building data (LoD2)

- **Source**: provided by the *Senatsverwaltung für Stadtentwicklung, Bauen und Wohnen Berlin* (https://daten.berlin.de/datensaetze/3d-gebaudemodelle-im-level-of-detail-2-lod-2-3c7c49af).
- **How to access**: clicking on the "Resource link leads to the download of the r9Ul3STr, an ATOM feed. Inside this file there is the link http://inspire.ec.europa.eu/schemas/inspire_dls/1.0, which leads to another file download (0.atom) which also contains a list of further links: one link containing the tiling of the state of Berlin and one link for each of the tiles in a zip file. When a zip file is downloaded, it contains only one .xml file, which can be opened in the KITModelViewer software (https://www.iai.kit.edu/english/1302.php) via *File > Open... > Open GML file*. Onece a tile has been loaded, other ones can be merged into it (*File > Merge*) There, the whole tile becomes visible. Each building is divided in subparts (area, walls, roof) and these are also further difided in sub-elements (polygonds). Each building has a unique identifier: glm:id. Note that also subparts have a comparable identifier!
- **License**: Für die Nutzung der Daten ist die Datenlizenz Deutschland - Zero - Version 2.0 anzuwenden. Die Lizenz ist über https://www.govdata.de/dl-de/zero-2-0 abrufbar.
- **Use**: contains information about the geometry of a building including the roof. TThis is useful for 
    - determining feasability: how tall i sthe building, how big is the roof, which geometry the roof has?
    - determining potential attic surface

### Satellite data
- **Use**: Required for examining the roof to detrmine if the attic is already converted (e.g. has windows)

### GPS/street data
- **Use**: as nexus between different data sources and entry point for the user

### Cadastral information? - tbc
- **Use**: as nexus between different data sources and entry point for the user


## Miscellaneous

- **Dachausbau regulations for Berlin**: https://www.berlin.de/ba-friedrichshain-kreuzberg/politik-und-verwaltung/aemter/stadtentwicklungsamt/themen/bauberatungsservice/artikel.1497107.php
