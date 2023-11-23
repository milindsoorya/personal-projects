import streamlit as st
import sys
import os

# Add the 'scripts' directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
scripts_dir = os.path.join(parent_dir, 'scripts')
sys.path.append(scripts_dir)

# Now, import your modules
from job_fetcher import fetch_jobs
from job_filter import filter_top_10_jobs
from config import get_env_variable


# # Now, import your modules
# from scripts.job_fetcher import fetch_jobs
# from scripts.job_filter import filter_top_10_jobs
# from scripts.config import get_env_variable

def main():
    st.title("Job Search Dashboard")

    # Sidebar for inputs
    st.sidebar.header("Job Search Parameters")
    keyword = st.sidebar.text_input("Keyword", "Data Scientist")
    location = st.sidebar.text_input("Location", "London")
    distance = st.sidebar.number_input("Distance (miles)", 10, 100, 10)
    
    # Button to fetch jobs
    fetch_data = st.sidebar.button("Fetch Jobs")

    # Button to filter and show top 10 jobs
    filter_data = st.sidebar.button("Show Top 10 Jobs")

    data_folder = './data'

    if fetch_data:
        try:
            api_key = get_env_variable("REED_API_KEY")
            base_url = "https://www.reed.co.uk/api/1.0/search"

            fetch_jobs(api_key, base_url, keyword, location, distance)
            st.success("Data fetched successfully!")

        except Exception as e:
            st.error(f"An error occurred while fetching data: {e}")

    if filter_data:
        try:
            top_jobs = filter_top_10_jobs(data_folder, [keyword])
            st.write(top_jobs)

        except Exception as e:
            st.error(f"An error occurred while filtering data: {e}")

if __name__ == '__main__':
    main()
