"""
JOHANNA 2/2021
"""

import pandas as pd
import matplotlib.pyplot as plt

# own functions for reading open data from Turku
from abo_measurements import *

from street_info import *

def select_location(locations):

    """
    ask the user to select a location for the analysis

    input:
    locations: dataframe 
        list of locations (dataframe)

    output:
        int 
        row of the dataframe of selected location
    """

    # list locations with a number: 1. address1, 2. address2,...
    # and show those to the user
    loc_list = [str(num + 1) + ') ' + loc for num, loc in enumerate(locations['address'])]
    for loc in loc_list:
        print(loc)

    # select the location
    streets_numbers = [str(ii) for ii in range(1,27)]
    street = 'a'
    while street not in streets_numbers:
         street = input('Mitä katua haluat tarkastella? Anna numero 1 - 26. ')


    # return the selected street when index = selection - 1
    return int(street)-1
    
def make_geodf(df, lat_col_name='latitude', lon_col_name='longitude'):

    import geopandas as gpd

    """
    Take a dataframe with latitude and longitude columns, and turn
    it into a geopandas df. Needed to plot the map.
    
    The function is more or less copy-pasted from 
    https://www.martinalarcon.org/2018-12-31-d-geopandas/

    """
    try:
        df = df.copy()
        lat = df[lat_col_name]
        lon = df[lon_col_name]
        geodf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(lon, lat))
        geodf = geodf.set_crs("EPSG:4326")
        geodf = geodf.to_crs("EPSG:3877") 
    except:
        print('Jotain meni pieleen, kun data yritettiin muuntaa geodataframeen.')
        geodf = []

    return geodf

def plot_map(locations, sel_street):

    """ 
    plot map of Turku.
    The data is from https://api.turku.fi/wfs2gml/
    
    """

    kortteli = get_gml_data('Data/Paikkatieto/akaava-kortteli.gml')
    kiinteistot = get_gml_data('Data/Paikkatieto/kanta-kiinteisto.gml')

    base = kortteli.plot()
    kiinteistot.plot(ax=base, color='lightblue')
    locations.plot(ax=base, color='red', markersize=20)

    # selected location with a bigger and more red
    loc_df = pd.DataFrame()
    loc_df = loc_df.append(locations.iloc[int(sel_street)-1])
    loc_df = make_geodf(loc_df, lat_col_name='lat', lon_col_name='long')
    loc_df.plot(ax=base, color='darkred', markersize=100)

    plt.show()

def main():

    # check if geopandas library installed -> plotting a map is possible
    try:
        import geopandas as gpd
        map = True
    except ModuleNotFoundError:
        map = False

    # Read all the measurement locations
    location_df = get_locations()

    # Add geometry to dataframe if plotting a map is possible (geopandas)
    if map == True:
        location_df = make_geodf(location_df, 'lat', 'long')

    # ask the location which is the most interesting
    location_sel = select_location(location_df)

    # calculate statistics and show them
    street = STREET(location_df.iloc[location_sel])
    street.get_measurement_df()
    street.hourly_statistics()
    street.print_statistics()

    # check if we will plot a map for the locations
    if map == False:
        print('\nKarttakuvan piirtämiseksi tarvitset '\
            'geopandas-kirjaston.\n')
    else:
        while map not in ['k', 'e']:
            map = input('Haluatko nähdä karttakuvan? (k/e) ') 
            if map not in ['k', 'e']:
                print('Vastaa joko k(yllä) tai e(i).')

    # show a map if selected (k)
    if map == 'k':
        print('\nKuva avautuu hetken päästä. '\
            + 'Tarkastelemasi piste esitetään muita isompana merkkinä.\n')
        print('Voit lopettaa sulkemalla ikkunan.\n')
        plot_map(location_df, location_sel)
        print('\nEipä tässä muuta!\n')

if __name__ == '__main__':
    main()
