pip install requests 
pip install beautifulsoup4 
pip install numpy 
pip install pandas 
pip install matplotlib 
pip install seaborn 
pip install psycopg2-binary
pip install sqlalchemy 
pip install mysql-connector-python 
pip install plotly


# Se importan las librerías necesarias (prueba)
import requests
from bs4 import BeautifulSoup as Soup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import random
import psycopg2
import os
from sqlalchemy import create_engine 
import mysql.connector
import plotly.express as px

# url link is connected to a variable
url_base = "https://sofifa.com/players?offset="
url_2 = "https://sofifa.com/players?offset=60"
url_3 = "https://sofifa.com/players?offset=120"
url_4 = "https://sofifa.com/players?offset=180"

##################################################

player_data = []

for offset in range(0, 2):
    url = url_base + str(offset * 61)

    # Añadir un retraso aleatorio entre las solicitudes
    delay = random.uniform(1, 10)
    time.sleep(delay)

    # Configurar encabezados HTTP para simular un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Realizar la solicitud con encabezados y retraso
    p_html = requests.get(url, headers=headers)

    # Verificar si la solicitud fue exitosa antes de procesar la respuesta
    if p_html.status_code == 200:
        p_soup = p_html.text
        data = Soup(p_soup, 'html.parser')
        table = data.find('tbody')
print(table)

##################################################

# Define la lista de player_data antes del bucle
player_data = []

for i in table.findAll('tr'):
    data_dic = {}
    td = i.findAll('td')

    # Imprimir información para depuración
    print("=== New Player ===")

    try:
        data_dic["picture"] = td[0].find('img').get('data-src')
        print("Picture:", data_dic["picture"])
    except Exception as e:
        print("Error in picture:", e)

    try:
        data_dic["ID"] = td[0].find('img').get('id')
        print("ID:", data_dic["ID"])
    except Exception as e:
        print("Error in ID:", e)

    try:
        data_dic["flag"] = td[1].find('img').get('data-src')
        print("Flag:", data_dic["flag"])
    except Exception as e:
        print("Error in flag:", e)

    try:
        data_dic["Name"] = td[1].find("a").text
        print("Name:", data_dic["Name"])
    except Exception as e:
        print("Error in Name:", e)

    try:
        data_dic["Age"] = int(td[2].text.strip())
        print("Age:", data_dic["Age"])
    except Exception as e:
        print("Error in Age:", e)

    try:
        pos_tags = td[1].find_all("span")
        positions = [tag.text for tag in pos_tags]
        data_dic["Position"] = ", ".join(positions)
        print("Position:", data_dic["Position"])
    except Exception as e:
        print("Error in Position:", e)

    try:
        data_dic["Overall"] = td[3].find('span').text
        print("Overall:", data_dic["Overall"])
    except Exception as e:
        print("Error in Overall:", e)

    try:
        data_dic["Potential"] = td[4].find('span').text
        print("Potential:", data_dic["Potential"])
    except Exception as e:
        print("Error in Potential:", e)

    try:
        data_dic["Team_image"] = td[5].find('img').get('data-src')
        print("Team Image:", data_dic["Team_image"])
    except Exception as e:
        print("Error in Team Image:", e)

    try:
        data_dic["Team"] = td[5].find('a').text
        print("Team:", data_dic["Team"])
    except Exception as e:
        print("Error in Team:", e)

    try:
        data_dic["Value"] = td[6].text.strip()
        print("Value:", data_dic["Value"])
    except Exception as e:
        print("Error in Value:", e)

    try:
        data_dic["Wage"] = td[7].text.strip()
        print("Wage:", data_dic["Wage"])
    except Exception as e:
        print("Error in Wage:", e)

    try:
        data_dic["Total_Point"] = td[8].text.strip()
        print("Total_Point:", data_dic["Total_Point"])
    except Exception as e:
        print("Error in Total_Point:", e)

    # Agrega el diccionario a la lista player_data
    player_data.append(data_dic)

    # Imprimir el diccionario para verificar su contenido
    print("Player Dictionary:", data_dic)
    print("=================")

# Convierte la lista de diccionarios a un DataFrame de pandas
df = pd.DataFrame(player_data)

# Imprime el DataFrame
print(df.head())

##################################################

