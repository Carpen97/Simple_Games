import PySimpleGUI as sg
import numpy as np
import copy

W, H = 10,18
BOX_SIZE = 20
PREVIEW_BOX_SIZE = 5

COLOR_CODES = [
    'white',
    'brown',
    'cyan',
    'yellow',
    'red',
    'blue',
    'green',
    'purple',
    'pink'
]

SHAPES = [
    [(0,-1),(0,0),(0,1),(0,2)], #Pinnen
    [(0,0),(0,1),(1,0),(1,1)], #Kvadrat
    [(0,0),(1,0),(-1,0),(0,1)], #Triangeln
    [(0,1),(0,0),(0,-1),(1,-1)], #L
    [(0,1),(0,0),(0,-1),(-1,-1)], #Omvänt L
    [(0,1),(0,0),(-1,0),(-1,-1)], #S
    [(0,1),(0,0),(1,0),(1,-1)], #Omvänt S   
]

SHAPE_CENTERS = [
    (2,1.5), #Pinnen
    (1.5,1.5), #Kvadrat
    (2,1.5), #Triangeln
    (1.5,2), #L
    (2.5,2.5), #Omvänt L
    (2.5,2), #S
    (1.5,2), #Omvänt S   
]

LETTERS = {
    'S' : [(0,0),(1,0),(2,0),(2,1),(2,2),(1,2),(0,2),(0,3),(0,4),(1,4),(2,4)],
    'C': [(0,0),(1,0),(2,0),(0,1),(0,2),(0,3),(0,4),(1,4),(2,4)],
    'O': [(0,0),(1,0),(2,0),(0,1),(0,2),(0,3),(0,4),(1,4),(2,4),(2,1),(2,2),(2,3)],
    'R' : [(0,0),(2,0),(2,1),(1,2),(0,2),(0,3),(0,4),(1,4),(2,4),(0,1),(2,3)],
    'E': [(0,0),(1,0),(2,0),(0,1),(0,2),(0,3),(0,4),(1,4),(2,4),(1,2),(2,4),],
}

SCORES = [
    0,
    W, # 1 Row
    W*3, # 2 Rows
    W*6, # 3 Rows
    W*10, # 4 Rows
]
FONT = ('Helvetica_bold', 30) #Score font

GAME_SPEED = 10 #Milliseconds per game "tick"

def out_of_bounds(x,y): # Check wheter a coordinate is within the game frame
    return not (-1<x<W and -1<y<H) 

