# %%
import pandas as pd
from scipy.stats import zscore


df = pd.read_csv('./../data/derived/final.csv')

def find_optimal_counties(df, included_states=None, excluded_states=[]):
    # Ask the user for their criteria
    min_population = int(input("Enter the smallest population size you'll live in: "))
    max_crime_rate = float(input("Enter the highest crime rate you'll tolerate (per 100,000 people): "))
    max_price = int(input("Enter the highest median home price you can afford: "))

    # Determine states to include or exclude in the filter
    if included_states is not None:
        filtered_df = df[df['STNAME'].isin(included_states)]
    else:
        filtered_df = df[~df['STNAME'].isin(excluded_states)]

    # Further filter the dataframe based on the user's criteria
    filtered_df = filtered_df[(filtered_df['POPESTIMATE2020'] >= min_population) & 
                              (filtered_df['crime_rate_per_100000'] <= max_crime_rate) & 
                              (filtered_df['median_price'] <= max_price)]
    filtered_df = filtered_df[filtered_df['CTYNAME'] != filtered_df['STNAME']]
    sorted_df = filtered_df.sort_values(by='AVG_PCT_CHANGE_LAST_5_YEARS', ascending=False)
    selected_columns_df = sorted_df[['CTYNAME', 'STNAME', 'AVG_PCT_CHANGE_LAST_5_YEARS', 'median_price', 'crime_rate_per_100000', 'POPESTIMATE2020']]
    return selected_columns_df

# Example usage
included_states = ['Arizona', 'California', 'New Mexico', 'Oregon', 'Washington', 'Utah', 'Virginia', 'South Carolina', 'North Carolina', ] 
excluded_states = ['Texas', 'Florida']
optimal_counties_df = find_optimal_counties(df, included_states=included_states, excluded_states=excluded_states)
optimal_counties_df[['CTYNAME', 'STNAME', 'AVG_PCT_CHANGE_LAST_5_YEARS', 'median_price', 'POPESTIMATE2020']][:10]


# %%