# Quitar el símbolo de la moneda y convertir a valor numérico
df['Letra_Value_2'] = df['Value'].str.extract('([MK])', expand=False)

# Obtener valores únicos de 'Value_2'
unique_letra_values = df['Letra_Value_2'].unique().tolist()
print(unique_letra_values)

# Quitar el símbolo de la moneda y convertir a valor numérico
df['Value_2'] = df['Value'].replace('[\€,M,K]', '', regex=True).astype(float)

# Obtener valores únicos de 'Value'
unique_values = df['Value'].unique().tolist()

# Crear la nueva variable 'Value_limpia'
df['Value_Millones'] = df['Value_2']
df.loc[df['Letra_Value_2'] == 'K', 'Value_Millones'] = df['Value_2'] / 1000
df.loc[df['Value'] == '€0', 'Value_Millones']  = df['Value_2']
df.loc[df['Letra_Value_2'].isna(), 'Value_Millones'] /= 10000

# Redondear 'Value_limpia' a dos decimales
df['Value_Millones'] = df['Value_Millones'].round(2)

# Quitar el símbolo de la moneda y convertir a valor numérico
df['Letra_Wage_2'] = df['Wage'].str.extract('([MK])', expand=False)

# Obtener valores únicos de 'Wage_2'
unique_letra_values = df['Letra_Wage_2'].unique().tolist()
print(unique_letra_values)

# Quitar el símbolo de la moneda y convertir a valor numérico
df['Wage_2'] = df['Wage'].replace('[\€,M,K]', '', regex=True).astype(float)

# Obtener valores únicos de 'Value'
unique_wages = df['Wage_2'].unique().tolist()

# Crear la nueva variable 'Wage_limpia' con ambas condiciones
df['Wage_Miles'] = df['Wage_2'].copy()
df.loc[df['Letra_Wage_2'].isna(), 'Wage_Miles'] /= 1000

# Redondear 'Value_limpia' a dos decimales
df['Wage_Miles'] = df['Wage_Miles'].round(2)

# Imprimir la lista de valores únicos
print(df)

# Cambiar el nombre del DataFrame a df_nuevo
df_nuevo = df.copy()  # Para evitar modificar el DataFrame original
df_nuevo.name = 'df_nuevo'

##################################################
##################################################

player_data2 = []

for offset in range(0, 2):
    url2 = url_2 + str(offset * 61)

    # Añadir un retraso aleatorio entre las solicitudes
    delay = random.uniform(1, 10)
    time.sleep(delay)

    # Configurar encabezados HTTP para simular un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Realizar la solicitud con encabezados y retraso
    p_html2 = requests.get(url2, headers=headers)

    # Verificar si la solicitud fue exitosa antes de procesar la respuesta
    if p_html2.status_code == 200:
        p_soup2 = p_html2.text
        data2 = Soup(p_soup2, 'html.parser')
        table2 = data2.find('tbody')
print(table2)

##################################################

# Define la lista de player_data antes del bucle
player_data2 = []

