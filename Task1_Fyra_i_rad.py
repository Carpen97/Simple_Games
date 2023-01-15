####################
# ---> READ ME <---#
# Kör 'pip install PySimpleGUI' i termninalen för att 
# ladda hem biblioteket så kan du köra koden

import PySimpleGUI as sg

#Definierar variabler för utseende. Testa gärna att ändra
WINDOW_TITLE = 'FYRA I RAD'
BUTTON_WIDTH = 10
BUTTON_HEGIHT = 4
PLAYER_1_COLOR = 'red'
PLAYER_2_COLOR = 'yellow'
NEUTRAL_COLOR = 'white'
TEXT_COLOR = 'black'
DISPLAY_COORDINATES = False
X_LENGTH = 7
Y_LENGTH = 6

#Backend datastruktuerena
isPlayerOnesTurn = True #Håller koll på vems tur det är
board = [[] for _ in range(X_LENGTH)]
is_game_over = False

#Frontend
layout = []
for j in range(Y_LENGTH):
    row = []
    for i in range(X_LENGTH):
        button = sg.Button(
            f'X:{i},Y:{Y_LENGTH-1-j}' if DISPLAY_COORDINATES else '', #Text på knappen
            key = f'Type:BUTTON,X:{i},Y:{Y_LENGTH-1-j}',
            button_color = (TEXT_COLOR,NEUTRAL_COLOR),
            size = (BUTTON_WIDTH,BUTTON_HEGIHT)
        )
        row.append(button)
    layout.append(row)
window = sg.Window(WINDOW_TITLE, layout)



def parse_button(key):
    temp = key.split(',') # A list where we split the string on ","
    x = int(temp[1][-1])
    y = int(temp[2][-1])
    return x, y

def coordinates_to_button_key(x,y):
    return f'Type:BUTTON,X:{x},Y:{y}'

def paint_board(): #Används för att uppdatera färgerna på alla "buttons" i fönstret aka variabeln "window"
    for x, column in enumerate(board): 
        for y, cell_color in enumerate(column):
            key = coordinates_to_button_key(x,y)
            window[key].update(button_color = cell_color)

### TODO ###
#Notera i nuläget kan paint_board funktionen skapa ett ERROR om en spelare fortsätter lägga fler än 6 poletter i en column.
#Någon slags safety check behöver implementeras
   

def print_board(board): #Används för att skriva ut brädet i terminalen
    print('----------------  BOARD  ------------------')
    for index, col in enumerate(board):
        print(f'Column {index}:' + str(col))
    print('-------------------------------------------')


### TODO ###
def is_game_over(board): #Ska användas för att avgöra om spelet är över dvs då returna True istället



    #Denna funktionen behöver implementeras


    return False


while True:
    event, values = window.read() # Läs input från fönstret i början av varje loop
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    
    if 'BUTTON' in event: # Var eventet en knapp tryckning?

        x, y = parse_button(event) # Parsea koordinaterna för knappen

        color = PLAYER_1_COLOR if isPlayerOnesTurn else PLAYER_2_COLOR #Bestäm vilken färg nästa "polett" ska ha.
        isPlayerOnesTurn = not isPlayerOnesTurn #Swap turn inbetween events
        
        board[x].append(color)
        paint_board()

    if is_game_over(board):#<--- Denna funktionen bevhöver implementeras
        break#När spelet är slut avslutar vi loopen

    #event is the key of the lasest 'update' of the window
    print('EVENT:' + event)
    print_board(board) 

window.close()