import PySimpleGUI as sg
import numpy as np
import copy

W, H = 10,18
SQUARE_SIZE = 30

COLOR_CODES = [
    'white',
    'black',
    'red',
    'blue',
    'green',
    'yellow',
    'purple',
    'cyan',
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

GAME_SPEED = 1000

def out_of_bounds(x,y):
    return not (-1<x<W and -1<y<H) 

class Tetris:

    def __init__(self):
        self.speed = GAME_SPEED
        self.grid = [['white' for _ in range(H)] for _ in range(W)]
        self.blocks = []
        self.generate_new_block()
        self.initialize_graphics()
        self.play()

    def initialize_graphics(self):
        self.graph = sg.Graph(
            canvas_size=(W*SQUARE_SIZE, H*SQUARE_SIZE),
            graph_bottom_left=(0, 0),
            graph_top_right=(W*SQUARE_SIZE/2, H*SQUARE_SIZE/2),
            key='-GRAPH-',
            change_submits=True,
            drag_submits=False,
            background_color='lightblue'
        )
        layout = [
            [self.graph]
        ]
        self.window = sg.Window(
            'TETRIS',
            layout, 
            finalize=True,
            return_keyboard_events=True,
            use_default_focus=False
        )
        
    
    def draw_graphics(self):
        BOX_SIZE = 15
        self.graph.erase()
        grid = self.generate_grid_with_block()
        for i in range(W):
            for j in range(H):
                color = grid[i][j]
                if color == 'white': continue
                self.graph.draw_rectangle(
                    (i * BOX_SIZE, j * BOX_SIZE),
                    ((i+1) * BOX_SIZE, (j+1) * BOX_SIZE),
                    line_color='black',
                    fill_color=color
                )
        
    def play(self):
        GAME_OVER = False
        while not GAME_OVER:
            self.draw_graphics()
            event, values = self.window.read(timeout = self.speed)
            self.handle_event(event)
            if self.collision_check():
                self.update_grid_with_new_block()
            if event == sg.WIN_CLOSED:
                self.window.close()
                break

    def handle_event(self,event):
        print(event)
        if event == ' ':
            while True:
                self.current_block.fall()
                if self.collision_check():
                    self.update_grid_with_new_block()
                    break
        if event == 'Left:37':
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
        elif event == 'd':
            self.current_block.rotate_clockwise()
            if not self.is_legal_block_position():
                self.current_block.rotate_anti_clockwise()
        elif event == 'Down:40':
            self.current_block.fall()
        elif event == '__TIMEOUT__':
            self.current_block.fall()

    def generate_new_block(self):
        self.current_block = self.Block()

    def generate_grid_with_block(self, merge = False):
        if not merge:
            grid = copy.deepcopy(self.grid)
        for x,y in self.current_block.get_coords():
            if out_of_bounds(x,y):continue
            if merge:
                self.grid[x][y] = COLOR_CODES[1]
            else:
                grid[x][y] = self.current_block.color 
        if merge: return
        return grid

    def collision_check(self):
        for x,y in self.current_block.get_coords():
            if out_of_bounds(x,y):continue
            if y == 0:
                print("FLOOR COLLISION!")
                return True
            if self.grid[x][y-1] == COLOR_CODES[1]:
                print("COLLISION!")
                return True
        return False

    def is_legal_block_position(self):
        for x,y in self.current_block.get_coords():
            if y>=H:continue
            if out_of_bounds(x,y):
                return False
            if self.grid[x][y] == COLOR_CODES[1]:
                return False
        return True

    def update_grid_with_new_block(self):
        self.generate_grid_with_block(merge=True)
        self.generate_new_block()

    class Block:
        
        def __init__(self):
            self.x, self.y = np.random.randint(W-1), H-1
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
            self.shape = [(-y,x) for x,y in self.shape]

        def rotate_anti_clockwise(self):
            self.shape = [(y,-x) for x,y in self.shape]

        def get_coords(self):
            return [(self.x+dx, self.y+dy) for dx, dy in self.shape]

if (__name__ == "__main__"):
    game = Tetris()