for i in table2.findAll('tr'):
    data_dic2 = {}
    td = i.findAll('td')

    # Imprimir información para depuración
    print("=== New Player ===")

    try:
        data_dic2["picture"] = td[0].find('img').get('data-src')
        print("Picture:", data_dic2["picture"])
    except Exception as e:
        print("Error in picture:", e)

    try:
        data_dic2["ID"] = td[0].find('img').get('id')
        print("ID:", data_dic2["ID"])
    except Exception as e:
        print("Error in ID:", e)

    try:
        data_dic2["flag"] = td[1].find('img').get('data-src')
        print("Flag:", data_dic2["flag"])
    except Exception as e:
        print("Error in flag:", e)

    try:
        data_dic2["Name"] = td[1].find("a").text
        print("Name:", data_dic2["Name"])
    except Exception as e:
        print("Error in Name:", e)

    try:
        data_dic2["Age"] = int(td[2].text.strip())
        print("Age:", data_dic2["Age"])
    except Exception as e:
        print("Error in Age:", e)

    try:
        pos_tags2 = td[1].find_all("span")
        positions2 = [tag.text for tag in pos_tags]
        data_dic2["Position"] = ", ".join(positions2)
        print("Position:", data_dic2["Position"])
    except Exception as e:
        print("Error in Position:", e)

    try:
        data_dic2["Overall"] = td[3].find('span').text
        print("Overall:", data_dic2["Overall"])
    except Exception as e:
        print("Error in Overall:", e)

    try:
        data_dic2["Potential"] = td[4].find('span').text
        print("Potential:", data_dic2["Potential"])
    except Exception as e:
        print("Error in Potential:", e)

    try:
        data_dic2["Team_image"] = td[5].find('img').get('data-src')
        print("Team Image:", data_dic2["Team_image"])
    except Exception as e:
        print("Error in Team Image:", e)

    try:
        data_dic2["Team"] = td[5].find('a').text
        print("Team:", data_dic2["Team"])
    except Exception as e:
        print("Error in Team:", e)

    try:
        data_dic2["Value"] = td[6].text.strip()
        print("Value:", data_dic2["Value"])
    except Exception as e:
        print("Error in Value:", e)

    try:
        data_dic2["Wage"] = td[7].text.strip()
        print("Wage:", data_dic2["Wage"])
    except Exception as e:
        print("Error in Wage:", e)

    try:
        data_dic2["Total_Point"] = td[8].text.strip()
        print("Total_Point:", data_dic2["Total_Point"])
    except Exception as e:
        print("Error in Total_Point:", e)

    # Agrega el diccionario a la lista player_data
    player_data2.append(data_dic2)

    # Imprimir el diccionario para verificar su contenido
    print("Player Dictionary:", data_dic2)
    print("=================")

# Convierte la lista de diccionarios a un DataFrame de pandas
df2 = pd.DataFrame(player_data2)

##################################################

# Quitar el símbolo de la moneda y convertir a valor numérico
df2['Letra_Value_2'] = df2['Value'].str.extract('([MK])', expand=False)

# Obtener valores únicos de 'Value_2'
unique_letra_values = df2['Letra_Value_2'].unique().tolist()
print(unique_letra_values)

# Quitar el símbolo de la moneda y convertir a valor numérico
df2['Value_2'] = df2['Value'].replace('[\€,M,K]', '', regex=True).astype(float)

# Obtener valores únicos de 'Value'
unique_values = df2['Value'].unique().tolist()

# Crear la nueva variable 'Value_limpia'
df2['Value_Millones'] = df2['Value_2']
df2.loc[df2['Letra_Value_2'] == 'K', 'Value_Millones'] = df2['Value_2'] / 1000
df2.loc[df2['Value'] == '€0', 'Value_Millones']  = df2['Value_2']
df2.loc[df2['Letra_Value_2'].isna(), 'Value_Millones'] /= 10000

# Redondear 'Value_limpia' a dos decimales
df2['Value_Millones'] = df2['Value_Millones'].round(2)

# Quitar el símbolo de la moneda y convertir a valor numérico
df2['Letra_Wage_2'] = df2['Wage'].str.extract('([MK])', expand=False)

# Obtener valores únicos de 'Wage_2'
unique_letra_values = df2['Letra_Wage_2'].unique().tolist()
print(unique_letra_values)

# Quitar el símbolo de la moneda y convertir a valor numérico
df2['Wage_2'] = df2['Wage'].replace('[\€,M,K]', '', regex=True).astype(float)

# Obtener valores únicos de 'Value'
unique_wages = df2['Wage_2'].unique().tolist()

# Crear la nueva variable 'Wage_limpia' con ambas condiciones
df2['Wage_Miles'] = df2['Wage_2'].copy()
df2.loc[df2['Letra_Wage_2'].isna(), 'Wage_Miles'] /= 1000

# Redondear 'Value_limpia' a dos decimales
df2['Wage_Miles'] = df2['Wage_Miles'].round(2)

# Imprimir la lista de valores únicos
print(df2)

##################################################

# Cambiar el nombre del DataFrame a df_nuevo
df_nuevo2 = df2.copy()  # Para evitar modificar el DataFrame original
df_nuevo2.name = 'df_nuevo'

# Ahora df_nuevo es simplemente una referencia al DataFrame original con un nuevo nombre
print(df_nuevo2)

##################################################
##################################################

player_data3 = []

