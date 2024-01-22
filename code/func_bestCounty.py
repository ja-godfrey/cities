# %%
import pandas as pd
from scipy.stats import zscore


df = pd.read_csv('./../data/derived/final.csv')

def find_optimal_counties(df):
    # Ask the user for their criteria
    min_population = int(input("Enter the smallest population size you'll live in: "))
    max_crime_rate = float(input("Enter the highest crime rate you'll tolerate (per 100,000 people): "))
    max_price = int(input("Enter the highest median home price you can afford: "))

    # Filter the dataframe based on the user's criteria
    filtered_df = df[(df['POPESTIMATE2020'] >= min_population) & (df['crime_rate_per_100000'] <= max_crime_rate) & (df['median_price'] <= max_price)]
    filtered_df = filtered_df[filtered_df['CTYNAME'] != filtered_df['STNAME']]
    
    # Calculate z-scores
    filtered_df['zscore_pct_change'] = zscore(filtered_df['AVG_PCT_CHANGE_LAST_5_YEARS'])
    filtered_df['zscore_median_price'] = zscore(filtered_df['median_price'])
    
    # Compute average z-score (note: for median price, we take negative as lower prices are better)
    filtered_df['average_zscore'] = (filtered_df['zscore_pct_change'] - filtered_df['zscore_median_price']) / 2

    # Sort based on average z-score in descending order
    sorted_df = filtered_df.sort_values(by='average_zscore', ascending=False)

    # Select only the specified columns
    selected_columns_df = sorted_df[['CTYNAME', 'STNAME', 'AVG_PCT_CHANGE_LAST_5_YEARS', 'median_price', 'crime_rate_per_100000', 'POPESTIMATE2020', 'average_zscore']]

    # Return the dataframe with selected columns
    return selected_columns_df

# Assuming df is your dataframe with the required columns
optimal_counties_df = find_optimal_counties(df)
optimal_counties_df

# %%