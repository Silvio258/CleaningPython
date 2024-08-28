import pandas as pd


df=pd.read_csv('netflix_titles.csv')

#Exploracion Inicial
print(df.head())

print(df.info())

print(df.describe())

print(df.columns.tolist())

print(df.isnull().sum())

print(df.nunique())




#Reemplazar valores vacios con NA
df.replace('', pd.NA, inplace=True)

#Para las columnas string pasar a mayus y llenar los NA con "N/S"
missing_string_columns=['type','title','director','cast','country','listed_in']
for column in missing_string_columns:
        df[column] = df[column].str.upper()
        df[column].fillna('N/S', inplace=True)


#Dividir la columna de fecha
df['date_added'] = pd.to_datetime(df['date_added'], format="%B %d, %Y", errors='coerce')
df['day_added'] = df['date_added'].dt.day
df['month_added'] = df['date_added'].dt.month
df['year_added'] = df['date_added'].dt.year

#Encontrar los valores incorrectos que pertenecen a duration en rating
incorrect_values = df['rating'].str.contains(r'min', na=False)
df.loc[incorrect_values, 'duration'] = df.loc[incorrect_values, 'rating']
df.loc[incorrect_values, 'rating'] = 'NR'


#Separar la columna de duration en numero y tipo
df['duration'] = df['duration'].str.strip().str.upper()
df[['duration_value', 'duration_type']] = df['duration'].str.split(' ', n=1, expand=True)
df['duration_value'] = pd.to_numeric(df['duration_value'], errors='coerce')
df['duration_type'] = df['duration_type'].replace('SEASON', 'SEASONS')

#Reemplazar valores vacios con 0
missing_number_columns=['day_added','month_added','year_added','duration_value']

for column in missing_number_columns:
        df[column].fillna(0, inplace=True)

#Existe UR y NR, para ello se eligio NR como el valor que indique que no hay un rating
df['rating'] = df['rating'].replace('UR', 'NR')
df['rating'].fillna('NR', inplace=True)

#Imprimir valores finales
print(df['director'])
print(df['cast'])
print(df['country'])
print(df['rating'])
print(df['day_added'])
print(df['month_added'])
print(df['year_added'])
print(df['duration_value'])
print(df['duration_type'])
print(df['listed_in'])
print(df['duration_type'].unique())
print(df[['duration', 'duration_value', 'duration_type']].head(20))

columns_to_save = ['show_id','type','title','director', 'cast', 'country', 'rating', 'release_year','day_added', 'month_added', 'year_added','duration_value', 'duration_type', 'listed_in']

df_final = df[columns_to_save]

df_final.to_csv('netflix_titles_clean.csv', index=False)





