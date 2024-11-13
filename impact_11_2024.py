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

# print(df.head())
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

# Check for duplicate rows
# duplicate_rows = df[df.duplicated(subset=['First Name'], keep=False)]
# print(f"Duplicate rows found: \n {duplicate_rows}")

# Get the count of duplicate 'First Name' values
# duplicate_count = df['First Name'].duplicated(keep=False).sum()

# Print the count of duplicate 'First Name' values
# print(f"Count of duplicate 'First Name' values: {duplicate_count}")

# Remove duplicate rows based on 'First Name'
df = df.drop_duplicates(subset=['First Name'], keep='first')

# Verify removal of duplicates
# duplicate_count_after_removal = df['First Name'].duplicated(keep=False).sum()
# print(f"Count of duplicate 'First Name' values after removal: {duplicate_count_after_removal}")

# # Merge the "Zip Code" columns if they exist
# if 'Zip Code' in df.columns:
#     zip_code_columns = [col for col in df.columns if col == 'Zip Code']
#     if len(zip_code_columns) > 1:
#         df['Zip Code'] = df[zip_code_columns[0]].combine_first(df[zip_code_columns[1]])
#         # Drop the duplicate "Zip Code" columns, keeping only the merged one
#         df = df.loc[:, ~df.columns.duplicated()]

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

df.to_sql("bmhc_responses_q4_2024", con, if_exists='replace', index=False, method="multi")

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

# # # SQL Query to group ages columns into decades
df_decades = pd.read_sql_query("""
SELECT
  CASE
    WHEN AGE BETWEEN 0 AND 9 THEN '0-9'
    WHEN AGE BETWEEN 10 AND 19 THEN '10-19'
    WHEN AGE BETWEEN 20 AND 29 THEN '20-29'
    WHEN AGE BETWEEN 30 AND 39 THEN '30-39'
    WHEN AGE BETWEEN 40 AND 49 THEN '40-49'
    WHEN AGE BETWEEN 50 AND 59 THEN '50-59'
    WHEN AGE BETWEEN 60 AND 69 THEN '60-69'
    WHEN AGE BETWEEN 70 AND 79 THEN '70-79'
    ELSE '80+'
  END AS Age_Group,
  COUNT(*) AS Patient_Visits
FROM bmhc_responses_q4_2024
GROUP BY Age_Group
ORDER BY MIN(AGE);
""", con)

df_zip = pd.read_sql_query("""
SELECT `Zip Code`,
COUNT(*) AS Residents_In_Zip_Code
FROM bmhc_responses_q4_2024
GROUP BY `Zip Code`;
""", con)

df_zip['Zip Code'] = df_zip['Zip Code'].astype(int)
df_zip['Residents_In_Zip_Code'] = df_zip['Residents_In_Zip_Code'].astype(int)

df_service = pd.read_sql_query("""
SELECT Service,
COUNT(*) AS Count
FROM bmhc_responses_q4_2024
GROUP BY SERVICE;                  
""", con)

df_coverage = pd.read_sql_query("""
SELECT Coverage,
COUNT(*) AS Count
FROM bmhc_responses_q4_2024
GROUP BY Coverage;  
""", con)

df_referral = pd.read_sql_query("""
SELECT `BMHC Referrals`,
COUNT(*) AS Count
FROM bmhc_responses_q4_2024
GROUP BY `BMHC Referrals`;  
""", con)

df_diversion = pd.read_sql_query("""
SELECT Diversion,
COUNT(*) AS Count
FROM bmhc_responses_q4_2024
GROUP BY Diversion;  
""", con)

df_income = pd.read_sql_query("""
SELECT Income,
COUNT(*) AS Count
FROM bmhc_responses_q4_2024
GROUP BY Income;  
""", con)

df_housing = pd.read_sql_query(""" 
SELECT Housing,
COUNT(*) AS Count
FROM bmhc_responses_q4_2024 
GROUP BY Housing;
""", con)

# print(df_housing)

# Pie chart Veteran Status
df_veteran = pd.read_sql_query("""
SELECT Veteran,
COUNT(*) AS COUNT
FROM bmhc_responses_q4_2024
GROUP BY Veteran;
""", con)

df_social = pd.read_sql_query("""
SELECT `Social Services`,
       COUNT(*) AS Count
FROM bmhc_responses_q4_2024
GROUP BY `Social Services`;
""", con)

df_status = pd.read_sql_query("""
SELECT `Status`,
       COUNT(*) AS Count
FROM bmhc_responses_q4_2024
GROUP BY `Status`;
""", con)


