# %%
import pandas as pd
import us
df = pd.read_csv('./../data/derived/crime.csv')

def add_fips_column(df):
    """
    Adds a 'fips' column to the DataFrame based on 'STNAME' and 'CTYNAME'.

    Parameters:
    df (pandas.DataFrame): DataFrame with columns 'STNAME' and 'CTYNAME'

    Returns:
    pandas.DataFrame: DataFrame with an additional 'fips' column
    """

    def get_fips(state_name, county_name):
        state = us.states.lookup(state_name)
        if state is None:
            return None
        state_fips = state.fips
        county_fips = None

        for c, fips in us.states.mapping('name', 'fips')[state_fips].items():
            if c.lower() == county_name.lower():
                county_fips = fips
                break

        if county_fips:
            return f'{state_fips}{county_fips}'
        else:
            return None

    df['fips'] = df.apply(lambda row: get_fips(row['STNAME'], row['CTYNAME']), axis=1)
    return df

# Example usage:
# Assume df is your pandas DataFrame with 'STNAME' and 'CTYNAME' columns
# df = pd.DataFrame({'STNAME': ['California', 'Texas'], 'CTYNAME': ['Alameda County', 'Travis County']})
df_with_fips = add_fips_column(df)
# print(df_with_fips)


# %%