for offset in range(0, 2):
    url3 = url_3 + str(offset * 61)

    # Añadir un retraso aleatorio entre las solicitudes
    delay = random.uniform(1, 10)
    time.sleep(delay)

    # Configurar encabezados HTTP para simular un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Realizar la solicitud con encabezados y retraso
    p_html = requests.get(url3, headers=headers)

    # Verificar si la solicitud fue exitosa antes de procesar la respuesta
    if p_html.status_code == 200:
        p_soup = p_html.text
        data = Soup(p_soup, 'html.parser')
        table = data.find('tbody')
print(table)

##################################################

# Define la lista de player_data antes del bucle
player_data3 = []

for i in table.findAll('tr'):
    data_dic3 = {}
    td = i.findAll('td')

    # Imprimir información para depuración
    print("=== New Player ===")

    try:
        data_dic3["picture"] = td[0].find('img').get('data-src')
        print("Picture:", data_dic3["picture"])
    except Exception as e:
        print("Error in picture:", e)

    try:
        data_dic3["ID"] = td[0].find('img').get('id')
        print("ID:", data_dic3["ID"])
    except Exception as e:
        print("Error in ID:", e)

    try:
        data_dic3["flag"] = td[1].find('img').get('data-src')
        print("Flag:", data_dic3["flag"])
    except Exception as e:
        print("Error in flag:", e)

    try:
        data_dic3["Name"] = td[1].find("a").text
        print("Name:", data_dic3["Name"])
    except Exception as e:
        print("Error in Name:", e)

    try:
        data_dic3["Age"] = int(td[3].text.strip())
        print("Age:", data_dic3["Age"])
    except Exception as e:
        print("Error in Age:", e)

    try:
        pos_tags3 = td[1].find_all("span")
        positions3 = [tag.text for tag in pos_tags]
        data_dic3["Position"] = ", ".join(positions3)
        print("Position:", data_dic3["Position"])
    except Exception as e:
        print("Error in Position:", e)

    try:
        data_dic3["Overall"] = td[3].find('span').text
        print("Overall:", data_dic3["Overall"])
    except Exception as e:
        print("Error in Overall:", e)

    try:
        data_dic3["Potential"] = td[4].find('span').text
        print("Potential:", data_dic3["Potential"])
    except Exception as e:
        print("Error in Potential:", e)

    try:
        data_dic3["Team_image"] = td[5].find('img').get('data-src')
        print("Team Image:", data_dic3["Team_image"])
    except Exception as e:
        print("Error in Team Image:", e)

    try:
        data_dic3["Team"] = td[5].find('a').text
        print("Team:", data_dic3["Team"])
    except Exception as e:
        print("Error in Team:", e)

    try:
        data_dic3["Value"] = td[6].text.strip()
        print("Value:", data_dic3["Value"])
    except Exception as e:
        print("Error in Value:", e)

    try:
        data_dic3["Wage"] = td[7].text.strip()
        print("Wage:", data_dic3["Wage"])
    except Exception as e:
        print("Error in Wage:", e)

    try:
        data_dic3["Total_Point"] = td[8].text.strip()
        print("Total_Point:", data_dic3["Total_Point"])
    except Exception as e:
        print("Error in Total_Point:", e)

    # Agrega el diccionario a la lista player_data
    player_data3.append(data_dic3)

    # Imprimir el diccionario para verificar su contenido
    print("Player Dictionary:", data_dic3)
    print("=================")

##################################################

# Convierte la lista de diccionarios a un DataFrame de pandas
df3 = pd.DataFrame(player_data3)

##################################################

# Quitar el símbolo de la moneda y convertir a valor numérico
df3['Letra_Value_2'] = df3['Value'].str.extract('([MK])', expand=False)

# Obtener valores únicos de 'Value_3'
unique_letra_values = df3['Letra_Value_2'].unique().tolist()
print(unique_letra_values)

# Quitar el símbolo de la moneda y convertir a valor numérico
df3['Value_2'] = df3['Value'].replace('[\€,M,K]', '', regex=True).astype(float)

# Obtener valores únicos de 'Value'
unique_values = df3['Value'].unique().tolist()

# Crear la nueva variable 'Value_limpia'
df3['Value_Millones'] = df3['Value_2']
df3.loc[df3['Letra_Value_2'] == 'K', 'Value_Millones'] = df3['Value_2'] / 1000
df3.loc[df3['Value'] == '€0', 'Value_Millones']  = df3['Value_2']
df3.loc[df3['Letra_Value_2'].isna(), 'Value_Millones'] /= 10000

