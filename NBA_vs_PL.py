import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import sqlite3
import os
import json

def setUpDatabase(db_name):
    '''
    Create the database and return the cursor and connection objects.
    Used in function to update databses
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

def joinCal(filename):
    '''
    Do the Calculations:
    - Get the average height of all players in the NBA and the Premier Soccer League
    Imput is json file that holds the data.
    The new calculations are outputted to the json file as new key 'NBA_vs_PL'
    '''
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as jsonFile:
       data = json.load(jsonFile)

    total_soccer_height = 0
    total_NBA_height = 0 
    tempCount = 0
    tempCount2 = 0
    
    cur, conn = setUpDatabase('sports.db')
    cur.execute('SELECT height, id FROM Premier_League')
    soccer_data = cur.fetchall()

    #get the total height for the amount of Soccer players in the database
    for height in soccer_data:
        tempCount += 1
        total_soccer_height += height[0]
    
    # get the mean height by dividing by the total amount of Soccer players in the database
    soccer_mean_height = total_soccer_height / tempCount  

    cur, conn = setUpDatabase('sports.db')
    cur.execute('SELECT height, id FROM PlayerHeight')
    NBA_data = cur.fetchall()

    #get the total height for the amount of NBA players in the database
    for height2 in NBA_data:
        tempCount2 += 1
        total_NBA_height += height2[0]
    
    # get the mean height by dividing by the total amount of NBA players in the database
    NBA_mean_height = total_NBA_height / tempCount2 

    data['NBA_vs_PL'] = {'Avg NBA Player Height': NBA_mean_height, 'Avg PL Soccer Player Height': soccer_mean_height}

    with open(full_path, 'w') as f:
       json.dump(data, f, indent = 4)

def constructCombined(filename):
    '''
    Create the visual for the bar chart.
    The bar chart displays average height of all players in the NBA and the Premier Soccer League 
    Input is json file with the data and output is the visual
    '''
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as jsonFile:
        data = json.load(jsonFile)
        
    avg_player_height = data["NBA_vs_PL"].values()
    sport = data["NBA_vs_PL"].keys()

    plt.bar(sport, avg_player_height, align='center', alpha=0.5, color=['#187bcd', 'red'], edgecolor='black')
    plt.ylabel('Player Height (inches)')
    plt.xlabel('NBA vs Premier League')
    plt.title('Avg NBA Player Height vs. Avg Soccer Player Height')
    plt.show()

if __name__ == '__main__':
    joinCal('data.json') 
    constructCombined('data.json')