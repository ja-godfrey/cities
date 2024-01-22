# %%
import plotly.express as px
import pandas as pd

df = pd.read_csv('./../data/derived/final.csv')

# filters
df = df[df['POPESTIMATE2020'] >= 80000]
df = df[df['median_price'] <= 150000]
df = df[df['crime_rate_per_100000'] <= 250]
df = df[df['CTYNAME'] != df['STNAME']]

# Sort df by 'AVG_PCT_CHANGE' in descending order
df_sorted = df.sort_values(by='AVG_PCT_CHANGE_LAST_5_YEARS', ascending=False) # PCT_CHANGE_2020 | AVG_PCT_CHANGE

# Select every 100th row from the sorted dataframe
df_thinned = df_sorted.iloc[::1] # this number is 1 in every x it will display

# Create a new column 'X_Order' for x-axis positions in the thinned dataframe
df_thinned['X_Order'] = range(len(df_thinned))

# Create the bubble chart using the thinned dataframe
fig = px.scatter(
    df_thinned,
    x='X_Order',
    y='AVG_PCT_CHANGE_LAST_5_YEARS', # PCT_CHANGE_2020 | AVG_PCT_CHANGE
    size='POPESTIMATE2020',  # Adjust the size of the bubble based on population
    hover_name='CTYNAME',  # Shows the county name when you hover over a bubble
    hover_data=['POPESTIMATE2020', 'STNAME', 'crime_rate_per_100000', 'median_price'],  # Additional data to show on hover
    title='% Pop Growth by County'
)

# Customize the layout
fig.update_layout(
    xaxis_title='County (Ordered by Average Percent Change)',
    yaxis_title='Average Percent Change (%)',
)

# Update x-axis ticks to show county names
# fig.update_xaxes(tickvals=df_thinned['X_Order'], ticktext=df_thinned['CTYNAME'])

# Show the plot
fig.show()
# %%