# Redondear 'Value_limpia' a dos decimales
df3['Value_Millones'] = df3['Value_Millones'].round(2)

# Quitar el símbolo de la moneda y convertir a valor numérico
df3['Letra_Wage_2'] = df3['Wage'].str.extract('([MK])', expand=False)

# Obtener valores únicos de 'Wage_2'
unique_letra_values = df3['Letra_Wage_2'].unique().tolist()
print(unique_letra_values)

# Quitar el símbolo de la moneda y convertir a valor numérico
df3['Wage_2'] = df3['Wage'].replace('[\€,M,K]', '', regex=True).astype(float)

# Obtener valores únicos de 'Value'
unique_wages = df3['Wage_2'].unique().tolist()

# Crear la nueva variable 'Wage_limpia' con ambas condiciones
df3['Wage_Miles'] = df3['Wage_2'].copy()
df3.loc[df3['Letra_Wage_2'].isna(), 'Wage_Miles'] /= 1000

# Redondear 'Value_limpia' a dos decimales
df3['Wage_Miles'] = df3['Wage_Miles'].round(2)

# Imprimir la lista de valores únicos
print(df3)

##################################################

# Cambiar el nombre del DataFrame a df_nuevo
df_nuevo3 = df3.copy()  # Para evitar modificar el DataFrame original
df_nuevo3.name = 'df_nuevo'

# Ahora df_nuevo es simplemente una referencia al DataFrame original con un nuevo nombre
print(df_nuevo3)

##################################################

player_data4 = []

for offset in range(0, 2):
    url4 = url_4 + str(offset * 61)

    # Realizar la solicitud con encabezados y retraso
    p_html4 = requests.get(url4, headers=headers)

    # Verificar si la solicitud fue exitosa antes de procesar la respuesta
    if p_html4.status_code == 200:
        p_soup4 = p_html4.text
        data4 = Soup(p_soup4, 'html.parser')
        table4 = data4.find('tbody')
print(table4)

##################################################

# Define la lista de player_data4 antes del bucle
player_data4 = []

for i in table4.findAll('tr'):
    data_dic = {}
    td = i.findAll('td')

    # Imprimir información para depuración
    print("=== New Player ===")

    try:
        data_dic["picture"] = td[0].find('img').get('data-src')
        print("Picture:", data_dic["picture"])
    except Exception as e:
        print("Error in picture:", e)

    try:
        data_dic["ID"] = td[0].find('img').get('id')
        print("ID:", data_dic["ID"])
    except Exception as e:
        print("Error in ID:", e)

    try:
        data_dic["flag"] = td[1].find('img').get('data-src')
        print("Flag:", data_dic["flag"])
    except Exception as e:
        print("Error in flag:", e)

    try:
        data_dic["Name"] = td[1].find("a").text
        print("Name:", data_dic["Name"])
    except Exception as e:
        print("Error in Name:", e)

    try:
        data_dic["Age"] = int(td[2].text.strip())
        print("Age:", data_dic["Age"])
    except Exception as e:
        print("Error in Age:", e)

    try:
        pos_tags = td[1].find_all("span")
        positions = [tag.text for tag in pos_tags]
        data_dic["Position"] = ", ".join(positions)
        print("Position:", data_dic["Position"])
    except Exception as e:
        print("Error in Position:", e)

    try:
        data_dic["Overall"] = td[3].find('span').text
        print("Overall:", data_dic["Overall"])
    except Exception as e:
        print("Error in Overall:", e)

    try:
        data_dic["Potential"] = td[4].find('span').text
        print("Potential:", data_dic["Potential"])
    except Exception as e:
        print("Error in Potential:", e)

    try:
        data_dic["Team_image"] = td[5].find('img').get('data-src')
        print("Team Image:", data_dic["Team_image"])
    except Exception as e:
        print("Error in Team Image:", e)

    try:
        data_dic["Team"] = td[5].find('a').text
        print("Team:", data_dic["Team"])
    except Exception as e:
        print("Error in Team:", e)

    try:
        data_dic["Value"] = td[6].text.strip()
        print("Value:", data_dic["Value"])
    except Exception as e:
        print("Error in Value:", e)

    try:
        data_dic["Wage"] = td[7].text.strip()
        print("Wage:", data_dic["Wage"])
    except Exception as e:
        print("Error in Wage:", e)

    try:
        data_dic["Total_Point"] = td[8].text.strip()
        print("Total_Point:", data_dic["Total_Point"])
    except Exception as e:
        print("Error in Total_Point:", e)

    # Agrega el diccionario a la lista player_data4
    player_data4.append(data_dic)

    # Imprimir el diccionario para verificar su contenido
    print("Player Dictionary:", data_dic)
    print("=================")

