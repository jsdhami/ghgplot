import requests
import folium
import folium.plugins
from folium import Map, TileLayer
from pystac_client import Client
import branca
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Provide the STAC and RASTER API endpoints
# The endpoint is referring to a location within the API that executes a request on a data collection nesting on the server.
def flux(observation_date_1, observation_date_2, lat, lon):
# The STAC API is a catalog of all the existing data collections that are stored in the GHG Center.
    STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"

# The RASTER API is used to fetch collections for visualization
    RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

# The collection name is used to fetch the dataset from the STAC API. First, we define the collection name as a variable
# Name of the collection for ECCO Darwin CO₂ flux monthly emissions
    collection_name = "eccodarwin-co2flux-monthgrid-v5"

# Fetch the collection from the STAC API using the appropriate endpoint
# The 'requests' library allows a HTTP request possible
    collection = requests.get(f"{STAC_API_URL}/collections/{collection_name}").json()

    pd.set_option('display.max_colwidth', None)  # Set maximum column width to "None" to prevent cutting off text

# Extract the relevant information about the collection
    collection_info = {
    "Title": collection.get("title", "N/A"), # Extract the title of the collection
    "Description": collection.get("description", "N/A"), # Extract the dataset description
    "Temporal Extent": collection.get("extent", {}).get("temporal", {}).get("interval", "N/A"), # Extract the temporal coverage of the collection
    "Spatial Extent": collection.get("extent", {}).get("spatial", {}).get("bbox", "N/A"), # Extract the spatial coverage of the collection
}

# Convert the derived information into a DataFrame format
    properties_table = pd.DataFrame(list(collection_info.items()), columns=["Collection Summary", ""])

# Display the properties in a table
    collection_summary = properties_table.style.set_properties(**{'text-align': 'left'}) \
                                           .set_table_styles([
    {
        'selector': 'th.col0, td.col0',    # Select the first column
        
        'props': [('min-width', '200px'),  # Set a minimum width
                  ('text-align', 'left')]  # Align text to the left
    },
    {
        'selector': 'td.col1',             # Select the second column
        'props': [('text-align', 'left')]  # Align text to the left
    }
])


# Create a function that would search for data collection in the US GHG Center STAC API

# First, we need to define the function
# The name of the function is "get_item_count"
# The argument that will be passed to the defined function is "collection_id"
    def get_item_count(collection_id):

    # Set a counter for the number of items existing in the collection
        count = 0

    # Define the path to retrieve the granules (items) of the collection of interest in the STAC API
        items_url = f"{STAC_API_URL}/collections/{collection_id}/items"

    # Run a while loop to make HTTP requests until there are no more URLs associated with the collection in the STAC API
        while True:

        # Retrieve information about the granules by sending a "get" request to the STAC API using the defined collection path
            response = requests.get(items_url)

        # If the items do not exist, print an error message and quit the loop
            if not response.ok:
                print("error getting items")
                exit()

        # Return the results of the HTTP response as JSON
            stac = response.json()

        # Increase the "count" by the number of items (granules) returned in the response
            count += int(stac["context"].get("returned", 0))

        # Retrieve information about the next URL associated with the collection in the STAC API (if applicable)
            next = [link for link in stac["links"] if link["rel"] == "next"]

        # Exit the loop if there are no other URLs
            if not next:
                break

        # Ensure the information gathered by other STAC API links associated with the collection are added to the original path
        # "href" is the identifier for each of the tiles stored in the STAC API
            items_url = next[0]["href"]

    # Return the information about the total number of granules found associated with the collection
        return count


# Apply the function created above "get_item_count" to the Air-Sea CO2 Flux ECCO-Darwin collection
    number_of_items = get_item_count(collection_name)

# Get the information about the number of granules found in the collection
    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]

# Sort the items based on their date-time attribute
    items_sorted = sorted(items, key=lambda x: x["properties"]["start_datetime"])

# Create an empty list
    table_data = []
# Extract the ID and date-time information for each granule and add them to the list
# By default, only the first 5 items in the collection are extracted to be displayed in the table.
# To see the date-time of all existing granules in this collection, remove "5" from "item_sorted[:5]" in the line below.
    for item in items_sorted[:5]:
        table_data.append([item['id'], item['properties']['start_datetime']])

