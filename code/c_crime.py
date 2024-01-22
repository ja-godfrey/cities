# %%
import pandas as pd

df_old = pd.read_csv('./../data/derived/houseprice.csv')
df_new = pd.read_csv('./../data/raw/crime2016.csv')

state_mapping = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 
    'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 
    'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'
}
df_new[['CTYNAME', 'STNAME']] = df_new['county_name'].str.split(', ', expand=True)
df_new['STNAME'] = df_new['STNAME'].map(state_mapping)

df_old.rename(columns={'MunicipalCodeFIPS': 'FIPS_CTY'}, inplace=True)  # Rename the column

merged_df = pd.merge(df_old, df_new[['CTYNAME', 'STNAME', 'crime_rate_per_100000']], on=['CTYNAME', 'STNAME'], how='left')

# clean 
merged_df['crime_rate_per_100000'] = merged_df.groupby('STNAME')['crime_rate_per_100000'].transform(lambda x: x.fillna(x.mean())) # fill unmatched counties with state average
merged_df['crime_rate_per_100000'] = merged_df['crime_rate_per_100000'].round() # Round to the nearest integer
merged_df.dropna(subset=['crime_rate_per_100000'], inplace=True)

merged_df.to_csv('./../data/derived/crime.csv', index=False)
len(merged_df)
# %%

# Find matches
matches = df_old['CTYNAME'].isin(df_new['CTYNAME'])

# Count the number of matches and non-matches
num_matches = matches.sum()
num_non_matches = len(df_old) - num_matches

num_matches, num_non_matches

# %%
