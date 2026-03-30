from .Error import InvalidSyntaxError
from .SyntaxTools import CFG, PREDICTSET

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens                        # Tokens read by lexer
        self.token_idx = 0                          # Used to tell which index to read from the list of tokens
        self.curr_token = tokens[self.token_idx]    # Points to the current token based on the index
    
    def advance(self):
        while True:
            self.token_idx += 1
            if self.token_idx < len(self.tokens): #if still inside bounds
                self.curr_token = self.tokens[self.token_idx]
                if self.curr_token.type not in ['\n', ' ', '\\n', 'space']:      # Skip whitespaces, brekas if it finds another token
                    break
            else:
                self.curr_token = None
                break
        return self.curr_token #current token now is the next token that is not a whitespace
    
    ################################
    # Main syntax analyzer algorithm
    ################################
    def syntax_analyze(self):
        stack = ['<program>']
        error = None
        prev_popped_nonterminal = None
        
        while self.curr_token.type in ['\\n', '\\t', 'space']:
            self.advance()

        while stack:
            # print(stack)            ##### track which path the syntax goes (Can be removed)
            # print(str(self.curr_token.type) + '\n')
            top = stack[-1]
            if self.curr_token is None or self.curr_token.type == 'EOF':            # If there are no more tokens or reached the EOF
                self.curr_token = type('Token', (object,), {                        # Point to token indicating the EOF
                    'type': 'EOF',
                    'pos_start': self.tokens[-1].pos_end if self.tokens else None,
                    'pos_end': self.tokens[-1].pos_end if self.tokens else None
                })()

            if is_nonterminal(top):                                                                         # If top of stack is non-terminal
                if top in PREDICTSET.PREDICT_SET and self.curr_token.type in PREDICTSET.PREDICT_SET[top]:   # Check if non-terminal is in the predict set and the current token is in the predict set of the non-terminal
                    prod_key = PREDICTSET.PREDICT_SET[top][self.curr_token.type]                            # Gets the list in the predict set where the top and current token is found
                    prod = CFG.CFG[prod_key[0]][prod_key[1]]                                                # Gets the reference of the predict set from the CFG (which production and product set)
                    stack.pop()
                    prev_popped_nonterminal = top
                    stack.extend(reversed(prod))
                else:
                    expected_tokens = list(PREDICTSET.PREDICT_SET[top].keys())                 # If non-terminal is not in the predict set, error
                    error = InvalidSyntaxError(self.curr_token.pos_start, self.curr_token.pos_end, f'Unexpected -> {self.curr_token.type} <- \nExpected tokens: {expected_tokens}')
                    break
            else:                                                                              # If terminal, check if the top of the stack is the same as the terminal
                stack.pop()
                if top == self.curr_token.type:
                    self.advance()
                    prev_popped_nonterminal = None
                else:                                                                          # Getting expected tokens to put in the error message                          
                    if prev_popped_nonterminal and is_nonterminal(prev_popped_nonterminal):
                        print("hello")
                        if prev_popped_nonterminal == '<chain_or>':
                            expected_tokens = ['OR', 'AND', '+', '-', '*', '/', '**', '&', '>', '<', '>=', '<=', '==', '!=', '++', '--', ')']
                        else:
                            expected_tokens = list(get_first_set(prev_popped_nonterminal))
                        if top not in expected_tokens:
                            expected_tokens.append(top)
                    else:
                        expected_tokens = [top]
                    if self.curr_token.type in expected_tokens:
                        expected_tokens.remove(self.curr_token.type)
                    error = InvalidSyntaxError(self.curr_token.pos_start, self.curr_token.pos_end, f'Unexpected -> {self.curr_token.type} <-\nExpected tokens: {expected_tokens}')
                    break
        if error:
            return error
        return []

# Function to return a boolean whether a text is a non-terminal by checking if it starts and ends with < and > respectively
def is_nonterminal(text):
    return text.startswith('<') and text.endswith('>')

# Function to get the first set of a non-terminal
# Loops through the CFG of the given non-terminal
# If there are productions, get the first symbol
    # If the first symbol is also a non-terminal, get its first set and put it into the set
    # If the first symbol is a terminal, directly add it to the list
def get_first_set(non_terminal):
    first_set = set()
    for prod in CFG[non_terminal]:
        if prod:
            first_symbol = prod[0]
            if is_nonterminal(first_symbol):
                first_set.update(get_first_set(first_symbol))
            else:
                first_set.add(first_symbol)
    return first_set

def syntax_analyze(tokens):
    syntax = SyntaxAnalyzer(tokens)
    error = syntax.syntax_analyze()
    if error:
        print(error)
        return "❌ Failure from Syntax Analyzer", error
    print("####### Successful Syntax #######")
    return "✅ Success from Syntax Analyzer", None