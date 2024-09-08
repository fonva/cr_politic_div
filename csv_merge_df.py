import pandas as pd

# check encoding of file in terminal
# file -I /Users/[username]/Documents/mapa_cr/poblacion_vivienda_distrito.csv

pob_file_path = '/Users/ronnyfonsecavargas/Documents/_mapa_cr/poblacion_vivienda_distrito2.csv'
df_pob = pd.read_csv(pob_file_path,sep=';',decimal=',',thousands='.')
print(df_pob.head(3))
df_pob