# Define the table headers
    headers = ["Item ID", "Start Date-Time"]


# Once again, apply the function created above "get_item_count" to the collection
# This step allows retrieving the number of granules “observations” in the collection.
    number_of_items = get_item_count(collection_name)
    items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]

# Now you need to create a dictionary where the start datetime values for each granule are queried more explicitly by year and month (e.g., 2020-02)
    items = {item["properties"]["start_datetime"]: item for item in items}

# Next, you need to specify the asset name for this collection.
# The asset name refers to the raster band containing the pixel values for the parameter of interest.
# For the case of this collection, the parameter of interest is “co2”.
    asset_name = "co2"


# Fetch the minimum and maximum values for the CO2 value range
    rescale_values = {"max":0.0007, "min":-0.0007}


# Choose a color map for displaying the first observation (event)
# Please refer to matplotlib library if you'd prefer to choose a different color ramp.
# For more information on Colormaps in Matplotlib, please visit https://matplotlib.org/stable/users/explain/colors/colormaps.html
    color_map = "magma"


# You can retrieve the first observation of interest by defining the last 6 digits of its Item ID.
# The numbers indicate the year and month (YYYYMM) when the data was gathered.
# For example, the observation collected in December 2022 has the following item ID: eccodarwin-co2flux-monthgrid-v5-202212
# To set the time, you will need to insert "202212" in the line below.


# Set the time
# If you want to select another time, you can refer to the Data Browser on the U.S. Greenhouse Gas Center website
# URL to the Air-Sea CO2 Flux ECCO-Darwin collection in the US GHG Center: https://dljsq618eotzp.cloudfront.net/browseui/#eccodarwin-co2flux-monthgrid-v5/


# Don't change anything here
    observation_1 = f'eccodarwin-co2flux-monthgrid-v5-{observation_date_1}'


# Make a GET request to retrieve information for the December 2022 tile
# A GET request is made for the December 2022 tile.
    december_2022_tile = requests.get(

    # Pass the collection name, the item number in the list, and its ID
        f"{RASTER_API_URL}/collections/{items[list(items.keys())[0]]['collection']}/items/{items[list(items.keys())[0]]['id']}/tilejson.json?"

    # Pass the asset name
        f"&assets={asset_name}"

    # Pass the color formula and colormap for custom visualization
        f"&color_formula=gamma+r+1.05&colormap_name={color_map}"

    # Pass the minimum and maximum values for rescaling
        f"&rescale={rescale_values['min']},{rescale_values['max']}")

# Return the response in JSON format
# Access the response object from the tuple before calling .json()
    december_2022_tile = december_2022_tile.json() # Modified line: Access the response object from the tuple


# You will repeat the same approach used in the previous step to retrieve the second observation of interest


# Don't change anything here
    observation_2 = f'eccodarwin-co2flux-monthgrid-v5-{observation_date_2}'


# Make a GET request to retrieve information for the December 2022 tile
# A GET request is made for the April 2021 tile.
    april_2021_tile = requests.get(

    # Pass the collection name, the item number in the list, and its ID
        f"{RASTER_API_URL}/collections/{items[list(items.keys())[20]]['collection']}/items/{items[list(items.keys())[20]]['id']}/tilejson.json?"

    # Pass the asset name
        f"&assets={asset_name}"

    # Pass the color formula and colormap for custom visualization
        f"&color_formula=gamma+r+1.05&colormap_name={color_map}"

    # Pass the minimum and maximum values for rescaling
        f"&rescale={rescale_values['min']},{rescale_values['max']}") # Removed the extra comma here

# Return the response in JSON format
    april_2021_tile = april_2021_tile.json() # Now april_2021_tile is a Response object

####### To change the location, you can simply insert the latitude and longitude of the area of your interest in the "location=(LAT, LONG)" statement

# Set the initial zoom level and center of map for both tiles
# 'folium.plugins' allows mapping side-by-side
    map_ = folium.plugins.DualMap(location=(lat, lon), zoom_start=4)


