
from datetime import datetime, timedelta
from abo_measurements import *


class STREET():

    """ 
        Street is a measurement location with more or less useful information.

        Street includes location (lat, lon, address), measurements and some calculated values (hourly_statistics).
    """

    def __init__(self,location_df):

        """
        input: 
            location_df is actually just a Series which includes information for the location.

        """

        self.lat = location_df['lat']
        self.lon = location_df['long']
        self.address = location_df['address']
        self.geometry = location_df['geometry']
        self.serial = location_df['serial']

    def get_measurement_df(self):

        self.measurements_df = get_measurements(self.serial)
        self.measurements_df.rename(columns={'0': 'time', self.serial: 'kulkijoita'}, inplace=True)

        # use the local time (+02:00) instead of UTC
        # correct the time -15 minutes
        time_format = '%Y-%m-%d %H:%M:%S+02:00'

        self.measurements_df['time'] = self.measurements_df['time'].apply(lambda x: datetime.strptime(x, time_format)\
            + timedelta(minutes=-15)) 
        self.measurements_df['hour'] = self.measurements_df['time'].apply(lambda x: x.hour)

    def hourly_statistics(self):

        """ 
        Calculate hourly statistics for the selected location. 
        > number of passengers
        > time for most and least people

        """

        # group by hour and calculate mean, max, min and sum for passengers for every hour
        hourly_statistics_df = self.measurements_df.groupby('hour').agg(\
            {'kulkijoita': ['mean', 'max', 'min', 'sum'],\
            'time': ['min', 'max']
            })

        # first and last masurements time
        self.meas_first = hourly_statistics_df['time']['min'].min()
        self.meas_last = hourly_statistics_df['time']['max'].max()

        # total number of people
        self.total_number = hourly_statistics_df['kulkijoita']['sum'].sum()

        # time for most people
        sel_time = hourly_statistics_df['kulkijoita']['mean'] == hourly_statistics_df['kulkijoita']['mean'].max() 
        self.meas_most_time_begin = hourly_statistics_df['time']['min'][sel_time].iloc[0]

        sel_time = hourly_statistics_df['kulkijoita']['mean'] == hourly_statistics_df['kulkijoita']['mean'].min() 
        self.meas_least_time_begin = hourly_statistics_df['time']['min'][sel_time].iloc[0]

    def print_statistics(self):

        """ 
        print the results.
        """

        ### print information and some calculated values
        print('\n\n\n')
        print('Valitsemasi osoite: ' + self.address)
        print('Sijainti: ' + '{:.2f}'.format(self.lat)\
            + '\xb0N ' + '{:.2f}'.format(self.lon) + '\xb0E\n')

        # when measured passangers
        time_format = '%d.%m.%Y klo %H.%M'
        time_begin = datetime.strftime(self.meas_first, time_format)
        time_end = datetime.strftime(self.meas_last, time_format)
        print('Ajanjaksona ' + time_begin + ' - ' + time_end)

        # how many in total 
        print('> Havaittiin '\
            + '{:.0f}'.format(self.total_number)\
            + ' ohikulkijaa, joilla bluetooth-laite oli päällä.')

        # when most flow
        time_format = '%H.%M'
        time_end = datetime.strftime(self.meas_most_time_begin + timedelta(hours=1), time_format)
        time_begin = datetime.strftime(self.meas_most_time_begin, time_format)
        print('> Eniten ihmisiä liikkui klo ' + time_begin + ' - ' + time_end)

        # when least flow
        time_end = datetime.strftime(self.meas_least_time_begin + timedelta(hours=1), time_format)
        time_begin = datetime.strftime(self.meas_least_time_begin, time_format)
        print('> Vähiten ihmisiä liikkui klo ' + time_begin + ' - ' + time_end + '\n')