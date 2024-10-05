import numpy as np
import pandas as pd
from glob import glob
from io import StringIO
import matplotlib.pyplot as plt
import requests
import warnings

def site_code(gas_type):
  github_repo_owner = "NASA-IMPACT"
  github_repo_name = "noaa-viz"
  folder_path_ch4, folder_path_co2 = "flask/ch4", "flask/co2"
  combined_df_co2, combined_df_ch4 = pd.DataFrame(), pd.DataFrame()


  # Function to fetch and append a file from GitHub
  def append_github_file(file_url):
      response = requests.get(file_url)
      response.raise_for_status()
      return response.text

  # Get the list of CH4 files in the specified directory using GitHub API
  github_api_url = f"https://api.github.com/repos/{github_repo_owner}/{github_repo_name}/contents/{folder_path_ch4}"
  response = requests.get(github_api_url)
  response.raise_for_status()
  file_list_ch4 = response.json()

  # Get the list of CO2 files in the specified directory using GitHub API
  github_api_url = f"https://api.github.com/repos/{github_repo_owner}/{github_repo_name}/contents/{folder_path_co2}"
  response = requests.get(github_api_url)
  response.raise_for_status()
  file_list_co2 = response.json()
  warnings.filterwarnings("ignore")

  for file_info in file_list_ch4:
      if file_info["name"].endswith("txt"):
          file_content = append_github_file(file_info["download_url"])
          Lines = file_content.splitlines()
          index = Lines.index("# VARIABLE ORDER")+2
          df_ch4 = pd.read_csv(StringIO("\n".join(Lines[index:])), delim_whitespace=True)
          combined_df_ch4 = pd.concat([combined_df_ch4, df_ch4], ignore_index=True)


  for file_info in file_list_co2:
      if file_info["name"].endswith("txt"):
          file_content = append_github_file(file_info["download_url"])
          Lines = file_content.splitlines()
          index = Lines.index("# VARIABLE ORDER")+2
          df_co2 = pd.read_csv(StringIO("\n".join(Lines[index:])), delim_whitespace=True)
          combined_df_co2 = pd.concat([combined_df_co2, df_co2], ignore_index=True)


  if gas_type.lower() == "ch4":
        return combined_df_ch4['site_code'].unique()
  elif gas_type.lower() == "co2":
        return combined_df_co2['site_code'].unique()
  else:
        raise ValueError("Invalid gas type. Use 'ch4' or 'co2'.")
  
  
def locate_site(site_code):
  return(f'https://gml.noaa.gov/dv/site/?stacode={site_code}')


def get_df_co2(site_code):

  github_repo_owner = "NASA-IMPACT"
  github_repo_name = "noaa-viz"
  folder_path_ch4, folder_path_co2 = "flask/ch4", "flask/co2"
  combined_df_co2, combined_df_ch4 = pd.DataFrame(), pd.DataFrame()
  def append_github_file(file_url):
      response = requests.get(file_url)
      response.raise_for_status()
      return response.text

  github_api_url = f"https://api.github.com/repos/{github_repo_owner}/{github_repo_name}/contents/{folder_path_co2}"
  response = requests.get(github_api_url)
  response.raise_for_status()
  file_list_co2 = response.json()
  warnings.filterwarnings("ignore")

  for file_info in file_list_co2:
      if file_info["name"].endswith("txt"):
          file_content = append_github_file(file_info["download_url"])
          Lines = file_content.splitlines()
          index = Lines.index("# VARIABLE ORDER")+2
          df_co2 = pd.read_csv(StringIO("\n".join(Lines[index:])), delim_whitespace=True)
          combined_df_co2 = pd.concat([combined_df_co2, df_co2], ignore_index=True)

  site_to_filter = site_code
  filtered_df = combined_df_co2[combined_df_co2['site_code'] == site_to_filter]

  filtered_df['datetime'] = pd.to_datetime(filtered_df['datetime'])

  # Set the "Date" column as the index
  filtered_df.set_index('datetime', inplace=True)
  return filtered_df


def get_df_ch4(site_code):

  github_repo_owner = "NASA-IMPACT"
  github_repo_name = "noaa-viz"
  folder_path_ch4, folder_path_co2 = "flask/ch4", "flask/c02"
  combined_df_co2, combined_df_ch4 = pd.DataFrame(), pd.DataFrame()
  def append_github_file(file_url):
      response = requests.get(file_url)
      response.raise_for_status()
      return response.text

  github_api_url = f"https://api.github.com/repos/{github_repo_owner}/{github_repo_name}/contents/{folder_path_ch4}"
  response = requests.get(github_api_url)
  response.raise_for_status()
  file_list_ch4 = response.json()
  warnings.filterwarnings("ignore")

  for file_info in file_list_ch4:
      if file_info["name"].endswith("txt"):
          file_content = append_github_file(file_info["download_url"])
          Lines = file_content.splitlines()
          index = Lines.index("# VARIABLE ORDER")+2
          df = pd.read_csv(StringIO("\n".join(Lines[index:])), delim_whitespace=True)
          combined_df_ch4 = pd.concat([combined_df_ch4, df], ignore_index=True)

  site_to_filter = site_code
  filtered_df = combined_df_ch4[combined_df_ch4['site_code'] == site_to_filter]

  filtered_df['datetime'] = pd.to_datetime(filtered_df['datetime'])

  # Set the "Date" column as the index
  filtered_df.set_index('datetime', inplace=True)
  return filtered_df

def get_ch4_plot(site_code):
  github_repo_owner = "NASA-IMPACT"
  github_repo_name = "noaa-viz"
  folder_path_ch4, folder_path_co2 = "flask/ch4", "flask/c02"
  combined_df_co2, combined_df_ch4 = pd.DataFrame(), pd.DataFrame()
  def append_github_file(file_url):
      response = requests.get(file_url)
      response.raise_for_status()
      return response.text

  github_api_url = f"https://api.github.com/repos/{github_repo_owner}/{github_repo_name}/contents/{folder_path_ch4}"
  response = requests.get(github_api_url)
  response.raise_for_status()
  file_list_ch4 = response.json()
  warnings.filterwarnings("ignore")

  for file_info in file_list_ch4:
      if file_info["name"].endswith("txt"):
          file_content = append_github_file(file_info["download_url"])
          Lines = file_content.splitlines()
          index = Lines.index("# VARIABLE ORDER")+2
          df = pd.read_csv(StringIO("\n".join(Lines[index:])), delim_whitespace=True)
          combined_df_ch4 = pd.concat([combined_df_ch4, df], ignore_index=True)

  site_to_filter = site_code
  filtered_df = combined_df_ch4[combined_df_ch4['site_code'] == site_to_filter]

  filtered_df['datetime'] = pd.to_datetime(filtered_df['datetime'])

  # Set the "Date" column as the index
  filtered_df.set_index('datetime', inplace=True)

  #filtered_df = filtered_df[(filtered_df['value'] >= 1700) & (filtered_df['value'] <= 2100)]
  # Create a time series plot for 'Data' and 'Value'
  plt.figure(figsize=(12, 6))
  plt.plot(filtered_df.index, filtered_df['value'], label='Methane Ch4 Concentration (ppb)')
  plt.xlabel("Observation Date/Time")
  plt.ylabel("Methane Ch4 Concentration (ppb)")
  plt.title(f"Observed CH4 Concentration {site_to_filter}")
  plt.legend()
  plt.grid(True)
  return plt.show()