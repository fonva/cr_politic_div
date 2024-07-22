import numpy as np
import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

dist_page = requests.get("https://es.wikipedia.org/wiki/Distritos_de_Costa_Rica").text

soup = BeautifulSoup(dist_page, 'html.parser')

print('Classes of each table:')
for table in soup.find_all('table'):
    print(table.get('class'))

tablas = soup.find_all('table')

tabla = soup.find('table', class_='wikitable sortable')

# La tabla contiene encabezado con varias líneas
# vamos directo a la primer fila con datos

#primer_pos = tabla.text.find('San José')
#tabla.text = tabla.text[primer_pos:]

#df_list = {}
#for i in range(0,len(tabla)):
#    rows = tabla.find_all('tr')
#    df_list[i] = rows


df = pd.DataFrame(columns=['Canton','Distrito', 'CodigoPostal', 'Area', 'Poblacion2022','Vinculo'])
#prev_df = pd.DataFrame(columns=['Distrito', 'CodigoPostal', 'Area', 'Poblacion2022'])
# Collecting Ddata
for fila in tabla.tbody.find_all('tr'):
    # Find all data for each column
    columnas = fila.find_all('td')
    n_filas = len(columnas)
    if (columnas != []):
        if n_filas > 8:
            Canton = columnas[n_filas-9].text.strip()
        Distrito = columnas[n_filas-8].text.strip()
        CodigoPostal = columnas[n_filas-7].text.strip()
        Area = columnas[n_filas-6].text.strip()
        Poblacion2022 = columnas[n_filas-5].text.strip()
        vinculo = columnas[n_filas-8].a.attrs.get('href')

        prev_df = pd.DataFrame(data={'Canton':[Canton],
                                     'Distrito': [Distrito],
                                     'CodigoPostal': [CodigoPostal],
                                     'Area': [Area],
                                     'Poblacion2022': [Poblacion2022],
                                     'Vinculo': [vinculo]})
        df = pd.concat([df,prev_df], ignore_index=True )

df.to_excel('lista_distritos.xlsx',engine='xlsxwriter')

#obtener XXXXX m s. n. m. Buscar con regex. Link de cada distrito esta en
#<a class="mw-redirect" href="/wiki/Duacar%C3%AD_(Costa_Rica)"
df['dist_elevacion'] = 'No info'
for i in range(0,len(df.Vinculo)):
    prev_dir = 'http://es.wikipedia.org'+df.Vinculo[i]
    #print(prev_dir)
    prev_dist_pag = requests.get(prev_dir).text
    sopadeliciosa = BeautifulSoup(prev_dist_pag, 'html.parser')
    msnm = sopadeliciosa.find(string='m s. n. m.')
    if msnm is not None:
        msnm = msnm.parent.find_previous().text
        if len(msnm) > 10:
            msnm = str(re.search(r'\d+', msnm).group())
            df.loc[[i],'dist_elevacion'] = msnm

sopadeliciosa.find(string='m s. n. m.').parent.find_previous().text