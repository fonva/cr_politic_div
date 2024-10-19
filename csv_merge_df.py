import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


# check encoding of file in terminal
# file -I /Users/[username]/Documents/mapa_cr/poblacion_vivienda_distrito.csv

pob_file_path = '/Users/ronnyfonsecavargas/Documents/_mapa_cr/poblacion_vivienda_distrito2.csv'
caren_file_path = '/Users/ronnyfonsecavargas/Documents/_mapa_cr/carencias_distrito.csv'
df_pob = pd.read_csv(pob_file_path,sep=';',decimal=',',thousands='.')
df_caren = pd.read_csv(caren_file_path,sep=';',decimal=',',thousands=' ', encoding='cp1252')

df_caren.columns = ['codigo', 'distrito', 'poblacion_una_carencia',
       'p_hog_unaomas_carencia','p_hog_una_carencia','p_hog_dosomas_carencia',
       'p_hog_carencia_albergue','p_hog_carencia_salud']
df_caren.drop(columns=['distrito'],inplace=True)

df_pob.drop(columns=['prov', 'num_prov', 'cant', 'num_cant', 'dist', 'num_dist'],inplace=True)
df_pob.columns = ['codigo','area', 'densidad_poblacion', 'crecimiento_poblacion',
       'crecimiento_vivienda', 'relacion_hombre_mujer', 'hombres',
       'mujeres', 'vivienda_ocupada', 'vivienda_desocupada',
       'promedio_ocupantes']

df = df_pob.merge(df_caren, on = 'codigo', how='outer')

df['crecimiento_poblacion'] = pd.to_numeric(df.crecimiento_poblacion.str.replace(',','.'), errors='coerce')
df['crecimiento_vivienda'] = pd.to_numeric(df.crecimiento_vivienda.str.replace(',','.'), errors='coerce')

webscrap_df = pd.read_csv('./lista_distritos.csv')
webscrap_df = webscrap_df[['codigo', 'Area', 'Poblacion2022', 'dist_elevacion']]


df = df.merge(webscrap_df,on='codigo',how='left')
df.set_index('codigo',inplace=True)

nulls_df = df[df.isna().any(axis=1)]
df = df[~df.isna().any(axis=1)]

# Standardize Dataframe
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)

# PCA
pca = PCA(n_components=2)  # Reduce to 2 principal components
principal_components = pca.fit_transform(scaled_data)

# DataFrame with the principal components
pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])

pca_df = pca_df.assign(
    prov = df.index.astype('str').str[:1],
    canton = df.index.astype('str').str[:3],
    distrito = df.index.astype('str').str[3:]
)

_ = plt.ion()
# Visualization
plt.figure()
plt.scatter(pca_df['PC1'], pca_df['PC2'], c = pca_df['canton'].astype('int'))#, cmap='viridis')
plt.title('PCA Result')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True)
plt.show(block=True)

# Explained variance ratio (importance of each principal component)
print("Explained variance ratio:", pca.explained_variance_ratio_)

##using plotly
import plotly.express as px

labels = {
    str(i): f"PC {i+1} ({var:.1f}%)"
    for i, var in enumerate(pca.explained_variance_ratio_ * 100)
}

fig = px.scatter_matrix(
    pca_df,
    labels=labels
)
fig.update_traces(diagonal_visible=False)
fig.show(block=True)

