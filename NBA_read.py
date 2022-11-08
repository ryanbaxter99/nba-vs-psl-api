import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import sqlite3
import os
import json


def setUpDatabase(db_name):
    '''
    Create the database and return the cursor and connection objects.
    Used in this function to update databses
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + db_name)
    cur = conn.cursor()
    return cur, conn

def heightCalculations(filename):
    '''
    Do the Calculations:
    - Get the average height of each player by position which is labled 0-3
    and pushes the players into list by their position.
    Imput is json file that holds the data.
    The new calculations are outputted to the json file as new key 'NBA'
    '''
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as jsonFile:
       data = json.load(jsonFile)
    
    cur, conn = setUpDatabase('sports.db')
    db_data = cur.execute('SELECT PlayerHeight.height, IDs.position FROM PlayerHeight JOIN IDs ON PlayerHeight.NBA_id = IDs.NBA_id').fetchall()

    guard = []
    center = []
    forward = []
    mixed = []

    for val in db_data:
        if val[1] == 0:
            mixed.append(val[0])
        elif val[1] == 1:
            forward.append(val[0])
        elif val[1] == 2:
            center.append(val[0])
        else:
            guard.append(val[0])

    avg_Guard = sum(guard) / len(guard)
    avg_Center = sum(center) / len(center)
    avg_Forward = sum(forward) / len(forward)
    avg_mixed = sum(mixed) / len(mixed)


    data['NBA'] = {'Avg Guard Height': avg_Guard, 'Avg Center Height': avg_Center, 'Avg Forward Height': avg_Forward, 'Avg Mixed Height': avg_mixed}
    data['NBA_Player_Positions'] = {'Guard': len(guard), 'Center': len(center), 'Forward': len(forward), 'Mixed': len(mixed)}

    with open(full_path, 'w') as f:
       json.dump(data, f, indent = 4)  

def height_by_position_NBAviz(filename):
    '''
    Create the visual for the bar chart.
    The bar chart displays the average height for players
    per their positon in the NBA. 
    Input is json file with the data and output is the visual
    '''
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as jsonFile:
        data = json.load(jsonFile)

    heights = data['NBA'].values()
    positions = data['NBA'].keys()
    gs = gs = gridspec.GridSpec(1, 1)
    fig = plt.figure()
    viz1 = fig.add_subplot(gs[0, 0])

    viz1.bar(positions, heights, align='center', alpha=0.5, color=['red', 'yellow', 'purple', 'cyan'], edgecolor='black')
    viz1.set(ylabel='Average Height (inches)', xlabel='Positions', title='Average Heights By Position for Basketball Players in the NBA')
    plt.show()

def position_NBAviz(filename):
    '''
    Create the second visual for the NBA data-- extra credit additional visualization
    The bar chart displays the numbers of players in each position in the NBA
    Input is json file with the data and output is the visual
    '''

    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as jsonFile:
        data = json.load(jsonFile)

    num_players = data['NBA_Player_Positions'].values()
    positions = data['NBA_Player_Positions'].keys()

    plt.bar(positions, num_players, align='center', alpha=0.5, color=['green', 'magenta', 'blue', 'orange'], edgecolor='black')
    plt.ylabel('Number of Players')
    plt.xlabel('Positions')
    plt.title('Positions for Basketball in NBA')

    plt.show()
    
if __name__ == '__main__':
    heightCalculations('data.json')
    height_by_position_NBAviz('data.json')
    position_NBAviz('data.json')


