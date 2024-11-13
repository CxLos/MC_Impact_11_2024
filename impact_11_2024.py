# =================================== IMPORTS ================================= #
import csv, sqlite3
import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.figure_factory as ff
import plotly.graph_objects as go
from geopy.geocoders import Nominatim
from folium.plugins import MousePosition
import plotly.express as px
import datetime
import folium
import os
import sys
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.development.base_component import Component
# 'data/~$bmhc_data_2024_cleaned.xlsx'
# print('System Version:', sys.version)
# -------------------------------------- DATA ------------------------------------------- #

current_dir = os.getcwd()
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path1 = 'data/BMHC_Navigation_Outreach.xlsx'
data_path2 = 'data/BMHC_MarCom_Impact_Report.xlsx'
file_path1 = os.path.join(script_dir, data_path1)
file_path2 = os.path.join(script_dir, data_path2)

# Sheet Names
responses = 'Responses'
marcom = 'MarCom'

# Read data from excel file
data_r = pd.read_excel(file_path1, sheet_name=responses)
data_r2 = pd.read_excel(file_path2, sheet_name=responses)
data_m = pd.read_excel(file_path2, sheet_name=marcom)

df_r = data_r2.copy()
df_m = data_m.copy()

# Concatenate dataframes
# df = pd.concat([data1, data2], ignore_index=True)

# Trim leading and trailing whitespaces from column names
df_r.columns = df_r.columns.str.strip()
df_m.columns = df_m.columns.str.strip()

# Define a discrete color sequence
color_sequence = px.colors.qualitative.Plotly

print(df_m.head())
# print('Total entries: ', len(df))
# print('Column Names: \n', df.columns)
# print('DF Shape:', df.shape)
# print('Dtypes: \n', df.dtypes)
# print('Info:', df.info())
# print("Amount of duplicate rows:", df.duplicated().sum())

# print('Current Directory:', current_dir)
# print('Script Directory:', script_dir)
# print('Path to data:',file_path)

# ================================= Columns ================================= #



# ------------------------------- Missing Values ----------------------------------- #

# missing = df.isnull().sum()
# print('Columns with missing values before fillna: \n', missing[missing > 0])


# ============================== Data Preprocessing ========================== #

# Check for duplicate columns
# duplicate_columns = df.columns[df.columns.duplicated()].tolist()
# print(f"Duplicate columns found: {duplicate_columns}")
# if duplicate_columns:
#     print(f"Duplicate columns found: {duplicate_columns}")

# Fill Missing Values
# df['screener_id'] = df['screener_id'].fillna("N/A")
# df['referral_id'] = df['referral_id'].fillna("N/A")
# # df['created_at'] = df['created_at'].fillna("N/A")
# df['site'] = df['site'].fillna('google forms')
# # df['Timestamp'] = df['Timestamp'].interpolate()
# df['Last Name'] = df['Last Name'].fillna('N/A')
# df['Gender'] = df['Gender'].fillna('N/A')
# df['Age'] = df['Age'].fillna(0)
# df['Physical Appointment'] = df['Physical Appointment'].fillna('N/A')
# df['Coverage'] = df['Coverage'].fillna('N/A')
# df['Status'] = df['Status'].fillna('N/A')
# df['Service'] = df['Service'].fillna('N/A')
# df['Housing'] = df['Housing'].fillna('N/A')
# df['Income'] = df['Income'].fillna('N/A')
# df['BMHC Referrals'] = df['BMHC Referrals'].fillna('N/A')
# df['Mental Health'] = df['Mental Health'].fillna('N/A')
# df['Transportation'] = df['Transportation'].fillna('N/A')
# df['Diversion'] = df['Diversion'].fillna('N/A')
# df['Communication Type'] = df['Communication Type'].fillna('N/A')
# df['Race/Ethnicity'] = df['Race/Ethnicity'].fillna('N/A')
# df['Social Services'] = df['Social Services'].fillna('N/A')
# df['Rating'] =df['Rating'].fillna(0)
# df['Rating'] = df['Rating'].astype('Int64')
# df['Completed Survey'] =df['Completed Survey'].fillna('N/A')
# df['Veteran'] = df['Veteran'].fillna('N/A')
# df['Services Not Completed'] =df['Services Not Completed'].fillna('N/A')
# df['Reason for No Show'] =df['Reason for No Show'].fillna('N/A')
# df['Zip Code'].fillna(df['Zip Code'].mode()[0], inplace=True)
# df['Zip Code'] = df['Zip Code'].astype('Int64')
# df['Zip Code'] = df['Zip Code'].replace(-1, df['Zip Code'].mode()[0])