class Tetris:

    def __init__(self):
        self.score = 0
        self.speed = GAME_SPEED
        self.grid = [['white' for _ in range(W)] for _ in range(H)]
        self.blocks = []
        self.initialize_graphics()
        self.next_block = self.Block()
        self.new_block()
        self.draw_score_str()
        self.play()


    def initialize_graphics(self):
        self.graph = sg.Graph(
            canvas_size=(W*BOX_SIZE*2, H*BOX_SIZE*2),
            graph_bottom_left=(0, 0),
            graph_top_right=(W*BOX_SIZE, H*BOX_SIZE),
            key='-GRAPH-',
            change_submits=True,
            drag_submits=False,
            background_color='lightblue'
        )
        self.preview_graph = sg.Graph(
            canvas_size=(PREVIEW_BOX_SIZE * 20, PREVIEW_BOX_SIZE * 20),
            graph_bottom_left=(0,0),
            graph_top_right=(PREVIEW_BOX_SIZE * 5, PREVIEW_BOX_SIZE * 5),
            key='-PREVIEW_GRAPH-',
            change_submits=True,
            drag_submits=False,
            background_color='lightblue'
        )
        self.score_graph = sg.Graph(
            canvas_size=(PREVIEW_BOX_SIZE * 50, PREVIEW_BOX_SIZE * 20),
            graph_bottom_left=(0, -1),
            graph_top_right=(PREVIEW_BOX_SIZE * 25, PREVIEW_BOX_SIZE * 5 +1),
            key='-PREVIEW_GRAPH-',
            change_submits=True,
            drag_submits=False,
            #background_color='lightblue'
        )
        layout = [
            [sg.Text(self.score_str(), key = '__SCORE__',font=FONT, justification='right')],
            [self.score_graph, self.preview_graph],
            [self.graph]
        ]
        self.window = sg.Window(
            'TETRIS',
            layout, 
            finalize=True,
            return_keyboard_events=True,
            use_default_focus=False
        )
        
    
    def draw_score_str(self):
        xx = 0
        for index, letter in enumerate('SCORE'):
            print("LETTER",letter)
            for dx,y in LETTERS[letter]:
                x = xx+dx
                print(x,y)
                self.score_graph.draw_rectangle(
                        (x* PREVIEW_BOX_SIZE,y* PREVIEW_BOX_SIZE),
                        ((x+1) * PREVIEW_BOX_SIZE, (y+1) * PREVIEW_BOX_SIZE),
                        line_color='black',
                        fill_color=COLOR_CODES[index+2]
                    )
            xx += 5
        
    def score_str(self):
        return f'SCORE: {self.score}'
    
    def draw_graphics(self):
        self.graph.erase()
        grid = self.generate_grid_with_block()
        for y in range(H):
            for x in range(W):
                color = grid[y][x]
                if color == 'white': continue
                self.graph.draw_rectangle(
                    (x * BOX_SIZE, y * BOX_SIZE),
                    ((x+1) * BOX_SIZE, (y+1) * BOX_SIZE),
                    line_color='black',
                    fill_color=color
                )
    
    def draw_preview(self):
        self.preview_graph.erase()
        self.next_block = self.Block()
        xx,yy = SHAPE_CENTERS[self.next_block.type_number]
        for dx,dy in self.next_block.shape:
            x,y = dx+xx, dy+yy
            self.preview_graph.draw_rectangle(
                    (x* PREVIEW_BOX_SIZE,y* PREVIEW_BOX_SIZE),
                    ((x+1) * PREVIEW_BOX_SIZE, (y+1) * PREVIEW_BOX_SIZE),
                    line_color='black',
                    fill_color=self.next_block.color
                )

        
    def play(self):
        GAME_OVER = False
        self.GAME_TIME = 0 
        while not GAME_OVER:
            self.draw_graphics()
            event, values = self.window.read(timeout = self.speed)
            self.handle_event(event,values)
            if event == sg.WIN_CLOSED:
                self.window.close()
                break

    def update_game(self):
        if self.collision_check():
            self.generate_grid_with_block(merge=True)
            self.new_block()
            self.check_for_full_rows()
        self.current_block.fall()

    def handle_event(self,event,values):
        if event == '__TIMEOUT__':
            self.GAME_TIME += 1
            if self.GAME_TIME >= 50:
                self.update_game()
                self.GAME_TIME = 0
        else:
            print(values)
            print(event)
        if event == ' ':
            while True:
                self.current_block.fall()
                if self.collision_check():
                    self.generate_grid_with_block(merge=True)
                    self.new_block()
                    self.check_for_full_rows()
                    break
        elif event == 'Down:40':
            self.update_game()
        elif event == 'Left:37':
            self.current_block.move_left()
            if not self.is_legal_block_position():
                self.current_block.move_right()
        elif event == 'Right:39':
            self.current_block.move_right()
            if not self.is_legal_block_position():
                self.current_block.move_left()
        elif event == 'a':
            self.current_block.rotate_anti_clockwise()
            if not self.is_legal_block_position():
                self.current_block.rotate_clockwise()
        elif event == 'd' or event == 'Up:38':
            self.current_block.rotate_clockwise()
            if not self.is_legal_block_position():
                self.current_block.rotate_anti_clockwise()
        
            
    def generate_grid_with_block(self, merge = False):
        if not merge:
            grid = copy.deepcopy(self.grid)
        for x,y in self.current_block.get_coords():
            if out_of_bounds(x,y):continue
            if merge:
                self.grid[y][x] = COLOR_CODES[1]
            else:
                grid[y][x] = self.current_block.color 
        if merge: return
        return grid

    def collision_check(self):
        for x,y in self.current_block.get_coords():
            if out_of_bounds(x,y):continue
            if y == 0:
                print("FLOOR COLLISION!")
                return True
            if self.grid[y-1][x] == COLOR_CODES[1]:
                print("COLLISION!")
                return True
        return False

    def check_for_full_rows(self):
        n_full_rows= 0
        row_indices_to_delete = []
        for y, row in enumerate(self.grid):
            is_full_row = True
            for cell in row:
                if not cell == COLOR_CODES[1]:
                    is_full_row = False
                    break
            if is_full_row:
                n_full_rows += 1
                row_indices_to_delete.append(y)
        self.score += SCORES[n_full_rows]
        self.window['__SCORE__'].update(self.score_str())
        for y in row_indices_to_delete:
            del self.grid[y]
            self.grid.append([COLOR_CODES[0] for _ in range(W)])


    def is_legal_block_position(self):
        for x,y in self.current_block.get_coords():
            if y>=H:continue
            if out_of_bounds(x,y):
                return False
            if self.grid[y][x] == COLOR_CODES[1]:
                return False
        return True

    def new_block(self):
        self.current_block = self.next_block
        self.next_block = self.Block()
        self.draw_preview()

    class Block:
        
        def __init__(self):
            self.x, self.y = 1+np.random.randint(W-2), H-1
            self.type_number = np.random.randint(len(SHAPES))
            self.shape = SHAPES[self.type_number]
            self.color = COLOR_CODES[2+self.type_number]

        def fall(self):
            self.y -=1

        def move_left(self):
            self.x-=1
        
        def move_right(self):
            self.x+=1

        def rotate_clockwise(self):
            if self.type_number == 1: return #Dont rotate the square
            self.shape = [(-y,x) for x,y in self.shape]

        def rotate_anti_clockwise(self):
            if self.type_number == 1: return #Dont rotate the square
            self.shape = [(y,-x) for x,y in self.shape]

        def get_coords(self):
            return [(self.x+dx, self.y+dy) for dx, dy in self.shape]

if (__name__ == "__main__"):
    game = Tetris()