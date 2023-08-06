import pandas as pd
import numpy as np
import unicodedata
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from functools import reduce
from relational_querier import RelationalQuerier
#from graph_querier import GraphQuerier

# os dados climaticos brutos foram baixados diretamente do link: https://www.kaggle.com/PROPPG-PPG/hourly-weather-surface-brazil-southeast-region
abbreviation = ['date', 'station','precipitacao','pressao_at_max', 'pressao_at_min', 'radiacao', 'temp_max','temp_min','umidade','max_vent','velocidade_vent','region','state','lat','lon','elvt']

db = RelationalQuerier()

def d(x):
	y = x.split('-')
	y.reverse()
	return '/'.join(y)

def clean(file_name):
	"""
	! filter raw data from date and stations code
	! process data
	! clean na
	"""
	#format_csv(file_name)
	print('formatando dados')
	df = pd.read_csv(file_name)

	print('removendo valores nulos')
	for i in df.columns:
		df = df.loc[df[i] != -9999]
	print('removeu valores nulos')

	preci = df.groupby(['Data', 'station'])['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].sum().reset_index()
	max_pres = df.groupby(['Data', 'station'])['PRESSÃO ATMOSFERICA MAX.NA HORA ANT. (AUT) (mB)'].mean().reset_index()
	min_pres = df.groupby(['Data', 'station'])['PRESSÃO ATMOSFERICA MIN. NA HORA ANT. (AUT) (mB)'].mean().reset_index()
	rad = df.groupby(['Data', 'station'])['RADIACAO GLOBAL (Kj/m²)'].mean().reset_index()
	temp_max = df.groupby(['Data', 'station'])['TEMPERATURA MÁXIMA NA HORA ANT. (AUT) (°C)'].max().reset_index()
	temp_min = df.groupby(['Data', 'station'])['TEMPERATURA MÍNIMA NA HORA ANT. (AUT) (°C)'].min().reset_index()
	umidade = df.groupby(['Data', 'station'])['UMIDADE RELATIVA DO AR, HORARIA (%)'].mean().reset_index()
	max_vent = df.groupby(['Data', 'station'])['VENTO, RAJADA MAXIMA (m/s)'].max().reset_index()
	vel_vent = df.groupby(['Data', 'station'])['VENTO, VELOCIDADE HORARIA (m/s)'].mean().reset_index()
	region = df.groupby(['Data', 'station'])['region'].first().reset_index()
	state = df.groupby(['Data', 'station'])['state'].first().reset_index()
	latitude = df.groupby(['Data', 'station'])['latitude'].first().reset_index()
	longitude = df.groupby(['Data', 'station'])['longitude'].first().reset_index()
	height = df.groupby(['Data', 'station'])['height'].first().reset_index()

	max_pres.drop(columns=['Data', 'station'], inplace=True)
	min_pres.drop(columns=['Data', 'station'], inplace=True)
	rad.drop(columns=['Data', 'station'], inplace=True)
	temp_max.drop(columns=['Data', 'station'], inplace=True)
	temp_min.drop(columns=['Data', 'station'], inplace=True)
	umidade.drop(columns=['Data', 'station'], inplace=True)
	max_vent.drop(columns=['Data', 'station'], inplace=True)
	vel_vent.drop(columns=['Data', 'station'], inplace=True)
	region.drop(columns=['Data', 'station'], inplace=True)
	state.drop(columns=['Data', 'station'], inplace=True)
	latitude.drop(columns=['Data', 'station'], inplace=True)
	longitude.drop(columns=['Data', 'station'], inplace=True)
	height.drop(columns=['Data', 'station'], inplace=True)

	print('renomeando colunas')
	clmns = [preci, max_pres, min_pres, rad, temp_max, temp_min, umidade, max_vent, vel_vent, region, state, latitude, longitude, height]
	df_final = pd.concat(clmns, axis=1,join="outer",ignore_index=False,keys=None,levels=None,names=None,verify_integrity=False,copy=False)
	df_final.columns = abbreviation

	df_final['date'] = df_final['date'].map(lambda x: d(x))

	new_file_name = file_name.split('.')[0]+'_clean.'+file_name.split('.')[1]
	print(new_file_name)

	df_final.to_csv(new_file_name)
	print('exportou')

	return df_final, new_file_name

def add_data_relational(db, df = None, csv = None):
	print('adicionando dados')
	if df is None and csv is not None:
		df = pd.read_csv(csv)
		
	if len(df.columns) >= 17:
		df.drop(df.columns[0], axis=1, inplace=True)
	i = 0
	for data in df.values:
		i += 1
		print(i)
		query = """
		INSERT INTO Clima
		(date,station,precipitacao,pressao_at_max, pressao_at_min, radiacao,
		temp_max,temp_min,umidade,max_vent,velocidade_vent,region,
		state,lat,lon,elvt)
		VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""

		result = db.query(query, data)
	db.commit()

def normalize_names(s):
	s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
	return s.replace("'", "").replace("  ", " ").lower()

def add_data_relational_stations(db, df = None, csv = None):
	print('adicionando estacoes meteo')
	if df is None and csv is not None:
		df = pd.read_csv(csv)
	
	df['region'] = df['region'].map(normalize_names)

	i = 0
	for data in df.values:
		i+=1
		print(i)
		query = """
		INSERT INTO Estacoes
		(Estacao,Regiao,UF,Codigo,Prim_data,alt,lon,lat)
		VALUES(?,?,?,?,?,?,?,?);"""

		result = db.query(query, data)
	db.commit()

if __name__ == "__main__":
	# le o caminho do arquivo
	Tk().withdraw()
	files = askopenfilenames()
	print(files)
	# para cada um dos arquivos
	for file in files:
		print('iniciando processamento')
		name = file.split('/')[-1].split('.')[0]
		print("processando arquivo:",name)
		if name in ["central_west", "north", "northeast", "south", "southeast"]:
			print('arquivo nao formatado, iniciando limpeza de arquivo', name)
			df, new_file_name = clean(file)
			add_data_relational(db, df = df)
	
		# caso contrario apenas adicione no banco de dados
		elif name in ["central_west_clean", "north_clean", "northeast_clean", "south_clean", "southeast_clean"]:
			print('arquivo formatado, iniciando insercao no banco de dados')
			# only uncomment if you want do use the databses
			add_data_relational(db, csv = file)
		
		elif name == 'stations':
			add_data_relational_stations(db, csv = file)

		print('processamento e insercao concluidos\n')
	db._close()
