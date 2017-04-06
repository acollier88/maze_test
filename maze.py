class Maze(object):

    def __init__(self, width, height, grid_data, definitions=None):
        self.width = width
        self.height = height
        self.grid_data = grid_data
        if definitions is not None:
            self.data_enum = definitions
        else:
            self.data_enum = {
                1:'UP',
                2:'RIGHT',
                4:'DOWN',
                8:'LEFT',
                16:'START',
                32:'END',
                64:'MINE'
            }
            self.type_enum = {
                'UP': 1,
                'RIGHT': 2,
                'DOWN': 4,
                'LEFT': 8,
                'START': 16,
                'END': 32,
                'MINE': 64,  
            }

    def get_cell_data(self, coord_x, coord_y):
        if coord_x > self.width or coord_x < 0:
            raise Exception('Invalid X Coord {0} is not in the range 0 to {1}'
                            .format(coord_x,self.width))
        if coord_y > self.height or coord_y < 0:
            raise Exception('Invalid Y Coord {0} is not in the range 0 to {1}'
                            .format(coord_y,self.height))
        index = coord_y * self.width + coord_x
        return self.grid_data[index]
    
    def cell_to_dict(self, coord_x, coord_y):
        if coord_x > self.width or coord_x < 0:
            raise Exception('Invalid X Coord {0} is not in the range 0 to {1}'
                            .format(coord_x,width))
        if coord_y > self.height or coord_y < 0:
            raise Exception('Invalid Y Coord {0} is not in the range 0 to {1}'
                            .format(coord_y,height))
        index = coord_y * self.width + coord_x
        cell = self.grid_data[index]        
        return {
            'UP': cell & 1,
            'RIGHT': cell & 2,
            'DOWN': cell & 4,
            'LEFT': cell & 8,
            'START': cell & 16,
            'END': cell & 32,
            'MINE': cell & 64,  
        }
    
    def index_to_dict(self, index):
        cell = self.grid_data[index]        
        return {
            'UP': cell & 1,
            'RIGHT': cell & 2,
            'DOWN': cell & 4,
            'LEFT': cell & 8,
            'START': cell & 16,
            'END': cell & 32,
            'MINE': cell & 64,  
        }
    
    def translate_movement(self, movement, index):
        result = {
            'UP': lambda x: x - self.width,
            'RIGHT': lambda x: x + 1,
            'DOWN': lambda x: x + self.width,
            'LEFT': lambda x: x - 1,
        }[movement](index)
        return result
    
class MovementNode(object):
    def __init__(self, index, value, parent_index, parent_move, children=[],
                 is_mined=False):
        self.index = index
        self.value = value
        self.parent_index = parent_index
        self.parent_move = parent_move
        self.is_mined = is_mined
        self.children = children