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
        df_words = pd.read_csv('estado_dominios.csv')
    except FileNotFoundError:
        print("Archivo 'estado_dominios.csv' no encontrado, se iniciará el proceso desde el principio.")
        df_words = pd.read_csv("template_norw_words.csv")
        df_words['Words'] = df_words['Words'].str.replace(r'-$', '', regex=True)
        df_words["Words"] = df_words["Words"].str.lower()+".no"

    try:
        with open('ultimo_indice.txt', 'r') as f:
            start_index = int(f.read())
    except FileNotFoundError:
        print("Archivo 'ultimo_indice.txt' no encontrado, se iniciará el proceso desde el principio.")
        start_index = 0

    fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d')

    if fecha_actual not in df_words.columns:
        df_words[fecha_actual] = None

    for i, row in tqdm(df_words.iterrows(), total=df_words.shape[0], initial=start_index):
        if i >= start_index:
            dominio = row['Words']
            try:
                socket.gethostbyname(dominio)
                df_words.at[i, fecha_actual] = 'Ocupado'
            except socket.gaierror:
                df_words.at[i, fecha_actual] = 'Disponible'
            except UnicodeError:
                df_words.at[i, fecha_actual] = 'Error de codificación Unicode'

            with open('ultimo_indice.txt', 'w') as f:
                f.write(str(i))

    df_words.to_csv('estado_dominios.csv', index=False)

    return df_words
