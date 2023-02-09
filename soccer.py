#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import base64
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import io
import re
import plotly.express as px
from PIL import Image

#cd Desktop/AleClasses/Soccer
#streamlit run soccer.py


st.set_page_config(page_title="Soccer", page_icon="⚽️",layout="wide",)

st.sidebar.header("Soccer Forecast ⚽️")


option1, option2 = st.columns(2)
with option1:
    st.title('Forecast from FiveThirtyEight')
with option2:
#     htp5="https://github.com/alemachado24/Soccer/blob/4d34d13b274394ad33104b3deb5ef934dda625e0/soccer_ball.png"
    st.image('https://github.com/alemachado24/Soccer/blob/4d34d13b274394ad33104b3deb5ef934dda625e0/soccer_ball.png')#,caption= 'logo', width=350)
#     st.image(nba_logo(),width=150)


st.sidebar.markdown("This app performs simple webscraping of Soccer player stats data")
st.sidebar.markdown("Data Sources: fivethirtyeight")

@st.cache
def get_new_data538():
    '''
    Function to pull NFL stats from 538 Reference (https://projects.fivethirtyeight.com/2023-nba-predictions/?ex_cid=irpromo).
    - year : year (int)
    '''
    # pull data
    url = f'https://projects.fivethirtyeight.com/soccer-predictions/matches/'
    html = requests.get(url).text
    #to make sure the url is corrext check the .text
#     st.text(url)

    # parse the data
    soup = BeautifulSoup(html,'html.parser')
#     st.header('soup')

    #find the id in the table by inspecting the website
    table = soup.find("table", id="all-matches")
#         st.dataframe(table)

    #find the right body
    gdp_table_body = table.tbody.find("tbody")#[2:] 

    #to find all row values in the table
    gdp_table_data = table.tbody.find_all("tr")#[2:] 
#         st.dataframe(gdp_table_data)

    #it's not for headings, it's for the row data
    headings = []
    for tablerow in gdp_table_data:
        # remove any newlines and extra spaces from left and right
#         headings.append([tabledata.get_text(strip=True) for tabledata in tablerow.find_all('time-league')])
        headings.append([tabledata.get_text(strip=True) for tabledata in tablerow.find("td")])
        headings.append([tabledata.get_text(strip=True) for tabledata in tablerow.find_all("td")])
#     st.dataframe(headings)
#tabledata.get_text(strip=True)

    df = pd.DataFrame(headings)
#         st.dataframe(df)

    #Instead of dropping the columns and selecting the columns I'm going to use
    index = list(range(0,4))
    new_data_standings = df.iloc[:,index].copy()


    #Rename columns
    col_names = ['Date/Team', 'Team Probability', 'Tie Probability','New Column']
    new_data_standings.columns = col_names
    new_data_standings=new_data_standings.loc[new_data_standings['Date/Team']!='']
    new_data_standings["Tie Probability"].fillna("", inplace = True)
    new_data_standings["New Column"].fillna("To Leave", inplace = True)
    new_data_standings['New Column'] = new_data_standings['New Column'].apply(lambda x: 'To Leave' if 'p.m.' in x else x)
    new_data_standings['New Column'] = new_data_standings['New Column'].apply(lambda x: 'To Leave' if 'a.m.' in x else x)
    new_data_standings=new_data_standings.loc[new_data_standings['New Column']=='To Leave']
    new_data_standings['Tie Probability'] = new_data_standings['Tie Probability'].apply(lambda x: 'null' if '%' not in x else x)
    new_data_standings['Tie Probability'] = new_data_standings['Tie Probability'].str.replace('null','')
    new_data_standings=new_data_standings.drop(['New Column'], axis=1)
    
    return new_data_standings

#Dataframe with Standing Predictions from 538

# st.dataframe(get_new_data538())

def color_negative_red(val):
    '''
    highlight the maximum in a Series yellow.
    '''
    color = 'lightgreen' if str(val) > str(55) and len(str(val)) <= 3 else 'white'
    return 'background-color: %s' % color
s = get_new_data538().style.applymap(color_negative_red, subset=['Team Probability'])
#         st.text('')
#         st.text('')
#         st.text('')
#         st.text('')
#         st.text('')
st.dataframe(s)


    
