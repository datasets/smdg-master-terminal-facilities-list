import os
import requests
import pandas as pd

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
    return link

def retrieve_content(link):
    # Retrieve content from the link
    response = requests.get(link)
    with open(file_name + '.xlsx', 'wb') as f:
        f.write(response.content)

def transform_csv():
    df = pd.read_excel(file_name + '.xlsx', engine='openpyxl')
    # Skip 6 rows and change the headers

    df = df.iloc[6:]
    df.columns = headers

    # Remove 00:00:00 from the date columns string
    df['Last Change'] = pd.to_datetime(df['Last Change']).dt.date
    df['Valid From'] = pd.to_datetime(df['Valid From']).dt.date
    df['Valid Until'] = pd.to_datetime(df['Valid Until']).dt.date

    df.to_csv('data/' + file_name + '.csv', index=False)

def clean_up():
    os.remove(file_name + '.xlsx')

if __name__ == '__main__':
    link = get_link()
    retrieve_content(link)
    transform_csv()
    clean_up()