df_rating = pd.read_sql_query("""
SELECT `Rating`,
COUNT(*) AS Count
FROM bmhc_responses_q4_2024
WHERE `Rating` != 0
GROUP BY `Rating`;
""", con)

# print(df_rating.head())

con.close()

# ---------------------------- FOLIUM ----------------------------------

m = folium.Map([30.2672, -97.7431], zoom_start=9)

# Add different tile sets

folium.TileLayer('OpenStreetMap', attr='© OpenStreetMap contributors').add_to(m)
folium.TileLayer('Stamen Terrain', attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(m)
folium.TileLayer('Stamen Toner', attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(m)
folium.TileLayer('Stamen Watercolor', attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(m)
folium.TileLayer('CartoDB positron', attr='Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(m)
folium.TileLayer('CartoDB dark_matter', attr='Map tiles by CartoDB, under CC BY 3.0. Data by OpenStreetMap, under ODbL.').add_to(m)

# Available map styles
map_styles = {
    'OpenStreetMap': {
        'tiles': 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
        'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    },
    'Stamen Terrain': {
        'tiles': 'https://stamen-tiles.a.ssl.fastly.net/terrain/{z}/{x}/{y}.jpg',
        'attribution': 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under ODbL.'
    },
    'Stamen Toner': {
        'tiles': 'https://stamen-tiles.a.ssl.fastly.net/toner/{z}/{x}/{y}.png',
        'attribution': 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under ODbL.'
    },
    'Stamen Watercolor': {
        'tiles': 'https://stamen-tiles.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg',
        'attribution': 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under ODbL.'
    },
    'CartoDB positron': {
        'tiles': 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
        'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    },
    'CartoDB dark_matter': {
        'tiles': 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png',
        'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
    },
    'ESRI Imagery': {
        'tiles': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        'attribution': 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
    }
}

# Add tile layers to the map
for style, info in map_styles.items():
    folium.TileLayer(tiles=info['tiles'], attr=info['attribution'], name=style).add_to(m)

# Select a style
# selected_style = 'OpenStreetMap'
# selected_style = 'Stamen Terrain'
# selected_style = 'Stamen Toner'
# selected_style = 'Stamen Watercolor'
selected_style = 'CartoDB positron'
# selected_style = 'CartoDB dark_matter'
# selected_style = 'ESRI Imagery'

# Apply the selected style
if selected_style in map_styles:
    style_info = map_styles[selected_style]
    # print(f"Selected style: {selected_style}")
    folium.TileLayer(
        tiles=style_info['tiles'],
        attr=style_info['attribution'],
        name=selected_style
    ).add_to(m)
else:
    print(f"Selected style '{selected_style}' is not in the map styles dictionary.")
     # Fallback to a default style
    folium.TileLayer('OpenStreetMap').add_to(m)

# Function to get coordinates from zip code
def get_coordinates(zip_code):
    geolocator = Nominatim(user_agent="response_q4_2024.py")
    location = geolocator.geocode({"postalcode": zip_code, "country": "USA"})
    if location:
        return location.latitude, location.longitude
    else:
        print(f"Could not find coordinates for zip code: {zip_code}")
        return None, None

# Apply function to dataframe to get coordinates
df_zip['Latitude'], df_zip['Longitude'] = zip(*df_zip['Zip Code'].apply(get_coordinates))

# Filter out rows with NaN coordinates
df_zip = df_zip.dropna(subset=['Latitude', 'Longitude'])
# print(df_zip.head())
# print(df_zip[['Zip Code', 'Latitude', 'Longitude']].head())
# print(df_zip.isnull().sum())

# instantiate a feature group for the incidents in the dataframe
incidents = folium.map.FeatureGroup()

for index, row in df_zip.iterrows():
    lat, lng = row['Latitude'], row['Longitude']

    if pd.notna(lat) and pd.notna(lng):  
        incidents.add_child(# Check if both latitude and longitude are not NaN
        folium.vector_layers.CircleMarker(
            location=[lat, lng],
            radius=row['Residents_In_Zip_Code'] * 1.2,  # Adjust the multiplication factor to scale the circle size as needed,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.4
        ))

# add pop-up text to each marker on the map
latitudes = list(df_zip['Latitude'])
longitudes = list(df_zip['Longitude'])

# labels = list(df_zip[['Zip Code', 'Residents_In_Zip_Code']])
labels = df_zip.apply(lambda row: f"Zip Code: {row['Zip Code']}, Patients: {row['Residents_In_Zip_Code']}", axis=1)

for lat, lng, label in zip(latitudes, longitudes, labels):
    if pd.notna(lat) and pd.notna(lng):
        folium.Marker([lat, lng], popup=label).add_to(m)
 
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

m.add_child(mouse_position)

# add incidents to map
m.add_child(incidents)

map_path = 'zip_code_map.html'
map_file = os.path.join(script_dir, map_path)
m.save(map_file)
map_html = open(map_file, 'r').read()

# ========================== DataFrame Table ========================== #

df_table = go.Figure(data=[go.Table(
    # columnwidth=[50, 50, 50],  # Adjust the width of the columns
    header=dict(
        values=list(df.columns),
        fill_color='paleturquoise',
        align='left',
        height=30,  # Adjust the height of the header cells
        # line=dict(color='black', width=1),  # Add border to header cells
        font=dict(size=12)  # Adjust font size
    ),
    cells=dict(
        values=[df[col] for col in df.columns],
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
        
        html.H1('BMHC Quarter 4 2024 Report', 
        className='title'),

        html.A(
        'Repo',
        href='https://github.com/CxLos/BMHC_Responses_Q4_2024',
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
html.Div(
    className='row1',
    children=[
        html.Div(
            className='graph1',
            children=[
                dcc.Graph(
                    id='new-patient-bar-chart',
                    figure=go.Figure(
                        data=[
                            go.Bar(
                                x=['Q3', 'Q4'],  # X-axis labels for Q3 and Q4
                                y=[new_patients_count_q3, new_patients_count_q4],  # Y-axis values for each quarter
                                marker=dict(color=['orange', 'blue'])  # Color for each bar
                            )
                        ]
                    ).update_layout(
                        title="New Patients Over Each Quarter",
                        xaxis_title="Quarter",
                        yaxis_title="Number of New Patients",
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    )
                )
            ]
        ),
        html.Div(
            className='graph2',
            children=[
                dcc.Graph(
                    id='service-graph',
                    figure=px.bar(
                        df_status,
                        x='Status',
                        y='Count',
                        color='Status'
                    ).update_layout(
                        title='Eligibility Status',
                        xaxis_title='Service',
                        yaxis_title='Count',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        hovertemplate='<b>Service</b>: %{x}<br><b>Count</b>: %{y}<extra></extra>'
                    )
                )
            ]
        )
    ]
),

# Row 2
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph3',
            children=[
                dcc.Graph(
                    id='age-graph',
                    figure=px.bar(
                        df_decades,
                        x='Age_Group',
                        y='Patient_Visits',
                        color='Age_Group'
                    ).update_layout(
                        title='Patient Visits by Age',
                        xaxis_title='Age',
                        yaxis_title='Number of Visits',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        hovertemplate='<b>Age</b>: %{x}<br><b>Number of Visits</b>: %{y}<extra></extra>'
                    )
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    id='gender-graph',
                    figure=px.pie(
                        df,
                        names='Gender'
                    ).update_layout(
                        title='Patient Visits by Gender',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        textinfo='label+percent',
                        hovertemplate='<b>%{label} Visits</b>: %{value}<extra></extra>'
                    )
                )
            ]
        )
    ]
),

# ROW 3
html.Div(
    className='row1',
    children=[
        html.Div(
            className='graph3',
            children=[
                dcc.Graph(
                    id='race-graph',
                    figure=px.pie(
                        df,
                        names='Race/Ethnicity'
                    ).update_layout(
                        title='Patient Visits by Race',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        hovertemplate='<b>%{label} Visits</b>: %{value}<extra></extra>'
                    )
                )
            ]
        ),
        html.Div(
            className='graph4',
            children=[
                dcc.Graph(
                    id='service-graph',
                    figure=px.bar(
                        df_service,
                        x='Count',
                        y='Service',
                        color='Service'
                    ).update_layout(
                        title='Services Provided',
                        xaxis_title='Service',
                        yaxis_title='Count',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        hovertemplate='<b>Service</b>: %{x}<br><b>Count</b>: %{y}<extra></extra>'
                    )
                )
            ]
        )
    ]
),


# ROW 4
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph1',
            children=[
                dcc.Graph(
                    id='coverage-graph',
                    figure=px.bar(
                        df_coverage,
                        x='Coverage',
                        y='Count',
                        color='Coverage'
                    ).update_layout(
                        title='Patient Coverage',
                        xaxis_title='Coverage',
                        yaxis_title='Count',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        hovertemplate='<b>Coverage</b>: %{x}<br><b>Count</b>: %{y}<extra></extra>'
                    )
                )
            ]
        ),
        html.Div(
            className='graph2',
            children=[
                dcc.Graph(
                    id='referral-graph',
                    figure=px.bar(
                        df_referral,
                        x='Count',
                        y='BMHC Referrals',
                        color='BMHC Referrals'
                    ).update_layout(
                        title='Referrals',
                        xaxis_title='Count',
                        yaxis_title='Name',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        hovertemplate='<b>Service</b>: %{x}<br><b>Count</b>: %{y}<extra></extra>'
                    )
                )
            ]
        )
    ]
),

# ROW 5
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph1',
            children=[
                dcc.Graph(
                    id='social-Services-graph',
                    figure=px.pie(
                        df,
                        names='Social Services'
                    ).update_layout(
                        title='Social Services',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        hovertemplate='<b>%{label}</b>: %{value}<extra></extra>',
                        rotation=90
                    )
                )
            ]
        ),
        html.Div(
            className='graph2',
            children=[
                dcc.Graph(
                    id='income-graph',
                    figure=px.pie(
                        df,
                        names='Income'
                    ).update_layout(
                        title='Income Levels',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        hovertemplate='<b>%{label} Count</b>: %{value}<extra></extra>'
                    )
                )
            ]
        )
    ]
),

# ROW 6
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph1',
            children=[
                dcc.Graph(
                    id='housing-graph',
                    figure=px.pie(
                        df,
                        names='Housing'
                    ).update_layout(
                        title='Housing Status',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        hovertemplate='<b>%{label}</b>: %{value}<extra></extra>',
                        rotation=90
                    )
                )
            ]
        ),
        html.Div(
            className='graph2',
            children=[
                dcc.Graph(
                    id='communication-graph',
                    figure=px.pie(
                        df,
                        names='Communication Type'
                    ).update_layout(
                        title='How did you hear about us?',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        hovertemplate='<b>%{label} Count</b>: %{value}<extra></extra>'
                    )
                )
            ]
        )
    ]
),

