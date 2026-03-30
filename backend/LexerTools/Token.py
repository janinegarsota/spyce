########## TOKEN CLASS ##########
class Token:
    def __init__(self, type, value = None, pos_start = None, pos_end = None): # value is none bc operators dont have value
        self.type = type # might be TT_INTLIT type and 42 val for integer
        self.value = value

        # if a starting position is provided, we set both start and end positions. default for one char token
        # advance the pos_end to simulate the end of a single character token
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        
        # if caller provided a specific end position, we should use it instead. overrides if pos_end is already set by pos_start
        if pos_end:
            self.pos_end = pos_end
    
    # string representation of the tokens
    def __repr__(self):
        if self.value: #if it has value
            return f'{self.value}: {self.type}'
        return f'{self.type}' #if no value