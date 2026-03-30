import string

########## DEFINITIONS ##########
# From regular definitions
DIGITS = '0123456789'
ALPHABET = string.ascii_letters
ALPHADIG = DIGITS + ALPHABET
WHITESPACE = '\n\t '

ASCII =  ''.join(chr(i) for i in range (32, 127)) + '\n\t '   
EMOJI = ''.join(chr(i) for i in range(0x1F300, 0x1FAFF + 1))
UNICODE_ALPGHADIG = ASCII + EMOJI

ARITH = '+-/*%'
RELATIONAL = '==!=><>=<='
OTHERSYMS = '({[]}),;:'
ESCAPE_SEQ = 'nt\'"\\' + ALPHADIG + ARITH + RELATIONAL + OTHERSYMS 

########## DELIMITERS ##########
delim = {
    'arith_dlm':            set(WHITESPACE + ALPHADIG + '-' + '('  + '~'),
    'assignop_dlm':         set(WHITESPACE + ALPHADIG + '('  + '"' + '-'  + '{'+ '~'),                                                                                          
    'bool_dlm':             set(WHITESPACE + ARITH + RELATIONAL + ';' + ',' + '}' + ']' + ')' + '=' + '!' + ':' + '~'),                                                    
    'clcurlb_dlm':          set(WHITESPACE + ALPHABET + ';' + '}' + ')' + ',' + '~'),
    'cldoublequotes_dlm':   set(WHITESPACE + RELATIONAL + ';' + ',' + '}' + ')' + '+' + ':' + ']' + '~'),                                                              
    'clparenth_dlm':        set(WHITESPACE + ARITH + RELATIONAL + ALPHABET + ';' + ',' + ')' + '{' + '}' + ']' + '~'),              
    'clquotes_dlm':         set(WHITESPACE + RELATIONAL + ALPHABET + ';' + ',' + '}' + ')' + ':' + '~'),
    'clsqrb_dlm':           set(WHITESPACE + ARITH + RELATIONAL + ',' + ';' + '=' + '['+ ']' + '{' + '}' + ')' + ':' + '~'),             
    'cmpassignop_dlm':      set(WHITESPACE + ALPHADIG + '"' + '-' + '(' + '~'),                                                                                            
    'comb0_dlm':            set(WHITESPACE + '(' + '~'),
    'comb1_dlm':            set(WHITESPACE + '{' + '~'),
    'comb2_dlm':            set(WHITESPACE + ';' + '~'),
    'comb3_dlm':            set(ALPHADIG  + '~'),
    'comb4_dlm':            set(WHITESPACE + ':' + '~'),
    'comb5_dlm':            set(WHITESPACE + '(' + ';' +'~'),
    'comma_dlm':            set(WHITESPACE + ALPHADIG + '"' + '(' + '{' + '+' + '-' + '~'),                 
    'colon_dlm':            set(WHITESPACE + ALPHADIG + '"' + '-'  + '+' + '~'),                            
    'dt_dlm':               set(WHITESPACE + '{' + '~'),                                                                                                              
    'func_dlm':             set(WHITESPACE + ALPHADIG + '~'),                                                                                                               
    'identifier_dlm':       set(WHITESPACE + ARITH + RELATIONAL + '(' + ')' + '[' + ']' + ',' + ';' + ':' + '{' + '}' + '=' + '~'), 
    'int_lit_dlm':          set(WHITESPACE + ARITH + RELATIONAL + ')' + ',' + ';' + '}' + ']' + ':' + '~'),
    'lit_dlm':              set(WHITESPACE + ARITH + RELATIONAL + ':' + ';' + '}' + ')' +']' + ',' + '~'),
    'minus_dlm':            set(WHITESPACE + ALPHADIG + '('  + '~' + '+'),
    'opcurlb_dlm':          set(WHITESPACE + ALPHADIG + '{' + '}' + '"' + '-'  + '+' + '~'),                                                                   
    'opparenth_dlm':        set(WHITESPACE + ALPHADIG + '-'  + '(' + ')' + '"' + '{' + '+' + '~' + ';'),                                            
    'opsqrb_dlm':           set(WHITESPACE + ALPHADIG + ']' + '+' + '-' + '(' + '"' + '~'),                
    'relational_dlm':       set(WHITESPACE + ALPHADIG  + '~'),
    'unary_dlm':            set(WHITESPACE + ALPHABET  + ';' + ')' + '~'),
    'void_dlm':             set(WHITESPACE + '{' + ';' + '~')
}