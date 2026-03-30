# string (production) : object (string:list(production, pangilang production))
PREDICT_SET = {
    '<program>':{    
        'const':    ['<program>', 0],       
        'int':      ['<program>', 0],
        'float':    ['<program>', 0],
        'string':   ['<program>', 0],
        'bool':     ['<program>', 0],
        'mix':      ['<program>', 0],
        'make':     ['<program>', 0],
        'spyce':    ['<program>', 0]
    },

    '<global_var>':{    
        'const':    ['<global_var>', 0],    
        'int':      ['<global_var>', 1],    
        'float':    ['<global_var>', 1],
        'string':   ['<global_var>', 1],
        'bool':     ['<global_var>', 1],
        'mix':      ['<global_var>', 1],
        'make':     ['<global_var>', 2],     
        'spyce':    ['<global_var>', 2]
    },

    '<var_type>':{    
        'int':      ['<var_type>', 0],      
        'float':    ['<var_type>', 0],
        'string':   ['<var_type>', 0],     
        'bool':     ['<var_type>', 0],   
        'mix':      ['<var_type>', 1]       
    },
    
    '<arrtype>':{    
        'id':   ['<arrtype>', 0],
        '[':    ['<arrtype>', 1]
    },


    '<data_type>':{    
        'int':      ['<data_type>', 0],
        'float':    ['<data_type>', 1],
        'string':   ['<data_type>', 2],
        'bool':     ['<data_type>', 3]
    },

    
    '<scaldec_tail>':{    
        ',':['<scaldec_tail>', 0],
        ';':['<scaldec_tail>', 1]
    },

    '<num_lit>':{
        'int_lit':    ['<num_lit>', 0],
        'float_lit':  ['<num_lit>', 1]
    },

    '<1d_val>':{       
      'id':['<1d_val>', 0],
      '{': ['<1d_val>', 1]  
    },

    '<inner_arr_indx>':{    
        '[':['<inner_arr_indx>', 0],
        '(':['<inner_arr_indx>', 1],
        ',':['<inner_arr_indx>', 2],
        ';':['<inner_arr_indx>', 2],
        '}':['<inner_arr_indx>', 2]
    },

    '<element_list>':{    
        'NOT':          ['<element_list>', 0],
        'int_lit':      ['<element_list>', 0],
        'float_lit':    ['<element_list>', 0],
        'string_lit':   ['<element_list>', 0],
        'true':         ['<element_list>', 0],
        'false':        ['<element_list>', 0],
        'tostr':        ['<element_list>', 0],
        'toint':        ['<element_list>', 0],
        'tofloat':      ['<element_list>', 0],
        'tobool':       ['<element_list>', 0],
        'len':          ['<element_list>', 0],
        'upper':        ['<element_list>', 0],
        'lower':        ['<element_list>', 0],
        'trunc':        ['<element_list>', 0],
        '(':            ['<element_list>', 0],
        'listen':       ['<element_list>', 0],
        '++':           ['<element_list>', 0],
        '--':           ['<element_list>', 0],
        'id':           ['<element_list>', 0],
        '}':            ['<element_list>', 1]
    },

    '<val_tail>':{    
        ',':['<val_tail>', 0],
        '}':['<val_tail>', 1],
        ')':['<val_tail>', 1]
    },

    '<1d_dec_tail>':{    
        ',':['<1d_dec_tail>', 0],
        ';':['<1d_dec_tail>', 1]
    },

    '<2d_val>':{    
        'id':   ['<2d_val>', 0],
        '{':    ['<2d_val>', 1]
    },

    '<2d_elem>':{    
        'id':   ['<2d_elem>', 0],
        '{':    ['<2d_elem>', 0],
        '}':    ['<2d_elem>', 1]
    },

    '<2dval_tail>':{    
        ',':   ['<2dval_tail>', 0],
        '}':   ['<2dval_tail>', 1]
    },

    '<2d_dec_tail>':{    
        ',':   ['<2d_dec_tail>', 0],
        ';':   ['<2d_dec_tail>', 1]
    },

    '<sub_func>':{       
        'make': ['<sub_func>', 0],
        'spyce':['<sub_func>', 1]
    },

    '<sub_funcdec>':{       
        'make':['<sub_funcdec>', 0]
    },

    '<parameters>':{       
        'int':      ['<parameters>', 0],
        'float':    ['<parameters>', 0],
        'string':   ['<parameters>', 0],
        'bool':     ['<parameters>', 0],
        'mix':     ['<parameters>', 0],
        ')':        ['<parameters>', 1]
    },
    
    '<par_dtype>':{
        'int':      ['<par_dtype>', 0],
        'float':    ['<par_dtype>', 0],
        'string':   ['<par_dtype>', 0],
        'bool':     ['<par_dtype>', 0],
        'mix':     ['<par_dtype>', 1]
    },

    '<1d_indx>':{       
        '[':    ['<1d_indx>', 0],
        'id':   ['<1d_indx>', 1],
    },

    '<2d_indx>':{      
        '[':    ['<2d_indx>', 0],
        'id':   ['<2d_indx>', 1]
    },

    '<par_tail>':{      
        ',':['<par_tail>', 0],
        ')':['<par_tail>', 1]
    },

    '<func_ret>':{       
       'int':   ['<func_ret>', 0],
       'float': ['<func_ret>', 0], 
       'string':['<func_ret>', 0], 
       'bool':  ['<func_ret>', 0], 
       'void':  ['<func_ret>', 1],
       'mix':   ['<func_ret>', 2]
    },
    
    '<mix_func>':{
        '[':    ['<mix_func>', 0],
        '{':    ['<mix_func>', 1]
    },
    
    '<func_body>':{       
        'const':        ['<func_body>', 0],
        'int':          ['<func_body>', 0],
        'float':        ['<func_body>', 0],
        'string':       ['<func_body>', 0],
        'bool':         ['<func_body>', 0],
        'mix':          ['<func_body>', 0],
        'id':           ['<func_body>', 0],     
        '++':           ['<func_body>', 0],
        '--':           ['<func_body>', 0],      
        'say':          ['<func_body>', 0],
        'listen':       ['<func_body>', 0],     
        'when':         ['<func_body>', 0],
        'choose':       ['<func_body>', 0],
        'for':          ['<func_body>', 0],
        'while':        ['<func_body>', 0],
        'giveback':     ['<func_body>', 0],
        '}':            ['<func_body>', 1]
    },
    
    '<main_func_body>':{       
        'const':        ['<main_func_body>', 0],
        'int':          ['<main_func_body>', 0],
        'float':        ['<main_func_body>', 0],
        'string':       ['<main_func_body>', 0],
        'bool':         ['<main_func_body>', 0],
        'mix':          ['<main_func_body>', 0],
        'id':           ['<main_func_body>', 0],     
        '++':           ['<main_func_body>', 0],
        '--':           ['<main_func_body>', 0],      
        'say':          ['<main_func_body>', 0],
        'listen':       ['<main_func_body>', 0],     
        'when':         ['<main_func_body>', 0],
        'choose':       ['<main_func_body>', 0],
        'for':          ['<main_func_body>', 0],
        'while':        ['<main_func_body>', 0],
        'giveback':     ['<main_func_body>', 1]
    },

    '<void>':{    
        'void': ['<void>', 0],
        ';':    ['<void>', 1] 
    },

    '<main_stmnt>':{       
        'const':        ['<main_stmnt>', 0],
        'int':          ['<main_stmnt>', 0],
        'float':        ['<main_stmnt>', 0],
        'string':       ['<main_stmnt>', 0],
        'bool':         ['<main_stmnt>', 0],
        'mix':          ['<main_stmnt>', 0],
        'id':           ['<main_stmnt>', 1],     
        '++':           ['<main_stmnt>', 2],
        '--':           ['<main_stmnt>', 2],      
        'say':          ['<main_stmnt>', 3],
        'listen':       ['<main_stmnt>', 3],     
        'when':         ['<main_stmnt>', 4],
        'choose':       ['<main_stmnt>', 4],
        'for':          ['<main_stmnt>', 5],
        'while':        ['<main_stmnt>', 5]
    },

    '<stmnt>':{       
        'const':        ['<stmnt>', 0],
        'int':          ['<stmnt>', 0],
        'float':        ['<stmnt>', 0],
        'string':       ['<stmnt>', 0],
        'bool':         ['<stmnt>', 0],
        'mix':          ['<stmnt>', 0],
        'id':           ['<stmnt>', 0],     
        '++':           ['<stmnt>', 0],
        '--':           ['<stmnt>', 0],      
        'say':          ['<stmnt>', 0],
        'listen':       ['<stmnt>', 0],     
        'when':         ['<stmnt>', 0],
        'choose':       ['<stmnt>', 0],
        'for':          ['<stmnt>', 0],
        'while':        ['<stmnt>', 0],
        'giveback':     ['<stmnt>', 1]
    },

    '<local_var>':{    
        'const':    ['<local_var>', 0],
        'int':      ['<local_var>', 1],
        'float':    ['<local_var>', 1],
        'string':   ['<local_var>', 1],
        'bool':     ['<local_var>', 1],
        'mix':      ['<local_var>', 1]
    },

    '<id_tail>':{       
        '[':    ['<id_tail>', 0],
        '(':    ['<id_tail>', 0],
        '++':   ['<id_tail>', 1],
        '--':   ['<id_tail>', 1],
        '=':    ['<id_tail>', 1],
        '+=':   ['<id_tail>', 1],
        '-=':   ['<id_tail>', 1],
        '*=':   ['<id_tail>', 1],
        '/=':   ['<id_tail>', 1],
        '**=':  ['<id_tail>', 1],
        '%=':   ['<id_tail>', 1]
    },

    '<id_accessor>':{      
        '[':            ['<id_accessor>', 0],
        '(':            ['<id_accessor>', 1]
    },
    
    '<accessor_tail>':{
        '++':   ['<accessor_tail>', 0],
        '--':   ['<accessor_tail>', 0],
        '=':    ['<accessor_tail>', 0],
        '+=':   ['<accessor_tail>', 0],
        '-=':   ['<accessor_tail>', 0],
        '*=':   ['<accessor_tail>', 0],
        '/=':   ['<accessor_tail>', 0],
        '**=':  ['<accessor_tail>', 0],
        '%=':   ['<accessor_tail>', 0],
        '[':    ['<accessor_tail>', 1]
    },
    
    '<str_accessor>':{
        '[':    ['<str_accessor>', 0],
        '++':   ['<str_accessor>', 1],
        '--':   ['<str_accessor>', 1],
        '=':    ['<str_accessor>', 1],
        '+=':   ['<str_accessor>', 1],
        '-=':   ['<str_accessor>', 1],
        '*=':   ['<str_accessor>', 1],
        '/=':   ['<str_accessor>', 1],
        '**=':  ['<str_accessor>', 1],
        '%=':   ['<str_accessor>', 1]
    },
    
    '<id_accessor_tail>':{     
        '++':   ['<id_accessor_tail>', 0],
        '--':   ['<id_accessor_tail>', 0],
        '=':    ['<id_accessor_tail>', 1],
        '+=':   ['<id_accessor_tail>', 1],
        '-=':   ['<id_accessor_tail>', 1],
        '*=':   ['<id_accessor_tail>', 1],
        '/=':   ['<id_accessor_tail>', 1],
        '**=':  ['<id_accessor_tail>', 1],
        '%=':   ['<id_accessor_tail>', 1]    
    },
    
    '<unary_op>':{
        '++':   ['<unary_op>', 0],
        '--':   ['<unary_op>', 1]
    },
    
    '<assign_type>':{     
        '=':    ['<assign_type>', 0],
        '+=':   ['<assign_type>', 0],
        '-=':   ['<assign_type>', 1],
        '*=':   ['<assign_type>', 1],
        '/=':   ['<assign_type>', 1],
        '**=':  ['<assign_type>', 1],
        '%=':   ['<assign_type>', 1]
    },
    
    '<str_assign_type>':{
        '=':    ['<str_assign_type>', 0],
        '+=':   ['<str_assign_type>', 1]
    },
    
    '<spec_assign_type>':{
        '-=':   ['<spec_assign_type>', 0],
        '*=':   ['<spec_assign_type>', 1],
        '/=':   ['<spec_assign_type>', 2],
        '**=':  ['<spec_assign_type>', 3],
        '%=':   ['<spec_assign_type>', 4]
    },

    '<args>':{    
        'NOT':          ['<args>', 0],
        'int_lit':      ['<args>', 0],
        'float_lit':    ['<args>', 0],
        'string_lit':   ['<args>', 0],
        'true':         ['<args>', 0],
        'false':        ['<args>', 0],
        'tostr':        ['<args>', 0],
        'toint':        ['<args>', 0],
        'tofloat':      ['<args>', 0],
        'tobool':       ['<args>', 0],
        'len':          ['<args>', 0],
        'upper':        ['<args>', 0],
        'lower':        ['<args>', 0],
        'trunc':        ['<args>', 0],
        '(':            ['<args>', 0],
        'listen':       ['<args>', 0],
        '++':           ['<args>', 0],
        '--':           ['<args>', 0],
        'id':           ['<args>', 0],
        '{':            ['<args>', 1],
        ')':            ['<args>', 2]
    },

    '<mix_lit>': {
        'NOT':          ['<mix_lit>', 0],
        'int_lit':      ['<mix_lit>', 0],
        'float_lit':    ['<mix_lit>', 0],
        'string_lit':   ['<mix_lit>', 0],
        'true':         ['<mix_lit>', 0],
        'false':        ['<mix_lit>', 0],
        'tostr':        ['<mix_lit>', 0],
        'toint':        ['<mix_lit>', 0],
        'tofloat':      ['<mix_lit>', 0],
        'tobool':       ['<mix_lit>', 0],
        'len':          ['<mix_lit>', 0],
        'upper':        ['<mix_lit>', 0],
        'lower':        ['<mix_lit>', 0],
        'trunc':        ['<mix_lit>', 0],
        '(':            ['<mix_lit>', 0],
        'listen':       ['<mix_lit>', 0],
        '++':           ['<mix_lit>', 0],
        '--':           ['<mix_lit>', 0],
        'id':           ['<mix_lit>', 0],
        '}':            ['<mix_lit>', 0],
        '{':            ['<mix_lit>', 1]
    },
    
    '<mix_lit_tail>':{    
        ',':     ['<mix_lit_tail>', 0],
        '}':     ['<mix_lit_tail>', 1]
    },

     '<id_val>':{    
        'id':     ['<id_val>', 0]
    },

    '<indx_access>':{
        '[':    ['<indx_access>', 0],
        '**':   ['<indx_access>', 1],
        '*':    ['<indx_access>', 1],
        '/':    ['<indx_access>', 1],
        '%':    ['<indx_access>', 1],
        '+':    ['<indx_access>', 1],
        '-':    ['<indx_access>', 1],
        ']':   ['<indx_access>', 1],
        '>':    ['<indx_access>', 1],
        '<':    ['<indx_access>', 1],
        '>=':   ['<indx_access>', 1],
        '<=':   ['<indx_access>', 1],
        '==':   ['<indx_access>', 1],
        '!=':   ['<indx_access>', 1],
        'AND':   ['<indx_access>', 1],
        'OR':   ['<indx_access>', 1],
        ',':   ['<indx_access>', 1],
        ';':   ['<indx_access>', 1],
        '}':   ['<indx_access>', 1],
        ')':   ['<indx_access>', 1],
        ':':   ['<indx_access>', 1],
        '++':   ['<indx_access>', 1],
        '--':   ['<indx_access>', 1]
    },

    '<indx_access_tail>':{
        '[':    ['<indx_access_tail>', 0],
        '**':   ['<indx_access_tail>', 1],
        '*':    ['<indx_access_tail>', 1],
        '/':    ['<indx_access_tail>', 1],
        '%':    ['<indx_access_tail>', 1],
        '+':    ['<indx_access_tail>', 1],
        '-':    ['<indx_access_tail>', 1],
        ']':   ['<indx_access_tail>', 1],
        '>':    ['<indx_access_tail>', 1],
        '<':    ['<indx_access_tail>', 1],
        '>=':   ['<indx_access_tail>', 1],
        '<=':   ['<indx_access_tail>', 1],
        '==':   ['<indx_access_tail>', 1],
        '!=':   ['<indx_access_tail>', 1],
        'AND':   ['<indx_access_tail>', 1],
        'OR':   ['<indx_access_tail>', 1],
        ',':   ['<indx_access_tail>', 1],
        ';':   ['<indx_access_tail>', 1],
        '}':   ['<indx_access_tail>', 1],
        ')':   ['<indx_access_tail>', 1],
        ':':   ['<indx_access_tail>', 1]
    },

    '<expr>':{    
        'NOT':          ['<expr>', 0],
        'int_lit':      ['<expr>', 0],
        'float_lit':    ['<expr>', 0],
        'string_lit':   ['<expr>', 0],
        'true':         ['<expr>', 0],
        'false':        ['<expr>', 0],
        'tostr':        ['<expr>', 0],
        'toint':        ['<expr>', 0],
        'tofloat':      ['<expr>', 0],
        'tobool':       ['<expr>', 0],
        'len':          ['<expr>', 0],
        'upper':        ['<expr>', 0],
        'lower':        ['<expr>', 0],
        'trunc':        ['<expr>', 0],
        '(':            ['<expr>', 0],
        'listen':       ['<expr>', 0],
        '++':           ['<expr>', 0],
        '--':           ['<expr>', 0],
        'id':           ['<expr>', 0]
    },

    '<logical_or_expr>':{    
        'NOT':          ['<logical_or_expr>', 0],
        'int_lit':      ['<logical_or_expr>', 0],
        'float_lit':    ['<logical_or_expr>', 0],
        'string_lit':   ['<logical_or_expr>', 0],
        'true':         ['<logical_or_expr>', 0],
        'false':        ['<logical_or_expr>', 0],
        'tostr':        ['<logical_or_expr>', 0],
        'toint':        ['<logical_or_expr>', 0],
        'tofloat':      ['<logical_or_expr>', 0],
        'tobool':       ['<logical_or_expr>', 0],
        'len':          ['<logical_or_expr>', 0],
        'upper':        ['<logical_or_expr>', 0],
        'lower':        ['<logical_or_expr>', 0],
        'trunc':        ['<logical_or_expr>', 0],
        '(':            ['<logical_or_expr>', 0],
        'listen':       ['<logical_or_expr>', 0],
        '++':           ['<logical_or_expr>', 0],
        '--':           ['<logical_or_expr>', 0],
        'id':           ['<logical_or_expr>', 0]
    },

    '<chain_or>':{    
        'OR':  ['<chain_or>', 0],
        ',':   ['<chain_or>', 1],
        ';':   ['<chain_or>', 1],
        '}':   ['<chain_or>', 1],
        ')':   ['<chain_or>', 1]
    },

    '<and_expr>':{    
        'int_lit':      ['<and_expr>', 0],
        'float_lit':    ['<and_expr>', 0],
        'string_lit':   ['<and_expr>', 0],
        'true':         ['<and_expr>', 0],
        'false':        ['<and_expr>', 0],
        'tostr':        ['<and_expr>', 0],
        'toint':        ['<and_expr>', 0],
        'tofloat':      ['<and_expr>', 0],
        'tobool':       ['<and_expr>', 0],
        'len':          ['<and_expr>', 0],
        'upper':        ['<and_expr>', 0],
        'lower':        ['<and_expr>', 0],
        'trunc':        ['<and_expr>', 0],
        '(':            ['<and_expr>', 0],
        'listen':       ['<and_expr>', 0],
        '++':           ['<and_expr>', 0],
        '--':           ['<and_expr>', 0],
        'id':           ['<and_expr>', 0],
        'NOT':           ['<and_expr>', 0]
    },

    '<chain_and>':{    
        'AND': ['<chain_and>', 0],
        'OR':  ['<chain_and>', 1],
        ',':   ['<chain_and>', 1],
        ';':   ['<chain_and>', 1],
        '}':   ['<chain_and>', 1],
        ')':   ['<chain_and>', 1]
    },

    '<equal_expr>':{    
        'int_lit':      ['<equal_expr>', 0],
        'float_lit':    ['<equal_expr>', 0],
        'string_lit':   ['<equal_expr>', 0],
        'true':         ['<equal_expr>', 0],
        'false':        ['<equal_expr>', 0],
        'tostr':        ['<equal_expr>', 0],
        'toint':        ['<equal_expr>', 0],
        'tofloat':      ['<equal_expr>', 0],
        'tobool':       ['<equal_expr>', 0],
        'len':          ['<equal_expr>', 0],
        'upper':        ['<equal_expr>', 0],
        'lower':        ['<equal_expr>', 0],
        'trunc':        ['<equal_expr>', 0],
        '(':            ['<equal_expr>', 0],
        'listen':       ['<equal_expr>', 0],
        '++':           ['<equal_expr>', 0],
        '--':           ['<equal_expr>', 0],
        'id':           ['<equal_expr>', 0],
        'NOT':          ['<equal_expr>', 0]
    },

    '<equal_expr_tail>':{    
        '==':  ['<equal_expr_tail>', 0],
        '!=':  ['<equal_expr_tail>', 1],
        'AND':  ['<equal_expr_tail>', 2],
        'OR':   ['<equal_expr_tail>', 2],
        ',':    ['<equal_expr_tail>', 2],
        ';':    ['<equal_expr_tail>', 2],
        '}':    ['<equal_expr_tail>', 2],
        ')':    ['<equal_expr_tail>', 2]
    },

    '<relational_expr>':{    
        'int_lit':      ['<relational_expr>', 0],
        'float_lit':    ['<relational_expr>', 0],
        'string_lit':   ['<relational_expr>', 0],
        'true':         ['<relational_expr>', 0],
        'false':        ['<relational_expr>', 0],
        'tostr':        ['<relational_expr>', 0],
        'toint':        ['<relational_expr>', 0],
        'tofloat':      ['<relational_expr>', 0],
        'tobool':       ['<relational_expr>', 0],
        'len':          ['<relational_expr>', 0],
        'upper':        ['<relational_expr>', 0],
        'lower':        ['<relational_expr>', 0],
        'trunc':        ['<relational_expr>', 0],
        '(':            ['<relational_expr>', 0],
        'listen':       ['<relational_expr>', 0],
        '++':           ['<relational_expr>', 0],
        '--':           ['<relational_expr>', 0],
        'id':           ['<relational_expr>', 0],
        'NOT':          ['<relational_expr>', 0]
    },

    '<relational_expr_tail>':{    
        '>':    ['<relational_expr_tail>', 0],
        '<':    ['<relational_expr_tail>', 0],
        '>=':   ['<relational_expr_tail>', 0],
        '<=':   ['<relational_expr_tail>', 0],
        '==':   ['<relational_expr_tail>', 1],
        '!=':   ['<relational_expr_tail>', 1],
        'AND':  ['<relational_expr_tail>', 1],
        'OR':   ['<relational_expr_tail>', 1],
        ',':    ['<relational_expr_tail>', 1],
        ';':    ['<relational_expr_tail>', 1],
        '}':    ['<relational_expr_tail>', 1],
        ')':    ['<relational_expr_tail>', 1]
    },

    '<relation_op>':{    
        '>':    ['<relation_op>', 0],
        '<':    ['<relation_op>', 1],
        '>=':   ['<relation_op>', 2],
        '<=':   ['<relation_op>', 3]
    }, 

    '<arith_expr>':{    
        'int_lit':      ['<arith_expr>', 0],
        'float_lit':    ['<arith_expr>', 0],
        'string_lit':   ['<arith_expr>', 0],
        'true':         ['<arith_expr>', 0],
        'false':        ['<arith_expr>', 0],
        'tostr':        ['<arith_expr>', 0],
        'toint':        ['<arith_expr>', 0],
        'tofloat':      ['<arith_expr>', 0],
        'tobool':       ['<arith_expr>', 0],
        'len':          ['<arith_expr>', 0],
        'upper':        ['<arith_expr>', 0],
        'lower':        ['<arith_expr>', 0],
        'trunc':        ['<arith_expr>', 0],
        '(':            ['<arith_expr>', 0],
        'listen':       ['<arith_expr>', 0],
        '++':           ['<arith_expr>', 0],
        '--':           ['<arith_expr>', 0],
        'id':           ['<arith_expr>', 0],
        'NOT':          ['<arith_expr>', 0]
    },

    '<arith_expr_tail>':{    
        '+':    ['<arith_expr_tail>', 0],
        '-':    ['<arith_expr_tail>', 1],
        ']':    ['<arith_expr_tail>', 2],
        '>':    ['<arith_expr_tail>', 2],
        '<':    ['<arith_expr_tail>', 2],
        '>=':   ['<arith_expr_tail>', 2],
        '<=':   ['<arith_expr_tail>', 2],
        '==':   ['<arith_expr_tail>', 2],
        '!=':   ['<arith_expr_tail>', 2],
        'AND':  ['<arith_expr_tail>', 2],
        'OR':   ['<arith_expr_tail>', 2],
        ',':    ['<arith_expr_tail>', 2],
        ';':    ['<arith_expr_tail>', 2],
        '}':    ['<arith_expr_tail>', 2],
        ')':    ['<arith_expr_tail>', 2]
    },

    '<arith_operand>':{    
        'int_lit':      ['<arith_operand>', 0],
        'float_lit':    ['<arith_operand>', 0],
        'string_lit':   ['<arith_operand>', 0],
        'true':         ['<arith_operand>', 0],
        'false':        ['<arith_operand>', 0],
        'tostr':        ['<arith_operand>', 0],
        'toint':        ['<arith_operand>', 0],
        'tofloat':      ['<arith_operand>', 0],
        'tobool':       ['<arith_operand>', 0],
        'len':          ['<arith_operand>', 0],
        'upper':        ['<arith_operand>', 0],
        'lower':        ['<arith_operand>', 0],
        'trunc':        ['<arith_operand>', 0],
        '(':            ['<arith_operand>', 0],
        'listen':       ['<arith_operand>', 0],
        '++':           ['<arith_operand>', 0],
        '--':           ['<arith_operand>', 0],
        'id':           ['<arith_operand>', 0],
        'NOT':          ['<arith_operand>', 0]
    },  

    '<arith_operand_tail>':{    
        '*':    ['<arith_operand_tail>', 0],
        '/':    ['<arith_operand_tail>', 1],
        '%':    ['<arith_operand_tail>', 2],
        '+':    ['<arith_operand_tail>', 3],
        '-':    ['<arith_operand_tail>', 3],
        ']':    ['<arith_operand_tail>', 3],
        '>':    ['<arith_operand_tail>', 3],
        '<':    ['<arith_operand_tail>', 3],
        '>=':   ['<arith_operand_tail>', 3],
        '<=':   ['<arith_operand_tail>', 3],
        '==':   ['<arith_operand_tail>', 3],
        '!=':   ['<arith_operand_tail>', 3],
        'AND':  ['<arith_operand_tail>', 3],
        'OR':   ['<arith_operand_tail>', 3],
        ',':    ['<arith_operand_tail>', 3],
        ';':    ['<arith_operand_tail>', 3],
        '}':    ['<arith_operand_tail>', 3],
        ')':    ['<arith_operand_tail>', 3]
    },

    '<expo_arith_operand>':{    
        'int_lit':      ['<expo_arith_operand>', 0],
        'float_lit':    ['<expo_arith_operand>', 0],
        'string_lit':   ['<expo_arith_operand>', 0],
        'true':         ['<expo_arith_operand>', 0],
        'false':        ['<expo_arith_operand>', 0],
        'tostr':        ['<expo_arith_operand>', 0],
        'toint':        ['<expo_arith_operand>', 0],
        'tofloat':      ['<expo_arith_operand>', 0],
        'tobool':       ['<expo_arith_operand>', 0],
        'len':          ['<expo_arith_operand>', 0],
        'upper':        ['<expo_arith_operand>', 0],
        'lower':        ['<expo_arith_operand>', 0],
        'trunc':        ['<expo_arith_operand>', 0],
        '(':            ['<expo_arith_operand>', 0],
        'listen':       ['<expo_arith_operand>', 0],
        '++':           ['<expo_arith_operand>', 0],
        '--':           ['<expo_arith_operand>', 0],
        'id':           ['<expo_arith_operand>', 0],
        'NOT':          ['<expo_arith_operand>', 0]
    },  
    
    '<expo_arith_operand_tail>':{    
        '**':   ['<expo_arith_operand_tail>', 0],
        '*':    ['<expo_arith_operand_tail>', 1],
        '/':    ['<expo_arith_operand_tail>', 1],
        '%':    ['<expo_arith_operand_tail>', 1],
        '+':    ['<expo_arith_operand_tail>', 1],
        '-':    ['<expo_arith_operand_tail>', 1],
        ']':    ['<expo_arith_operand_tail>', 1],
        '>':    ['<expo_arith_operand_tail>', 1],
        '<':    ['<expo_arith_operand_tail>', 1],
        '>=':   ['<expo_arith_operand_tail>', 1],
        '<=':   ['<expo_arith_operand_tail>', 1],
        '==':   ['<expo_arith_operand_tail>', 1],
        '!=':   ['<expo_arith_operand_tail>', 1],
        'AND':  ['<expo_arith_operand_tail>', 1],
        'OR':   ['<expo_arith_operand_tail>', 1],
        ',':    ['<expo_arith_operand_tail>', 1],
        ';':    ['<expo_arith_operand_tail>', 1],
        '}':    ['<expo_arith_operand_tail>', 1],
        ')':    ['<expo_arith_operand_tail>', 1]
    },

    '<operand>':{    
        'int_lit':      ['<operand>', 0],
        'float_lit':    ['<operand>', 0],
        'true':         ['<operand>', 1],
        'false':        ['<operand>', 1],
        'tostr':        ['<operand>', 2],
        'toint':        ['<operand>', 2],
        'tofloat':      ['<operand>', 2],
        'tobool':       ['<operand>', 2],
        'len':          ['<operand>', 2],
        'upper':        ['<operand>', 2],
        'lower':        ['<operand>', 2],
        'trunc':        ['<operand>', 2],
        '(':            ['<operand>', 3],
        'listen':       ['<operand>', 4],
        'string_lit':   ['<operand>', 5],
        'NOT':          ['<operand>', 6],
        '++':           ['<operand>', 7],
        '--':           ['<operand>', 7],
        'id':           ['<operand>', 8]
    },
    
    '<bool_lit>':{
        'true':         ['<bool_lit>', 0],
        'false':        ['<bool_lit>', 1]
    },
    
    '<id_operand_tail>':{    
        '(':    ['<id_operand_tail>', 0],
        '[':    ['<id_operand_tail>', 1],
        '++':   ['<id_operand_tail>', 2],
        '--':   ['<id_operand_tail>', 2],
        '**':   ['<id_operand_tail>', 3],
        '*':    ['<id_operand_tail>', 3],
        '/':    ['<id_operand_tail>', 3],
        '%':    ['<id_operand_tail>', 3],
        '+':    ['<id_operand_tail>', 3],
        '-':    ['<id_operand_tail>', 3],
        ']':    ['<id_operand_tail>', 3],
        '>':    ['<id_operand_tail>', 3],
        '<':    ['<id_operand_tail>', 3],
        '>=':   ['<id_operand_tail>', 3],
        '<=':   ['<id_operand_tail>', 3],
        '==':   ['<id_operand_tail>', 3],
        '!=':   ['<id_operand_tail>', 3],
        'AND':  ['<id_operand_tail>', 3],
        'OR':   ['<id_operand_tail>', 3],
        ',':    ['<id_operand_tail>', 3],
        ';':    ['<id_operand_tail>', 3],
        '}':    ['<id_operand_tail>', 3],
        ')':    ['<id_operand_tail>', 3]
    },
    
    '<op_depth_1>':{
        '++':   ['<op_depth_1>', 0],
        '--':   ['<op_depth_1>', 0],
        '[':    ['<op_depth_1>', 1],
        '**':   ['<op_depth_1>', 2],
        '*':    ['<op_depth_1>', 2],
        '/':    ['<op_depth_1>', 2],
        '%':    ['<op_depth_1>', 2],
        '+':    ['<op_depth_1>', 2],
        '-':    ['<op_depth_1>', 2],
        ']':    ['<op_depth_1>', 2],
        '>':    ['<op_depth_1>', 2],
        '<':    ['<op_depth_1>', 2],
        '>=':   ['<op_depth_1>', 2],
        '<=':   ['<op_depth_1>', 2],
        '==':   ['<op_depth_1>', 2],
        '!=':   ['<op_depth_1>', 2],
        'AND':  ['<op_depth_1>', 2],
        'OR':   ['<op_depth_1>', 2],
        ',':    ['<op_depth_1>', 2],
        ';':    ['<op_depth_1>', 2],
        '}':    ['<op_depth_1>', 2],
        ')':    ['<op_depth_1>', 2]
    },
    
    '<op_depth_2>':{
        '++':   ['<op_depth_2>', 0],
        '--':   ['<op_depth_2>', 0],
        '[':    ['<op_depth_2>', 1],
        '**':   ['<op_depth_2>', 2],
        '*':    ['<op_depth_2>', 2],
        '/':    ['<op_depth_2>', 2],
        '%':    ['<op_depth_2>', 2],
        '+':    ['<op_depth_2>', 2],
        '-':    ['<op_depth_2>', 2],
        ']':    ['<op_depth_2>', 2],
        '>':    ['<op_depth_2>', 2],
        '<':    ['<op_depth_2>', 2],
        '>=':   ['<op_depth_2>', 2],
        '<=':   ['<op_depth_2>', 2],
        '==':   ['<op_depth_2>', 2],
        '!=':   ['<op_depth_2>', 2],
        'AND':  ['<op_depth_2>', 2],
        'OR':   ['<op_depth_2>', 2],
        ',':    ['<op_depth_2>', 2],
        ';':    ['<op_depth_2>', 2],
        '}':    ['<op_depth_2>', 2],
        ')':    ['<op_depth_2>', 2]
    },
    
    '<spec_built_in>':{
        'tostr':        ['<spec_built_in>', 0],
        'toint':        ['<spec_built_in>', 1],
        'tofloat':      ['<spec_built_in>', 2],
        'tobool':       ['<spec_built_in>', 3],
        'len':          ['<spec_built_in>', 4],
        'upper':        ['<spec_built_in>', 5],
        'lower':        ['<spec_built_in>', 6],
        'trunc':        ['<spec_built_in>', 7]
    },

    '<IO>':{    
        'say':      ['<IO>', 0],
        'listen':   ['<IO>', 1]
    },
    
    '<say_arg>':{
        'type':     ['<say_arg>', 0],
        '{':        ['<say_arg>', 1],
        'NOT':      ['<say_arg>', 1],
        'int_lit':  ['<say_arg>', 1],
        'float_lit':['<say_arg>', 1],
        'string_lit':['<say_arg>', 1],
        'true':     ['<say_arg>', 1],
        'false':    ['<say_arg>', 1],
        'tostr':    ['<say_arg>', 1],
        'toint':    ['<say_arg>', 1],
        'tofloat':  ['<say_arg>', 1],
        'tobool':   ['<say_arg>', 1],
        'len':      ['<say_arg>', 1],
        'upper':    ['<say_arg>', 1],
        'lower':    ['<say_arg>', 1],
        'trunc':    ['<say_arg>', 1],
        '(':        ['<say_arg>', 1],
        'listen':   ['<say_arg>', 1],
        '++':       ['<say_arg>', 1],
        '--':       ['<say_arg>', 1],
        'id':       ['<say_arg>', 1]
    },
    
    '<func_arg>':{
        '{':        ['<func_arg>', 0],
        'NOT':      ['<func_arg>', 1],
        'int_lit':  ['<func_arg>', 1],
        'float_lit':['<func_arg>', 1],
        'string_lit':['<func_arg>', 1],
        'true':     ['<func_arg>', 1],
        'false':    ['<func_arg>', 1],
        'tostr':    ['<func_arg>', 1],
        'toint':    ['<func_arg>', 1],
        'tofloat':  ['<func_arg>', 1],
        'tobool':   ['<func_arg>', 1],
        'len':      ['<func_arg>', 1],
        'upper':    ['<func_arg>', 1],
        'lower':    ['<func_arg>', 1],
        'trunc':    ['<func_arg>', 1],
        '(':        ['<func_arg>', 1],
        'listen':   ['<func_arg>', 1],
        '++':       ['<func_arg>', 1],
        '--':       ['<func_arg>', 1],
        'id':       ['<func_arg>', 1]
    },

    '<ret_val>':{       
        'void':         ['<ret_val>', 0],
        ';':         ['<ret_val>', 0],
        '{':            ['<ret_val>', 1],
        'NOT':          ['<ret_val>', 1],
        'int_lit':      ['<ret_val>', 1],
        'float_lit':    ['<ret_val>', 1],
        'string_lit':   ['<ret_val>', 1],
        'true':         ['<ret_val>', 1],
        'false':        ['<ret_val>', 1],
        'tostr':        ['<ret_val>', 1],
        'toint':        ['<ret_val>', 1],
        'tofloat':      ['<ret_val>', 1],
        'tobool':       ['<ret_val>', 1],
        'len':          ['<ret_val>', 1],
        'upper':        ['<ret_val>', 1],
        'lower':        ['<ret_val>', 1],
        'trunc':        ['<ret_val>', 1],
        '(':            ['<ret_val>', 1],
        'listen':       ['<ret_val>', 1],
        '++':           ['<ret_val>', 1],
        '--':           ['<ret_val>', 1],
        'id':           ['<ret_val>', 1],
        'type':         ['<ret_val>', 2]
    },

    '<conditional>':{    
        'when':     ['<conditional>', 0],
        'choose':   ['<conditional>', 1]
    },

    '<ctrl_block>':{       
        'const':        ['<ctrl_block>', 0],
        'int':          ['<ctrl_block>', 0],
        'float':        ['<ctrl_block>', 0],
        'string':       ['<ctrl_block>', 0],
        'bool':         ['<ctrl_block>', 0],
        'mix':          ['<ctrl_block>', 0],
        'id':           ['<ctrl_block>', 0],
        '++':           ['<ctrl_block>', 0],
        '--':           ['<ctrl_block>', 0],
        'say':          ['<ctrl_block>', 0],
        'listen':       ['<ctrl_block>', 0],
        'when':         ['<ctrl_block>', 0],
        'choose':       ['<ctrl_block>', 0],
        'for':          ['<ctrl_block>', 0],
        'while':        ['<ctrl_block>', 0],
        'giveback':     ['<ctrl_block>', 0],
        'break':        ['<ctrl_block>', 0],
        'continue':     ['<ctrl_block>', 0]
    },

    '<ctrl_block_tail>':{       
        'const':        ['<ctrl_block_tail>', 0],
        'int':          ['<ctrl_block_tail>', 0],
        'float':        ['<ctrl_block_tail>', 0],
        'string':       ['<ctrl_block_tail>', 0],
        'bool':         ['<ctrl_block_tail>', 0],
        'mix':          ['<ctrl_block_tail>', 0],
        'id':           ['<ctrl_block_tail>', 0],
        '++':           ['<ctrl_block_tail>', 0],
        '--':           ['<ctrl_block_tail>', 0],
        'say':          ['<ctrl_block_tail>', 0],
        'listen':       ['<ctrl_block_tail>', 0],
        'when':         ['<ctrl_block_tail>', 0],
        'choose':       ['<ctrl_block_tail>', 0],
        'for':          ['<ctrl_block_tail>', 0],
        'while':        ['<ctrl_block_tail>', 0],
        'giveback':     ['<ctrl_block_tail>', 0],
        'break':        ['<ctrl_block_tail>', 0],
        'continue':     ['<ctrl_block_tail>', 0],
        '}':            ['<ctrl_block_tail>', 1],
        'case':         ['<ctrl_block_tail>', 1],
        'default':      ['<ctrl_block_tail>', 1]
    },

    '<ctrl_item>':{       
        'const':        ['<ctrl_item>', 0],
        'int':          ['<ctrl_item>', 0],
        'float':        ['<ctrl_item>', 0],
        'string':       ['<ctrl_item>', 0],
        'bool':         ['<ctrl_item>', 0],
        'mix':          ['<ctrl_item>', 0],
        'id':           ['<ctrl_item>', 0],
        '++':           ['<ctrl_item>', 0],
        '--':           ['<ctrl_item>', 0],
        'say':          ['<ctrl_item>', 0],
        'listen':       ['<ctrl_item>', 0],
        'when':         ['<ctrl_item>', 0],
        'choose':       ['<ctrl_item>', 0],
        'for':          ['<ctrl_item>', 0],
        'while':        ['<ctrl_item>', 0],
        'giveback':     ['<ctrl_item>', 0],
        'break':        ['<ctrl_item>', 1],
        'continue':     ['<ctrl_item>', 1]
    },

    '<ctrl_stmnt>':{    
        'break':    ['<ctrl_stmnt>', 0],
        'continue': ['<ctrl_stmnt>', 1]
    },
    
    '<else_tail>':{       
        'elsewhen':     ['<else_tail>', 0],
        'otherwise':    ['<else_tail>', 1],
        'const':        ['<else_tail>', 1],
        'int':          ['<else_tail>', 1],
        'float':        ['<else_tail>', 1],
        'string':       ['<else_tail>', 1],
        'bool':         ['<else_tail>', 1],
        'mix':          ['<else_tail>', 1],
        'id':           ['<else_tail>', 1],
        '++':           ['<else_tail>', 1],
        '--':           ['<else_tail>', 1],
        'say':          ['<else_tail>', 1],
        'listen':       ['<else_tail>', 1],
        'when':         ['<else_tail>', 1],
        'choose':       ['<else_tail>', 1],
        'for':          ['<else_tail>', 1],
        'while':        ['<else_tail>', 1],
        'giveback':     ['<else_tail>', 1],
        'break':        ['<else_tail>', 1],
        'continue':     ['<else_tail>', 1],
        '}':            ['<else_tail>', 1],
        'case':         ['<else_tail>', 1],
        'default':      ['<else_tail>', 1]
    },

    '<otherwise>':{       
        'otherwise':    ['<otherwise>', 0],
        'const':        ['<otherwise>', 1],
        'int':          ['<otherwise>', 1],
        'float':        ['<otherwise>', 1],
        'string':       ['<otherwise>', 1],
        'bool':         ['<otherwise>', 1],
        'mix':          ['<otherwise>', 1],
        'id':           ['<otherwise>', 1],
        '++':           ['<otherwise>', 1],
        '--':           ['<otherwise>', 1],
        'say':          ['<otherwise>', 1],
        'listen':       ['<otherwise>', 1],
        'when':         ['<otherwise>', 1],
        'choose':       ['<otherwise>', 1],
        'for':          ['<otherwise>', 1],
        'while':        ['<otherwise>', 1],
        'giveback':     ['<otherwise>', 1],
        'break':        ['<otherwise>', 1],
        'continue':     ['<otherwise>', 1],
        '}':            ['<otherwise>', 1],
        'case':         ['<otherwise>', 1],
        'default':      ['<otherwise>', 1]
    },

    '<case_tail>':{       
        'case':     ['<case_tail>', 0],
        'default':  ['<case_tail>', 1]
    },
    
    '<cases>':{
        'int_lit':      ['<cases>', 0],
        'float_lit':    ['<cases>', 0],
        'string_lit':   ['<cases>', 0],
        'true':         ['<cases>', 0],
        'false':        ['<cases>', 0],
        'id':           ['<cases>', 1]
    },

    '<literal>':{    
        'int_lit':      ['<literal>', 0],
        'float_lit':    ['<literal>', 0],
        'string_lit':   ['<literal>', 1],
        'true':         ['<literal>', 2],
        'false':        ['<literal>', 2]
    },

    '<iterative>':{    
        'for':      ['<iterative>', 0],
        'while':    ['<iterative>', 1]
    },

    '<ctrl_var>':{    
        'int':      ['<ctrl_var>', 0],
        'float':    ['<ctrl_var>', 1],
        'id':       ['<ctrl_var>', 2]
    },
    
    '<ctrl_id>':{
        '[':        ['<ctrl_id>', 0],
        ';':        ['<ctrl_id>', 0],
        '=':        ['<ctrl_id>', 1]
    },

    '<unary>':{    
        'id':['<unary>', 0],
        '++':['<unary>', 1],
        '--':['<unary>', 1]
    },
}