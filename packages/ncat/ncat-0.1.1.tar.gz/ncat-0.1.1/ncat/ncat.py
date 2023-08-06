import urllib.request
import json

def get_json(url):
    with urllib.request.urlopen(url) as json_url:
        return json.loads(json_url.read().decode())

def add_optional_parameters(url, optional_parameters):
    for parameter in optional_parameters:
        if parameter[1]==None: continue
        url += "&{}={}".format(parameter[0],parameter[1])
    return url

def llh(lat, lon, in_datum, out_datum, eht=None, spc_zone=None, utm_zone=None, a=None, invf=None, in_vert_datum=None, out_vert_datum=None, ortho_ht=None):
    # Base url with required parameters
    url = "https://geodesy.noaa.gov/api/ncat/llh?lat={}&lon={}&inDatum={}&outDatum={}".format(lat, lon, in_datum, out_datum)

    # Add optional parameters
    url = add_optional_parameters(url, [['eht', eht], ['spc_zone', spc_zone], ['utm_zone', utm_zone], ['a', a], ['invf', invf], ['in_vert_datum', in_vert_datum], ['out_vert_datum', out_vert_datum], ['ortho_ht', ortho_ht]])
    
    return get_json(url)

def spc(northing, easting, in_datum, out_datum, spc_zone, units=None, utm_zone=None, eht=None, in_vert_datum=None, out_vert_datum=None, ortho_ht=None):
    # Base url with required parameters
    url = "https://geodesy.noaa.gov/api/ncat/spc?northing={}&easting={}&inDatum={}&outDatum={}&spcZone={}".format(northing, easting, in_datum, out_datum, spc_zone)

    # Add optional parameters
    url = add_optional_parameters(url, [['units', units], ['utm_zone', utm_zone], ['eht', eht], ['in_vert_datum', in_vert_datum], ['out_vert_datum', out_vert_datum], ['ortho_ht', ortho_ht]])
    
    return get_json(url)

def utm(northing, easting, in_datum, out_datum, utm_zone, hemi=None, a=None, invf=None, spc_zone=None, eht=None, in_vert_datum=None, out_vert_datum=None, ortho_ht=None):
    # Base url with required parameters
    url = "https://geodesy.noaa.gov/api/ncat/utm?northing={}&easting={}&inDatum={}&outDatum={}&utmZone={}".format(northing, easting, in_datum, out_datum, utm_zone)

    # Add optional parameters
    url = add_optional_parameters(url, [['hemi', hemi], ['a', a], ['invf', invf], ['spc_zone', spc_zone], ['eht', eht], ['in_vert_datum', in_vert_datum], ['out_vert_datum', out_vert_datum], ['ortho_ht', ortho_ht]])
    
    return get_json(url)

def xyz(x, y, z, in_datum, out_datum, spc_zone=None, utm_zone=None, a=None, invf=None):
    # Base url with required parameters
    url = "https://geodesy.noaa.gov/api/ncat/xyz?x={}&y={}&z={}&inDatum={}&outDatum={}".format(x, y, z, in_datum, out_datum)

    # Add optional parameters
    url = add_optional_parameters(url, [['spc_zone', spc_zone], ['utm_zone', utm_zone], ['a', a], ['invf', invf]])
    
    return get_json(url)

def usng(usng, in_datum, out_datum, spc_zone=None, a=None, invf=None, eht=None, in_vert_datum=None, out_vert_datum=None, ortho_ht=None):
    # Base url with required parameters
    url = "https://geodesy.noaa.gov/api/ncat/usng?usng={}&inDatum={}&outDatum={}".format(usng, in_datum, out_datum)

    # Add optional parameters
    url = add_optional_parameters(url, [['spc_zone', spc_zone], ['a', a], ['invf', invf], ['eht', eht], ['in_vert_datum', in_vert_datum], ['out_vert_datum', out_vert_datum], ['ortho_ht', ortho_ht]])
    
    return get_json(url)