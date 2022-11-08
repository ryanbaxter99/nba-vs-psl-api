import matplotlib.pyplot as plt
import sqlite3
import os
import json


def setUpDatabase(db_name):
    '''
    Create the database and return the cursor and connection objects.
    Used in this function to update databses
    '''
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def doCalc(filename):
    '''
    Do the Calculations:
    - Get the average height of each player by position (0-3)
    Imput is json file that holds the data.
    The new calculations are outputted to the json file as new key 'Premier_League'
    '''
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as jsonFile:
       data = json.load(jsonFile)
    

    cur, conn = setUpDatabase('sports.db')
    cur.execute('SELECT height, position FROM Premier_League')

    player_heights = cur.fetchall()
    defender = []
    attacker = []
    goalkeeper = []
    mid = []
    for val in player_heights:
        if val[1] == 0:
            attacker.append(val[0])
        elif val[1] == 1:
            mid.append(val[0])
        elif val[1] == 2:
            defender.append(val[0])
        elif val[1] == 3:
            goalkeeper.append(val[0])

    avg_attacker = sum(attacker) / len(attacker)
    avg_mid = sum(mid) / len(mid)
    avg_defender = sum(defender) / len(defender)
    avg_goalie = sum(goalkeeper) / len(goalkeeper)

    data['Premier_League'] = {'Attacker': avg_attacker, 'Midfielder': avg_mid, 'Defender': avg_defender, 'Goalkeeper': avg_goalie}
    data['PL_Player_Positions'] = {'Attacker': len(attacker), 'Midfielder': len(mid), 'Defender': len(defender), 'Goalie': len(goalkeeper)}

    with open(full_path, 'w') as f:
       json.dump(data, f, indent=4)    
    

def height_by_position_PLviz(filename):
    '''
    Create the visual for the bar chart.
    The bar chart displays the average height for players
    per their positon in the Premier League. 
    Input is json file with the data and output is the visual
    '''
    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as jsonFile:
        data = json.load(jsonFile)
    
    heights = data['Premier_League'].values()
    positions = data['Premier_League'].keys()

    plt.bar(positions, heights, align='center', alpha=0.5, color=['green', 'cyan', 'orange', 'magenta'], edgecolor='black')
    plt.ylabel('Average Heights (inches)')
    plt.xlabel('Positions')
    plt.title('Average Height By Position for Players in the Premier Soccer League')
    plt.ylim(50, 80)

    plt.show()

def position_PLviz(filename):
    '''
    Create the second visual for the Soccer data-- extra credit additional visualization
    The bar chart displays the numbers of players in each position in the Premier League
    Input is json file with the data and output is the visual
    '''

    full_path = os.path.join(os.path.dirname(__file__), filename)
    with open(full_path, 'r') as jsonFile:
        data = json.load(jsonFile)

    num_players = data['PL_Player_Positions'].values()
    positions = data['PL_Player_Positions'].keys()

    plt.bar(positions, num_players, align='center', alpha=0.5, color=['purple', 'red', 'yellow', 'blue'], edgecolor='black')
    plt.ylabel('Number of Players')
    plt.xlabel('Positions')
    plt.title('Positions for Soccer in Premier League')

    plt.show()

 
if __name__ == '__main__':
    doCalc('data.json')
    height_by_position_PLviz('data.json')
    position_PLviz('data.json')