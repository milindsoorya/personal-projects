# job_fetcher.py
import requests
import json
from datetime import datetime
import time
from config import get_env_variable
import os

def fetch_jobs(api_key, base_url, keyword, location, distance):
    job_skip = 0
    request_number = 1  # Initialize request counter

    # Ensure the data directory exists
    data_directory = './data'
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    while True:
        params = {
            "keywords": keyword,
            "resultsToTake": 100,
            "resultsToSkip": job_skip,
            "locationName": location,
            "distanceFromLocation": distance
        }
        resp = requests.get(base_url, params=params, auth=(api_key, ""))
        result = json.loads(resp.content)

        num_results = len(result['results'])
        if num_results == 0:
            print(f"No more results for {keyword} in {location} within {distance} miles.")
            break

        print(f"Request #{request_number}: Fetched {num_results} results for '{keyword}' in {location} within {distance} miles. Skipping {job_skip} results.")

        # Save to local file
        today = datetime.now().date()
        file_name = f"./data/job-summary_{today.year}_{today.month}_{today.day}_{keyword.replace(' ', '_')}_{location}_{distance}_{job_skip}.json"
        
        with open(file_name, 'w') as file:
            json.dump(result, file, indent=4)

        job_skip += 100
        request_number += 1  # Increment request counter
        time.sleep(1)
