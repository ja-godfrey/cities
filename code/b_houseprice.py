#%%
import pandas as pd
df = pd.read_csv('./../data/raw/houseprice-county.csv')
df_ = pd.read_csv('./../data/derived/popgrowth.csv')

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

df['FullStateName'] = df['StateName'].map(state_mapping)

# Merge df_ with df on the specified conditions
merged_df = pd.merge(df_, df[['RegionName', 'FullStateName', '12/31/2023', 'MunicipalCodeFIPS']], 
                     left_on=['CTYNAME', 'STNAME'], 
                     right_on=['RegionName', 'FullStateName'],
                     how='left')

# clean 
merged_df.drop(['RegionName', 'FullStateName'], axis=1, inplace=True) # drop cols
merged_df['12/31/2023'] = merged_df.groupby('STNAME')['12/31/2023'].transform(lambda x: x.fillna(x.mean())) # fill unmatched counties with state average
merged_df['12/31/2023'] = merged_df['12/31/2023'].round() # Round the '12/31/2023' column to the nearest integer
merged_df.rename(columns={'12/31/2023': 'median_price'}, inplace=True)# Rename the column 
merged_df.dropna(subset=['median_price'], inplace=True)

merged_df.to_csv('./../data/derived/houseprice.csv', index=False)

# %%
# you're losing like 10% of the data here. Here is what you're missing. fix it later, maybe. Uncomment line 29 to find the broken stuff.
unmatched_rows = merged_df[merged_df['12/31/2023'].isna()]
unmatched_rows[['CTYNAME', 'STNAME']]
## %%

# %%
