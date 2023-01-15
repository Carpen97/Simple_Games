import PySimpleGUI as sg
import numpy as np
import copy

W, H = 10,18
SQUARE_SIZE = 30

COLOR_CODES = [
    'white'
    'red',
    'green',
    'yellow',
    'blue',
]

class Tetris:

    def __init__(self):
        self.grid = np.ones((W,H), dtype='i')
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
        self.window = sg.Window('TETRIS', layout, finalize=True)
        
    
    def draw_graphics(self):
        BOX_SIZE = 15
        self.graph.erase()
        grid = self.generate_grid_with_blocks()
        for i in range(W):
            for j in range(H):
                self.graph.draw_rectangle(
                    (i * BOX_SIZE, j * BOX_SIZE),
                    ((i+1) * BOX_SIZE, (j+1) * BOX_SIZE),
                    line_color='black',
                    fill_color=COLOR_CODES[grid[i][j]]
                )
        
    def play(self):
        GAME_OVER = False
        while not GAME_OVER:
            self.draw_graphics()
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:
                self.window.close()
                break

    def generate_new_block(self):
        self.blocks.append(self.Shape_L())

    def generate_grid_with_blocks(self):
        grid = self.grid
        for block in self.blocks:
            for x,y in block.get_coords():
                print(x,y)
                if y>=H:continue
                grid[x][y] = block.color_code
        return grid


    class Block:
        
        def __init__(self):
            pass

        def fall(self):
            self.y +=1

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
    
    class Shape_L(Block):

        def __init__(self):
            self.x, self.y = np.random.randint(W), H
            self.color_code = 2
            self.shape = [
                (0,0),
                (0,1),
                (0,-1),
                (1,-1),
            ]

        


if (__name__ == "__main__"):
    game = Tetris()