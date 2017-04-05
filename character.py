class Character(object):
    
    def __init__(self, max_lives=3):
        self.max_lives = max_lives
        self.death_counter = 0