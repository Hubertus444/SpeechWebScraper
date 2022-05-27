"""
by Hubertus Mitschke created on 05/29/22

Handle the data wrangling process after successfully scraping and saving data
"""
import csv
import pandas as pd

df = pd.read_csv("data/data.csv", header=0, index_col=0)
df = df.transpose()
print(df.head())
print(df)
df.to_csv("data/ecb_speeches.csv")