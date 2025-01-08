import numpy as np
print("numpy_version = ", np.__version__)

class chain_reaction:
    def __init__(self, row_count, column_count):
        self.row_count = row_count
        self.column_count = column_count
        self.move_limit = (3 * self.row_count * self.column_count) - (2 * self.row_count) - (2 * self.column_count)
        self.move_count = 0
        
    def get_initial_state(self):
        return np.zeros((self.row_count, self.column_count), dtype=int)
        
    def check_valid(self, state, player, action):
        row, column = action
        if row < 0 or row >= self.row_count:
            print("Index out of bound")
            return False
        if column < 0 or column >= self.column_count:
            print("Index out of bound")
            return False
            
        if state[row, column] * player < 0:
            print("Cell belongs to opponent")
            return False 
        return True
        
    def get_next_state(self, state, player, action):
        self.move_count += 1
        row, column = action
        print("row = ", row, "column = ", column)
        state[row,column] += player
        self.run_chain(state, player)
        return state
        
    def run_chain(self, state, player):
        while not self.check_stable(state):
            #1
            if abs(state[0,0]) > 1:
                state[0,0] = state[0,0] - 2*player
                state[0,1] = state[0,1]*player + player
                state[1,0] = state[1,0]*player + player
            if abs(state[0,self.column_count-1]) > 1:
                state[0,self.column_count-1] = state[0,self.column_count-1] - 2*player
                state[0,self.column_count-2] = state[0,self.column_count-2]*player + player
                state[1,self.column_count-1] = state[1,self.column_count-1]*player + player
            if abs(state[self.row_count-1,0]) > 1:
                state[self.row_count-1,0] = state[self.row_count-1,0] - 2*player
                state[self.row_count-1,1] = state[self.row_count-1,1]*player + player
                state[self.row_count-2,0] = state[self.row_count-2,0]*player + player     
            if abs(state[self.row_count-1,self.column_count-1]) > 1:
                state[self.row_count-1,self.column_count-1] = state[self.row_count-1,self.column_count-1] - 2*player
                state[self.row_count-1,self.column_count-2] = state[self.row_count-1,self.column_count-2]*player + player
                state[self.row_count-2,self.column_count-1] = state[self.row_count-2,self.column_count-1]*player + player 
            #2
            for col in range(1, self.column_count-1):
                if abs(state[0,col]) > 2:
                    state[0,col] = state[0,col] - 3*player
                    state[0,col-1] = state[0,col-1]*player + player
                    state[0,col+1] = state[0,col+1]*player + player
                    state[1,col] = state[1,col]*player + player     
                if abs(state[self.row_count-1,col]) > 2:
                    state[self.row_count-1,col] = state[self.row_count-1,col] - 3*player
                    state[self.row_count-1,col-1] = state[self.row_count-1,col-1]*player + player
                    state[self.row_count-1,col+1] = state[self.row_count-1,col+1]*player + player
                    state[self.row_count-2,col] = state[self.row_count-2,col]*player + player       
            for row in range(1, self.row_count-1):
                if abs(state[row, 0]) > 2:
                    state[row, 0] = state[row, 0] - 3*player
                    state[row-1,0] = state[row-1,0]*player + player 
                    state[row+1,0] = state[row+1,0]*player + player
                    state[row,1] = state[row,1]*player + player
                if abs(state[row, self.column_count-1]) > 2:
                    state[row, self.column_count-1] = state[row, self.column_count-1] - 3*player
                    state[row-1,self.column_count-1] = state[row-1,self.column_count-1]*player + player 
                    state[row+1,self.column_count-1] = state[row+1,self.column_count-1]*player + player
                    state[row,self.column_count-2] = state[row,self.column_count-2]*player + player
            #3
            for row in range(1, self.row_count-1):
                for col in range(1, self.column_count-1):
                    if abs(state[row,col]) > 3:
                        state[row,col] = state[row,col] - 4*player
                        state[row,col-1] = state[row,col-1]*player + player
                        state[row,col+1] = state[row,col+1]*player + player
                        state[row-1,col] = state[row-1,col]*player + player
                        state[row+1,col] = state[row+1,col]*player + player
                        
    def check_stable(self, state):
        #1
        if abs(state[0,0]) > 1 or abs(state[0,self.column_count-1]) > 1 or abs(state[self.row_count-1,0]) > 1 or abs(state[self.row_count-1,self.column_count-1]) > 1:
            return False
        #2
        for col in range(1, self.column_count-1):
            if abs(state[0,col]) > 2 or abs(state[self.row_count-1,col]) > 2:
                return False
        for row in range(1, self.row_count-1):
            if abs(state[row, 0]) > 2 or abs(state[row, self.column_count-1]) > 2:
                return False
        #3
        for row in range(1, self.row_count-1):
            for col in range(1, self.column_count-1):
                if abs(state[row,col]) > 3:
                    return False
        #else
        return True
        
    def get_value_and_terminated(self, state, player):
        if self.move_count < self.move_limit:
            return 0, False
        else:
            if self.check_win(state, player):
                return 1, True
            else:
                return 0, True
                
    def check_win(self, state, player):
        cell_count = (0,0)
        for row in range(0, self.row_count):
            for col in range(0, self.column_count):
                if state[row,col] > 0:
                    cell_count[0] += 1
                else:
                    cell_count[1] += 1
                    
        if cell_count[0] == 0 or cell_count[1] == 0:
            return True
        else:
            return False
        
    def get_opponent(self, player):
        return -player
        

# main code
cr = chain_reaction(3,3)
player = 1
state = cr.get_initial_state()

while True:
    print(state)
    action = tuple(map(int, input(f"{player}:").split(',')))
    print(action)
    if not cr.check_valid(state, player, action):
        continue
    state = cr.get_next_state(state, player, action)  
    value, is_terminal = cr.get_value_and_terminated(state, action)
    
    if is_terminal:
        print(state)
        if value == 1:
            print("Player %d won" % player)
        else:
            print("Draw")
        break
        
    player = cr.get_opponent(player)