# print(df.dtypes)

# income_mode = df['Income'].mode()
# print('Income Mode:', income_mode)

# missing = df.isnull().sum()
# print('Columns with missing values after fillna: \n', missing[missing>0])

# value counts for 'Rating' column
# rating_counts = df['Rating'].value_counts()
# print('Rating Counts:\n', rating_counts)

# -----------------------------------------------------------------------------

# Get the distinct values in column

# distinct_service = df['What service did/did not complete?'].unique()
# print('Distinct:\n', distinct_service)

# ------------------------------------ SQL ---------------------------------------

# Connect to SQL
con = sqlite3.connect("bmhc_2024.db")
cur = con.cursor()

df_m.to_sql("bmhc_responses_q4_2024", con, if_exists='replace', index=False, method="multi")

# # Show list of all tables in db.
# # tables = pd.read_sql_query("""
# #   SELECT name 
# #   FROM sqlite_master 
# #   WHERE type = 'table';
# # """, con)
# # print("Tables in the database:\n", tables)

# # # Check if data is inserted correctly
# # df_check = pd.read_sql_query("SELECT * FROM bmhc_responses_q3_2024 LIMIT 5;", con)
# # print(df_check)

con.close()

# ========================== DataFrame Table ========================== #

df_table = go.Figure(data=[go.Table(
    # columnwidth=[50, 50, 50],  # Adjust the width of the columns
    header=dict(
        values=list(df_m.columns),
        fill_color='paleturquoise',
        align='left',
        height=30,  # Adjust the height of the header cells
        # line=dict(color='black', width=1),  # Add border to header cells
        font=dict(size=12)  # Adjust font size
    ),
    cells=dict(
        values=[df_m[col] for col in df_m.columns],
        fill_color='lavender',
        align='left',
        height=25,  # Adjust the height of the cells
        # line=dict(color='black', width=1),  # Add border to cells
        font=dict(size=12)  # Adjust font size
    )
)])

df_table.update_layout(
    margin=dict(l=50, r=50, t=30, b=40),  # Remove margins
    height=400,
    # width=1500,  # Set a smaller width to make columns thinner
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
    plot_bgcolor='rgba(0,0,0,0)'  # Transparent plot area
)

# print(df.head())

# ----------------------------------- DASHBOARD -----------------------------------

app = dash.Dash(__name__)
server= app.server

