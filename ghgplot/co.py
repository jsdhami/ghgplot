import requests
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import plotly.graph_objs as go

def get_df(year, month, day):
    # Define the base URL for the data sets
    base_url = "https://donnees-data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/MOPITT/"

    # Construct the URL for the specific date
    url = f"{base_url}{year}/MOP02J-{year}{month:02d}{day:02d}-L2V18.0.3.csv"

    # Request the data
    response = requests.get(url)

    if response.status_code == 200:
        # Convert the content to a pandas DataFrame
        data = StringIO(response.content.decode('utf-8'))
        df = pd.read_csv(data)
        df.rename(columns={df.columns[0]: 'Latitude'}, inplace=True)
        df.rename(columns={df.columns[1]: 'Longitude'}, inplace=True)
        df.rename(columns={df.columns[2]: 'COTotalColumn'}, inplace=True)
        df.rename(columns={df.columns[8]: 'COMixingRatio 500hPa'}, inplace=True)
        df.rename(columns={df.columns[-1]: 'RetrievedSurfaceTemperature'}, inplace=True)
        print(f"Downloaded dataset for {year}-{month:02d}-{day:02d}")
        return df
    else:
        print(f"Error downloading dataset for {year}-{month:02d}-{day:02d}: {response.status_code}")
        return None
  

def get_plot(year, month, day, pressure, count):
    # Define the base URL for the data sets
    base_url = "https://donnees-data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/MOPITT/"

    # Construct the URL for the specific date
    url = f"{base_url}{year}/MOP02J-{year}{month:02d}{day:02d}-L2V18.0.3.csv"

    # Request the data
    response = requests.get(url)


        # Convert the content to a pandas DataFrame
    data = StringIO(response.content.decode('utf-8'))
    df = pd.read_csv(data)
    df.rename(columns={df.columns[0]: 'Latitude'}, inplace=True)
    df.rename(columns={df.columns[1]: 'Longitude'}, inplace=True)
    df.rename(columns={df.columns[2]: 'COTotalColumn'}, inplace=True)
    df.rename(columns={df.columns[8]: 'COMixingRatio 500hPa'}, inplace=True)

    # Define the scatter plot
    fig = go.Figure(go.Scattergeo(
        lon = df['Longitude'].head(count),
        lat = df['Latitude'].head(count),
        text = df[f'COMixingRatio {pressure}hPa'].head(count),
        marker = dict(
            size = 8,
            color = df[f'COMixingRatio {pressure}hPa'],
            colorscale = 'Viridis',
            showscale = True,
            colorbar = dict(title=f"COMixingRatio {pressure}hPa")
        )
    ))

    # Set layout for globe projection
    fig.update_geos(projection_type="orthographic", showcountries=True, showcoastlines=True, showland=True, landcolor="rgb(217, 217, 217)")

    # Set title and display
    fig.update_layout(title=f'COMixingRatio {pressure}hPa - Globe Visualization', margin={"r":0,"t":0,"l":0,"b":0})
    return fig.show()


def get_plot_temp(year, month, day, count):
    # Define the base URL for the data sets
    base_url = "https://donnees-data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/MOPITT/"

    # Construct the URL for the specific date
    url = f"{base_url}{year}/MOP02J-{year}{month:02d}{day:02d}-L2V18.0.3.csv"

    # Request the data
    response = requests.get(url)


        # Convert the content to a pandas DataFrame
    data = StringIO(response.content.decode('utf-8'))
    df = pd.read_csv(data)
    df.rename(columns={df.columns[0]: 'Latitude'}, inplace=True)
    df.rename(columns={df.columns[1]: 'Longitude'}, inplace=True)
    df.rename(columns={df.columns[2]: 'COTotalColumn'}, inplace=True)
    df.rename(columns={df.columns[8]: 'COMixingRatio 500hPa'}, inplace=True)
    df.rename(columns={df.columns[-1]: 'RetrievedSurfaceTemperature'}, inplace=True)
    # Define the scatter plot
    fig = go.Figure(go.Scattergeo(
        lon = df['Longitude'].head(count),
        lat = df['Latitude'].head(count),
        text = df['RetrievedSurfaceTemperature'].head(count),
        marker = dict(
            size = 8,
            color = df['RetrievedSurfaceTemperature'],
            colorscale = 'Viridis',
            showscale = True,
            colorbar = dict(title='RetrievedSurfaceTemperature')
        )
    ))

    # Set layout for globe projection
    fig.update_geos(projection_type="orthographic", showcountries=True, showcoastlines=True, showland=True, landcolor="rgb(217, 217, 217)")

    # Set title and display
    fig.update_layout(title='RetrievedSurfaceTemperature - Globe Visualization', margin={"r":0,"t":0,"l":0,"b":0})
    return fig.show()