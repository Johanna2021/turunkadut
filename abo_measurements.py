""" This includes functions to read open data 
from the city of Turku

"""

import pandas as pd

try:
    import geopandas as gpd
except ModuleNotFoundError:
    print('Tarvitset geopandas-kirjaston gml-datan lukemiseksi.')

def get_locations():

    """ Reads the measurement locations to a dataframe
    input: 

    output:
        locations: dataframe

    """

    dtype = {'id': str,\
            'lat': float,
            'lon': float,
            'address': str,
            }

    try:            
        locations = pd.read_csv('Data/kulkijat-mittauspisteet.csv', sep=',', dtype=dtype)
    except FileNotFoundError:
        print('\nMittauspisteet sisältävää tiedostoa kulkijat-mittauspisteet.csv ei löytynyt.\n')
        locations = pd.DataFrame()

    return locations

def get_measurements(serial):

    """ Reads all the measurements to a dataframe
    input:
        serial: str
        "serial number" of the measurement location
    output:
        measurements: dataframe
        measurements for selected location
    """
    try:            
        measurements = pd.read_csv('Data/kulkijat-15m.csv', sep=',')
    except FileNotFoundError:
        print('\nHaivantoja sisältävää tiedostoa kulkijat-15m.csv ei löytynyt.\n')
        measurements = pd.DataFrame()

    return measurements[['0', serial]]

def get_gml_data(file_path):

    """ gml data with bounding box 
    input:
    file_path: str 
        file location
    output: no idea...
        data
    """

    bbox = (2.34592e7,100+6.704e6,2.34603e7,700+6.704e6)
    return gpd.read_file(file_path, bbox=bbox)
