import os
import glob
import json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime

def filter_top_10_jobs(data_folder, keywords):
    # Find all JSON files in the data folder
    json_files = glob.glob(os.path.join(data_folder, 'job-summary_*.json'))

    # Check if JSON files are found
    if not json_files:
        raise FileNotFoundError(f"No JSON files found in {data_folder}")

    df_list = []

    for file in json_files:
        with open(file, 'r') as f:
            data = json.load(f)
            # Check if 'results' key is in JSON file
            if 'results' in data:
                df = pd.DataFrame(data['results'])
                df_list.append(df)
            else:
                print(f"No 'results' key found in {file}")

    # Check if DataFrame list is empty
    if not df_list:
        raise ValueError("No valid data found in JSON files")

    # Concatenate all dataframes
    combined_df = pd.concat(df_list, ignore_index=True)

    # Filter jobs based on keywords
    combined_df = combined_df[combined_df['jobTitle'].str.contains('|'.join(keywords), case=False, na=False)]

    # Normalize salary and applications
    scaler = MinMaxScaler()
    combined_df[['minimumSalary', 'maximumSalary', 'applications']] = combined_df[['minimumSalary', 'maximumSalary', 'applications']].fillna(0)
    combined_df['averageSalary'] = combined_df[['minimumSalary', 'maximumSalary']].mean(axis=1)
    combined_df[['normalizedSalary', 'normalizedApplications']] = scaler.fit_transform(combined_df[['averageSalary', 'applications']])

    # Convert 'date' to datetime and normalize it
    combined_df['date'] = pd.to_datetime(combined_df['date'], format='%d/%m/%Y')
    combined_df['normalizedDate'] = (datetime.now() - combined_df['date']).dt.days
    combined_df['normalizedDate'] = scaler.fit_transform(combined_df[['normalizedDate']])

    # NLP Analysis of Job Descriptions
    sia = SentimentIntensityAnalyzer()
    combined_df['descriptionScore'] = combined_df['jobDescription'].apply(lambda desc: sia.polarity_scores(desc)['compound'])

    # Define weights for scoring
    salary_weight = 0.4
    applications_weight = 0.3
    date_weight = 0.2
    description_weight = 0.1

    # Calculate composite score
    combined_df['compositeScore'] = (combined_df['normalizedSalary'] * salary_weight) + \
                                    ((1 - combined_df['normalizedApplications']) * applications_weight) + \
                                    ((1 - combined_df['normalizedDate']) * date_weight) + \
                                    (combined_df['descriptionScore'] * description_weight)

    # Sort and select top jobs
    top_jobs = combined_df.sort_values(by='compositeScore', ascending=False)
    top_10_jobs = top_jobs.head(10)

    return top_10_jobs
