import streamlit as st
import pandas as pd
#import plotly.express as px
import numpy as np
import glob
import os
#import matplotlib.pyplot as plt

#################################
#Sidebar
#=================================
with st.sidebar:
    st.subheader('Dades Meteorològiques')
    st.markdown('Jon Mujika')
    
st.sidebar.image('star-4167939__480.jpg', width=250)

#==================================

st.header('# Dades Meteorològiques')
st.markdown('''
Dades obtingudes des de:  
[Meteoprades](https://www.meteoprades.net)  : Vilaplana, La-Mussara, Alforja, l\'Aleixar, l'Albiol  
[AEMET](https://www.meteoprades.net/): Donosti, Bilbo, Gasteiz, Iruña, Alforja, Reus, Tarragona, Vigo  
  
Nota: fixeu-vos que en el cas d'Alforja hi ha dades de les dues fonts. Com diferenciar-les:  
$\cdot$ Dades de Meteoprades: alforja (tot en minúscula)  
$\cdot$ Dades d\'AEMET: Alforja (primera lletra en majúscula)  
''')

##=================================
###Datuak lortu
##=================================

f_csv='../Denak_batera.csv'

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
## Taula
##=================================

st.header('## Taula per filtrar totes les dades')
st.markdown('''
	Primer menú, tria el municipi. Hi ha l\'opció de triar tots els municipis  
	Segon menú tria el paràmetre. Les opecions són:  
			$\cdot$ Tmax: Temperatura màxima d'un dia  
			$\cdot$ Tmin: Temperatura mínima d'un dia  
			$\cdot$ Euria: Pluja d'un dia  
			$\cdot$ Vmax: Velocitat màxima del vent d'un dia  
	Tercer menú: tria quantes dades apareixeran a la taula.  
	Finalment, pren el botó de sota
	''')    

with st.form('Taula5'):

	selected_zer = st.selectbox(label='Paràmetre', options=['Tmax','Tmin','Euria','Vmax'])
	selected_toki5 = st.selectbox(label='Municipi', options=['Tots', 'vilaplana','la-mussara','laleixar','lalbiol','alforja',
		'Donostia','Bilbo','Gasteiz','Iruña','Alforja','Reus','Tarragona','Vigo'])
	selected_zenbat= st.selectbox(label='Nombre de dades', options=[5,10,20,30,50])
	submitted5 = st.form_submit_button('Envia selecció')

	data_all = df_all.sort_values(by=selected_zer,ascending=False)
	data_all.reset_index(inplace = True)
    #Orain, filtratu toki konkretu baterako
	if (selected_toki5=='Tots'):        
		if (selected_zer=='Tmin'):
			data_non=data_all.sort_values(by=selected_zer,ascending=True)
		else:
			data_non=data_all.sort_values(by=selected_zer,ascending=False)
	else: #Ez guztiak, hau da, toki konkretu bat
		if (selected_zer=='Tmin'):
			data_non=data_all.loc[data_all['Tokia'] == selected_toki5].sort_values(by=selected_zer,ascending=True)
		else:
			data_non=data_all.loc[data_all['Tokia'] == selected_toki5].sort_values(by=selected_zer,ascending=False)
	data_non.reset_index(inplace = True)
    
	df_table=data_non[['Tokia','Eguna','Hilab','Urtea',selected_zer]][:selected_zenbat]
	st.dataframe(df_table)


##=================================
## Grafika 1: Leku baterako, euria urteka
##=================================

st.header('## Gràfica 1: Pluja anual a cada municipi')
st.markdown('Primer, amb el menú, tria el municipi')   
st.markdown('Despres, pren el botó de sota')  


with st.form('Grafika1'):

	selected_toki1 = st.selectbox(label='Municipi', options=df_all['Tokia'].unique())
	submitted1 = st.form_submit_button('Envia selecció')

	if submitted1:
		filtered_tokia1 = df_all[df_all['Tokia'] == selected_toki1]
		datuak_gr1=filtered_tokia1.sort_values(['Urtea'],ascending=True).groupby(['Urtea'], sort = False).sum()['Euria'] 
		chart_data1 = datuak_gr1
		st.bar_chart(chart_data1)

##=================================
## Grafika 2: Leku baterako eta urte baterako, euria hilabeteka
##=================================

st.header('## Gràfica 2: Pluja mensual per any i per municipi')
st.markdown('Primer, amb el menú, tria el municipi')   
st.markdown('Segon, amb el altre menú, tria l\'any')   
st.markdown('Finalment, pren el botó de sota')  

with st.form('Grafika2'):

	selected_toki2 = st.selectbox(label='Municipi', options=df_all['Tokia'].unique())
	selected_urte2 = st.selectbox(label='Any', options=df_all['Urtea'].unique())
	submitted2 = st.form_submit_button('Envia selecció')

	if submitted2:
		tmp_tokia2 = df_all[df_all['Tokia'] == selected_toki2]
		filtered_2 = tmp_tokia2[tmp_tokia2['Urtea'] == selected_urte2]
		datuak_gr2=filtered_2.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria'] 
		chart_data2 = datuak_gr2
		st.bar_chart(chart_data2)

##=================================
## Grafika 3: Leku baterako, bi urteko euria konparatu hilabeteka
##=================================
#Ez det lortu

##=================================
## Grafika 4: Leku baterako eta urte baterako, haize-egunak hilabetero
##=================================
#Egiteko


