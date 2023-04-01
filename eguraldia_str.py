import streamlit as st
import pandas as pd
#import plotly.express as px
import numpy as np
import glob
import os
#import matplotlib.pyplot as plt

##=================================
###Datuak lortu
##=================================

#f_csv='../Denak_batera.csv' #Ubunturako
f_csv='./Denak_batera.csv' #Github-erako

@st.cache
def load_data(path):
    dataset = pd.read_csv(path, sep='\t')
    return dataset

df_all = load_data(f_csv)

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
  
Nota 1: fixeu-vos que en el cas d'Alforja hi ha dades de les dues fonts. Com diferenciar-les:  
$\cdot$ Dades de Meteoprades: alforja (tot en minúscula)  
$\cdot$ Dades d\'AEMET: Alforja (primera lletra en majúscula)   

Nota 2: Periode de les dades:  
$\cdot$ Dades de Meteoprades: a partir de 2019  
$\cdot$ Dades d\'AEMET: a partir de 2013  
''')

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
## Taula 0: Datu guztiak modu askotara
##=================================

st.header('## Taula per filtrar totes les dades')
st.markdown('''
	 
	Menú 'Paràmetre': tria el paràmetre. Les opecions són:  
			$\cdot$ Tmax: Temperatura màxima d'un dia  
			$\cdot$ Tmin: Temperatura mínima d'un dia  
			$\cdot$ Euria: Pluja d'un dia  
			$\cdot$ Vmax: Velocitat màxima del vent d'un dia  
	Menú 'Municipi': tria el municipi. Hi ha l\'opció de triar tots els municipis.  
	Menú 'Any': tria l'any. Hi ha l'opció de tots els anys.  
	Menú 'Mes': tria el mes. Hi ha l'opció de tots els messos.  
	Menú 'Nombre de dades': tria quantes dades apareixeran a la taula.  
	IMPORTANT: per que s'actualitzi la taula, pren el botó 'Envia selecció'.  
	''')    

with st.form('Taula0'):

	selected_zer0 = st.selectbox(label='Paràmetre', options=['Tmax','Tmin','Euria','Vmax'])
	selected_toki0 = st.selectbox(label='Municipi', options=['Tots', 'vilaplana','la-mussara','laleixar','lalbiol','alforja',
		'Donostia','Bilbo','Gasteiz','Iruña','Alforja','Reus','Tarragona','Vigo'])
	selected_urte0 = st.selectbox(label='Any', options=['Tots',2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013])
	selected_hilab0 = st.selectbox(label='Mes', options=['Tots', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
	selected_zenbat0= st.selectbox(label='Nombre de dades', options=[5,10,20,30,50])
	submitted0 = st.form_submit_button('Envia selecció')

	if submitted0:

    	#Aurrena, filtratu toki konkretu baterako
		if (selected_toki0 =='Tots'):
			filt_1 = df_all
		else:
			filt_1 = df_all[df_all['Tokia'] == selected_toki0]
		#Orain, urte baterako
		if (selected_urte0 =='Tots'):
			filt_2 = filt_1 
		else:
			filt_2 = filt_1[filt_1['Urtea'] == selected_urte0]
		#Azkenik, hilabeteka
		if (selected_hilab0 =='Tots'):
			filt_3 = filt_2 
		else:
			filt_3 = filt_2[filt_2['Hilab'] == selected_hilab0]


		if (selected_zer0=='Tmin'):
				data_all=filt_3.sort_values(by=selected_zer0,ascending=True)
		else:
				data_all=filt_3.sort_values(by=selected_zer0,ascending=False)
    
		df_table=data_all[['Tokia','Eguna','Hilab','Urtea',selected_zer0]][:selected_zenbat0]
		#st.table(df_table)
		st.table(df_table.style.format({selected_zer0: '{:.1f}'}))


##=================================
## Taula 2: Euriaren datuak urteka
##=================================

st.header('## Taula amb dades de pluja anuals per un municipi')
st.markdown('''
	Primer menú, tria el municipi.   
	Tot seguit, pren el botó de sota
	''')    

with st.form('Taula6'):

	selected_toki6 = st.selectbox(label='Municipi', options=['vilaplana','la-mussara','laleixar','lalbiol','alforja',
		'Donostia','Bilbo','Gasteiz','Iruña','Alforja','Reus','Tarragona','Vigo'])
	submitted6 = st.form_submit_button('Envia selecció')

	if submitted6:

		filtered_ta6 = df_all[df_all['Tokia'] == selected_toki6]

		datuak_ta6=filtered_ta6.sort_values(['Urtea'],ascending=True).groupby(['Urtea'], sort = False).sum()['Euria'] 
	#datuak_ta6.reset_index(inplace = True)
    
	#df_table6=datuak_ta6[['Tokia','Urtea','Euria']][:selected_zenbat]
	#st.dataframe(df_table6)
		st.table(datuak_ta6.map('{:.1f}'.format))#.style.format("{:.1f}"))

##=================================
## Taula 3: Euriaren datuak hilabeteka
##=================================

st.header('## Taula amb dades de pluja mensuals per any i per municipi')
st.markdown('''
	Primer menú, tria el municipi. 
	Segon menú, tria un any.   
	Per últim, pren el botó de sota
	''')    

with st.form('Taula7'):

	selected_toki7 = st.selectbox(label='Municipi', options=['vilaplana','la-mussara','laleixar','lalbiol','alforja',
		'Donostia','Bilbo','Gasteiz','Iruña','Alforja','Reus','Tarragona','Vigo'])
	#selected_urte7a = st.selectbox(label='Any 1', options=[2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013])
	#selected_urte7b = st.selectbox(label='Any 2', options=[2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013])
	submitted7 = st.form_submit_button('Envia selecció')

	if submitted7:

		tmp_tokia7 = df_all[df_all['Tokia'] == selected_toki7]

		if (selected_toki7=='vilaplana' or selected_toki7=='la-mussara' or selected_toki7=='laleixar' or 
			selected_toki7=='lalbiol' or selected_toki7=='alforja'):
			
			filtered_2023 = tmp_tokia7[tmp_tokia7['Urtea'] == 2023]
			filtered_2022 = tmp_tokia7[tmp_tokia7['Urtea'] == 2022]
			filtered_2021 = tmp_tokia7[tmp_tokia7['Urtea'] == 2021]
			filtered_2020 = tmp_tokia7[tmp_tokia7['Urtea'] == 2020]
			filtered_2019 = tmp_tokia7[tmp_tokia7['Urtea'] == 2019]
			
			datuak_2023=filtered_2023.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2022=filtered_2022.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2021=filtered_2021.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2020=filtered_2020.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2019=filtered_2019.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']

			batera = pd.concat([datuak_2023,datuak_2022,datuak_2021,datuak_2020,datuak_2019], ignore_index=True, axis=1)
			batera=batera.rename(columns = {0:'2023',1:'2022',2:'2021',3:'2020',4:'2019'})
		else:
			filtered_2023 = tmp_tokia7[tmp_tokia7['Urtea'] == 2023]
			filtered_2022 = tmp_tokia7[tmp_tokia7['Urtea'] == 2022]
			filtered_2021 = tmp_tokia7[tmp_tokia7['Urtea'] == 2021]
			filtered_2020 = tmp_tokia7[tmp_tokia7['Urtea'] == 2020]
			filtered_2019 = tmp_tokia7[tmp_tokia7['Urtea'] == 2019]
			filtered_2018 = tmp_tokia7[tmp_tokia7['Urtea'] == 2018]
			filtered_2017 = tmp_tokia7[tmp_tokia7['Urtea'] == 2017]
			filtered_2016 = tmp_tokia7[tmp_tokia7['Urtea'] == 2016]
			filtered_2015 = tmp_tokia7[tmp_tokia7['Urtea'] == 2015]
			filtered_2014 = tmp_tokia7[tmp_tokia7['Urtea'] == 2014]
			filtered_2013 = tmp_tokia7[tmp_tokia7['Urtea'] == 2013]
			
			datuak_2023=filtered_2023.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2022=filtered_2022.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2021=filtered_2021.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2020=filtered_2020.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2019=filtered_2019.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2018=filtered_2018.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2017=filtered_2017.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2016=filtered_2016.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2015=filtered_2015.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2014=filtered_2014.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']
			datuak_2013=filtered_2013.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria']

			batera = pd.concat([datuak_2023,datuak_2022,datuak_2021,datuak_2020,datuak_2019,datuak_2018,datuak_2017,datuak_2016,
				datuak_2015,datuak_2014,datuak_2013], ignore_index=True, axis=1)
			batera=batera.rename(columns = {0:'2023',1:'2022',2:'2021',3:'2020',4:'2019',5:'2018',6:'2017',7:'2016',8:'2015',9:'2014',10:'2013'})

		
		#st.dataframe(datuak_ta7)
		st.table(batera.style.format("{:.1f}"))

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
	#selected_urte2 = st.selectbox(label='Any', options=df_all['Urtea'].unique())
	#Goiko aukerarekin, urteak desordenatuta daude. Eskuz jarriko ditut
	selected_urte2 = st.selectbox(label='Any', options=[2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013])
	submitted2 = st.form_submit_button('Envia selecció')

	if submitted2:
		

		tmp_tokia2 = df_all[df_all['Tokia'] == selected_toki2]
		filtered_2 = tmp_tokia2[tmp_tokia2['Urtea'] == selected_urte2]
		datuak_gr2=filtered_2.sort_values(['Hilab'],ascending=True).groupby(['Hilab'], sort = False).sum()['Euria'] 
		chart_data2 = datuak_gr2
		if (selected_urte2<2019 and (selected_toki2=='vilaplana' or selected_toki2=='la-mussara' or 
			selected_toki2=='lalbiol' or selected_toki2=='laleixar' or selected_toki2=='alforja')):
			st.markdown("Per aquest municipi, dades disponibles a partir de l'any 2019")
		else:
			st.bar_chart(chart_data2)

##=================================
## Grafika 3: Leku baterako, bi urteko euria konparatu hilabeteka
##=================================
#Ez det lortu

##=================================
## Grafika 4: Leku baterako eta urte baterako, haize-egunak hilabetero
##=================================

st.header('## Gràfica 3: Dies de vent anual a cada municipi')
st.markdown('Per a un municipi, quans dies de vent hi van haver-hi.')   
st.markdown('Es pot triar la velocitat mínima del vent')  


with st.form('Grafika4'):

	selected_toki4 = st.selectbox(label='Municipi', options=df_all['Tokia'].unique())
	selected_vel = st.slider('Velocitat mínima del vent', 0, 100, 10)
	submitted4 = st.form_submit_button('Envia selecció')

	if submitted4:
		tmp_tokia4 = df_all[df_all['Tokia'] == selected_toki4]
		filtered_gr4 = tmp_tokia4[tmp_tokia4['Vmax'] > selected_vel]
		datuak_gr4=filtered_gr4.sort_values(['Urtea'],ascending=True).groupby(['Urtea']).agg(np.size)['Vmax']
		
		chart_data4 = datuak_gr4
		#st.write(datuak_gr4)
		st.bar_chart(chart_data4)


