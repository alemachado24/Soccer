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
# st.markdown("Soccer Forecast ⚽️")

# @st.cache
# def nba_logo():
#     '''
#     Function to pull Soccer stats from Pro Football Reference (https://www.pro-football-reference.com/).
#     - team : team name (str)
#     - year : year (int)
#     '''
#     # pull data
#     url = f'https://www.basketball-reference.com/leagues/NBA_2023.html'
#     html = requests.get(url).text
#     soup = BeautifulSoup(html,'html.parser')
#     table = soup.find("img",class_="teamlogo")
#     logo = table['src']
#     return logo

option1, option2 = st.columns(2)
with option1:
    st.title('Forecast from FiveThirtyEight')
with option2:
    st.text('')
#     st.image(nba_logo(),width=150)



st.sidebar.markdown("This app performs simple webscraping of Soccer player stats data")
st.sidebar.markdown("Data Sources: fivethirtyeight")

#sidebar
# selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990,2024))))

# general_stats, upcoming_games = st.tabs(["Standing Forecast", "Upcoming Games & Stats"])

##############################################################################################################################
############################################         Standing Forecast            ############################################
##############################################################################################################################

# with general_stats:

# st.header(f'Soccer Forecast from FiveThirtyEight ')
#---------------------------------538 Prediction Table
# @st.cache
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


    
    #---------------------------------End Of 538 Prediction Table


##############################################################################################################################
############################################           Upcoming Games             ############################################
##############################################################################################################################

# with upcoming_games:


#     #---------------------------------Week Forecast & Upcomming Games
#     row1_1, row1_2 = st.columns((3, 3))#st.columns(2)

#     with row1_1:

#         st.write(f'Games Win Probabilities in {selected_year} from FiveThirtyEight ')
#         #------------- webscrap for elo
#     #         @st.cache(hash_funcs={pd.DataFrame: lambda _: None})
#         @st.cache
#         def get_new_data538_games(year):
#             '''
#             Function to pull NFL stats from 538 Reference (https://projects.fivethirtyeight.com/2022-nfl-predictions/).
#             - year : year (int)
#             '''
#             # pull data
#             url = f'https://projects.fivethirtyeight.com/{selected_year}-nba-predictions/games/'
#             html = requests.get(url).text

#             soup = BeautifulSoup(html,'html.parser')

#             table2 = soup.find_all(class_=["day","h4","tr"])

#     #             st.write(table2)

#             data_tocheck = []

#             for tablerow in table2:
#                 data_tocheck.append([tabledata.get_text(strip=True) for tabledata in tablerow.find_all('h3')])
#                 data_tocheck.append([tabledata.get_text(strip=True) for tabledata in tablerow.find_all('th')])
#                 data_tocheck.append([tabledata.get_text(strip=True) for tabledata in tablerow.find_all('td')])


#             df_tocheck = pd.DataFrame(data_tocheck)
#     #             st.dataframe(df_tocheck)

#             index = [0,1,2,3,4,9]
#             df_tocheck2 = df_tocheck.iloc[:,index].copy()

#             col_names = ['Date','Time', 'Team', 'Spread', 'Probability','To Leave']
#             df_tocheck2.columns = col_names

#     #             st.dataframe(df_tocheck2)

#     #             df_tocheck2 = df_tocheck2[df_tocheck2.Date.notnull()]
#     #             df_tocheck2 = df_tocheck2[df_tocheck2.Time.notnull()]
#             df_tocheck2["Time"].fillna("Replace", inplace = True)
#             df_tocheck2["To Leave"].fillna("To Leave", inplace = True)
#             df_tocheck2['To Leave'] = np.where((df_tocheck2['Date']=='') & (df_tocheck2['Time']=='Replace') , 'To Remove', df_tocheck2['To Leave'])
#             df_tocheck2['To Leave'] = df_tocheck2['To Leave'].str.replace('Score','To Leave Not')

#     #             df_tocheck2['To Leave'] = df_tocheck2['Date'].str.replace('Score','To Leave')
#             df_tocheck2['Team'] = df_tocheck2['Team'].str.replace('RAPTOR spread','')
#             df_tocheck2['Spread'] = df_tocheck2['Spread'].str.replace('Win prob.','')
#             df_tocheck2['Probability'] = df_tocheck2['Probability'].str.replace('Score','')
#             df_tocheck2['Time'] = df_tocheck2['Time'].str.replace('Replace','')
#             df_tocheck2["Team"].fillna("", inplace = True)
#             df_tocheck2["Spread"].fillna("", inplace = True)
#             df_tocheck2["Probability"].fillna("", inplace = True)
#             df_tocheck2["Date"].fillna("", inplace = True)



#             return df_tocheck2


#         testFrame2=pd.DataFrame(get_new_data538_games(selected_year))
#         testFrame=pd.DataFrame(testFrame2)

#         new_value_time = []
#         new_value_date = []
#         time_column=[]
#         date_column=[]

#         for column in testFrame['Date'].iteritems():
#         #     print(column[0])
#             if column[1]!='':
#                 new_value_date=column[1]
#                 date_column.append(new_value_date)
#         #         print(new_value)
#             elif column[1]=='':
#                 date_column.append(new_value_date)

#         date_column_df=pd.DataFrame(date_column, columns=['Game Date'])



#         for column in testFrame['Time'].iteritems():
#         #     print(new_value_time)
#         #     print(column[1])
#             if column[1] == '' and new_value_time == []:
#         #         print('aca')
#                 time_column.append('first')
#             elif column[1]!='':
#                 new_value_time=column[1]
#                 time_column.append(new_value_time)
#         #         print(new_value)
#             elif column[1]=='':
#                 time_column.append(new_value_time)
#     #             time_column

#         time_column_df=pd.DataFrame(time_column, columns=['Game Time'])

#         combined_list = pd.concat([date_column_df,time_column_df], axis=1)
#         combined_list2 = pd.concat([combined_list,testFrame],ignore_index=True, axis=1) #['To Leave']=='To Leave'

#         col_names2 = ['Date','Time','NoDate','NoTime', 'Team', 'Spread', 'Probability','To Leave']
#         combined_list2.columns = col_names2
#         combined_list2=combined_list2.loc[combined_list2['To Leave']=='To Leave']
#         combined_list2=combined_list2.drop(['NoDate','NoTime','To Leave'], axis=1)
#         all_combined=combined_list2.loc[combined_list2['Team']!='']
#         all_combined=all_combined.loc[all_combined['Time']!='FINAL']
#     #         st.dataframe(all_combined)


#         def color_negative_red(val):
#             '''
#             highlight the maximum in a Series yellow.
#             '''
#             color = 'lightgreen' if str(val) > str(80) else 'white'
#             return 'background-color: %s' % color
#         s = all_combined.style.applymap(color_negative_red, subset=['Probability'])
#     #         st.text('')
#     #         st.text('')
#     #         st.text('')
#     #         st.text('')
#     #         st.text('')
#         st.dataframe(s)


        
