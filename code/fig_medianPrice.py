# %%
import json
import pandas as pd
import plotly.express as px

# Load GeoJSON file
with open('./../data/raw/counties.geojson') as f:
    counties = json.load(f)

# Load your DataFrame
df = pd.read_csv('./../data/derived/final.csv')

# Ensure FIPS codes are strings to match the GeoJSON format
df['FIPS_CTY'] = df['FIPS_CTY'].astype(str)

# Create the choropleth map
fig = px.choropleth(df, 
                    geojson=counties, 
                    locations='FIPS_CTY', 
                    color='median_price',
                    color_continuous_scale="Viridis",
                    scope="usa",
                    labels={'median_price':'Median House Price'}
                   )

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

# %%