# ROW 7
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph1',
            children=[
                dcc.Graph(
                    id='transportation-graph',
                    figure=px.pie(
                        df,
                        names='Transportation'
                    ).update_layout(
                        title='Transportation',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        hovertemplate='<b>%{label}</b>: %{value}<extra></extra>',
                        rotation=90
                    )
                )
            ]
        ),
        html.Div(
            className='graph2',
            children=[
                dcc.Graph(
                    id='Veteran-graph',
                    figure=px.pie(
                        df,
                        names='Veteran'
                    ).update_layout(
                        title='Veteran Status',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        hovertemplate='<b>%{label}</b>: %{value}<extra></extra>',
                        rotation=90
                    )
                )
            ]
        )
    ]
),

# Row 8
html.Div(
    className='row2',
    children=[
        html.Div(
            className='graph1',
            children=[
                dcc.Graph(
                    id='diversion-graph',
                    figure=px.pie(
                        df,
                        names='Diversion'
                    ).update_layout(
                        title='Diversion',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        hovertemplate='<b>%{label}</b>: %{value}<extra></extra>',
                        rotation=90
                    )
                )
            ]
        ),
        html.Div(
            className='graph2',
            children=[
                # Rating graph horizontal bar chart
                dcc.Graph(
                    id='rating-graph',
                    figure=px.bar(
                        df_rating,
                        x='Count',
                        y='Rating',
                        color='Rating',
                        orientation='h',
                        color_discrete_sequence=color_sequence 
                    ).update_layout(
                        title='Ratings',
                        title_x=0.5,
                        font=dict(
                            family='Calibri',
                            size=17,
                            color='black'
                        )
                    ).update_traces(
                        # hovertemplate='<b>%{label}</b>: %{value}<extra></extra>'
                        hovertemplate='<b>Rating</b>: %{y}<br><b>Count</b>: %{x}<extra></extra>'
                    )
                )
            ]
        )
    ]
),

# ROW 9
html.Div(
    className='row3',
    children=[
        html.Div(
            className='graph5',
            children=[
                html.H1(
                    'Number of Visitors by Zip Code', 
                    className='zip'
                ),
                html.Iframe(
                    className='folium',
                    id='folium-map',
                    srcDoc=map_html
                    # style={'border': 'none', 'width': '80%', 'height': '800px'}
                )
            ]
        )
    ]
)
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