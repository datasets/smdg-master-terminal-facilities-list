import os
import requests
import pandas as pd
import re
import json

from bs4 import BeautifulSoup

file_name = 'smdg-master-terminal-facilities-list'
url = 'https://smdg.org/documents/smdg-code-lists/smdg-terminal-code-list/'
headers = [
            'UNLOCODE',
            'Alternative UNLOCODE',
            'Terminal Code',
            'Terminal Facility Name',
            'Terminal Company Name',
            'Latitude(DMS)',
            'Longitude(DMS)',
            'Last Change',
            'Valid From',
            'Valid Until',
            'Terminal Website',
            'Terminal Address',
            'Remarks'
]
def get_link():
    # Get a tag link from the page
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    link = soup.find_all('a', {'class': 'mtli_attachment'})
    link = link[0].get('href')
    # Extract the date using regex
    date_match = re.search(r'v(\d{8})\.xlsx', link)
    if date_match:
        new_version = date_match.group(1)
        dpfile = 'datapackage.json'
        with open(dpfile, 'r', encoding='utf-8') as f:
            datapackage = json.load(f)

        old_version = datapackage.get('version', 'unknown')
        datapackage['version'] = new_version

        with open(dpfile, 'w', encoding='utf-8') as f:
            json.dump(datapackage, f, indent=2, ensure_ascii=False)

    return link

def retrieve_content(link):
    # Retrieve content from the link
    response = requests.get(link)
    with open(file_name + '.xlsx', 'wb') as f:
        f.write(response.content)

def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal = degrees + minutes / 60 + seconds / 3600
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def convert_dms(dms):
    parts = dms.split(' ')
    direction = parts[0]
    dms_values = parts[1].replace('°', ' ').replace('\'', ' ').replace('\"', '').split()

    degrees = int(dms_values[0])
    minutes = int(dms_values[1])
    seconds = float(dms_values[2])

    return dms_to_decimal(degrees, minutes, seconds, direction)

def transform_csv():
    df = pd.read_excel(file_name + '.xlsx', engine='openpyxl')
    # Skip 6 rows and change the headers

    df = df.iloc[6:]
    df.columns = headers

    # Remove 00:00:00 from the date columns string
    df['Last Change'] = pd.to_datetime(df['Last Change']).dt.date
    df['Valid From'] = pd.to_datetime(df['Valid From']).dt.date
    df['Valid Until'] = pd.to_datetime(df['Valid Until']).dt.date
    df['Longitude(Decimal)'] = round(df['Longitude(DMS)'].apply(convert_dms), 5)
    df['Latitude(Decimal)'] = round(df['Latitude(DMS)'].apply(convert_dms), 5)
    df['Coordinates'] = df['Latitude(Decimal)'].astype(str) + ', ' + df['Longitude(Decimal)'].astype(str)
    df.drop(['Latitude(DMS)', 'Longitude(DMS)', 'Longitude(Decimal)', 'Latitude(Decimal)'], axis=1, inplace=True)
    df.to_csv('data/' + file_name + '.csv', index=False)

def clean_up():
    os.remove(file_name + '.xlsx')

if __name__ == '__main__':
    link = get_link()
    retrieve_content(link)
    transform_csv()
    clean_up()
