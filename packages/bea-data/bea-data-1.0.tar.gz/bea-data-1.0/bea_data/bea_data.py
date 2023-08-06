"""
Interacts with the Bureau of Economic Analysis API with python.

By: Aaron Finocchiaro
"""
import os
import re
import urllib.parse as urlparse
import pandas as pd
import requests

BEA_API_URL = "http://apps.bea.gov/api/data?"

def bea_request(params:list) -> dict:
    """
    Creates query url and submits request to BEA API endpoint.
    Arguments:
        - params; a list of query parameters to include in the request.
    Returns dict
    """
    params.update({
        'UserID' : os.environ.get('BEA_API_KEY'),
        'ResultFormat' : 'JSON',
    })

    # remove spaces from passed arugments if any spaces exist for strings only
    params = {key: re.sub(r"\s?", "", val) if type(val) == str else val for key,val in params.items()}

    url_parts = list(urlparse.urlparse(BEA_API_URL))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlparse.urlencode(query)

    results = requests.get(urlparse.urlunparse(url_parts))
    return results.json()

def get_dataset_list() -> dict:
    """
    A function to call the GetDatasetList API endpoint and list all available datasets from the
    Bureau of Economic Analysis API.

    returns: dict of dataset and their descriptions
    """
    query_params = {
        'method' : 'getdatasetlist'
    }
    datasets = bea_request(query_params)
    return datasets['BEAAPI']['Results']['Dataset']

def get_dataset_params(dataset_name:str) -> dict:
    """
    A function to get all of the dataset parameters for a specific dataset.

    Paramters:
        - dataset_name = str; srting value associated to a dataset

    returns: dict of dataset parameters and their descriptions
    """
    query_params = {
        'method' : 'getparameterlist',
        'datasetname' : dataset_name,
    }
    parameters = bea_request(query_params)
    return parameters['BEAAPI']['Results']['Parameter']

class getData():
    """
    Retrieves data from the get data endpoint of the Bureau of Economic Analysis API.
    """
    def __init__(self, **kwargs):

        self.query_params = kwargs

        self.raw_data = bea_request(self.query_params)
        self.raw_df = pd.DataFrame(self.raw_data['BEAAPI']['Results']['Data'])
        self.notes = self.raw_data['BEAAPI']['Results']['Notes']
    
    def clean_df(self, index:str, cols:str, data:str):
        """
        cleans the raw dataframe to make it easily parsable
        """
        #deep copy to avoid overwriting
        clean_df = self.raw_df.copy()

        # strip asterisks off that indicate notes for a speicifc col
        clean_df[cols] = clean_df[cols].map(lambda x: x.rstrip(r'\*'))

        #organize the df
        clean_df = clean_df.pivot(index=index, columns=cols)[data]

        return clean_df

if __name__ == "__main__":
    bea_data = getData(datasetname="Regional",TableName="CAINC1",method='getdata',LineCode=3, GeoFIPS="04015,04027,04012,04000,00000", Year="2019")
    print(bea_data.clean_df('TimePeriod','GeoName','DataValue'))