# Define the first map layer with the CO2 Flux data for December 2022
    map_layer_1 = TileLayer(
        tiles=december_2022_tile["tiles"][0], # Path to retrieve the tile
        attr="GHG", # Set the attribution
        name='December 2022 CO2 Flux', # Title for the layer
        overlay=True, # The layer can be overlaid on the map
        opacity=0.8, # Adjust the transparency of the layer
    )
# Add the first layer to the Dual Map
    map_layer_1.add_to(map_.m1)


# Define the second map layer with the CO2 Flux data for April 2021
    map_layer_2 = TileLayer(
        tiles=april_2021_tile["tiles"][0], # Path to retrieve the tile
        attr="GHG", # Set the attribution
        name='April 2021 CO2 Flux', # Title for the layer
        overlay=True, # The layer can be overlaid on the map
        opacity=0.8, # Adjust the transparency of the layer
    )
# Add the second layer to the Dual Map
    map_layer_2.add_to(map_.m2)


# Display data markers (titles) on both maps
    folium.Marker((lat, lon), tooltip="both").add_to(map_)

# Add a layer control to switch between map layers
    folium.LayerControl(collapsed=False).add_to(map_)

# Add a legend to the dual map using the 'branca' library
# Note: the inserted legend is representing the minimum and maximum values for both tiles
# Minimum value = -0.0007, maximum value = 0.0007
    colormap = branca.colormap.LinearColormap(colors=["#0000FF", "#3399FF", "#66CCFF", "#FFFFFF", "#FF66CC", "#FF3399", "#FF0000"], vmin=-0.0007, vmax=0.0007)

# Add the data unit as caption
    colormap.caption = 'Millimoles per meter squared per second (mmol m²/s)'

# Define custom tick values for the legend bar
    tick_val = [-0.0007, -0.00035, 0, 0.00035, 0.0007]

# Create a HTML representation
    legend_html = colormap._repr_html_()

# Create a customized HTML structure for the legend
    legend_html = f'''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; width: 400px; height: auto; background-color: rgba(255, 255, 255, 0.8);
                border-radius: 5px; border: 1px solid grey; padding: 10px; font-size: 14px; color: black;">
        <b>{colormap.caption}</b><br>
        <div style="display: flex; justify-content: space-between;">
            <div>{tick_val[0]}</div>
            <div>{tick_val[1]}</div>
            <div>{tick_val[2]}</div>
            <div>{tick_val[3]}</div>
            <div>{tick_val[4]}</div>
        </div>
        <div style="background: linear-gradient(to right,
                    {'#0000FF'}, {'#3399FF'} {20}%,
                    {'#3399FF'} {20}%, {'#66CCFF'} {40}%,
                    {'#66CCFF'} {40}%, {'#FFFFFF'} {50}%,
                    {'#FFFFFF'} {50}%, {'#FF66CC'} {80}%,
                    {'#FF66CC'} {80}%, {'#FF3399'}); height: 10px;"></div>
    </div>
    '''

    map_.get_root().html.add_child(folium.Element(legend_html))
    return(map_)


# aoimap function
def aoimap(lat1,lon1,lat2,lon2,lat3,lon3,lat4,lon4):
 # Create a polygon for the area of interest (aoi)
    california_coast_aoi = {
        "type": "Feature", # Create a feature object
        "properties": {},
        "geometry": { # Set the bounding coordinates for the polygon
            "coordinates": [
                [
                    [lon1, lat1], # North-west bounding coordinate
                    [lon2, lat2], # North-east bounding coordinate
                    [lon3, lat3], # South-east bounding coordinate
                    [lon4, lat4], # South-west bounding coordinate
                    [lon1, lat1]  # North-west bounding coordinate (closing the polygon)
                ]
            ],
            "type": "Polygon",
        },
    }

    # Create a new map to display the generated polygon
    aoi_map = Map(

        # Base map is set to OpenStreetMap
        tiles="OpenStreetMap",

        # Define the spatial properties for the map
        location=[

        # Set the center of the map
            (lat1+lat2+lat3+lat4)/4, (lon1+lon2+lon3+lon4)/4
        ],

        # Set the zoom value
        zoom_start=5,
    )

    # Insert the Coastal California polygon to the map
    folium.GeoJson(california_coast_aoi, name="Coastal California").add_to(aoi_map)
    # Visualize the map
    return aoi_map


