# ncat-python

Python wrapper for NGS Coordinate Conversion and Transformation Tool (NCAT) API.

## Installation

Install using pip:
```bash
pip install ncat
```

## Quickstart

```python
from ncat import ncat

response = ncat.llh(39.2240867222, -98.5421515000, 'nad83(1986)', 'nad83(2011)')

print('lat:', response['destLat'])
print('lon:', response['destLon'])
```

## Services

### [Latitude-Longitude-Height](https://geodesy.noaa.gov/web_services/ncat/lat-long-height-service.shtml)
```python
ncat.llh(lat, lon, in_datum, out_datum, eht=None, spc_zone=None, utm_zone=None, a=None, invf=None, in_vert_datum=None, out_vert_datum=None, ortho_ht=None)
```

### [State Plance Coordinates (SPC)](https://geodesy.noaa.gov/web_services/ncat/spc-service.shtml)
```python
ncat.spc(northing, easting, in_datum, out_datum, spc_zone, units=None, utm_zone=None, eht=None, in_vert_datum=None, out_vert_datum=None, ortho_ht=None)
```

### [Universal Transverse Mercator (UTM)](https://geodesy.noaa.gov/web_services/ncat/utm-service.shtml)
```python
ncat.utm(northing, easting, in_datum, out_datum, utm_zone, hemi=None, a=None, invf=None, spc_zone=None, eht=None, in_vert_datum=None, out_vert_datum=None, ortho_ht=None)
```

### [Cartesian Coordinates (XYZ)](https://geodesy.noaa.gov/web_services/ncat/xyz-service.shtml)
```python
ncat.xyz(x, y, z, in_datum, out_datum, spc_zone=None, utm_zone=None, a=None, invf=None)
```

### [U.S. National Grid (USNG)](https://geodesy.noaa.gov/web_services/ncat/usng-service.shtml)
```python
ncat.usng(usng, in_datum, out_datum, spc_zone=None, a=None, invf=None, eht=None, in_vert_datum=None, out_vert_datum=None, ortho_ht=None)
```

## Meta
```json
{
  "ID": "A timestamp associated with an API response",
  "deltaLat": "Estimated latitude transformation shift in meters",
  "deltaLon": "Estimated longitude transformation shift in meters",
  "destDatum": "Output reference frame, a reference frame to be transformed to",
  "destEht": "Output height, in meters, above the geometric reference frame ellipsoid;set to N/A, if not defined or transformed",
  "destLat": "Output latitude, in decimal degrees, positive north of the equator",
  "destLatDms": "Output latitude in Degrees-Minutes-Seconds with a 'N'orth or 'S'outh hemisphere prefix",
  "destLon": "Output longitude in decimal degrees; negative west of the prime meridian",
  "destLonDms": "Output longitude in Degrees-Minutes-Seconds with an 'E'ast or 'W'est hemisphere prefix",
  "destOrthoht": "Ouput orthometric height in Meters;set to N/A, if not defined or transformed",
  "destVertDatum": "output geopotential datum, a geopotential datum to be transformed to",
  "nadconVersion": "Version of Nadcon transformation",
  "sigEht": "Ellipsoid height transformation error estimate in meters;set to N/A, if not defined or transformed",
  "sigLat": "Latitude transformation error estimate in arcseconds",
  "sigLat_m": "Latitude transformation error estimate in meters",
  "sigLon": "Longitude transformation error estimate in arcseconds",
  "sigLon_m": "Longitude transformation error estimate in meters",
  "sigOrthoht": "Orthometric height transformation error in meters",
  "spcCombinedFactor": "A product of scale factor and elevation factor that varies by latitude and ellipsoid height",
  "spcConvergence": "Angular difference between grid north and geodetic north, in Degrees-Minutes-Seconds",
  "spcEasting_ift": "East coordinate of State Plane in IFT",
  "spcEasting_m": "East coordinate of State Plane in meters",
  "spcEasting_usft": "East coordinate of State Plane in USFT",
  "spcNorthing_ift": "North coordinate of State Plane in IFT",
  "spcNorthing_m": "North coordinate of State Plane in meters",
  "spcNorthing_usft": "North coordinate of State Plane in USFT",
  "spcScaleFactor": "The ratio of the length of a linear increment on the grid to the length of the corresponding increment on the ellipsoid at a given point",
  "spcZone": "Name of a State Plane Coordinate zone",
  "srcDatum": "Input reference frame, a reference frame to be transformed from",
  "srcEht": "Input height, in meters, above the geometric reference frame ellipsoid;set to N/A, if not defined",
  "srcLat": "Input latitude, in decimal degrees, positive north of the equator",
  "srcLatDms": "Input latitude in Degrees-Minutes-Seconds with a 'N'orth or 'S'outh hemisphere prefix",
  "srcLon": "Input longitude in decimal degrees; negative west of the prime meridian",
  "srcLonDms": "Input longitude in Degrees-Minutes-Seconds with an 'E'ast or 'W'est hemisphere prefix",
  "srcOrthoht": "Input orthometric height in Meters;set to N/A, if not defined",
  "srcVertDatum": "Input geopotential datum, a geopotential datum to be transformed from",
  "usng": "United States National Grid representation of an UTM coordinate",
  "utmCombinedFactor": "A product of UTM scale factor and elevation factor that varies by latitude and ellipsoid height",
  "utmConvergence": "Angular difference between grid north and geodetic north, in Degrees-Minutes-Seconds",
  "utmEasting": "East coordinate of UTM in meters",
  "utmNorthing": "North coordinate of UTM in meters",
  "utmScaleFactor": "The ratio of the length of a linear increment on the grid to the length of the corresponding increment on the ellipsoid at a given point",
  "utmZone": "Name of a Universal Transverse Mercator(UTM)zone",
  "vertconVersion": "Version of Vertcon transformation",
  "x": "Cartesian X-coordinate in meters",
  "y": "Cartesian Y-coordinate in meters",
  "z": "Cartesian Z-coordinate in meters"
}
```

## Resources
- NCAT: https://geodesy.noaa.gov/NCAT/
- NCAT Web Services Docs: https://geodesy.noaa.gov/web_services/ncat/index.shtml