##################################################

# Convierte la lista de diccionarios a un DataFrame de pandas
df4 = pd.DataFrame(player_data4)

# Imprime el DataFrame
print(df4)

##################################################

# Quitar el símbolo de la moneda y convertir a valor numérico
df4['Letra_Value_2'] = df4['Value'].str.extract('([MK])', expand=False)

# Obtener valores únicos de 'Value_2'
unique_letra_values = df4['Letra_Value_2'].unique().tolist()
print(unique_letra_values)

# Quitar el símbolo de la moneda y convertir a valor numérico
df4['Value_2'] = df4['Value'].replace('[\€,M,K]', '', regex=True).astype(float)

# Obtener valores únicos de 'Value'
unique_values = df4['Value'].unique().tolist()

# Crear la nueva variable 'Value_limpia'
df4['Value_Millones'] = df4['Value_2']
df4.loc[df4['Letra_Value_2'] == 'K', 'Value_Millones'] = df4['Value_2'] / 1000
df4.loc[df4['Value'] == '€0', 'Value_Millones']  = df4['Value_2']
df4.loc[df4['Letra_Value_2'].isna(), 'Value_Millones'] /= 10000

# Redondear 'Value_limpia' a dos decimales
df4['Value_Millones'] = df4['Value_Millones'].round(2)

# Quitar el símbolo de la moneda y convertir a valor numérico
df4['Letra_Wage_2'] = df4['Wage'].str.extract('([MK])', expand=False)

# Obtener valores únicos de 'Wage_2'
unique_letra_values = df4['Letra_Wage_2'].unique().tolist()
print(unique_letra_values)

# Quitar el símbolo de la moneda y convertir a valor numérico
df4['Wage_2'] = df4['Wage'].replace('[\€,M,K]', '', regex=True).astype(float)

# Obtener valores únicos de 'Value'
unique_wages = df4['Wage_2'].unique().tolist()

# Crear la nueva variable 'Wage_limpia' con ambas condiciones
df4['Wage_Miles'] = df4['Wage_2'].copy()
df4.loc[df4['Letra_Wage_2'].isna(), 'Wage_Miles'] /= 1000

# Redondear 'Value_limpia' a dos decimales
df4['Wage_Miles'] = df4['Wage_Miles'].round(2)

# Imprimir la lista de valores únicos
print(df4)

##################################################

# Cambiar el nombre del DataFrame a df4_nuevo
df_nuevo4 = df4.copy()  # Para evitar modificar el DataFrame original
df_nuevo4.name = 'df_nuevo4'

##################################################
################## MERGE #########################
##################################################

def merge_all_dfs():
    # Concatenar todos los DataFrames
    combined_df = pd.concat([df_nuevo, df_nuevo2, df_nuevo3, df_nuevo4], ignore_index=True)
    return combined_df

# Llamar a la función y guardar el resultado en un nuevo DataFrame
final_merged_df = merge_all_dfs()

# Puedes imprimir o guardar final_merged_df según tus necesidades
print(final_merged_df)

# Cambiar el nombre del DataFrame a df_nuevo para evitar modificar el DataFrame original
df_nuevo = final_merged_df.copy() 
df_nuevo.name = 'df_nuevo'

# Intenta convertir la columna 'Potential' a tipo numérico
df_nuevo['Potential'] = pd.to_numeric(df_nuevo['Potential'], errors='coerce')

# Calcula cuartiles para Value, Wage y Potential
value_quartiles = pd.qcut(df_nuevo['Value_Millones'], q=[0, 0.25, 0.5, 0.75, 1], labels=['Muy Bajo', 'Bajo', 'Alto', 'Muy Alto'])
wage_quartiles = pd.qcut(df_nuevo['Wage_Miles'], q=[0, 0.25, 0.5, 0.75, 1], labels=['Muy Bajo', 'Bajo', 'Alto', 'Muy Alto'])
potential_quartiles = pd.qcut(df_nuevo['Potential'], q=[0, 0.25, 0.5, 0.75, 1], labels=['Muy Bajo', 'Bajo', 'Alto', 'Muy Alto'])

