# Makes using letters easy instead of manually typing each
import string
from .Error import LexicalError
from .LexerTools.Position import Position
from .LexerTools.Token import Token
from .LexerTools import delim, keywords

# data types
TT_INT = 'int'
TT_FLOAT = 'float'
TT_STRING = 'string'
TT_BOOL = 'bool'

# input and output
TT_SAY = 'say'
TT_LISTEN = 'listen'

# logical operators
TT_AND = 'AND'
TT_OR = 'OR'
TT_NOT = 'NOT'

# conditionals
TT_WHEN = 'when'
TT_ELSEWHEN = 'elsewhen'
TT_OTHERWISE = 'otherwise'
TT_CHOOSE = 'choose'
TT_CASE = 'case'
TT_DEFAULT = 'default'

# iteration
TT_FOR = 'for'
TT_WHILE = 'while'
TT_BREAK = 'break'
TT_CONTINUE = 'continue'

# others
TT_TRUE = 'true'
TT_FALSE = 'false'
TT_MAKE = 'make'
TT_SPYCE = 'spyce'
TT_CONST = 'const'
TT_VOID = 'void'
TT_GIVEBACK = 'giveback'
TT_MIX = 'mix'  

# built-in methods 
TT_TOINT = 'toint'
TT_TOFLOAT = 'tofloat'
TT_TOSTR = 'tostr'
TT_TOBOOL = 'tobool'
TT_LEN = 'len'
TT_TYPE = 'type'
TT_UPPER = 'upper'
TT_LOWER = 'lower'
TT_TRUNC = 'trunc'

# arithmetic operators
TT_PLUS = '+'
TT_MINUS = '-'
TT_DIVIDE = '/'
TT_MULTIPLY = '*'
TT_POW = '**'
TT_MOD = '%'

# assignment operators
TT_ASSIGN = '='
TT_ADDASSIGN = '+='
TT_SUBASSIGN = '-='
TT_MULASSIGN = '*='
TT_DIVASSIGN = '/='
TT_MODASSIGN = '%='
TT_POWASSIGN = '**='

# relational operators
TT_EQUAL = '=='
TT_NOTEQ = '!='
TT_GREAT = '>'
TT_LESS = '<' 
TT_GREATEQ = '>='
TT_LESSEQ = '<='

# unary operator
TT_INC = '++'
TT_DEC = '--'

# others
TT_RETURN = '->'
TT_LCURL = '{'
TT_RCURL = '}'
TT_LPAREN = '('
TT_RPAREN = ')'
TT_LSQR = '['
TT_RSQR = ']'
TT_SEMICOLON = ';'
TT_COLON = ':'
TT_COMMA = ','

# LITERALS
TT_INTLIT = 'int_lit'
TT_FLOATLIT = 'float_lit'
TT_STRINGLIT = 'string_lit'
TT_COMMENTLIT = 'comment'

# IDENTIFIER
TT_IDENTIFIER = 'id'

TT_SPACE = 'space'
TT_NEWLINE = '\\n'

