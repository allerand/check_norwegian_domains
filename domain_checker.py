# domain_checker.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import unquote
import socket
from tqdm import tqdm
import datetime

def domain_status():
    try:
        df_words = pd.read_csv('domain_status.csv')
    except FileNotFoundError:
        print("File 'domain_status.csv' not found, will start the process from the beginning.")
        df_words = pd.read_csv("template_norw_words.csv")
        df_words['Words'] = df_words['Words'].str.replace(r'-$', '', regex=True)
        df_words['Words'] = df_words['Words'].str.replace(' ', '')
        df_words["Words"] = df_words["Words"].str.lower()+".no"

    try:
        with open('last_index.txt', 'r') as f:
            start_index = int(f.read())
    except FileNotFoundError:
        print("File 'last_index.txt' not found, the process will start from the beginning.")
        start_index = 0

    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    if current_date not in df_words.columns:
        df_words[current_date] = None

    try:
        for i, row in tqdm(df_words.iterrows(), total=df_words.shape[0], initial=0):
            if i >= start_index:
                dominio = row['Words']
                try:
                    socket.gethostbyname(dominio)
                    df_words.at[i, current_date] = 'Not available'
                except socket.gaierror:
                    df_words.at[i, current_date] = 'Available'
                except UnicodeError:
                    df_words.at[i, current_date] = 'Unicode encoding error'

                if i % 1000 == 0:
                    df_words.to_csv('domain_status.csv', index=False)

                with open('last_index.txt', 'w') as f:
                    f.write(str(i))
    except KeyboardInterrupt:
        print(f"\nThe script was interrupted and saved in domain_status.csv. The last processed domain was {dominio} at index {i}.")
        df_words.to_csv('domain_status.csv', index=False)
        return df_words

    df_words.to_csv('domain_status.csv', index=False)

    return df_words