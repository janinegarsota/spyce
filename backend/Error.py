############# ERROR CLASS ##########
# pos_start = where the error began
# pos_end = where the error ended
# error_name = error name
# info = details about the error
class Error:
    def __init__(self, pos_start, pos_end, error_name, info):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.info = info

    # formatted string representation of the error
    def __repr__(self):
        result = f'{self.error_name}: {self.info} \n'
        result += f'at Line {self.pos_start.ln + 1}, Column {self.pos_end.col}\n\n' #line 0 becomes line 1 for users
        result += self.visual_error() #adds output of visual arrows
        return result
    
    def visual_error(self):
        result = ''
        formatted_line = self.pos_start.fullText.replace('\t', ' ')
        line = formatted_line.split('\n')[self.pos_start.ln] #breaks full text into indiv lines, picks line that has error

        prefix_title = f'Line {self.pos_start.ln + 1} | '
        prefix_space = ' ' * len(prefix_title) #creates space = length of prefix_title

        spaces = ' ' * self.pos_start.col #creates spaces to move the arrow to the error's starting col
        arrows = '^' * (self.pos_end.col - self.pos_start.col)
        if len(arrows) == 0: arrows = '^' #if start & end is the same, at least 1

        result += f'{prefix_title + line}\n'
        result += f'{prefix_space + spaces + arrows}\n'

        return result
        
#reuses all formatting logic
class LexicalError(Error):
    def __init__(self, pos_start, pos_end, info):
        super().__init__(pos_start, pos_end, 'Lexical Error', info) #reuses init of error

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, info):
        super().__init__(pos_start, pos_end, 'Syntax Error', info)

class ParseError(Error):
    def __init__(self, pos_start, pos_end, info):
        super().__init__(pos_start, pos_end, 'Parse Error', info)

class SemanticError(Error):
    def __init__(self, pos_start, pos_end, info):
        super().__init__(pos_start, pos_end, 'Semantic Error', info)

class RuntimeError(Error):
    def __init__(self, pos_start, pos_end, info):
        super().__init__(pos_start, pos_end, 'Runtime Error', info)

#############
# EXCEPTIONS
#############
# Not necesarrily errors but are tools to control the flow of the execution of the program
class ContIteration(Exception):
    pass

class ReturnException(Exception):
    def __init__(self, value=None):
        self.value = value

# Another built in exception in python will be used
# StopIteration - simulates the break statement of the program's execution