########## MAIN LEXER CLASS ##########
class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = Position(0, 0, 0, source)

        if len(source) > 0:
            self.current_char = self.source[0]
        else:
            self.current_char = None

    # moves the position of the lexer to the next character
    def advance(self):
        self.pos.advance(self.current_char)

        # if lexer location is still within the source code, updates current character using the new index, now points to the next real character
        if self.pos.idx < len(self.source):
            self.current_char = self.source[self.pos.idx]
        # otherwise, set the current_char to None, indicating EOF (end of file)
        else:
            self.current_char = None

    # function to peek at the first non-whitespace character before a character
    def lookback(self):
        idx = self.pos.idx - 1
        while idx >= 0 and self.source[idx] in [' ', '\n', '\t']: #ignores whitespaces
            idx -= 1
        
        return self.source[idx] if idx >= 0 else None #returns the character

    # function to peek at the first non-whitespace character before a character
    def lookahead(self):
        idx = self.pos.idx + 1
        while self.source[idx] in [' ', '\n', '\t'] and idx < len(self.source):
            idx += 1

        return self.source[idx] if self.source[idx] else None

    # function to look at the next character
    def next_char(self):
        return self.source[self.pos.idx + 1] if self.source[self.pos.idx + 1] else None

    # function to look at the previous character
    def prev_char(self):
        return self.source[self.pos.idx - 1] if self.source[self.pos.idx - 1] else None

    ########## MAIN TOKENIZER ALGORITHM ##########
    def tokenize(self):
        tokens = []     # where tokens generated will be stored
        errors = []     # where errors found will be stored
        states = []     # state tracking
        unique_id = 0   # counter for unique id in the source code

        while self.current_char is not None:
            ############### KEYWORD OR IDENTIFIER ###############
            if self.current_char in delim.ALPHABET + '_':
                identifier_state = 277
                new_string = ''                 # where the next characters will be appended
                identifier_count = 0            # count if an identifier is greater than the limit
                pos_start = self.pos.copy()     # copy the position of the text
                match self.current_char:
                    # AND
                    case 'A':
                        states.append(1)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        if self.current_char == 'N':
                            states.append(2)
                            new_string += self.current_char
                            identifier_count += 1
                            self.advance()
                            if self.current_char == 'D':
                                states.append(3)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char is not None:
                                    if self.current_char in delim.delim['comb0_dlm']:
                                        states.append(4)
                                        tokens.append(Token(TT_AND, new_string, pos_start, self.pos.copy()))
                                        continue
                                    elif self.current_char not in delim.delim['comb0_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                        pass
                                    elif self.current_char not in delim.delim['comb0_dlm']:
                                        pos_end = self.pos.copy()
                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                        continue
                    # NOT
                    case 'N':
                        states.append(5)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        if self.current_char == 'O':
                            states.append(6)
                            new_string += self.current_char
                            identifier_count += 1
                            self.advance()
                            if self.current_char == 'T':
                                states.append(7)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char is not None:
                                    if self.current_char in delim.delim['comb0_dlm']:
                                        states.append(8)
                                        tokens.append(Token(TT_NOT, new_string, pos_start, self.pos.copy()))
                                        continue
                                    elif self.current_char not in delim.delim['comb0_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                        pass
                                    elif self.current_char not in delim.delim['comb0_dlm']:
                                        pos_end = self.pos.copy()
                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                        continue
                    # OR
                    case 'O':
                        states.append(9)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        if self.current_char == 'R':
                            states.append(10)
                            new_string += self.current_char
                            identifier_count += 1
                            self.advance()
                            if self.current_char is not None:
                                if self.current_char in delim.delim['comb0_dlm']:
                                    states.append(11)
                                    tokens.append(Token(TT_OR, new_string, pos_start, self.pos.copy()))
                                    continue
                                elif self.current_char not in delim.delim['comb0_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                    pass
                                elif self.current_char not in delim.delim['comb0_dlm']:
                                    pos_end = self.pos.copy()
                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                    continue
                    # b
                    case 'b':
                        states.append(12)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        match self.current_char:
                            # bool
                            case 'o':
                                states.append(13)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'o':
                                    states.append(14)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'l':
                                        states.append(15)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char is not None:
                                            if self.current_char in delim.delim['dt_dlm']:
                                                states.append(16)
                                                tokens.append(Token(TT_BOOL, new_string, pos_start, self.pos.copy()))
                                                continue
                                            elif self.current_char not in delim.delim['dt_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                                pass
                                            elif self.current_char not in delim.delim['dt_dlm']:
                                                pos_end = self.pos.copy()
                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                continue
                            # break
                            case 'r':
                                states.append(17)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'e':
                                    states.append(18)    
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'a':
                                        states.append(19)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char == 'k':
                                            states.append(20)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char is not None:
                                                if self.current_char in delim.delim['comb2_dlm']:
                                                    states.append(21)
                                                    tokens.append(Token(TT_BREAK, new_string, pos_start, self.pos.copy()))
                                                    continue
                                                elif self.current_char not in delim.delim['comb2_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                                    pass
                                                elif self.current_char not in delim.delim['comb2_dlm']:
                                                    pos_end = self.pos.copy()
                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                    continue
                    # c
                    case 'c':
                        states.append(22)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        match self.current_char:
                            # case
                            case 'a':
                                states.append(23)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 's':
                                    states.append(24)
                                    new_string += self.current_char
                                    identifier_count += 1 #increase length
                                    self.advance()
                                    if self.current_char == 'e':
                                        states.append(25)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char is not None:
                                            if self.current_char in delim.WHITESPACE:
                                                states.append(26)
                                                tokens.append(Token(TT_CASE, new_string, pos_start, self.pos.copy()))
                                                continue
                                            elif self.current_char not in delim.WHITESPACE and self.current_char in delim.delim['comb3_dlm']: #if identifier
                                                pass
                                            elif self.current_char not in delim.WHITESPACE:
                                                pos_end = self.pos.copy()
                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after  "{new_string}"'))
                                                continue
                            # h
                            case 'h':
                                states.append(27)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                # choose
                                if self.current_char == 'o':
                                    states.append(28)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'o':
                                        states.append(29)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char == 's':
                                            states.append(30)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 'e':
                                                states.append(31)
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char is not None:
                                                    if self.current_char in delim.delim['comb0_dlm']:
                                                        states.append(32)
                                                        tokens.append(Token(TT_CHOOSE, new_string, pos_start, self.pos.copy()))
                                                        continue
                                                    elif self.current_char not in delim.delim['comb0_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                                        pass
                                                    elif self.current_char not in delim.delim['comb0_dlm']:
                                                        pos_end = self.pos.copy()
                                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                        continue
                            # o
                            case 'o':
                                states.append(33)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                # n
                                if self.current_char == 'n':
                                    states.append(34)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    match self.current_char:
                                        # const
                                        case 's':
                                            states.append(35)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 't':
                                                states.append(36)
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char is not None:
                                                    if self.current_char in delim.WHITESPACE:
                                                        states.append(37)
                                                        tokens.append(Token(TT_CONST, new_string, pos_start, self.pos.copy()))
                                                        continue
                                                    elif self.current_char not in delim.WHITESPACE and self.current_char in delim.delim['comb3_dlm']:
                                                        pass
                                                    elif self.current_char not in delim.WHITESPACE:
                                                        pos_end = self.pos.copy()
                                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                        continue
                                        # continue
                                        case 't':
                                            states.append(38)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 'i':
                                                states.append(39)
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char == 'n':
                                                    states.append(40)
                                                    new_string += self.current_char
                                                    identifier_count += 1
                                                    self.advance()
                                                    if self.current_char == 'u':
                                                        states.append(41)
                                                        new_string += self.current_char
                                                        identifier_count += 1
                                                        self.advance()
                                                        if self.current_char == 'e':
                                                            states.append(42)
                                                            new_string += self.current_char
                                                            identifier_count += 1
                                                            self.advance()
                                                            if self.current_char is not None:
                                                                if self.current_char in delim.delim['comb2_dlm']:
                                                                    states.append(43)
                                                                    tokens.append(Token(TT_CONTINUE, new_string, pos_start, self.pos.copy()))
                                                                    continue
                                                                elif self.current_char not in delim.delim['comb2_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                                                    pass
                                                                elif self.current_char not in delim.delim['comb2_dlm']:
                                                                    pos_end = self.pos.copy()
                                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                                    continue    
                    # default
                    case 'd':
                        states.append(44)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        if self.current_char == 'e':
                            states.append(45)
                            new_string += self.current_char
                            identifier_count += 1
                            self.advance()
                            if self.current_char == 'f':
                                states.append(46)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'a':
                                    states.append(47)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'u':
                                        states.append(48)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char == 'l':
                                            states.append(49)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 't':
                                                states.append(50)
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char is not None:
                                                    if self.current_char in delim.delim['comb4_dlm']:
                                                        states.append(51)
                                                        tokens.append(Token(TT_DEFAULT, new_string, pos_start, self.pos.copy()))
                                                        continue
                                                    elif self.current_char not in delim.delim['comb4_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                                        pass
                                                    elif self.current_char not in delim.delim['comb4_dlm']:
                                                        pos_end = self.pos.copy()
                                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                        continue
                    # elsewhen
                    case 'e':
                        states.append(52)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        if self.current_char == 'l':
                            states.append(53)
                            new_string += self.current_char
                            identifier_count += 1
                            self.advance()
                            if self.current_char == 's':
                                states.append(54)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'e':
                                    states.append(55)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'w':
                                        states.append(56)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char == 'h':
                                            states.append(57)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 'e':
                                                states.append(58)
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char == 'n':
                                                    states.append(59)
                                                    new_string += self.current_char
                                                    identifier_count += 1
                                                    self.advance()
                                                    if self.current_char is not None:
                                                        if self.current_char in delim.delim['comb0_dlm']:
                                                            states.append(60)
                                                            tokens.append(Token(TT_ELSEWHEN, new_string, pos_start, self.pos.copy()))
                                                            continue
                                                        elif self.current_char not in delim.delim['comb0_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                                            pass
                                                        elif self.current_char not in delim.delim['comb0_dlm']:
                                                            pos_end = self.pos.copy()
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                            continue
                    # f
                    case 'f':
                        states.append(61)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        match self.current_char:
                            # false
                            case 'a':
                                states.append(62)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'l':
                                    states.append(63)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 's':
                                        states.append(64)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char == 'e':
                                            states.append(65)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char is not None:
                                                if self.current_char in delim.delim['bool_dlm']:
                                                    states.append(66)
                                                    tokens.append(Token(TT_FALSE, new_string, pos_start, self.pos.copy()))
                                                    continue
                                                elif self.current_char not in delim.delim['bool_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                                    pass
                                                elif self.current_char not in delim.delim['bool_dlm']:
                                                    pos_end = self.pos.copy()
                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                    continue
                            # float
                            case 'l':
                                states.append(67)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'o':
                                    states.append(68)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'a':
                                        states.append(69)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char == 't':
                                            states.append(70)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char is not None:
                                                if self.current_char in delim.delim['dt_dlm']:
                                                    states.append(71)
                                                    tokens.append(Token(TT_FLOAT, new_string, pos_start, self.pos.copy()))
                                                    continue
                                                elif self.current_char not in delim.delim['dt_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                                    pass
                                                elif self.current_char not in delim.delim['dt_dlm']:
                                                    pos_end = self.pos.copy()
                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                    continue
                            # for
                            case 'o':
                                states.append(72)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'r':
                                    states.append(73)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char is not None:
                                        if self.current_char in delim.delim['comb0_dlm']:
                                            states.append(74)
                                            tokens.append(Token(TT_FOR, new_string, pos_start, self.pos.copy()))
                                            continue
                                        elif self.current_char not in delim.delim['comb0_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                            pass
                                        elif self.current_char not in delim.delim['comb0_dlm']:
                                            pos_end = self.pos.copy()
                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                            continue
                    # giveback
                    case 'g':
                        states.append(75)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        if self.current_char == 'i':
                            states.append(76)
                            new_string += self.current_char
                            identifier_count += 1
                            self.advance()
                            if self.current_char == 'v':
                                states.append(77)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'e':
                                    states.append(78)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'b':
                                        states.append(79)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char == 'a':
                                            states.append(80)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 'c':
                                                states.append(81)
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char == 'k':
                                                    states.append(82)
                                                    new_string += self.current_char
                                                    identifier_count += 1
                                                    self.advance()
                                                    if self.current_char is not None:
                                                        if self.current_char in delim.delim['comb5_dlm']:
                                                            states.append(83)
                                                            tokens.append(Token(TT_GIVEBACK, new_string, pos_start, self.pos.copy()))
                                                            continue
                                                        elif self.current_char not in delim.delim['comb5_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                                            pass
                                                        elif self.current_char not in delim.delim['comb5_dlm']:
                                                            pos_end = self.pos.copy()
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                            continue
                    # int
                    case 'i':
                        states.append(84)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        if self.current_char == 'n':
                            states.append(85)
                            new_string += self.current_char
                            identifier_count += 1
                            self.advance()
                            if self.current_char == 't':
                                states.append(86)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char is not None:
                                    if self.current_char in delim.delim['dt_dlm']:
                                        states.append(87)
                                        tokens.append(Token(TT_INT, new_string, pos_start, self.pos.copy()))
                                        continue
                                    elif self.current_char not in delim.delim['dt_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                        pass
                                    elif self.current_char not in delim.delim['dt_dlm']:
                                        pos_end = self.pos.copy()
                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                        continue
                    case 'l':
                        states.append(91)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        match self.current_char:
                            # len
                            case 'e':
                                states.append(91)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'n':
                                    states.append(92)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char is not None:
                                        if self.current_char == '(':
                                            states.append(97)
                                            tokens.append(Token(TT_LEN, new_string, pos_start, self.pos.copy())) # FIXEDDDDDD TT_LEN
                                            continue
                                        elif self.current_char != '(' and self.current_char in delim.delim['comb3_dlm']:
                                            pass
                                        elif self.current_char != '(':
                                            pos_end = self.pos.copy()
                                            if self.current_char == '\n':
                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "\\n" after "{new_string}"'))
                                            elif self.current_char == ' ':
                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "space" after "{new_string}"'))
                                            else:
                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                            continue
                            # listen
                            case 'i':
                                states.append(91)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 's':
                                    states.append(93)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 't':
                                        states.append(94)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char == 'e':
                                            states.append(95)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 'n':
                                                states.append(96)
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char is not None:
                                                    if self.current_char == '(':
                                                        states.append(97)
                                                        tokens.append(Token(TT_LISTEN, new_string, pos_start, self.pos.copy()))
                                                        continue
                                                    elif self.current_char != '(' and self.current_char in delim.delim['comb3_dlm']:
                                                        pass
                                                    elif self.current_char != '(':
                                                        pos_end = self.pos.copy()
                                                        if self.current_char == '\n':
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "\\n" after "{new_string}"'))
                                                        elif self.current_char == ' ':
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "space" after "{new_string}"'))
                                                        else:
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                        continue
                            # lower
                            case 'o':
                                states.append(91)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'w':
                                    states.append(93)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'e':
                                        states.append(94)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char == 'r':
                                            states.append(96)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char is not None:
                                                if self.current_char == '(':
                                                    states.append(97)
                                                    tokens.append(Token(TT_LOWER, new_string, pos_start, self.pos.copy())) # FIXEDDDDDD TT_LOWER
                                                    continue
                                                elif self.current_char != '(' and self.current_char in delim.delim['comb3_dlm']:
                                                    pass
                                                elif self.current_char != '(':
                                                    pos_end = self.pos.copy()
                                                    if self.current_char == '\n':
                                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "\\n" after "{new_string}"'))
                                                    elif self.current_char == ' ':
                                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "space" after "{new_string}"'))
                                                    else:
                                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                    continue
                    # make
                    case 'm':
                        states.append(98)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        match self.current_char:
                            # make
                            case 'a':
                                states.append(99)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'k':
                                    states.append(100)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'e':
                                        states.append(101)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char is not None:
                                            if self.current_char in delim.WHITESPACE:
                                                states.append(102)
                                                tokens.append(Token(TT_MAKE, new_string, pos_start, self.pos.copy()))
                                                continue
                                            elif self.current_char not in delim.WHITESPACE and self.current_char in delim.delim['comb3_dlm']:
                                                pass
                                            elif self.current_char not in delim.WHITESPACE:
                                                pos_end = self.pos.copy()
                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                continue
                            # mix
                            case 'i':
                                states.append(99)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'x':
                                    states.append(101)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char is not None:
                                        if self.current_char == '[':
                                            states.append(97)
                                            tokens.append(Token(TT_MIX, new_string, pos_start, self.pos.copy())) 
                                            continue
                                        elif self.current_char != '[' and self.current_char in delim.delim['comb3_dlm']:    
                                            pass
                                        elif self.current_char != '[':  
                                            pos_end = self.pos.copy()
                                            if self.current_char == '\n':
                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "\\n" after "{new_string}"'))
                                            elif self.current_char == ' ':
                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "space" after "{new_string}"'))
                                            else:
                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                            continue
                    # otherwise
                    case 'o':
                        states.append(108)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        if self.current_char == 't':
                            states.append(109)
                            new_string += self.current_char
                            identifier_count += 1
                            self.advance()
                            if self.current_char == 'h':
                                states.append(110)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'e':
                                    states.append(111)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'r':
                                        states.append(112)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char == 'w':
                                            states.append(113)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 'i':
                                                states.append(114)
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char == 's':
                                                    states.append(115)
                                                    new_string += self.current_char
                                                    identifier_count += 1
                                                    self.advance()
                                                    if self.current_char == 'e':
                                                        states.append(116)
                                                        new_string += self.current_char
                                                        identifier_count += 1
                                                        self.advance()
                                                        if self.current_char is not None:
                                                            if self.current_char in delim.delim['comb1_dlm']:
                                                                states.append(117)
                                                                tokens.append(Token(TT_OTHERWISE, new_string, pos_start, self.pos.copy()))
                                                                continue
                                                            elif self.current_char not in delim.delim['comb1_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                                                pass
                                                            elif self.current_char not in delim.delim['comb1_dlm']:
                                                                pos_end = self.pos.copy()
                                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                            continue
                    # s
                    case 's':
                        states.append(118)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        match self.current_char:
                            # say
                            case 'a':
                                states.append(119)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'y':
                                    states.append(120)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char is not None:
                                        if self.current_char == '(':
                                            states.append(121)
                                            tokens.append(Token(TT_SAY, new_string, pos_start, self.pos.copy()))
                                            continue
                                        elif self.current_char != '(' and self.current_char in delim.delim['comb3_dlm']:
                                            pass
                                        elif self.current_char != '(':
                                            pos_end = self.pos.copy()
                                            if self.current_char == '\n':
                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "\\n" after "{new_string}"'))
                                            elif self.current_char == ' ':
                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "space" after "{new_string}"'))
                                            else:
                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                            continue
                            # spyce
                            case 'p':
                                states.append(126)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'y':
                                    states.append(127)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'c':
                                        states.append(128)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char == 'e':
                                            states.append(129)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char is not None:
                                                if self.current_char == '(':
                                                    states.append(130)
                                                    tokens.append(Token(TT_SPYCE, new_string, pos_start, self.pos.copy()))
                                                    continue
                                                elif self.current_char != '(' and self.current_char in delim.delim['comb3_dlm']:
                                                    pass
                                                elif self.current_char != '(':
                                                    pos_end = self.pos.copy()
                                                    if self.current_char == '\n':
                                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "\\n" after "{new_string}"'))
                                                    elif self.current_char in ['\t', ' ']:
                                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "space" after "{new_string}"'))
                                                    else:
                                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                    continue
                            # string
                            case 't':
                                states.append(131)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance() 
                                if self.current_char == 'r':
                                    states.append(132)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'i':
                                        states.append(133)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char == 'n':
                                            states.append(134)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 'g':
                                                states.append(135)
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char is not None:
                                                    if self.current_char in delim.delim['dt_dlm']:
                                                        states.append(136)
                                                        tokens.append(Token(TT_STRING, new_string, pos_start, self.pos.copy()))
                                                        continue
                                                    elif self.current_char not in delim.delim['dt_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                                        pass
                                                    elif self.current_char not in delim.delim['dt_dlm']:
                                                        pos_end = self.pos.copy()
                                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                        continue
                    # t
                    case 't':
                        states.append(137)                     
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        match self.current_char:    # o, r, y
                            # to
                            case 'o':
                                states.append(138)                 
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                match self.current_char:    # bool, float, int, str
                                    # tobool
                                    case 'b':
                                        states.append(131)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance() 
                                        if self.current_char == 'o':
                                            states.append(127)              
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 'o':
                                                states.append(128)          
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char == 'l':
                                                    states.append(135)          
                                                    new_string += self.current_char
                                                    identifier_count += 1
                                                    self.advance()
                                                    if self.current_char is not None:
                                                        if self.current_char == '(':
                                                            states.append(130)
                                                            tokens.append(Token(TT_TOBOOL, new_string, pos_start, self.pos.copy()))     # FIXEDDDDDD TOBOOL
                                                            continue
                                                        elif self.current_char != '(' and self.current_char in delim.delim['comb3_dlm']:
                                                            pass
                                                        elif self.current_char != '(':
                                                            pos_end = self.pos.copy()
                                                            if self.current_char == '\n':
                                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "\\n" after "{new_string}"'))
                                                            elif self.current_char in ['\t', ' ']:
                                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "space" after "{new_string}"'))
                                                            else:
                                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                            continue
                                    # tofloat
                                    case 'f':
                                        states.append(131)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance() 
                                        if self.current_char == 'l':
                                            states.append(127)              
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 'o':
                                                states.append(128)          
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char == 'a':
                                                    states.append(135)          
                                                    new_string += self.current_char
                                                    identifier_count += 1
                                                    self.advance()
                                                    if self.current_char == 't':
                                                        states.append(135)          
                                                        new_string += self.current_char
                                                        identifier_count += 1
                                                        self.advance()
                                                        if self.current_char is not None:
                                                            if self.current_char == '(':
                                                                states.append(130)
                                                                tokens.append(Token(TT_TOFLOAT, new_string, pos_start, self.pos.copy()))        # FIXEDDDDDD TOFLOAT
                                                                continue
                                                            elif self.current_char != '(' and self.current_char in delim.delim['comb3_dlm']:
                                                                pass
                                                            elif self.current_char != '(':
                                                                pos_end = self.pos.copy()
                                                                if self.current_char == '\n':
                                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "\\n" after "{new_string}"'))
                                                                elif self.current_char in ['\t', ' ']:
                                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "space" after "{new_string}"'))
                                                                else:
                                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                                continue
                                    # toint
                                    case 'i':
                                        states.append(131)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance() 
                                        if self.current_char == 'n':
                                            states.append(127)              
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 't':
                                                states.append(128)          
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char is not None:
                                                    if self.current_char == '(':
                                                        states.append(130)
                                                        tokens.append(Token(TT_TOINT, new_string, pos_start, self.pos.copy()))        # FIXEDDDDDD TOINT
                                                        continue
                                                    elif self.current_char != '(' and self.current_char in delim.delim['comb3_dlm']:
                                                        pass
                                                    elif self.current_char != '(':
                                                        pos_end = self.pos.copy()
                                                        if self.current_char == '\n':
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "\\n" after "{new_string}"'))
                                                        elif self.current_char in ['\t', ' ']:
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "space" after "{new_string}"'))
                                                        else:
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                        continue
                                    # tostr
                                    case 's':
                                        states.append(131)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance() 
                                        if self.current_char == 't':
                                            states.append(127)              
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 'r':
                                                states.append(128)          
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char is not None:
                                                    if self.current_char == '(':
                                                        states.append(130)
                                                        tokens.append(Token(TT_TOSTR, new_string, pos_start, self.pos.copy()))        # FIXEDDDDDD TOSTR
                                                        continue
                                                    elif self.current_char != '(' and self.current_char in delim.delim['comb3_dlm']:
                                                        pass
                                                    elif self.current_char != '(':
                                                        pos_end = self.pos.copy()
                                                        if self.current_char == '\n':
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "\\n" after "{new_string}"'))
                                                        elif self.current_char in ['\t', ' ']:
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "space" after "{new_string}"'))
                                                        else:
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                        continue
                            # tru
                            case 'r':
                                states.append(138)                 
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'u':
                                    states.append(127)              
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    match self.current_char:    
                                        # true
                                        case 'e':
                                            states.append(128)          
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char is not None:
                                                if self.current_char in delim.delim['bool_dlm']:            
                                                    states.append(136)
                                                    tokens.append(Token(TT_TRUE, new_string, pos_start, self.pos.copy()))       
                                                    continue
                                                elif self.current_char not in delim.delim['bool_dlm'] and self.current_char in delim.delim['comb3_dlm']:        # FIXEDDDDDD bool_dlm
                                                    pass
                                                elif self.current_char not in delim.delim['bool_dlm']:      
                                                    pos_end = self.pos.copy()
                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                    continue
                                        # trunc
                                        case 'n':
                                            states.append(128)          
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char == 'c':
                                                states.append(127)              
                                                new_string += self.current_char
                                                identifier_count += 1
                                                self.advance()
                                                if self.current_char is not None:
                                                    if self.current_char == '(':
                                                        states.append(130)
                                                        tokens.append(Token(TT_TRUNC, new_string, pos_start, self.pos.copy()))        # FIXEDDDDDD TRUNC
                                                        continue
                                                    elif self.current_char != '(' and self.current_char in delim.delim['comb3_dlm']:
                                                        pass
                                                    elif self.current_char != '(':
                                                        pos_end = self.pos.copy()
                                                        if self.current_char == '\n':
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "\\n" after "{new_string}"'))
                                                        elif self.current_char in ['\t', ' ']:
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "space" after "{new_string}"'))
                                                        else:
                                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                        continue
                            # type
                            case 'y':
                                states.append(138)                 
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'p':
                                    states.append(127)              
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'e':
                                        states.append(128)          
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char is not None:
                                            if self.current_char == '(':
                                                states.append(130)
                                                tokens.append(Token(TT_TYPE, new_string, pos_start, self.pos.copy()))        # FIXEDDDDDD TYPE
                                                continue
                                            elif self.current_char != '(' and self.current_char in delim.delim['comb3_dlm']:
                                                pass
                                            elif self.current_char != '(':
                                                pos_end = self.pos.copy()
                                                if self.current_char == '\n':
                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "\\n" after "{new_string}"'))
                                                elif self.current_char in ['\t', ' ']:
                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "space" after "{new_string}"'))
                                                else:
                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                continue
                    # u
                    case 'u':
                        states.append(137)                     
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        if self.current_char == 'p':
                            states.append(143)
                            new_string += self.current_char
                            identifier_count += 1
                            self.advance()
                            if self.current_char == 'p':
                                states.append(144)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'e':
                                    states.append(145)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'r':
                                        states.append(145)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char is not None:
                                            if self.current_char == '(':
                                                states.append(130)
                                                tokens.append(Token(TT_UPPER, new_string, pos_start, self.pos.copy()))   
                                                continue
                                            elif self.current_char != '(' and self.current_char in delim.delim['comb3_dlm']:
                                                pass
                                            elif self.current_char != '(':
                                                pos_end = self.pos.copy()
                                                if self.current_char == '\n':
                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "\\n" after "{new_string}"'))
                                                elif self.current_char in ['\t', ' ']:
                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "space" after "{new_string}"'))
                                                else:
                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                continue
                    # void
                    case 'v':
                        states.append(142)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        if self.current_char == 'o':
                            states.append(143)
                            new_string += self.current_char
                            identifier_count += 1
                            self.advance()
                            if self.current_char == 'i':
                                states.append(144)
                                new_string += self.current_char
                                identifier_count += 1
                                self.advance()
                                if self.current_char == 'd':
                                    states.append(145)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char is not None:
                                        if self.current_char in delim.delim['void_dlm']:
                                            states.append(146)
                                            tokens.append(Token(TT_VOID, new_string, pos_start, self.pos.copy()))
                                            continue
                                        elif self.current_char not in delim.delim['void_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                            pass
                                        elif self.current_char not in delim.delim['void_dlm']:
                                            pos_end = self.pos.copy()
                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                            continue
                    # w
                    case 'w':
                        states.append(147)
                        new_string += self.current_char
                        identifier_count += 1
                        self.advance()
                        # h
                        if self.current_char == 'h':
                            states.append(148)
                            new_string += self.current_char
                            identifier_count += 1
                            self.advance()
                            match self.current_char:
                                # when
                                case 'e':
                                    states.append(149)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'n':
                                        states.append(150)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char is not None:
                                            if self.current_char in delim.delim['comb0_dlm']:
                                                states.append(151)
                                                tokens.append(Token(TT_WHEN, new_string, pos_start, self.pos.copy()))
                                                continue
                                            elif self.current_char not in delim.delim['comb0_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                                pass
                                            elif self.current_char not in delim.delim['comb0_dlm']:
                                                pos_end = self.pos.copy()
                                                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                continue
                                # while
                                case 'i':
                                    states.append(152)
                                    new_string += self.current_char
                                    identifier_count += 1
                                    self.advance()
                                    if self.current_char == 'l':
                                        states.append(153)
                                        new_string += self.current_char
                                        identifier_count += 1
                                        self.advance()
                                        if self.current_char == 'e':
                                            states.append(154)
                                            new_string += self.current_char
                                            identifier_count += 1
                                            self.advance()
                                            if self.current_char is not None:
                                                if self.current_char in delim.delim['comb0_dlm']:
                                                    states.append(155)
                                                    tokens.append(Token(TT_WHILE, new_string, pos_start, self.pos.copy()))
                                                    continue
                                                elif self.current_char not in delim.delim['comb0_dlm'] and self.current_char in delim.delim['comb3_dlm']:
                                                    pass
                                                elif self.current_char not in delim.delim['comb0_dlm']:
                                                    pos_end = self.pos.copy()
                                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                                    continue

                # Identifier
                while identifier_count == 0 and self.current_char == '_': #catches identifier that start with _
                    errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid character -> {self.current_char} <-'))
                    self.advance()
                    while self.current_char == ' ':
                        self.advance()
        
                while self.current_char is not None and self.current_char in delim.ALPHADIG + '_' and identifier_count < 25: #identifier rule
                    states.append(identifier_state)
                    new_string += self.current_char
                    identifier_count += 1
                    identifier_state += 1
                    self.advance()
                
                pos_end = self.pos.copy()
                if self.current_char is not None and new_string in keywords.keywords:
                    errors.append(LexicalError(pos_start, pos_end, info=f'Keyword "{new_string}" cannot be used as identifier'))
                    continue
                elif self.current_char is not None and self.current_char in delim.ALPHADIG + '_' and identifier_count == 25:
                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}". Exceeding maximum identifier length of 25 characters.'))
                    continue
                elif self.current_char is None or self.current_char not in delim.delim['identifier_dlm']:
                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                    continue
                else:
                    found = False #same identifier not found yet
                    for t in tokens:
                        # If the same identifier is read, input the same token
                        if t.value == new_string:
                            found = True
                            tokens.append(Token(t.type, new_string, pos_start, pos_end))
                            break
                    # If a new identifier is read, concatenate a counter for the token
                    # Removed counter for counting identifier
                    if not found:
                        unique_id += 1
                        tokens.append(Token(f'{TT_IDENTIFIER}', new_string, pos_start, pos_end))
                
            ############### AN ARITHMETIC AND RELATIONAL SYMBOL ###############
            elif self.current_char in delim.ARITH + delim.RELATIONAL:
                new_string = ''
                pos_start = self.pos.copy()
                match self.current_char:
                    # +
                    case '+':
                        states.append(156)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char is not None and self.current_char in delim.delim['assignop_dlm']:
                            states.append(157)
                            tokens.append(Token(TT_PLUS, new_string, pos_start, self.pos.copy()))
                            continue
                        elif self.current_char not in delim.delim['assignop_dlm']:
                            match self.current_char:
                                # ++
                                case '+':
                                    states.append(158)
                                    new_string += self.current_char
                                    self.advance()
                                    if self.current_char is not None and self.current_char in delim.delim['unary_dlm']:
                                        states.append(159)
                                        tokens.append(Token(TT_INC, new_string, pos_start, self.pos.copy()))
                                        continue
                                    else:
                                        errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                        continue
                                # +=
                                case '=':
                                    states.append(160)
                                    new_string += self.current_char
                                    self.advance()
                                    if self.current_char is not None and self.current_char in delim.delim['cmpassignop_dlm']:
                                        states.append(161)
                                        tokens.append(Token(TT_ADDASSIGN, new_string, pos_start, self.pos.copy()))
                                        continue
                                    else:
                                        errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                        continue
                                case _:
                                    errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                    continue
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue    

                    # -
                    case '-':
                        new_string = ''
                        pos_start = self.pos.copy()
                        # --
                        if self.next_char() == '-':
                            new_string += self.current_char
                            self.advance()
                            new_string += self.current_char
                            self.advance()
                            if self.current_char in delim.delim['unary_dlm']:
                                states.append(165)
                                tokens.append(Token(TT_DEC, new_string, pos_start, self.pos.copy()))
                                continue
                            else:
                                errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                continue
                        # -=
                        elif self.next_char() == '=':
                            new_string += self.current_char
                            self.advance()
                            new_string += self.current_char
                            self.advance()
                            if self.current_char is not None and self.current_char in delim.delim['cmpassignop_dlm']:
                                states.append(167)
                                tokens.append(Token(TT_SUBASSIGN, new_string, pos_start, self.pos.copy()))
                                continue
                            else:
                                errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                continue
                        # ->
                        elif self.next_char() == '>':
                            new_string += self.current_char
                            self.advance()
                            new_string += self.current_char
                            self.advance()
                            if self.current_char is not None and self.current_char in delim.delim['func_dlm']:
                                states.append(169)
                                tokens.append(Token(TT_RETURN, new_string, pos_start, self.pos.copy()))
                                continue
                            else:
                                errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                continue
                        # negative number                            
                        elif self.lookahead() in delim.DIGITS: #check if next char is digit
                            int_count = 0 #for max int length
                            decimal_count = 0
                            if self.lookback() in [None, '[', '{', '(', '+', '*', '/', '%', '=', '<', '>']: #unary minus allowed here
                                new_string += self.current_char #append -
                                self.advance()

                                while self.current_char in delim.WHITESPACE: #-  5
                                    self.advance()

                                new_string += self.current_char #append next int
                                int_count += 1 #first integer count
                                self.advance()
                                while self.current_char is not None and self.current_char in delim.DIGITS and self.current_char != '.' and int_count < 19: #read more integers
                                    int_count += 1
                                    new_string += self.current_char
                                    self.advance()
                                pos_end = self.pos.copy()

                                # If a . is found; float value
                                if self.current_char == '.':
                                    new_string += self.current_char #append .
                                    self.advance()
                                    if self.current_char is None or self.current_char not in delim.DIGITS:
                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "." after value "{new_string[:-1]}"'))
                                        continue

                                    while self.current_char is not None and self.current_char in delim.DIGITS and decimal_count < 5:
                                        decimal_count += 1
                                        new_string += self.current_char
                                        self.advance()
                                    pos_end = self.pos.copy()

                                    if self.current_char is not None and self.current_char in delim.delim['lit_dlm']:
                                        num_parts = new_string.split('.')               # split whole value to two parts <integer>.<float>
                                        int_part = num_parts[0].lstrip('0') or '0'      # strip leading 0 except 1 for integer
                                        float_part = num_parts[1].rstrip('0') or '0'    # strip trailing 0 except 1 for float
                                        new_string = f'{int_part}.{float_part}'
                                        pos_end = self.pos.copy()
                                        if new_string == '-0.0':
                                            pos_end = self.pos.copy()
                                            new_string = '0.0'
                                            tokens.append(Token(TT_FLOATLIT, float(new_string), pos_start, pos_end))
                                            continue
                                        else:
                                            tokens.append(Token(TT_FLOATLIT, float(new_string), pos_start, pos_end))
                                            continue
                                    elif self.current_char is not None and self.current_char in delim.DIGITS:
                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}". Exceeding maximum number of decimal values of 5 digits'))
                                        continue
                                    else:
                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                        continue
                                # If only integers
                                elif self.current_char is not None and self.current_char in delim.delim['int_lit_dlm']:
                                    unary = new_string[0]                                        # save the -
                                    number_lit = new_string[1:].lstrip('0') or '0'               # save the number literals
                                    new_string = unary + number_lit                              # strip leading 0 except 1
                                    pos_end = self.pos.copy()
                                    if new_string == '-0':
                                        pos_end = self.pos.copy()
                                        new_string = '0'
                                        tokens.append(Token(TT_INTLIT, int(new_string), pos_start, pos_end))
                                        continue
                                    else:
                                        tokens.append(Token(TT_INTLIT, int(new_string), pos_start, pos_end))
                                        continue
                                elif self.current_char is not None and self.current_char in delim.DIGITS:
                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}". Exceeding maximum number of 19 digits for integers'))
                                    continue
                                else:
                                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                    continue
                            # cases like i-- - 4 or i-- - -4
                            elif self.prev_char() in delim.WHITESPACE and self.lookback() == '-': #if prev nonwhitespace was -
                                tok_indx = -1
                                while tokens[tok_indx].type in ['space', '\n']: #skips trailing
                                    tok_indx -= 1
                                
                                # i-- - 4: read as binary subtraction
                                if tokens[tok_indx].type == '--': #if decrement, it reads as minus
                                    new_string += self.current_char # add -
                                    self.advance()
                                    if self.current_char is not None and self.current_char in delim.delim['minus_dlm']:
                                        tokens.append(Token(TT_MINUS, new_string, pos_start, self.pos.copy()))
                                        continue
                                    else:
                                        errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                        continue
                                # otherwise, read as negative number
                                else:
                                    new_string += self.current_char #append -
                                    self.advance()

                                    while self.current_char in delim.WHITESPACE:
                                        self.advance()

                                    new_string += self.current_char #append int
                                    int_count += 1
                                    self.advance()
                                    while self.current_char is not None and self.current_char in delim.DIGITS and self.current_char != '.' and int_count < 19:
                                        int_count += 1
                                        new_string += self.current_char
                                        self.advance()
                                    pos_end = self.pos.copy()

                                    # If a . is found; float value
                                    if self.current_char == '.':
                                        new_string += self.current_char
                                        self.advance()
                                        if self.current_char is None or self.current_char not in delim.DIGITS:
                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "." after value "{new_string[:-1]}"'))
                                            continue
                                        while self.current_char is not None and self.current_char in delim.DIGITS and decimal_count < 5:
                                            decimal_count += 1
                                            new_string += self.current_char
                                            self.advance()
                                        pos_end = self.pos.copy()

                                        if self.current_char is not None and self.current_char in delim.delim['lit_dlm']:
                                            num_parts = new_string.split('.')               # split whole value to two parts <integer>.<float>
                                            int_part = num_parts[0].lstrip('0') or '0'      # strip leading 0 except 1 for integer
                                            float_part = num_parts[1].rstrip('0') or '0'    # strip trailing 0 except 1 for float
                                            new_string = f'{int_part}.{float_part}'
                                            pos_end = self.pos.copy()
                                            if new_string == '-0.0':
                                                pos_end = self.pos.copy()
                                                new_string = '0.0'
                                                tokens.append(Token(TT_FLOATLIT, float(new_string), pos_start, pos_end))
                                                continue
                                            else:
                                                tokens.append(Token(TT_FLOATLIT, float(new_string), pos_start, pos_end))
                                                continue
                                        elif self.current_char is not None and self.current_char in delim.DIGITS:
                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}". Exceeding maximum number of decimal values of 5 digits'))
                                            continue
                                        else:
                                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                            continue
                                    # If only integers
                                    elif self.current_char is not None and self.current_char in delim.delim['int_lit_dlm']:
                                        unary = new_string[0]                                        # save the -
                                        number_lit = new_string[1:].lstrip('0') or '0'               # save the number literals
                                        new_string = unary + number_lit                              # strip leading 0 except 1
                                        pos_end = self.pos.copy()
                                        if new_string == '-0':
                                            pos_end = self.pos.copy()
                                            new_string = '0'
                                            tokens.append(Token(TT_INTLIT, int(new_string), pos_start, pos_end))
                                            continue
                                        else:
                                            tokens.append(Token(TT_INTLIT, int(new_string), pos_start, pos_end))
                                            continue
                                    elif self.current_char is not None and self.current_char in delim.DIGITS:
                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}". Exceeding maximum number of 19 digits for integers'))
                                        continue
                                    else:
                                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                        continue
                            else:
                                new_string += self.current_char
                                self.advance()
                                if self.current_char is not None and self.current_char in delim.delim['minus_dlm']:
                                    tokens.append(Token(TT_MINUS, new_string, pos_start, self.pos.copy()))
                                    continue
                                else:
                                    errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                    continue
                        else:
                            new_string += self.current_char
                            self.advance()
                            if self.current_char is not None and self.current_char in delim.delim['minus_dlm']:
                                tokens.append(Token(TT_MINUS, new_string, pos_start, self.pos.copy()))
                                continue
                            else:
                                errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                continue

                    # *
                    case '*':
                        states.append(170)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char is not None and self.current_char in delim.delim['arith_dlm']:
                            states.append(171)
                            tokens.append(Token(TT_MULTIPLY, new_string, pos_start, self.pos.copy()))
                            continue
                        elif self.current_char not in delim.delim['arith_dlm']:
                            match self.current_char:
                                # **
                                case '*':
                                    states.append(172)
                                    new_string += self.current_char
                                    self.advance()
                                    if self.current_char is not None and self.current_char in delim.delim['arith_dlm']:
                                        states.append(173)
                                        tokens.append(Token(TT_POW, new_string, pos_start, self.pos.copy()))
                                        continue
                                    # **=
                                    elif self.current_char == '=':
                                        states.append(174)
                                        new_string += self.current_char
                                        self.advance()
                                        if self.current_char is not None and self.current_char in delim.delim['cmpassignop_dlm']:
                                            states.append(175)
                                            tokens.append(Token(TT_POWASSIGN, new_string, pos_start, self.pos.copy()))
                                            continue
                                        else:
                                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                            continue
                                    else:
                                        errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                        continue
                                # *=
                                case '=':
                                    states.append(176)
                                    new_string += self.current_char
                                    self.advance()
                                    if self.current_char is not None and self.current_char in delim.delim['cmpassignop_dlm']:
                                        states.append(177)
                                        tokens.append(Token(TT_MULASSIGN, new_string, pos_start, self.pos.copy()))
                                        continue
                                    else:
                                        errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                        continue
                                case _:
                                    errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                    continue
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue 
                    # /
                    case '/':
                        states.append(178)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char is not None and self.current_char in delim.delim['arith_dlm']:
                            states.append(179)
                            tokens.append(Token(TT_DIVIDE, new_string, pos_start, self.pos.copy()))
                            continue
                        # /=
                        elif self.current_char == '=':
                            states.append(180)
                            new_string += self.current_char
                            self.advance()
                            if self.current_char is not None and self.current_char in delim.delim['cmpassignop_dlm']:
                                states.append(181)
                                tokens.append(Token(TT_DIVASSIGN, new_string, pos_start, self.pos.copy()))
                                continue
                            else:
                                errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                continue  
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue 
                    # %
                    case '%':
                        states.append(182)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char is not None and self.current_char in delim.delim['arith_dlm']:
                            states.append(183)
                            tokens.append(Token(TT_MOD, new_string, pos_start, self.pos.copy()))
                            continue
                        # %=
                        elif self.current_char == '=':
                            states.append(184)
                            new_string += self.current_char
                            self.advance()
                            if self.current_char is not None and self.current_char in delim.delim['cmpassignop_dlm']:
                                states.append(185)
                                tokens.append(Token(TT_MODASSIGN, new_string, pos_start, self.pos.copy()))
                                continue
                            else:
                                errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                continue  
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue  
                    # =
                    case '=':
                        states.append(186)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char is not None and self.current_char in delim.delim['assignop_dlm']:
                            states.append(187)
                            tokens.append(Token(TT_ASSIGN, new_string, pos_start, self.pos.copy()))
                            continue
                        elif self.current_char == '=':
                            states.append(188)
                            new_string += self.current_char
                            self.advance()
                            if self.current_char is not None and self.current_char in delim.delim['assignop_dlm']:
                                states.append(189)
                                tokens.append(Token(TT_EQUAL, new_string, pos_start, self.pos.copy()))
                                continue
                            else:
                                errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                continue  
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue
                    # !
                    case '!':
                        states.append(190)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char == '=':
                            states.append(191)
                            new_string += self.current_char
                            self.advance()
                            if self.current_char is not None and self.current_char in delim.delim['assignop_dlm']:
                                states.append(192)
                                tokens.append(Token(TT_NOTEQ, new_string, pos_start, self.pos.copy()))
                                continue
                            else:
                                errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                continue
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Character -> {new_string} <-'))
                            continue
                    # >
                    case '>':
                        states.append(193)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char is not None and self.current_char in delim.delim['assignop_dlm']:
                            states.append(194)
                            tokens.append(Token(TT_GREAT, new_string, pos_start, self.pos.copy()))
                            continue
                        elif self.current_char == '=':
                            states.append(195)
                            new_string += self.current_char
                            self.advance()
                            if self.current_char is not None and self.current_char in delim.delim['assignop_dlm']:
                                states.append(196)
                                tokens.append(Token(TT_GREATEQ, new_string, pos_start, self.pos.copy()))
                                continue
                            else:
                                errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                continue  
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue
                    # <
                    case '<':
                        states.append(197)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char is not None and self.current_char in delim.delim['assignop_dlm']:
                            states.append(198)
                            tokens.append(Token(TT_LESS, new_string, pos_start, self.pos.copy()))
                            continue
                        # <=
                        elif self.current_char == '=':
                            states.append(199)
                            new_string += self.current_char
                            self.advance()
                            if self.current_char is not None and self.current_char in delim.delim['assignop_dlm']:
                                states.append(200)
                                tokens.append(Token(TT_LESSEQ, new_string, pos_start, self.pos.copy()))
                                continue
                            else:
                                errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                                continue  
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue
            
            ############### OTHER SYMBOLS (()[]{},:;) ###############
            elif self.current_char in delim.OTHERSYMS:
                new_string = ''
                pos_start = self.pos.copy()
                match self.current_char:
                    # (
                    case '(':
                        states.append(201)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char in delim.delim['opparenth_dlm']:
                            states.append(202)
                            tokens.append(Token(TT_LPAREN, new_string, pos_start, self.pos.copy()))
                            continue
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue
                    # )
                    case ')':
                        states.append(203)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char in delim.delim['clparenth_dlm']:
                            states.append(204)
                            tokens.append(Token(TT_RPAREN, new_string, pos_start, self.pos.copy()))
                            continue
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue
                    # {
                    case '{':
                        states.append(205)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char in delim.delim['opcurlb_dlm']:
                            states.append(206)
                            tokens.append(Token(TT_LCURL, new_string, pos_start, self.pos.copy()))
                            continue
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue
                    # }
                    case '}':
                        states.append(207)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char is None or self.current_char in delim.delim['clcurlb_dlm']:
                            states.append(208)
                            tokens.append(Token(TT_RCURL, new_string, pos_start, self.pos.copy()))
                            continue
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue
                    # [
                    case '[':
                        states.append(209)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char is not None and self.current_char in delim.delim['opsqrb_dlm']:
                            states.append(210)
                            tokens.append(Token(TT_LSQR, new_string, pos_start, self.pos.copy()))
                            continue
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue
                    # ]
                    case ']':
                        states.append(211)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char in delim.delim['clsqrb_dlm']:
                            states.append(212)
                            tokens.append(Token(TT_RSQR, new_string, pos_start, self.pos.copy()))
                            continue
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue
                    # :
                    case ':':
                        states.append(213)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char is not None and self.current_char in delim.WHITESPACE:
                            states.append(214)
                            tokens.append(Token(TT_COLON, new_string, pos_start, self.pos.copy()))
                            continue
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue
                    # ,
                    case ',':
                        states.append(215)
                        new_string += self.current_char
                        self.advance()
                        if self.current_char in delim.delim['comma_dlm']:
                            states.append(216)
                            tokens.append(Token(TT_COMMA, new_string, pos_start, self.pos.copy()))
                            continue
                        else:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                            continue
                    # ;
                    case ';':
                        states.append(217)
                        new_string += self.current_char
                        tokens.append(Token(TT_SEMICOLON, new_string, pos_start, self.pos.copy()))
                        self.advance()
                        continue

            ############### INT AND FLOAT LITERALS ###############
            # If literal starts with a number, only for positive literals
            elif self.current_char in delim.DIGITS:
                decimal_state = 259
                num_lit_state = 221
                states.append(num_lit_state)
                new_string = ''
                int_count = 0
                decimal_count = 0
                pos_start = self.pos.copy()
                new_string += self.current_char

                # If first digit is not a zero (leading zeros should not increase count)
                has_non_zero = self.current_char != '0'
                if has_non_zero:            
                    int_count += 1
                self.advance()

                # Collect all digits
                while self.current_char is not None and self.current_char in delim.DIGITS and self.current_char != '.' and int_count < 19:            
                    new_string += self.current_char
                    # If this digit or the starting digit is a non-zero, start counting
                    if self.current_char != '0' or has_non_zero:
                        has_non_zero = True
                        int_count += 1
                        num_lit_state += 1
                        states.append(num_lit_state)
                    self.advance()
                pos_end = self.pos.copy()

                # If a . is found; float value
                if self.current_char == '.':
                    states.append(decimal_state)
                    new_string += self.current_char
                    self.advance()
                    if self.current_char is None or self.current_char not in delim.DIGITS:            
                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter "." after value "{new_string[:-1]}"'))
                        continue

                    while self.current_char is not None and self.current_char in delim.DIGITS and (decimal_count < 5 or self.current_char == '0'):
                        decimal_count += 1
                        decimal_state += 1
                        states.append(decimal_state)
                        new_string += self.current_char
                        self.advance()
                    pos_end = self.pos.copy()

                    if self.current_char is not None and self.current_char in delim.delim['lit_dlm']:
                        states.append(decimal_state)
                        num_parts = new_string.split('.')               # split whole value to two parts <integer>.<float>
                        int_part = num_parts[0].lstrip('0') or '0'      # strip leading 0 except 1 for integer
                        float_part = num_parts[1].rstrip('0') or '0'    # strip trailing 0 except 1 for float

                        # Check if decimal digits do not exceed 5
                        if len(float_part) > 5:
                            errors.append(LexicalError(pos_start, pos_end, info=f'Invalid number of significant decimal digits in "{new_string}". Maximum is 5.'))
                            continue
                        digit_val = f'{int_part}.{float_part}'
                        tokens.append(Token(TT_FLOATLIT, float(digit_val), pos_start, pos_end))
                        continue
                    elif self.current_char is not None and self.current_char in delim.DIGITS:
                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}". Exceeding maximum number of significant decimal digits of 5'))
                        continue
                    else:
                        errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                        continue

                # If only integers, only positive numbers
                elif self.current_char is not None and self.current_char in delim.delim['int_lit_dlm']:
                    states.append(num_lit_state)
                    digit_val = new_string.lstrip('0') or '0'           # strip leading 0 except 1 
                    tokens.append(Token(TT_INTLIT, int(digit_val), pos_start, pos_end))
                    continue
                elif self.current_char is not None and self.current_char in delim.DIGITS:
                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}". Exceeding maximum number of significant digits for integers'))
                    continue
                else:
                    errors.append(LexicalError(pos_start, pos_end, info=f'Invalid Delimiter -> {self.current_char} <- after "{new_string}"'))
                    continue            

            ############### STRING LITERAL ###############
            elif self.current_char == '"':
                states.append(274)
                pos_start = self.pos.copy()
                string_val = ''
                escape_seq = ''
                string_val += self.current_char
                withNonAscii = False
                self.advance()

                while self.current_char is not None and self.current_char != '"':
                    if self.current_char == '\\':
                        escape_seq += self.current_char
                        self.advance()
                        if self.current_char is None or self.current_char not in delim.ESCAPE_SEQ:
                            errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid character -> {self.current_char} <- after \\. "\\{self.current_char}" is an unknown escape sequence'))
                            continue
                        else:
                            escape_seq += self.current_char
                            string_val += escape_seq
                            escape_seq = '' #reset to empty bc done processing
                            self.advance()
                            continue
                    
                    if self.current_char == '\n':
                        string_val += ' '
                        self.advance()
                        continue
                    
                    string_val += self.current_char
                    self.advance()

                if self.current_char == '"':
                    states.append(275)
                    string_val += self.current_char
                    self.advance()
                    pos_end = self.pos.copy()
                    
                    # check if all characters are in ASCII
                    for i in string_val.replace(' ', ''):
                        if i not in delim.UNICODE_ALPGHADIG: # delim.ASCII <- pinalitan ko to ========= into delim.UNICODE_ALPGHADIG
                            withNonAscii = True
                            break
                    if withNonAscii:
                        errors.append(LexicalError(pos_start, self.pos.copy(), info=f'String values must only be delim.ASCII values: {string_val}'))
                        continue
                    # if valid string
                    if self.current_char is not None and self.current_char in delim.delim['cldoublequotes_dlm']:
                        states.append(276)
                        tokens.append(Token(TT_STRINGLIT, string_val, pos_start, pos_end))
                        continue
                    else:
                        errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid Delimiter -> {self.current_char} <- after {string_val}'))
                        continue

                # if string is not closed
                else:
                    errors.append(LexicalError(pos_start, pos_start, info=f'String not closed: {string_val}'))
                    continue

            ############### COMMENT ###############
            elif self.current_char == '~':
                states.append(327)
                comment_val = ''
                pos_start = self.pos.copy()
                comment_val += self.current_char # add ~
                self.advance()

                # next character must also be ~, otherwise an error occurs
                if self.current_char == '~':
                    states.append(328)
                    comment_val += self.current_char #append ~~
                    self.advance()

                    # read until EOF or ~
                    while self.current_char is not None:
                        if self.current_char == '~': #can be end or part of inside
                            comment_val += self.current_char
                            self.advance()

                            # another ~ to end the comment
                            if self.current_char == '~':
                                states.append(329)
                                comment_val += self.current_char
                                self.advance()
                                states.append(330)
                                break

                        # add everything as a comment   
                        else:
                            comment_val += self.current_char
                            self.advance()
                            
                    # if comment is unclosed
                    else:
                        errors.append(LexicalError(pos_start, pos_start, info=f'Comment not closed: {comment_val}'))
                        continue
                else:
                    errors.append(LexicalError(pos_start, self.pos.copy(), info=f'Invalid character "{comment_val}"'))
                    continue
            
            ############### WHITESPACE ###############
            elif self.current_char in delim.WHITESPACE:
                new_string = ''
                pos_start = self.pos.copy()
                match self.current_char:
                    case ' ':
                        while self.current_char == ' ': #while current char is still a space
                            states.append(218)
                            self.advance()
                        new_string += 'space'
                        tokens.append(Token(TT_SPACE, new_string, pos_start, self.pos.copy()))
                        continue
                    case '\t':
                        while self.current_char == '\t':
                            states.append(218)
                            self.advance()
                        new_string += 'space'
                        tokens.append(Token(TT_SPACE, new_string, pos_start, self.pos.copy()))
                        continue
                    case '\n':
                        new_string += '\\n'
                        states.append(219)
                        self.advance()
                        tokens.append(Token(TT_NEWLINE, new_string, pos_start, self.pos.copy()))
                        continue

            ############## IF CHARACTER IS UNRECOGNIZED BY THE COMPILER ##############
            else:
                pos_start = self.pos.copy() #saves start where invalid char was found
                invalid_char = self.current_char #stores
                self.advance()
                pos_end = self.pos.copy() #saves end
                errors.append(LexicalError(pos_start, pos_end, info=f'Invalid character -> {invalid_char} <-'))
                continue
        
        ############## ALWAYS APPEND EOF at the end of the lexeme table ##############
        tokens.append(Token('EOF', '', self.pos.copy(), self.pos.copy()))
        return tokens, errors

# this will be the main function to be called by the server to send source code to backend
# this takes 'source' as the source code from the code editor and returns the generated tokens and errors
def lexical_analyze(source):
    lexer = Lexer(source)
    tokens, errors = lexer.tokenize()

    return tokens, errors