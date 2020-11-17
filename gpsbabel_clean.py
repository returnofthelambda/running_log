'''
Clean files from garmin forerunner 305 pulled by gpsbabel
1) connect forerunner and run:
    gpsbabel -t -r -w -i garmin -f usb: -o garmin301 file.csv
    This will produce a csv file that contains time, lat, long, alt and hr.
2)
use pd.to_datetime(df.Timestamp, units='s') to convert time
'''
import numpy as np
import pandas as pd


def haversine(row1, row2):
    '''Function below was modified from the stackoverflow answer found here:
            https://stackoverflow.com/a/56769419

    This uses the ‘haversine’ formula to calculate the great-circle distance
    between two points – that is, the shortest distance over the earth’s
    surface – giving an ‘as-the-crow-flies’ distance between the points
    (ignoring any hills they fly over, of course!).
    Haversine formula:
        a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
        c = 2 ⋅ atan2( √a, √(1−a) )
        d = R ⋅ c
        where   φ is latitude, λ is longitude,
        R is earth’s radius (mean radius = 6,371km);
        note that angles need to be in radians to pass to trig functions!
    '''
    lat1, lon1, lat2, lon2 = map(np.radians, [row1.Latitude, row1.Longitude,
                                              row2.Latitude, row2.Longitude])
    R = 6371.0088
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2) ** 2
    c = 2 * np.arctan2(a**0.5, (1-a)**0.5)
    d = R * c

    return round(d, 4)


def run_clean(csv_str):
    '''
    Take in a csv and read it into a dataframe. Convert time from seconds, add
    haversine calculation for distance, and calculate pace. Data goes from here
    to being plotted, or used for other functions.
    '''
    run_df = pd.read_csv(csv_str, skiprows=[0])
    run_df.columns = [_.strip() for _ in run_df.columns]
    run_df = run_df[run_df.Timestamp > 1]
    run_df['Time'] = pd.to_datetime(run_df.Timestamp, unit='s')

    # insert function to parse by date

    dist = [haversine(run_df.loc[_], run_df.loc[_ - 1])
            for _ in run_df.index[1:]]
    dist.insert(0, 0)
    run_df['Distance'] = dist

    return run_df
