#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Sales Statistics Dashboard"

# ---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]

# ---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1 Add title to the dashboard
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'color': 'darkblue',
            'textAlign': 'center',
            'fontSize': '36px',
            'fontWeight': 'bold',
            'padding': '20px',
            'backgroundColor': '#f0f0f0',
            'borderRadius': '10px'
        }
    ),  # Include style for title
    
    # TASK 2.2: Add two dropdown menus
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',  # Default value
            placeholder='Select a report type'
        )
    ]),
    
    # Dropdown for selecting a year
    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(i), 'value': i} for i in year_list],
            value=None,  # Initially no value
            placeholder='Select a year'
        )
    ]),
    
    # Output container for displaying graphs
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
    ])
])

# TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output('select-year', 'disabled'),
    [Input('dropdown-statistics', 'value')]
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return False  # Enable the year dropdown
    else: 
        return True  # Disable the year dropdown

# Callback for plotting the graphs based on selected statistics and year
@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'), Input('select-year', 'value')]
)
def update_output_container(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Average Automobile Sales fluctuation over Recession Period (year-wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales Fluctuation Over Recession Period"
            )
        )

        # Plot 2: Average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average No. of Vehicles Sold by Vehicle Type"
            )
        )

        # Plot 3: Pie chart for average expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                names='Vehicle_Type',
                values='Advertising_Expenditure',
                title="Advertising Expenditure Share by Vehicle Type"
            )
        )

        # Plot 4: Effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[R_chart3, R_chart4], style={'display': 'flex'})
        ]

    # TASK 2.6: Yearly Report Statistics
    elif selected_statistics == 'Yearly Statistics' and input_year:
        # Filter data for the selected year
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Yearly Automobile Sales using line chart for the selected year
        yas = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(yas, 
                x='Year', 
                y='Automobile_Sales', 
                title=f"Automobile Sales for the Year {input_year}"
            )
        )

        # Plot 2: Total Monthly Automobile Sales using line chart
        mas = yearly_data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(mas, 
                x='Month', 
                y='Automobile_Sales', 
                title='Total Monthly Automobile Sales'
            )
        )

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(avr_vdata, 
                x='Vehicle_Type', 
                y='Automobile_Sales', 
                title=f'Average Vehicles Sold by Vehicle Type in the Year {input_year}'
            )
        )

        # Plot 4: Total Advertising Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(exp_data,
                names='Vehicle_Type',
                values='Advertising_Expenditure',
                title=f"Total Advertisement Expenditure for Each Vehicle Type in {input_year}"
            )
        )

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4], style={'display': 'flex'})
        ]
    
    else:
        return None

# Run the Dash app
# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)


