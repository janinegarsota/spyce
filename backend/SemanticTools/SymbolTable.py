########## SYMBOL TABLE ##########
# The symbol table keeps track of all the variables declared and called in the program
# It stores declared variables and checks whether one is already declared or not
# It differentiates variabels based on their scope
# This also remembers the values stored in variables

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]          # Keeps track of a variables accesibility as local or global

    def push(self):
        self.scopes.append({})      # Creates a new scope level

    def pop(self):
        self.scopes.pop()

    def get(self, name):            # Searches for the variable called from the innermost scope
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None
    
    def get_local(self, name):      # Only checks the if the variable called is a local variable
        if name in self.scopes[-1]:
            return self.scopes[-1][name]
        else:
            print(f'{name} not in local scope')
            return None
    
    def get_type(self, name):       # Gets the data type of the variable called
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name].datatype if hasattr(scope[name], 'datatype') else scope[name]
        return None
        
    def set(self, name, value):     # Handles declaration, assignment, and reassignment, if variable does not exist, it creates one
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return
            
        if not self.scopes:
            self.scopes.append({})
        self.scopes[-1][name] = value

    def set_local(self, name, value):   # Puts the variable in the current scope even if the same identifier exists
        self.scopes[-1][name] = value