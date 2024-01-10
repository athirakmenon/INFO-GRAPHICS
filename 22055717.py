# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 17:20:45 2024

@author: ak23aai
"""

import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap
import seaborn as sns  # Import Seaborn

# Function to load data
def load_data(file_path):
    return pd.read_csv(file_path)

# Set the size of each visualization
figsize = (12, 10)  # Adjust the size of individual plots
page_size = (2400, 1800)  # Set the size of the combined image

# Create a combined image using PIL
combined_img = Image.new('RGB', page_size, color=(255, 255, 245))
draw = ImageDraw.Draw(combined_img)
font_default = ImageFont.load_default()

# Specify a larger font size for the main heading
font_size_heading = 60  # Adjust the font size here
# Load the font
font_heading = ImageFont.truetype("times.ttf", font_size_heading)

# Function to paste the plot onto the combined image
def paste_plot(file_name, x, y, title, background_color=(255, 255, 245)):
    # Open the image using PIL
    plot_img = Image.open(file_name)

    # Paste the plot onto the combined image
    combined_img.paste(plot_img, (x, y))
    

# Visualization 1: Line Plot of Renewable Energy Consumption Over Time
def visualize_renewable_energy_consumption(df, draw, font):
    world_data = df[df['country'] == 'World']

    # Use Seaborn style
    sns.set(style="whitegrid")

    plt.figure(figsize=figsize)
    sns.lineplot(x='year', y='solar_consumption', label='Solar',\
                 data=world_data, linewidth=2)
    sns.lineplot(x='year', y='wind_consumption', label='Wind',\
                 data=world_data, linewidth=2)
    sns.lineplot(x='year', y='hydro_consumption', label='Hydro',\
                 data=world_data, linewidth=2)
    sns.lineplot(x='year', y='other_renewable_consumption',\
                 label='Other Renewables', data=world_data, linewidth=2)

    plt.xlabel('Year', fontsize=16)
    plt.ylabel('Consumption in Renewable Energy (Replace with your \
               appropriate unit)', fontsize=16)
    plt.title('Consumption of Different Renewable Energy Sources Over\
              Time', fontsize=20, color='brown', weight='bold')
    plt.legend(loc='upper left', fontsize='large')

    # Save the plot as an image file
    plt.savefig('renewable_energy_plot.png', bbox_inches='tight')
    paste_plot('renewable_energy_plot.png',50, 200,\
               "Renewable Energy Consumption Over Time")
# Visualization 2: Grouped Bar Chart of Hydro Electricity Production in Selected Continents (1970 and 2022)


# Visualization 2: Grouped Bar Chart of Hydro Electricity Production in Selected Continents (1970 and 2022)
def visualize_hydro_electricity_production(df, draw, font):
    bar_width = 0.35
    selected_continents = ['Africa', 'Australia', 'North America', \
                           'South America', 'Asia', 'Europe']

    selected_years_data = df[(df['country'].isin(selected_continents))\
                             & ((df['year'] == 1970) | (df['year'] == 2022))]

    years = [1970, 2022]
    x_positions = np.arange(len(selected_continents))

    colors_bar = ['gold', 'olive']  # You can customize the colors here

    plt.figure(figsize=figsize)
    for i, year in enumerate(years):
        year_data = selected_years_data[selected_years_data['year'] == year]
        plt.bar(x_positions + (i * bar_width),\
                year_data['hydro_electricity'], label=str(year), width=bar_width, color=colors_bar[i],edgecolor='black')

    plt.xlabel('Continent', fontsize=16)
    plt.ylabel('Hydro electricity', fontsize=16)
    plt.title('Hydro electricity production \in Selected Continents\
              (1970 and 2022)', fontsize=20, color='brown', weight='bold')
    plt.legend(title='Year',fontsize='large')
    plt.xticks(x_positions + bar_width / 2, selected_continents)

    # Save the plot as an image file
    plt.savefig('hydro_electricity_plot.png', bbox_inches='tight')
    paste_plot('hydro_electricity_plot.png', 1570, 200,\
               "Hydro Electricity Production Over Time")



# Visualization 3: Pie Chart of Energy Sources Distribution in Australia (2022)
def visualize_electricity_sources_distribution(df, draw, font):
    australia_2022 = df[(df['country'] == 'Australia') & (df['year'] == 2022)]

    all_sources = [
        'hydro_electricity', 'wind_electricity', \
            'other_renewable_electricity', 'solar_electricity', 'biofuel_electricity',
        'coal_electricity', 'oil_electricity', 'gas_electricity', \
            'nuclear_electricity', 'fossil_electricity'
    ]

    # Use Seaborn style
    sns.set(style="whitegrid")

    plt.figure(figsize=figsize)
    australia_2022[all_sources] = australia_2022[all_sources].fillna(0)

    explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    plt.pie(australia_2022[all_sources].values.flatten(), \
            labels=all_sources, autopct='%1.1f%%', startangle=140,
            explode=explode, wedgeprops={'edgecolor': 'black', \
                                         'width': 0.5, 'linewidth': 2.5},
            textprops={'fontsize': 13})
    plt.gca().add_artist(plt.Circle((0, 0), 0.6, fc='white'))
    plt.title('Electricity Sources Distribution in Australia (2022)',\
              fontsize=20, color='brown', weight='bold')

    # Save the plot as an image file
    plt.savefig('electricity_distribution_plot.png', bbox_inches='tight')
    # Move to the right side
    paste_plot('electricity_distribution_plot.png', 50, 1000, \
               "Electricity Sources Distribution in Australia (2022)")

# Visualization 4: Line Chart of Carbon Intensity of Electricity for Selected Continents Over Time
def visualize_carbon_intensity_over_time(df, draw, font):
    selected_continents = ['Africa', 'Australia', 'North America', \
                           'South America', 'Asia', 'Europe']
    selected_continents_data = df[df['country'].isin(selected_continents)]

    pivot_data = selected_continents_data.pivot(index='year',\
                                                columns='country', values='carbon_intensity_elec')

    # Use Seaborn style
    sns.set(style="whitegrid")

    plt.figure(figsize=figsize)

    for i, continent in enumerate(pivot_data.columns):
        sns.lineplot(x=pivot_data.index, \
                     y=pivot_data[continent], label=continent, linewidth=2)

    plt.xlabel('Year', fontsize=16)
    plt.ylabel('Carbon Intensity of Electricity', fontsize=16)
    plt.title('Carbon Intensity of Electricity for Selected Continents Over\
              Time', fontsize=20, color='brown', weight='bold')

    plt.legend(loc='upper right', fontsize='large')

    # Save the plot as an image file
    plt.savefig('carbon_intensity_plot.png', bbox_inches='tight')
    # Move to the right side
    paste_plot('carbon_intensity_plot.png', 1570, 1000,\
               "Carbon Intensity Over Time")

# Load data
file_path = "World Energy Consumption.csv"
df = load_data(file_path)

# Visualizations
visualize_renewable_energy_consumption(df, draw, font_heading)
visualize_hydro_electricity_production(df, draw, font_heading)
visualize_electricity_sources_distribution(df, draw, font_heading)
visualize_carbon_intensity_over_time(df, draw, font_heading)

# Add main heading
main_heading = "ANALYZING AUSTRALIA'S ENERGY PROFILE"
heading_width, heading_height = font_heading.getsize(main_heading)
heading_position = ((page_size[0] - heading_width) // 2, 50)  # Centered at the top
draw.text(heading_position, main_heading, font=font_heading, fill=(101, 67, 33))

# Add textbox at the center
textbox_width = 400  # Adjust the width as needed
textbox_height = 800
textbox_position = ((combined_img.width - textbox_width) // 2.25,\
                    (combined_img.height - textbox_height) // 5.5)
draw.rectangle([textbox_position, \
                (textbox_position[0] + textbox_width, textbox_position[1] + textbox_height)],
               fill=(255, 255, 245))

# Wrap the text and draw it inside the textbox
textbox_text = """ The initial line graph on global energy\
    consumption reveals a persistent and positive trend in \
    hydro consumption. Notably, hydro remains consistently\
    high worldwide, signifying its enduring importance in the energy landscape.
    The subsequent grouped bar chart comparing hydro electricity\
    production across continents places Australia in the spotlight.\
    The significant increase in hydroelectricity production\
    from 1970 to 2022 positions Australia as a major player\
    in harnessing hydroelectric power.
    The pie chart for Australia's 2022 energy distribution reflects a \
    heavy reliance on fossil fuels, particularly coal, oil, and gas. \
    In contrast, hydro power makes up a relatively small share. \
    This distribution signals the importance of shifting\
    owards more sustainable and renewable energy sources.
    Analyzing the carbon intensity graph from 2000 to 2022 reinforces\
   the fact that Australia has been a significant contributor to \
   carbon emissions in electricity generation. This highlights the\
   critical need for the country to expedite its transition to cleaner\
   and greener energy alternatives, addressing environmental concerns and\
   fostering a more sustainable energy
"""
textbox_font = ImageFont.truetype("times.ttf", 30)
wrapped_text = textwrap.fill(textbox_text, width=55)  # Adjust width as needed
# Adjust the line spacing between sentences in the text box
line_spacing = 40  # Adjust the value as needed

draw.multiline_text((textbox_position[0] + 0.01, textbox_position[1] + 40),
                    wrapped_text, font=textbox_font, fill='#000000',\
                        align='left', spacing=line_spacing)

signature_text = "Name: ATHIRA KUMAR MENON\nStudent ID: 22055717"
signature_font = ImageFont.truetype("times.ttf", 20)
signature_position = (50, page_size[1] - 150)  # Adjust position as needed

draw.multiline_text(signature_position, signature_text,\
                    font=signature_font, fill='#000000', align='left')

combined_img.save('22055717.png')

