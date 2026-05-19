from pyproj import Transformer
from geopy.geocoders import Nominatim

def coordinate_to_address(x, y, source_crs="EPSG:25833"):
    '''Convert coordinates from a given CRS to latitude and longitude, then reverse geocode to get the address.'''
    transformer = Transformer.from_crs(source_crs, "EPSG:4326", always_xy=True)
    lon, lat = transformer.transform(x, y)

    geolocator = Nominatim(user_agent="attic-conversion-project")
    location = geolocator.reverse((lat, lon), exactly_one=True)

    return location.address if location else None

address = coordinate_to_address(392000, 5820000)
print(address)