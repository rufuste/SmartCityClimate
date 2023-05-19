import pandas as pd
import requests
import io
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class AggData:
    instances = []
    data_params={}
    df=pd.DataFrame()
    
    def __init__(self, variable):
        api_date_string_format = "%Y%m%d%H%M%S"

        current_time = datetime.now()

        start_time = current_time - timedelta(days=1)

        start_time = datetime(start_time.year, start_time.month, start_time.day, start_time.hour)
        end_time = datetime(current_time.year, current_time.month, current_time.day, current_time.hour)


        # Set up parameters
        self.data_params = dict(
            data_variable=variable,
            agg_method='median',
            agg_period='15mins',
            starttime=start_time.strftime(api_date_string_format),
            endtime=end_time.strftime(api_date_string_format),
            sensor_type=variable
        )
        
        # Call fetch data method
        self.df = AggData.FetchAggData(self.data_params)
        
        # Append to instances of this class
        AggData.instances.append(self)
        
    @classmethod
    def FetchAggData(cls, data_params):
        r = requests.get('http://uoweb3.ncl.ac.uk/api/v1.1/sensors/data/agg/csv/', data_params)
        df = pd.read_csv(io.StringIO(r.text))
        return df
        
    def __str__(self):
        return f"{self.data_params['data_variable']}"

def Remove_Suspect(df):
    
#     print (df.shape)
    df = df[df['Value']>0]
#     print("Remove flagged as suspect readings")
    df = df[df['Flagged as Suspect Reading'] == False]
#     print(df.shape)
    return df


def Remove_Outlier_Indices(df):
    
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    trueList = ~((df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR)))
    return trueList


def IQR(df):
    
    nonOutliers = Remove_Outlier_Indices(df['Value'])

    # Non-Outlier Subset of the Given Dataset
    dfIQR= df[nonOutliers]
#     print(df.shape)
#     print ("Removed outliers")
#     print(dfIQR.shape)
    return dfIQR


import matplotlib.pyplot as plt
from scipy import stats

def plot_line_graph(df, data_params):
    fig, ax = plt.subplots(figsize=(15,15))

    for sensor_name,sensor_data in  df.groupby('Sensor Name'):
        datetimes = pd.to_datetime(sensor_data['Timestamp'])
        plt.plot(datetimes,sensor_data['Value'],label=sensor_name)
        plt.xlabel("MMDDHH")
        plt.ylabel(data_params["data_variable"])

    plt.legend()

    
