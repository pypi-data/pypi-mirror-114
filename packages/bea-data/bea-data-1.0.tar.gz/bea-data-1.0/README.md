# BEA Data

BEA Data is a python library designed to interact with the Bureau of Economic Analysis API and organize the returned data into Pandas dataframes. 

Requires python 3.7+

## Installation

```
pip install py_bea
```

## Setup

You **MUST** set your api key as an environment variable on the machine that you are using. To do this, set it using the following instructions:

Windows:
```powershell
$Env:BEA_API_KEY='{YOUR_API_KEY}'
```

Mac/Linux:
```sh
export BEA_API_KEY='{YOUR_API_KEY}'
```
## Usage
### get_dataset_list

The `get_dataset_list()` function is designed to just query the getdatasetlist API endpoint and return a dict
of available datasets from the BEA.

```python
from bea_data.bea_data import get_dataset_list

get_dataset_list()
```

### get_dataset_params

Gets the list of parameters that are applicable to a specific dataset from BEA. Returns a dict containing these, and their descriptions.

```python
from bea_data.bea_data import get_dataset_params

get_dataset_params("Regional")
```

### getData

This is a class that gets the data from the BEA API and constructs a pandas dataframe from the returned data.

```python
from bea_data.bea_data import getData

data = getData(datasetname="Regional",
                 TableName="CAINC1",
                 method='getdata',
                 LineCode=3,
                 GeoFIPS="04015, 04027, 04012, 04000, 00000",
                 Year="2019")
```

#### *getData.clean_df(index, col, data)*

Paramaters:
- index = str; The column that should be used as the index
- col = str; the column that should be used as column headers
- data = str; the column that should be used as the data

Returns: Pandas.DataFrame

A method that organizes the datafame by making a specific column the index column, using one column as the headers, and another column as the data. Simplfies the data in the table and prepares it for being used in a visualization. 

Example:

```python
data.clean_df('TimePeriod','GeoName','DataValue')
```



