#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 23:50:23 2023

@author: Baudouin
"""

#%%Importing Libraries

import pandas as pd
import numpy as np

#%%Importing data
table_1 = pd.read_csv('/Users/Baudouin/Desktop/Chess_exploration/dataset/table_1.csv')
table_2 = pd.read_csv('/Users/Baudouin/Desktop/Chess_exploration/dataset/table_2.csv')
table_3 = pd.read_excel('/Users/Baudouin/Desktop/Chess_exploration/dataset/Table_3.xlsx')
table_4 = pd.read_csv('/Users/Baudouin/Desktop/Chess_exploration/dataset/table_4.csv')
dataset = [table_1,table_2,table_3,table_4]

#%%Data exploration
def inital_exploration(table):
    print(table.info())
    print(table.isnull().sum())
    for col in table.columns.to_list():
        print(table[col].value_counts())
        
for table in dataset:
    print(f"###{table}###")
    inital_exploration(table)
    
#Table 1 : process date and time, encode game_type, encode outcome
#Table 2 : drop extra index col, rename columns, drop +- col, turn avg col in int
#Table 3 : compare eco codes with values in table_1 drop extra index col
#Table 4 : drop extra index col

#%%Table 1
#drop null values
table_1 = table_1.dropna()
#manage date and time
table_1['year']=table_1['date'].apply(lambda x : x.split('.')[0])
table_1['month']=table_1['date'].apply(lambda x : x.split('.')[1])
table_1['day']=table_1['date'].apply(lambda x : x.split('.')[2])
table_1['hour']=table_1['time'].apply(lambda x : x.split(':')[0])
table_1['minute']=table_1['time'].apply(lambda x : x.split(':')[1])
table_1['second']=table_1['time'].apply(lambda x : x.split(':')[2])
table_1.drop(['date','time'],axis=1,inplace=True)
table_1['datetime'] = pd.to_datetime(table_1[['year', 'month', 'day', 'hour', 'minute', 'second']],
                                format='%Y-%m-%d %H:%M:%S')
table_1.drop(['year','month','day','hour','minute','second'],axis=1,inplace=True)

#encode game type


def game_type(cell):
    if '/' in cell :
        gametype = 'daily'
    elif '+' in cell:
        if int(cell.split('+')[0])<600:
            gametype = 'blitz bullet'
        else :
            gametype = 'rapid bullet'
    elif int(cell)<600:
        gametype = 'blitz'
    elif int(cell)<=3600:
        gametype='rapid'
    else:
        gametype='long'
    return gametype
        
table_1['gt']=table_1['game_type']        
table_1.drop('game_type',axis=1,inplace=True)
table_1['game_type'] = table_1['gt'].apply(lambda x : game_type(x))       
table_1['game_length_in_seconds']=table_1['gt'].apply( lambda x : '-' if '/' in x else x.split('+')[0])
table_1.drop('gt',axis=1,inplace=True)   
        
#encode outcome
def outcome(outcome, player_id, opponent):
    if 'drawn' in outcome:
        gameoutcome = 0.5
    elif player_id in outcome:
        gameoutcome = 1
    elif opponent in outcome:
        gameoutcome = 0
    else:
        gameoutcome = '-'
    return gameoutcome

table_1['out'] = table_1['outcome']
table_1.drop('outcome',axis=1,inplace=True)
table_1['outcome'] = table_1.apply(lambda row : outcome(row['out'],row['player_id'],row['opponent']), axis=1)
table_1['end'] = table_1['out'].apply(lambda x : x.split(' ')[-1])      
table_1.drop('out',axis=1,inplace=True)      
table_1.drop('Unnamed: 0',axis=1,inplace=True)   

#encode game moves
def pgn_to_move_list(string):
    a = string.split(' { ')
    a = [i.split(' } ')[1] if ' } ' in i else i for i in a]
    a = a[:-1]
    a = [i.split('... ')[-1] if '... ' in i else i.split('. ')[-1] for i in a]
    return a

table_1['moves']=table_1['game'].apply(pgn_to_move_list)

#calculate the number of moves in a game

table_1['moves_count']=table_1['moves'].apply(lambda x : len(x))

for i in range(5):
    table_1[f"move {i+1}"] = table_1['moves'].apply(lambda x : x[i] if i<len(x) else '-')
table_1.drop(table_1['game'],inplace= True)       
       
 #%%Table 2
#dropping useless features
col_to_drop = ['Unnamed: 0',  'Avg12M']
table_2.drop(col_to_drop,axis=1,inplace=True)       
#renaming columns
new_col_name = [['name', 'fed', 'rating', 'birth_year']]      
table_2.columns =  new_col_name    
#turning avg_rating_over_12_months in an integer:

#%% Table 3
table_1['ECO'].value_counts
a = []
table_1['ECO'].apply(lambda x : a.append(x))
a = sorted(list(set(a)))
b=[]
table_3['ECO'].apply(lambda x : b.append(x))
b = sorted(list(set(b)))
c = [i for i in a if i not in b]

#%% Table 4
table_4.drop('Unnamed: 0', axis = 1, inplace = True)


#%% Save cleaned databases
table_1.to_csv('/Users/Baudouin/Desktop/Chess_exploration/dataset/table_1.csv')
table_2.to_csv('/Users/Baudouin/Desktop/Chess_exploration/dataset/table_2.csv')
table_3.to_csv('/Users/Baudouin/Desktop/Chess_exploration/dataset/table_3.csv')
table_4.to_csv('/Users/Baudouin/Desktop/Chess_exploration/dataset/table_4.csv')