# Combina las etiquetas para obtener categorías combinadas
df_nuevo['indicador'] = (
    value_quartiles.astype(str) + ' Value, ' +
    wage_quartiles.astype(str) + ' Wage, ' +
    potential_quartiles.astype(str) + ' Potential'
)

#Nos quedamos con las variables de interes
columnas_seleccionadas = ['Name', 'Value_Millones', 'Wage_Miles', 'Potential', 'indicador', 'Age', 'Team', 'picture',	'ID',	'flag',	'Position',	'Team_image']
df_nuevo = df_nuevo[columnas_seleccionadas]

# Ahora df_nuevo es simplemente una referencia al DataFrame original con un nuevo nombre
print(df_nuevo)

##################################################
################GRAFICOS##########################
##################################################

# Crear una figura y ejes para el scatter plot
fig, ax = plt.subplots()

# Obtener una lista única de equipos
equipos_unicos = df_nuevo['Team'].unique()

# Asignar un color único a cada equipo
colores_equipos = plt.cm.get_cmap('viridis', len(equipos_unicos))

# Mapear cada equipo a su color correspondiente
colores_por_equipo = {equipo: colores_equipos(i) for i, equipo in enumerate(equipos_unicos)}

# Crear un scatter plot con colores por equipo
scatter = ax.scatter(
    df_nuevo['Wage_Miles'],
    df_nuevo['Value_Millones'],
    c=df_nuevo['Team'].map(colores_por_equipo),
    cmap='viridis',  # Puedes cambiar el mapa de colores según tus preferencias
)

# Configurar ejes y etiquetas
ax.set_xlabel('Wage_Miles')
ax.set_ylabel('Value_Millones')
ax.set_title('Scatter Plot de Wage_Miles vs Value_Millones por Equipo')

# Agregar una leyenda
legend = ax.legend(*scatter.legend_elements(), title='Equipos')
ax.add_artist(legend)

# Mostrar el scatter plot
plt.show()

###############################################################
# Crear un gráfico de dispersión interactivo con plotly express
fig = px.scatter(
    df_nuevo,
    x='Wage_Miles',
    y='Value_Millones',
    color='Team',
    hover_name='Team',  # Puedes cambiar esto según lo que quieras mostrar al posicionar el ratón
    hover_data=['Name'],  # Puedes agregar más información para mostrar al posicionar el ratón
    title='Scatter Plot de Wage_Miles vs Value_Millones por Equipo',
)

# Mostrar el gráfico interactivo
fig.show()

##################################################
############GUARDAMOS EL CSV######################
##################################################

# Supongamos que final_merged_df es tu DataFrame
df_nuevo = merge_all_dfs()

# Especifica la ruta y el nombre del archivo CSV
ruta_csv = '/jugadores_promesa/tabla_jugadores.csv'

# Guarda el DataFrame en un archivo CSV
df_nuevo.to_csv(ruta_csv, index=False)

##################################################
##################################################
##################################################
##################################################
############Cargar datos  a PostgreSQL############
##################################################
##################################################
##################################################

# Parámetros de conexión a la base de datos PostgreSQL
db_params = {
    'host': 'postgres',
    'port': '5432',
    'user': 'scout_barcelona',
    'password': 'mesqueunclub',
    'database': 'tabla_jugadores'
}

# Establecer la conexión con la base de datos
connection = psycopg2.connect(**db_params)

# Crear un motor SQLAlchemy usando la conexión PostgreSQL
engine = create_engine(f"postgresql+psycopg2://{db_params['user']}:{db_params['password']}@{db_params['host']}:{db_params['port']}/{db_params['database']}")

# Nombre de la tabla en la base de datos PostgreSQL
tabla_jugadores = 'tabla_jugadores'

# Cargar el DataFrame en la tabla existente o crear una nueva
df_nuevo.to_sql(tabla_jugadores, engine, if_exists='replace', index=False)

# Cerrar la conexión
connection.close()


##################################################
##################################################
##################################################
##################################################
##################################################
##################################################