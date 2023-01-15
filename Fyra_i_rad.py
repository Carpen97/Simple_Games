####################
# ---> READ ME <---#
# Kör 'pip install PySimpleGUI' i termninalen för att 
# ladda hem biblioteket så kan du köra koden

import PySimpleGUI as sg

#Definierar variabler för utseende. Testa gärna att ändra
WINDOW_TITLE = 'FYRA I RAD'
BUTTON_WIDTH = 5
BUTTON_HEGIHT = 2
BUTTON_FONT = ("Arial", 20)
PLAYER_1_COLOR = 'red'
PLAYER_2_COLOR = 'blue'
NEUTRAL_COLOR = 'white'
TEXT_COLOR = 'gold'
DISPLAY_COORDINATES = False
X_LENGTH = 7
Y_LENGTH = 6

#Backend datastruktuerena
isPlayerOnesTurn = True #Håller koll på vems tur det är
board = [[] for _ in range(X_LENGTH)]

#Frontend
layout = []
for j in range(Y_LENGTH):
    row = []
    for i in range(X_LENGTH):
        button = sg.Button(
            f'X:{i},Y:{Y_LENGTH-1-j}' if DISPLAY_COORDINATES else '', #Text på knappen
            key = f'Type:BUTTON,X:{i},Y:{Y_LENGTH-1-j}',
            button_color = (TEXT_COLOR, NEUTRAL_COLOR),
            size = (BUTTON_WIDTH, BUTTON_HEGIHT),
            font = BUTTON_FONT
        )
        row.append(button)
    layout.append(row)
window = sg.Window(WINDOW_TITLE, layout)


def parse_button(key):
    temp = key.split(',') # A list where we split the string on ","
    x = int(temp[1].split(':')[-1])
    y = int(temp[2].split(':')[-1])
    return x, y

def coordinates_to_button_key(x,y):
    return f'Type:BUTTON,X:{x},Y:{y}'

def paint_board(board): #Används för att uppdatera färgerna på alla "buttons" i fönstret aka variabeln "window"
    for x in range(X_LENGTH):
        max_y = len(board[x])
        for y in range(Y_LENGTH):
            key = coordinates_to_button_key(x,y)
            color = board[x][y] if y < max_y else NEUTRAL_COLOR
            window[key].update(
                button_color = color,
                text = ""
            )
    """
    for x, column in enumerate(board): 
        for y, cell_color in enumerate(column):
            key = coordinates_to_button_key(x,y)
            window[key].update(
                button_color = cell_color,
                text = ""
            )
    """

def print_board(board): #Används för att skriva ut brädet i terminalen
    print('----------------  BOARD  ------------------')
    for index, col in enumerate(board):
        print(f'Column {index}:' + str(col))
    print('-------------------------------------------')

def is_game_over(board): #Ska användas för att avgöra om spelet är över dvs då returna True istället

    def is_cell_occupied(x,y):# Hjälp funktion
        return y < len(board[x])

    def is_valid_cell_coordinate(x,y):# Hjälp funktion
        return 0 <= x < X_LENGTH and 0 <= y < Y_LENGTH

    def get_victory_coordinates(start_x, start_y, n_steps, dx, dy):
        return [(start_x + dx*steps, start_y + dy*steps) for steps in range(n_steps+1)]

    for x in range(X_LENGTH):

        for y in range(len(board[x])):
            color = board[x][y]

            for direction in [(1,0),(1,1),(0,1),(-1,1)]:
                dx, dy = direction
                is_winning = True

                #print(f'DIRECTION: {direction}, COLOR: {color}')

                for n_steps in range(1,4):
                    #Beräknar koordinaten vi vill kolla på
                    target_x = x + dx*n_steps
                    target_y = y + dy*n_steps

                    if not is_valid_cell_coordinate(target_x,target_y):
                        #print("STOP! Cause: is_not_valid_cell_coordinate")
                        #print(f'X:{x}, Y:{y}, TARGET: {target_x},{target_y}, STEPS: {n_steps}')
                        is_winning = False
                        break

                    if not is_cell_occupied(target_x,target_y):
                        #print("STOP! Cause: cell_is_not_occupied")
                        #print(f'X:{x}, Y:{y}, TARGET: {target_x},{target_y}, STEPS: {n_steps}')
                        is_winning = False
                        break
                    
                    if not board[target_x][target_y] == color:
                        #print(f'STOP! Cause: Not the right color. Target color was {board[target_x][target_y]}')
                        #print(f'X:{x}, Y:{y}, TARGET: {target_x},{target_y}, STEPS: {n_steps}')
                        is_winning = False
                        break
                
                if is_winning:
                    victory_coordinates = get_victory_coordinates(x, y, n_steps, dx, dy)
                    return True, color, victory_coordinates, direction

    return False, None, None, None

def is_legal_move(board,x):
    return len(board[x]) < Y_LENGTH

#Dictionary for drawing on buttons with strings
directions_to_patterns={
    (1, 0): "O O O",
    (1, 1): "        O\nO\nO        ",
    (0, 1): "O\nO\nO",
    (-1,1): "O        \nO\n        O",
}

def reset_game():
    global board, isPlayerOnesTurn
    isPlayerOnesTurn = True 
    board = [[] for _ in range(X_LENGTH)]

def display_main_menu(winner):
    text = f'{winner.capitalize()} player has won the game!'
    layout = [
        [sg.Text(text=text, key="text")],
        [sg.Button("Play again", key="restart"), sg.Button("Exit", key="exit")]
        ]
    event, values = sg.Window("Main Window", layout).read(close = True)
    return event

while True: #Game loop
    event, values = window.read() # Läs input från fönstret i början av varje loop
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    
    if 'Type:BUTTON' in event: # Var eventet en knapp tryckning?

        x, y = parse_button(event) # Parsea koordinaterna för knappen

        color = PLAYER_1_COLOR if isPlayerOnesTurn else PLAYER_2_COLOR #Bestäm vilken färg nästa "polett" ska ha.
        
        if is_legal_move(board,x):
            #Make the move
            board[x].append(color)
            isPlayerOnesTurn = not isPlayerOnesTurn #Swap turn inbetween events
        else:
            sg.Popup(f'Illegal move. Please pick another column!', keep_on_top=True)

        paint_board(board)

    #event is the key of the latest 'update' of the window
    print('EVENT:' + event)
    print_board(board)

    game_over, winner, victory_coordinates, direction = is_game_over(board)#<--- Denna funktionen bevhöver implementeras
    if game_over:
        for x, y in victory_coordinates:
            window[coordinates_to_button_key(x,y)].update(text = directions_to_patterns[direction])
        feed_back = display_main_menu(winner)
        if feed_back == 'restart':
            reset_game()
            paint_board(board)
        else:
            break

window.close()