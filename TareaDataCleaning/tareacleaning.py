import pandas as pd


data=pd.read_csv('game_info.csv')

#Exploracion Inicial
print(data.head())

print(data.info())

print(data.describe())

print(data.columns.tolist())

print(data.isnull().sum())

print(data.nunique())


#Reemplazar valores vacios con NA
data.replace('', pd.NA, inplace=True)

#Para las columnas string pasar a mayus y llenar los NA con "N/S"
missing_string_columns=[ 'name', 'slug' ,'website', 'platforms', 'developers', 'genres', 'publishers','esrb_rating','updated'] 

for column in missing_string_columns:
        data[column] = data[column].str.upper()
        data[column].fillna('N/S', inplace=True)

missing_number_columns=[  'playtime','metacritic', 'rating', 'rating_top','achievements_count', 'ratings_count', 'suggestions_count',  'reviews_count',
'added_status_yet', 'added_status_owned', 'added_status_beaten', 'added_status_toplay', 'added_status_dropped', 'added_status_playing'] 

for column in missing_number_columns:
        data[column].fillna(0, inplace=True)

#Juegos que tienen itch en su slug se quita y se agrega la pagina web        
print(data[['slug','website']])
def add_website(row):
    if '(ITCH)' in row['name']:
        row['website'] = 'HTTP://WWW.ITCH.IO'
        row['slug'] = row['slug'].replace('-ITCH', '')
    return row        
data = data.apply(add_website, axis=1)    

print(data[['slug','website']])

#Dejar un espacio en vez de -
data['slug'] = data['slug'].str.replace('-', ' ')
data['game_name']=data['slug']

#Dividir la fecha
data['released'] = pd.to_datetime(data['released'])
data['release_year'] = data['released'].dt.year
data['release_month'] = data['released'].dt.month
data['release_day'] = data['released'].dt.day

print(data[['released','release_year','release_month','release_day']])

#Dividir fecha y hora

data['updated'] = pd.to_datetime(data['updated'])
data['updated_date'] = data['updated'].dt.date
data['updated_time'] = data['updated'].dt.time

print(data[['updated','updated_date','updated_time']])

#Cambiar || por ,
data['platforms'] = data['platforms'].str.replace('||', ',')
data['developers'] = data['developers'].str.replace('||', ',')
data['genres'] = data['genres'].str.replace('||', ',')
data['publishers'] = data['publishers'].str.replace('||', ',')

print(data['platforms'])
print(data['developers'])
print(data['genres'])
print(data['publishers'])

columns_to_save=['id', 'game_name','website','platforms','genres','release_year','release_month','release_day', 'developers', 'publishers', 'updated_date','updated_time','esrb_rating', 'metacritic','ratings_count', 'rating', 'rating_top','suggestions_count','reviews_count', 'added_status_yet', 'added_status_owned', 'added_status_beaten', 'added_status_toplay', 'added_status_dropped', 'added_status_playing']
data_final=data[columns_to_save]
data_final.to_csv('game_info_clean.csv', index=False)