def time_series(lat1,lon1,lat2,lon2,lat3,lon3,lat4,lon4,):

    # The function takes an item (granule) and a JSON (polygon) as input parameters
        def generate_stats(item, geojson):

            # A POST request is made to submit the data associated with the item of interest (specific observation) within the boundaries of the polygon to compute its statistics
            result = requests.post(

                # Raster API Endpoint for computing statistics
                f"{RASTER_API_URL}/cog/statistics",

                # Pass the URL to the item, asset name, and raster identifier as parameters
                params={"url": item["assets"][asset_name]["href"]},

                # Send the GeoJSON object (polygon) along with the request
                json=geojson,

            # Return the response in JSON format
            ).json()


            # Return a dictionary containing the computed statistics along with the item's datetime information.
            return {
                **result["properties"],
                "datetime": item["properties"]["start_datetime"],
            }
            # Check the total number of items available within the collection


        # Check the total number of items available within the collection
        items = requests.get(
            f"{STAC_API_URL}/collections/{collection_name}/items?limit=600"
        ).json()["features"]
        stats = {}


        california_coast_aoi = {
            "type": "Feature", # Create a feature object
            "properties": {},
            "geometry": { # Set the bounding coordinates for the polygon
                "coordinates": [
                    [
                        [lon1, lat1], # North-west bounding coordinate
                        [lon2, lat2], # North-east bounding coordinate
                        [lon3, lat3], # South-east bounding coordinate
                        [lon4, lat4], # South-west bounding coordinate
                        [lon1, lat1]  # North-west bounding coordinate (closing the polygon)
                    ]
                ],
                "type": "Polygon",
            },
        }

        for item in items:
            date = item["properties"]["start_datetime"]  # Get the associated date
            year_month = date[:7].replace('-', '')  # Convert datetime to year-month
            stats[year_month] = generate_stats(item, california_coast_aoi)

        # Create a function that converts statistics in JSON format into a pandas DataFrame
        def clean_stats(stats_json) -> pd.DataFrame:
            pd.set_option('display.float_format', '{:.20f}'.format)
            stats_json_ = [stats_json[datetime] for datetime in stats_json]
            # Normalize the JSON data
            df = pd.json_normalize(stats_json_)

            # Replace the naming "statistics.b1" in the columns
            df.columns = [col.replace("statistics.b1.", "") for col in df.columns]

            # Set the datetime format
            df["date"] = pd.to_datetime(df["datetime"])

            # Return the cleaned format
            return df

        # Apply the generated function on the stats data
        df = clean_stats(stats)
        # Sort the DataFrame by the datetime column so the plot displays the values from left to right (2020 -> 2022)
        df_sorted = df.sort_values(by="datetime")

        # Plot the timeseries analysis of the monthly air-sea CO₂ flux changes along the coast of California
        # Figure size: 20 representing the width, 10 representing the height
        fig = plt.figure(figsize=(20, 10))
        plt.plot(
            df_sorted["datetime"],    # X-axis: sorted datetime
            df_sorted["max"],         # Y-axis: maximum CO₂ value
            color="purple",           # Line color
            linestyle="-",            # Line style
            linewidth=1,              # Line width
            label="CO2 Emissions",    # Legend label
        )

        # Display legend
        plt.legend()

        # Insert label for the X-axis
        plt.xlabel("Years")

        # Insert label for the Y-axis
        plt.ylabel("CO2 Emissions mmol m²/s")

        # Insert title for the plot
        plt.title("CO2 Emission Values for Selected Region (2020-2022)")

        # Rotate x-axis labels to avoid cramping
        plt.xticks(rotation=90)

        # Add data citation
        plt.text(
            df_sorted["datetime"].iloc[0],           # X-coordinate of the text (first datetime value)
            df_sorted["max"].min(),                  # Y-coordinate of the text (minimum CO2 value)

            # Text to be displayed
            "Source: NASA Air-Sea CO₂ Flux, ECCO-Darwin Model v5",
            fontsize=12,                             # Font size
            horizontalalignment="left",              # Horizontal alignment
            verticalalignment="bottom",              # Vertical alignment
            color="blue",                            # Text color
        )

        # Plot the time series
        return plt.show()