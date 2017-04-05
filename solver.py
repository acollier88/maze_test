import ast
import csv
import os
import codecs
import json

from character import Character
from collections import deque
from maze import Maze
from maze import MovementNode
from Queue import Queue

class Solver(object):
    
    def __init__(self, mazes_file, data_directory=None):
        if data_directory:
            self.data_directory = data_directory
        else:
            self.data_directory = os.path.realpath(os.path.dirname(__file__))
        self.mazes_file = mazes_file
        self.maze_list = []
        
    def find_start(self, maze):
        for i,cell in enumerate(maze.grid_data):  
            if not cell & maze.type_enum['START']:
                continue
            start_node = MovementNode(i, cell, None, None)
            return start_node,i
        raise Exception('No Start Found')

    def verify_survives(self, character, node, graph):
        death_counter = 0
        while node.parent_index is not None:
            mined = node.is_mined
            if mined:
                death_counter += 1
            if death_counter >= character.max_lives:
                return False
            node = graph[node.parent_index]
        return True

    def print_instructions(self, node, graph):
        instructions = []
        text = node.parent_move
        while node.parent_index is not None:
            instructions.append(text)
            node = graph[node.parent_index]
            text = node.parent_move
        instructions.reverse()
        print instructions
        
    def print_debug(self, maze, visited):
        for i,cell in enumerate(maze.grid_data):
            if cell & maze.type_enum['START']:
                print 'STRT',
            elif cell & maze.type_enum['END']:
                print 'END_',
            elif cell & maze.type_enum['MINE']:
                print 'MINE',
            elif i in visited:
                print '%04d' % i,
            else:
                text = ''
                if cell & maze.type_enum['LEFT']:
                    text = text + 'L'
                else:
                    text = text + '-'
                if cell & maze.type_enum['UP']:
                    text = text + 'U'
                else:
                    text = text + '-'
                if cell & maze.type_enum['DOWN']:
                    text = text + 'D'
                else:
                    text = text + '-'
                if cell & maze.type_enum['RIGHT']:
                    text = text + 'R'
                else:
                    text = text + '-'                 
                print text,
            if (i+1) % maze.width == 0:
                print ''        

    def import_mazes(self):
        maze_location = os.path.join(self.data_directory, self.mazes_file)
        with codecs.open(maze_location, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f, delimiter='-')
            for line in reader:
                size_tuple = ast.literal_eval(line[0])
                grid_data = ast.literal_eval(line[1])
                height, width = size_tuple
                new_maze = Maze(width, height, grid_data)
                self.maze_list.append(new_maze)
                
               
    def solve_all_mazes(self, character, debug=False):
        for maze in self.maze_list:
            print 'maze {0}x{1}'.format(maze.height,maze.width)
            
            visited = set()
            try_cells = Queue()
            graph = {}
            start, i = self.find_start(maze)
                
            visited.add(i)
            try_cells.put(start)
            
            #Used modified version of Breadth First Search, as mazes tend to 
            #be too random to benefit from A*
            while not try_cells.empty():
                current = try_cells.get()
                if current.value & maze.type_enum['END']:
                    if self.verify_survives(character, current, graph):
                        self.print_instructions(current, graph)
                        break
                options = maze.index_to_dict(current.index)           
                survival = True
                if options['MINE']:
                    current.is_mined = True
                    survival = self.verify_survives(character, current,
                                                    graph)
                if survival:
                    graph[current.index] = current
                else:
                    continue
                    
                for k,v in options.iteritems():
                    if not v:#invalid movement that is adjacent to cell
                        continue
                    if k in ['MINE','START']:
                        continue
                    new_index = maze.translate_movement(k,current.index)
                    if not new_index in visited:
                        visited.add(new_index)
                        new_index_value = maze.grid_data[new_index]
                        move = MovementNode(new_index, new_index_value,
                                            current.index, k)
                        try_cells.put(move)
            
            if debug:
                self.print_debug(maze,visited)    


if __name__ == '__main__':
    andrew = Character(max_lives=3)
    start = Solver('mazes.txt')
    start.import_mazes()
    start.solve_all_mazes(andrew)