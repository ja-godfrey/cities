# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

cols = ['STNAME', 'CTYNAME',  'POPESTIMATE2001', 'POPESTIMATE2002', 'POPESTIMATE2000', 'POPESTIMATE2003', 'POPESTIMATE2004', 'POPESTIMATE2005', 'POPESTIMATE2006', 'POPESTIMATE2007', 'POPESTIMATE2008', 'POPESTIMATE2009', 'POPESTIMATE2010']
encoding = 'ISO-8859-1'
df = pd.read_csv('./../data/raw/co-est2010-alldata.csv', encoding=encoding, usecols=cols)

cols = ['NAME', 'STNAME', 'POPESTIMATE2011',
       'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014',
       'POPESTIMATE2015', 'POPESTIMATE2016', 'POPESTIMATE2017',
       'POPESTIMATE2018', 'POPESTIMATE2019', 'POPESTIMATE2020']
df1 = pd.read_csv('./../data/raw/SUB-EST2020_ALL.csv', encoding=encoding, usecols=cols)

df = pd.merge(df, df1, left_on=['STNAME', 'CTYNAME'], right_on=['STNAME', 'NAME'], how='inner')
df.drop('NAME', axis=1, inplace=True)

# Calculate the average percent change for each row
pct_change_df = df.loc[:, 'POPESTIMATE2000':'POPESTIMATE2020'].pct_change(axis=1) * 100
pct_change_df.columns = [f'PCT_CHANGE_{year}' for year in range(2000, 2021)]
pct_change_df.drop('PCT_CHANGE_2000', axis=1, inplace=True)
df = pd.concat([df, pct_change_df], axis=1)
df['AVG_PCT_CHANGE'] = pct_change_df.mean(axis=1)

#last 5 years avg
selected_years = pct_change_df.loc[:, 'PCT_CHANGE_2016':'PCT_CHANGE_2020']
df['AVG_PCT_CHANGE_LAST_5_YEARS'] = selected_years.mean(axis=1)

# Sort the dataframe by the average percent change in descending order and reset index
df = df.sort_values(by='AVG_PCT_CHANGE', ascending=False).reset_index(drop=True)
df.to_csv('./../data/derived/popgrowth.csv', index=False)

# %%
