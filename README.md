# Greenhouse Gas Data Analysis with `ghgplot`

Welcome to the Greenhouse Gas Data Analysis project! This repository contains tools and scripts for analyzing greenhouse gas (GHG) data, including CO2 flux, CH4 and CO2 concentrations, and CO mixing ratios.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [CO2 Air-to-Sea Flux](#co2-air-to-sea-flux)
  - [CH4 and CO2 Concentrations](#ch4-and-co2-concentrations)
  - [CO Mixing Ratio](#co-mixing-ratio)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction
This project leverages the `ghgplot` library to provide tools for analyzing various greenhouse gases. It includes functionalities for mapping areas of interest, comparing fluxes, and retrieving concentration data from different sources.

## Features
- **CO2 Air-to-Sea Flux Analysis**: Compare fluxes between different dates and locations.
- **CH4 and CO2 Concentration Data**: Retrieve and visualize concentration data from NOAA Global Monitoring Laboratory.
- **CO Mixing Ratio**: Analyze CO mixing ratios and surface temperatures from MOPITT data.

## Installation
To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/NASA-IMPACT/noaa-viz.git
cd noaa-viz
pip install -r requirements.txt
```

## Usage

### CO2 Air-to-Sea Flux
1. **Select Area of Interest**:
   ```python
   from ghgplot import co2
   co2.aoimap(lat1,lon1,lat2,lon2,lat3,lon3,lat4,lon4)
   ```

2. **Compare Flux Between Dates**:
   ```python
   co2.flux(YYYYMM,YYYYMM,lat,lon)
   ```

3. **Print Flux Statistics**:
   ```python
   co2.print_stats(lat1,lon1,lat2,lon2,lat3,lon3,lat4,lon4,yyyymm)
   ```

### CH4 and CO2 Concentrations
1. **Locate Site**:
   ```python
   from ghgplot import conc
   conc.locate_site('site_code')
   ```

2. **Get CO2 Dataframe**:
   ```python
   conc.get_df_co2('site_code')
   ```

3. **Get CH4 Dataframe**:
   ```python
   conc.get_df_ch4('site_code')
   ```

4. **Plot CH4 Concentration**:
   ```python
   conc.get_ch4_plot('site_code')
   ```

5. **Plot CO2 Concentration**:
   ```python
   conc.get_co2_plot('site_code')
   ```

### CO Mixing Ratio
1. **Get CO Dataframe**:
   ```python
   from ghgplot import co
   co.get_df(year, month, day)
   ```

2. **Plot CO Mixing Ratio**:
   ```python
   co.get_plot(year, month, day, pressure, count)
   ```

3. **Plot Surface Temperature**:
   ```python
   co.get_plot_temp(year, month, day, count)
   ```

## Contributing
We welcome contributions!

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or feedback, please contact us at [manish24864pande@gmail.com](mailto:manish24864pandey@gmail.com).
```
# SetUp Project

# Install all Required packages
```bash
pip install -r requirements.txt
```

# Make requirements.txt file
```bash
pip freeze > requirements.txt
```
# activate env
```bash
source env/bin/activate
``` window
env\Scripts\activate

