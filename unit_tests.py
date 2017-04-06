import unittest
from character import Character
from maze import Maze
from maze import MovementNode
from solver import Solver

class TestMaze(unittest.TestCase):

    def test_maze_init(self):
        new_maze = Maze(3, 3, [34,14,12,6,77,5,1,19,9])
        
        self.assertEqual(new_maze.height, 3)
        self.assertEqual(new_maze.width, 3)
        self.assertEqual(new_maze.grid_data, [34,14,12,6,77,5,1,19,9])

    def test_movement_node_init(self):
        move = MovementNode(7, 19, None, None)

        self.assertEqual(move.index, 7)
        self.assertEqual(move.value, 19)
        self.assertEqual(move.parent_index, None)
        self.assertEqual(move.parent_move, None)
        
    def test_character_init(self):
        default = Character()
        hard_mode = Character(max_lives=1)

        self.assertEqual(default.max_lives, 3)
        self.assertEqual(default.death_counter, 0)
        self.assertEqual(hard_mode.max_lives, 1)
        self.assertEqual(hard_mode.death_counter, 0)        
 
        
    def test_maze_value_functions(self):
        new_maze = Maze(3, 3, [34,14,12,6,77,5,1,19,9])
        
        d1 = new_maze.cell_to_dict(1, 2)
        d2 = new_maze.index_to_dict(7)
        ans_dict = {
            'DOWN': 0,
            'END': 0,
            'LEFT': 0,
            'MINE': 0,
            'RIGHT': 2,
            'START': 16,
            'UP': 1
        }
        val1 = new_maze.get_cell_data(1,2)
        val2 = new_maze.grid_data[7]
        ans_val = 19
        
        self.assertDictEqual(d1, ans_dict)
        self.assertDictEqual(d2, ans_dict)
        self.assertEqual(val1,ans_val)
        self.assertEqual(val2,ans_val)
        
    def test_maze_movements(self):
        new_maze = Maze(3, 3, [34,14,12,6,77,5,1,19,9])    
        self.assertEqual(new_maze.translate_movement('RIGHT',7), 8)
        self.assertEqual(new_maze.translate_movement('UP',7), 4)
        
    def test_maze_enums(self):
        new_maze = Maze(3, 3, [34,14,12,6,77,5,1,19,9])
        
        val = new_maze.grid_data[7]
        
        self.assertEqual(new_maze.type_enum['START'] & val, 16)
        self.assertEqual(new_maze.type_enum['END'] & val, 0)
        self.assertEqual(new_maze.type_enum['MINE'] & val, 0)
        self.assertEqual(new_maze.type_enum['UP'] & val, 1)
        self.assertEqual(new_maze.type_enum['DOWN'] & val, 0)
        self.assertEqual(new_maze.type_enum['LEFT'] & val, 0)
        self.assertEqual(new_maze.type_enum['RIGHT'] & val, 2)
        
        self.assertEqual(new_maze.type_enum['UP'], 1)
        self.assertEqual(new_maze.type_enum['RIGHT'], 2)
        self.assertEqual(new_maze.type_enum['DOWN'], 4)
        self.assertEqual(new_maze.type_enum['LEFT'], 8)
        self.assertEqual(new_maze.type_enum['START'], 16)
        self.assertEqual(new_maze.type_enum['END'], 32)
        self.assertEqual(new_maze.type_enum['MINE'], 64)
        
        self.assertEqual(new_maze.data_enum[1],'UP')
        self.assertEqual(new_maze.data_enum[2],'RIGHT')
        self.assertEqual(new_maze.data_enum[4],'DOWN')
        self.assertEqual(new_maze.data_enum[8],'LEFT')
        self.assertEqual(new_maze.data_enum[16],'START')
        self.assertEqual(new_maze.data_enum[32],'END')
        self.assertEqual(new_maze.data_enum[64],'MINE')

    def test_maze_import(self):
        start = Solver('mazes.txt')
        start.import_mazes()
        sample_data = [6,12,6,10,12,70,10,10,10,12,5,5,67,8,5,7,12,6,8,5,5,3,
                       10,12,3,9,5,7,14,9,7,10,40,3,10,74,9,7,11,12,1,6,78,14,
                       10,10,76,5,6,25,6,13,5,3,10,12,3,9,3,12,7,9,3,10,10,9,6,
                       14,10,9,7,10,10,12,6,10,73,5,2,12,3,74,76,5,7,14,12,3,
                       12,69,2,10,9,3,11,9,67,8,3,9]
        self.assertEqual(len(start.maze_list), 3)
        self.assertEqual(start.maze_list[0].height,10)
        self.assertEqual(start.maze_list[0].width,10)
        self.assertEqual(start.maze_list[0].grid_data, sample_data)
        
    def test_solver(self):
        andrew = Character(max_lives=3)
        no_respawn = Character(max_lives=1)
        start = Solver(None)
        new_maze = Maze(3, 3, [34,14,12,6,77,5,1,19,9])
        start.maze_list.append(new_maze)
        easy_answer = start.solve_all_mazes(andrew, unit_test=True)[0]
        hard_answer = start.solve_all_mazes(no_respawn, unit_test=True)[0]
        
        self.assertEqual(easy_answer,['up', 'up', 'left'])
        self.assertEqual(hard_answer,['right', 'up', 'up', 'left', 'left'])
        
        
            

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMaze)
    unittest.TextTestRunner(verbosity=2).run(suite)