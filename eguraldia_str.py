import streamlit as st
import pandas as pd
import numpy as np
import glob
import os

st.header('# Dades Meteorològiques')
st.markdown('''
Dades obtingudes des de:  
[Meteoprades](https://www.meteoprades.net)  
[AEMET](https://www.meteoprades.net/)  
''')

##=================================
###Datuak lortu
##=================================

f_csv='./Denak_batera.csv'

@st.cache
def load_data(path):
    dataset = pd.read_csv(path, sep='\t')
    return dataset

df_all = load_data(f_csv)


##=================================
##Euriaren kalkuluak
##=================================

#Dataframe berri bat euri-egunekin bakarrik (>1 litro)
euridunak= df_all[df_all['Euria'] > 1]

#Taldeak egin: Tokia eta urteko
euria_urteko=euridunak.sort_values(['Tokia','Urtea'],ascending=True).groupby(['Tokia','Urtea'], sort = False).sum()['Euria']

#Euri-egunak zenbatu toki eta urteko bakoitzerko
#Zutabe guztietan kalkulatzen du, baina nik behin behar det. Fetxa zutabera-ko datua gordeko dut, behin bakarrik edukitzeko
euri_egunak=euridunak.sort_values(['Tokia','Urtea'],ascending=True).groupby(['Tokia','Urtea']).agg(np.size)['Eguna']

##=================================
## Grafika 1: Leku baterako, euria urteka
##=================================

st.header('## Gràfica 1: Pluja anual a cada municipi')
st.markdown('Primer, amb el menú, tria el municipi')   
st.markdown('Despres, pren el botó de sota')  

selected_geography = st.selectbox(label='Municipi', options=df_all['Tokia'].unique())
submitted = st.button('Envia selecció')

if submitted:
	filtered_tokia = df_all[df_all['Tokia'] == selected_geography]
	datuak_gr1=filtered_tokia.sort_values(['Urtea'],ascending=True).groupby(['Urtea'], sort = False).sum()['Euria'] 
	chart_data = datuak_gr1
	st.bar_chart(chart_data)
