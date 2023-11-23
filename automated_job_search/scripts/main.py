# main.py
from job_fetcher import fetch_jobs
from config import get_env_variable
from job_filter import filter_top_10_jobs

def main():
    try:
        api_key = get_env_variable("REED_API_KEY")
    except ValueError as e:
        print(e)
        exit(1)

    base_url = "https://www.reed.co.uk/api/1.0/search"
    
    keywords = ["data scientist", "data engineer", "data analyst", "machine learning"]
    locations = ["London"]
    distance = 10  # Example distance in miles

    for keyword in keywords:
        for location in locations:
            fetch_jobs(api_key, base_url, keyword, location, distance)

    data_folder = './automated_job_search/data'
    top_10_jobs = filter_top_10_jobs(data_folder, keywords)
    print(top_10_jobs)

if __name__ == "__main__":
    main()