app.layout = html.Div(children=[ 

    html.Div(className='divv', children=[ 
        
        html.H1('BMHC MarCom November 2024 Report', 
        className='title'),

        html.A(
        'Repo',
        href='https://github.com/CxLos/MC_Impact_11_2024',
        className='btn')
    ]),    

# Data Table
html.Div(
    className='row0',
    children=[
        html.Div(
            className='table',
            children=[
                html.H1(
                    className='table-title',
                    children='Data Table'
                )
            ]
        ),
        html.Div(
            className='table2', 
            children=[
                dcc.Graph(
                    className='data',
                    figure=df_table
                )
            ]
        )
    ]
),

# ROW 1
# html.Div(
#     className='row1',
#     children=[
#         html.Div(
#             className='graph1',
#             children=[
#                 dcc.Graph(
#                     id='new-patient-bar-chart',
#                     figure=go.Figure(
#                         data=[
#                             go.Bar(
#                                 x=['Q3', 'Q4'],  # X-axis labels for Q3 and Q4
#                                 y=[new_patients_count_q3, new_patients_count_q4],  # Y-axis values for each quarter
#                                 marker=dict(color=['orange', 'blue'])  # Color for each bar
#                             )
#                         ]
#                     ).update_layout(
#                         title="New Patients Over Each Quarter",
#                         xaxis_title="Quarter",
#                         yaxis_title="Number of New Patients",
#                         title_x=0.5,
#                         font=dict(
#                             family='Calibri',
#                             size=17,
#                             color='black'
#                         )
#                     )
#                 )
#             ]
#         ),
#         html.Div(
#             className='graph2',
#             children=[
#                 dcc.Graph(
#                     id='service-graph',
#                     figure=px.bar(
#                         df_status,
#                         x='Status',
#                         y='Count',
#                         color='Status'
#                     ).update_layout(
#                         title='Eligibility Status',
#                         xaxis_title='Service',
#                         yaxis_title='Count',
#                         title_x=0.5,
#                         font=dict(
#                             family='Calibri',
#                             size=17,
#                             color='black'
#                         )
#                     ).update_traces(
#                         hovertemplate='<b>Service</b>: %{x}<br><b>Count</b>: %{y}<extra></extra>'
#                     )
#                 )
#             ]
#         )
#     ]
# ),


])

# Callback function
# @app.callback(
#     Output('', 'figure'),
#     [Input('', 'value')]
# )

if __name__ == '__main__':
    app.run_server(debug=
                   True)
                #    False)
# ----------------------------------------------- Updated Database ----------------------------------------

# updated_path = 'data/bmhc_q4_2024_cleaned.xlsx'
# data_path = os.path.join(script_dir, updated_path)
# df.to_excel(data_path, index=False)
# print(f"DataFrame saved to {data_path}")

# updated_path1 = 'data/service_tracker_q4_2024_cleaned.csv'
# data_path1 = os.path.join(script_dir, updated_path1)
# df.to_csv(data_path1, index=False)
# print(f"DataFrame saved to {data_path1}")

# -------------------------------------------- KILL PORT ---------------------------------------------------

# netstat -ano | findstr :8050
# taskkill /PID 24772 /F
# npx kill-port 8050

# ---------------------------------------------- Host Application -------------------------------------------

# 1. pip freeze > requirements.txt
# 2. add this to procfile: 'web: gunicorn impact_11_2024:server'
# 3. heroku login
# 4. heroku create
# 5. git push heroku main

# Create venv 
# virtualenv venv 
# source venv/bin/activate # uses the virtualenv

# Update PIP Setup Tools:
# pip install --upgrade pip setuptools

# Install all dependencies in the requirements file:
# pip install -r requirements.txt

# Check dependency tree:
# pipdeptree
# pip show package-name

# Remove
# pypiwin32
# pywin32
# jupytercore

# ----------------------------------------------------

# Heroku Setup:
# heroku login
# heroku create impact_11_2024
# heroku git:remote -a impact_11_2024
# git push heroku main

# Clear Heroku Cache:
# heroku plugins:install heroku-repo
# heroku repo:purge_cache -a impact_11_2024

# Set buildpack for heroku
# heroku buildpacks:set heroku/python

# Heatmap Colorscale colors -----------------------------------------------------------------------------

#   ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
            #  'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
            #  'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
            #  'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
            #  'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
            #  'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
            #  'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
            #  'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
            #  'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
            #  'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
            #  'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
            #  'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
            #  'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
            #  'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
            #  'ylorrd'].

# rm -rf ~$bmhc_data_2024_cleaned.xlsx
# rm -rf ~$bmhc_data_2024.xlsx
# rm -rf ~$bmhc_q4_2024_cleaned2.xlsx