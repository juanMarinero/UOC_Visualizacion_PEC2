#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :

import numpy as np
import pandas as pd

pd.set_option("display.max_columns", None)  # Display all columns


import os
import pickle

import holoviews as hv

hv.extension("bokeh")

#  import matplotlib.pyplot as plt
#  import matplotlib as mpl
#  import seaborn as sns


def display_img_files(img_files, xdg_open=True):
    import subprocess
    from PIL import Image

    if xdg_open:
        for img_file in img_files:
            try:
                subprocess.run(
                    ["xdg-open", img_file]
                )  # Use xdg-open to open files with the default program
            except Exception as e:
                xdg_open = False
                print("img_file:", img_file)
                break


def display_img_files(img_files, xdg_open=True):
    import subprocess
    from PIL import Image

    if xdg_open:
        for img_file in img_files:
            try:
                subprocess.run(
                    ["xdg-open", img_file]
                )  # Use xdg-open to open files with the default program
            except Exception as e:
                xdg_open = False
                print("img_file:", img_file)
                break


def dump_or_load(file, var=None, dump=False):
    if dump:
        # save variable to a file
        with open(file, "wb") as file:
            pickle.dump(var, file)
        print(f"Saved {file}")
        return
    else:
        # from file to variable
        with open(file, "rb") as file:
            var_loaded = pickle.load(file)
        print(f"Opened {file}")
        return var_loaded


def query_df():
    import datadotworld as dw

    try:
        results = dw.query(
            "cityofchicago/chicago-energy-benchmarking-1",
            "SELECT * FROM chicago_energy_benchmarking_1",
        )
    except Exception as err:
        print(f"\tError: {err}")
        print("Make sure to $ dw configure # terminal")
        # https://data.world/integrations/python
    df = results.dataframe
    return df


def pandas_import():
    df = pd.read_csv(
        "https://query.data.world/s/znbuwss47wy7cxt4yvz3tz4ak4xv4t?dws=00000"
    )
    return df


def get_df():
    df_filename = f"PEC2_ejer3_df.pkl"
    if not os.path.isfile(df_filename):
        #  df = query_df()
        df = pandas_import()
        dump_or_load(df_filename, df, dump=True)  # save to file
    else:
        df = dump_or_load(df_filename)  # get from file
    return df


def get_horizon_graph(df, cols, plot_file):
    # Ensure 'Data Year' is treated as a categorical variable
    df["Data Year"] = df["Data Year"].astype(str)

    # Load the Bokeh extension
    hv.extension("bokeh")

    # Create a list of years for the x-axis
    years = list(df["Data Year"].unique())

    areas = [[] for _ in cols]

    # Create a horizontal stack of areas for each year and each column
    for year in years:
        year_df = df[df["Data Year"] == year]
        for i, col in enumerate(cols):
            area = hv.Area((year_df.index, year_df[col]), label=f"{year} - {col}")
            areas[i].append(area)

    # Set options for individual areas and create overlays
    for i, col in enumerate(cols):
        for area in areas[i]:
            area.opts(
                width=1000,
                height=200,
                ylim=(0, df[col].max()),
            )
        overlay = hv.Overlay(areas[i])
        if i == 0:
            overlays = overlay
        else:
            overlays += overlay

    # Create a layout with shared x-axis
    layout = (overlays).cols(1)

    # Save the layout as an HTML file
    hv.save(layout, plot_file)

    return layout


def main():
    #  https://cityofchicago.linked.data.world/d/chicago-energy-benchmarking/file/chicago-energy-benchmarking-1.csv

    df = get_df()
    print("df:", df.head())
    print("df.columns:", df.columns)
    """
     ['Data Year', 'ID', 'Property Name', 'Address', 'ZIP Code',
       'Community Area', 'Primary Property Type',
       'Gross Floor Area - Buildings (sq ft)', 'Year Built', '# of Buildings',
       'ENERGY STAR Score', 'Electricity Use (kBtu)', 'Natural Gas Use (kBtu)',
       'District Steam Use (kBtu)', 'District Chilled Water Use (kBtu)',
       'All Other Fuel Use (kBtu)', 'Site EUI (kBtu/sq ft)',
       'Source EUI (kBtu/sq ft)', 'Weather Normalized Site EUI (kBtu/sq ft)',
       'Weather Normalized Source EUI (kBtu/sq ft)',
       'Total GHG Emissions (Metric Tons CO2e)',
       'GHG Intensity (kg CO2e/sq ft)', 'Latitude', 'Longitude', 'Location']
    """

    #  df = df.sort_values(by=['Data Year'])
    cols = ["Electricity Use (kBtu)"]
    cols.append("Natural Gas Use (kBtu)")
    cols.append("District Steam Use (kBtu)")
    cols.append("District Chilled Water Use (kBtu)")
    plot_file = "PEC2_ejer3_horizon_graph.html"
    get_horizon_graph(df, cols, plot_file)
    display_img_files([plot_file], xdg_open=True)


if __name__ == "__main__":
    main()
