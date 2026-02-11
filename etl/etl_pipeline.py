from trip_cleaning import clean_data
from excluded_logs import split_transactions

# Cleaning data
df = clean_data("etl/raw_data/train.csv")

# Separating the clean from the erroneous data
cleaned_df, excluded_df = split_transactions(df)

cleaned_df.to_csv("etl/processed_data/clean.csv", index=False)
excluded_df.to_csv("etl/processed_data/excluded.csv", index=False)