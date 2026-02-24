import os
import requests
import pandas as pd
import json
import re
from datetime import datetime

# File name
file_name = 'smdg-master-terminal-facilities-list'

# GitHub URLs
github_raw_url = 'https://raw.githubusercontent.com/smdg-org/Terminal-Code-List/master/SMDG%20Terminal%20Code%20List.csv'
github_api_url = 'https://api.github.com/repos/smdg-org/Terminal-Code-List/commits?path=SMDG%20Terminal%20Code%20List.csv&per_page=1'

# Headers for the new CSV format from GitHub
new_headers = [
    'UNLOCODE',
    'Alternative UNLOCODE',
    'Terminal Code',
    'Terminal Facility Name',
    'Terminal Company Name',
    'Latitude (DMS)',
    'Longitude (DMS)',
    'Latitude',
    'Longitude',
    'Last change',
    'Valid from',
    'Valid to',
    'Terminal Website',
    'Terminal Address',
    'Remarks'
]

def get_latest_commit_date():
    """Get the latest commit date from GitHub API"""
    try:
        response = requests.get(github_api_url)
        if response.status_code == 200:
            data = response.json()
            if data:
                commit_date = data[0]['commit']['committer']['date']
                return commit_date[:10]  # Return only YYYY-MM-DD
    except Exception as e:
        print(f"Error fetching GitHub data: {e}")
    return None

def check_for_updates():
    """Check if there is an update on GitHub"""
    commit_date = get_latest_commit_date()
    if not commit_date:
        print("Could not check for updates from GitHub")
        return None, None

    # Read current datapackage.json
    dpfile = 'datapackage.json'
    try:
        with open(dpfile, 'r', encoding='utf-8') as f:
            datapackage = json.load(f)

        current_version = datapackage.get('version', '')

        # Convert commit date to version format (YYYYMMDD)
        version_date = commit_date.replace('-', '')

        # If versions match, no update needed
        if current_version == version_date:
            print(f"No update available. Current version: {current_version}, GitHub version: {version_date}")
            return None, None

        print(f"Update available! Current version: {current_version}, New version: {version_date}")
        return commit_date, version_date
    except Exception as e:
        print(f"Error reading datapackage.json: {e}")
        return commit_date, commit_date.replace('-', '')

def download_csv():
    """Download the CSV file from GitHub"""
    print(f"Downloading CSV from GitHub...")
    response = requests.get(github_raw_url)
    if response.status_code == 200:
        # Save to temporary file
        temp_file = file_name + '_temp.csv'
        with open(temp_file, 'wb') as f:
            f.write(response.content)
        print(f"CSV downloaded successfully")
        return temp_file
    else:
        print(f"Failed to download CSV. Status code: {response.status_code}")
        return None

def process_csv(input_file, output_file):
    """Process the CSV file and rename columns"""
    print(f"Processing CSV file...")

    # Read the CSV
    df = pd.read_csv(input_file, encoding='utf-8')

    # Rename columns to match the expected format
    column_mapping = {
        'Last change': 'Last Change',
        'Valid from': 'Valid From',
        'Valid to': 'Valid Until'
    }

    df = df.rename(columns=column_mapping)

    # Add Coordinates column by combining Latitude and Longitude
    df['Coordinates'] = df['Latitude'].astype(str) + ', ' + df['Longitude'].astype(str)

    # Remove the Latitude and Longitude columns (keep only Coordinates)
    df.drop(['Latitude (DMS)', 'Longitude (DMS)', 'Latitude', 'Longitude'], axis=1, inplace=True)

    # Save to output file
    df.to_csv(output_file, index=False)
    print(f"CSV processed and saved to {output_file}")

    # Get the latest date from the CSV for version update
    latest_date = None
    if 'Last Change' in df.columns:
        dates = df['Last Change'].dropna()
        if not dates.empty:
            latest_date = pd.to_datetime(dates).max().strftime('%Y-%m-%d')
    elif 'Valid From' in df.columns:
        dates = df['Valid From'].dropna()
        if not dates.empty:
            latest_date = pd.to_datetime(dates).max().strftime('%Y-%m-%d')

    return latest_date

def update_datapackage(version_date, csv_date):
    """Update the datapackage.json with new version"""
    dpfile = 'datapackage.json'

    try:
        with open(dpfile, 'r', encoding='utf-8') as f:
            datapackage = json.load(f)

        # Update version
        if version_date:
            datapackage['version'] = version_date

        # Update schema fields (without Latitude/Longitude columns)
        if 'resources' in datapackage and len(datapackage['resources']) > 0:
            schema = datapackage['resources'][0]['schema']
            schema['fields'] = [
                {
                    "name": "UNLOCODE",
                    "description": "Main location UN/LOCODE. In an UN/EDIFACT message, use in a LOC segment, element C517.3225",
                    "type": "string"
                },
                {
                    "name": "Alternative UNLOCODE",
                    "type": "string"
                },
                {
                    "name": "Terminal Code",
                    "description": "In an UN/EDIFACT message, use in a LOC segment, element C519.3223",
                    "type": "string"
                },
                {
                    "name": "Terminal Facility Name",
                    "type": "string"
                },
                {
                    "name": "Terminal Company Name",
                    "type": "string"
                },
                {
                    "name": "Last Change",
                    "description": "Last change of this entry",
                    "type": "date"
                },
                {
                    "name": "Valid From",
                    "description": "Entry is valid from this date",
                    "type": "date"
                },
                {
                    "name": "Valid Until",
                    "description": "Entry is valid till this date",
                    "type": "date"
                },
                {
                    "name": "Terminal Website",
                    "type": "string"
                },
                {
                    "name": "Terminal Address",
                    "type": "string"
                },
                {
                    "name": "Remarks",
                    "type": "string"
                },
                {
                    "name": "Coordinates",
                    "type": "string"
                }
            ]

        # Write updated datapackage
        with open(dpfile, 'w', encoding='utf-8') as f:
            json.dump(datapackage, f, indent=2, ensure_ascii=False)

        print(f"datapackage.json updated with version {version_date}")

    except Exception as e:
        print(f"Error updating datapackage.json: {e}")

def clean_up(temp_file):
    """Clean up temporary files"""
    if temp_file and os.path.exists(temp_file):
        os.remove(temp_file)

def main():
    print("=== SMDG Terminal Code List Update Workflow ===")

    # Step 1: Check for updates on GitHub
    commit_date, version_date = check_for_updates()

    if not version_date:
        print("No updates available or error checking for updates.")
        return

    # Step 2: Download CSV from GitHub
    temp_file = download_csv()
    if not temp_file:
        print("Failed to download CSV. Exiting.")
        return

    try:
        # Step 3: Process the CSV
        output_file = f'data/{file_name}.csv'
        csv_date = process_csv(temp_file, output_file)

        # Step 4: Update datapackage.json
        update_datapackage(version_date, csv_date)

        print("\n=== Update completed successfully! ===")
        print(f"New version: {version_date}")
        print(f"CSV file: {output_file}")

    finally:
        # Step 5: Clean up
        clean_up(temp_file)

if __name__ == '__main__':
    main()
