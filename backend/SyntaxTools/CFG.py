# string (production): list ng list ng string (production set)
#it is a dictionary, each key (<program>) is a nonterminal, each value is list of alternatives/ways to expand
CFG = {
    '<program>':[
        ['<global_var>', '<sub_func>', 'spyce', '(', ')', '->', 'void', '{', '<main_func_body>', 'giveback', '<void>', ';', '}']
    ],

    '<global_var>':[
        ['const', '<var_type>', ';', '<global_var>'], 
        ['<var_type>', ';', '<global_var>'],           
        []                                              
    ],

    '<data_type>':[    
        ['int'],
        ['float'],
        ['string'],
        ['bool']
    ],

    '<var_type>':[    
        ['<data_type>', 'id', '=', '<expr>', '<scaldec_tail>'],
        ['mix', '[', '<num_lit>', ']', '<arrtype>']
    ],

    '<arrtype>':[    
        ['id', '=', '<1d_val>', '<1d_dec_tail>'],
        ['[', '<num_lit>', ']', 'id', '=', '<2d_val>', '<2d_dec_tail>']
    ],

    '<scaldec_tail>':[    
        [',', 'id', '=', '<expr>', '<scaldec_tail>'],
        []
    ],

    '<num_lit>':[
        ['int_lit'],
        ['float_lit']
    ],

    '<1d_val>':[    
        ['id', '<inner_arr_indx>'],
        ['{', '<element_list>', '}']
    ],

    '<inner_arr_indx>':[    
        ['[', '<arith_expr>', ']'],
        ['(', '<args>', ')'],
        []
    ],

    '<element_list>':[    
        ['<expr>', '<val_tail>'],
        []
    ],
    
    '<val_tail>':[    
        [',', '<expr>', '<val_tail>'],
        []
    ],

    '<1d_dec_tail>':[    
        [',', 'id', '=', '<1d_val>', '<1d_dec_tail>'],
        []
    ],

    '<2d_val>':[    
        ['id'],
        ['{', '<2d_elem>', '}']
    ],

    '<2d_elem>':[    
        ['<1d_val>', '<2dval_tail>'],
        []
    ],

    '<2dval_tail>':[    
        [',', '<1d_val>', '<2dval_tail>'],
        []
    ],

    '<2d_dec_tail>':[    
        [',', 'id', '=', '<2d_val>', '<2d_dec_tail>'],
        []
    ],

    '<sub_func>':[    
        ['<sub_funcdec>', '<sub_func>'],
        []
    ],

    '<sub_funcdec>':[    
        ['make', 'id', '(', '<parameters>', ')', '->', '<func_ret>']
    ],

    '<parameters>':[    
        ['<par_dtype>', '<1d_indx>', 'id', '<par_tail>'],
        []
    ],
    
    '<par_dtype>':[
        ['<data_type>'],
        ['mix']
    ],

    '<1d_indx>':[    
        ['[', '<num_lit>', ']', '<2d_indx>'],
        []
    ],

    '<2d_indx>':[    
        ['[', '<num_lit>', ']'],
        []
    ],

    '<par_tail>':[    
        [',', '<par_dtype>', '<1d_indx>', 'id', '<par_tail>'],
        []
    ],

    '<func_ret>':[    
        ['<data_type>', '{', '<func_body>', '}'],
        ['void', '{', '<func_body>', '}'],
        ['mix', '[', ']', '<mix_func>']
    ],

    '<mix_func>':[
        ['[', ']', '{', '<func_body>', '}'],
        ['{', '<func_body>', '}']
    ],

    '<func_body>':[    
        ['<stmnt>', '<func_body>'],
        []
    ],

    '<main_func_body>':[    
        ['<main_stmnt>', '<main_func_body>'],
        []
    ],

    '<void>':[    
        ['void'],
        []
    ],

    '<main_stmnt>':[    
        ['<local_var>', ';'],
        ['id', '<id_tail>', ';'],
        ['<unary_op>', '<id_val>', ';'],
        ['<IO>', ';'],
        ['<conditional>'],
        ['<iterative>']
    ],

    '<stmnt>':[    
        ['<main_stmnt>'],
        ['giveback', '<ret_val>', ';']
    ],

    '<local_var>':[
        ['const', '<var_type>'],
        ['<var_type>']
    ],

    '<id_tail>':[    
        ['<id_accessor>'],
        ['<id_accessor_tail>']
    ],

    '<id_accessor>':[    
        ['[', '<arith_expr>', ']', '<accessor_tail>'],
        ['(', '<args>', ')']
    ],

    '<accessor_tail>':[    
        ['<id_accessor_tail>'],
        ['[', '<arith_expr>', ']', '<str_accessor>']
    ],

    '<str_accessor>':[
        ['[', '<arith_expr>', ']', '<str_assign_type>', '<expr>'],
        ['<id_accessor_tail>']
    ],
    
    '<id_accessor_tail>':[
        ['<unary_op>'],
        ['<assign_type>', '<expr>']
    ],
    
    '<unary_op>':[    
        ['++'],
        ['--']
    ],

    '<assign_type>':[    
        ['<str_assign_type>'],
        ['<spec_assign_type>']
    ],

    '<str_assign_type>':[
        ['='],
        ['+='],
    ],

    '<spec_assign_type>':[
        ['-='],
        ['*='],
        ['/='],
        ['**='],
        ['%=']
    ],

    '<args>':[    
        ['<expr>', '<val_tail>'],
        ['{', '<mix_lit>', '}'],
        []
    ],

    '<mix_lit>':[    
        ['<element_list>'],
        ['{', '<element_list>', '}', '<mix_lit_tail>']
    ],
    
    '<mix_lit_tail>':[    
        [',', '{', '<element_list>', '}'],
        []
    ],

    '<id_val>':[    
        ['id', '<indx_access>']
    ],

    '<indx_access>':[
        ['[', '<arith_expr>', ']', '<indx_access_tail>'],
        []
    ],

    '<indx_access_tail>':[
        ['[', '<arith_expr>', ']'],
        []
    ],

    '<expr>':[    
        ['<logical_or_expr>']
    ],

    '<logical_or_expr>':[    
        ['<and_expr>', '<chain_or>']
    ],

    '<chain_or>':[    
        ['OR', '<and_expr>', '<chain_or>'],
        []
    ],

    '<and_expr>':[    
        ['<equal_expr>', '<chain_and>']
    ],

    '<chain_and>':[    
        ['AND', '<equal_expr>', '<chain_and>'],
        []
    ],

    '<equal_expr>':[
        ['<relational_expr>', '<equal_expr_tail>']    
    ],

    '<equal_expr_tail>':[    
        ['==', '<relational_expr>'],
        ['!=', '<relational_expr>'],
        []
    ],

    '<relational_expr>':[    
        ['<arith_expr>', '<relational_expr_tail>']
    ],

    '<relational_expr_tail>':[    
        ['<relation_op>', '<arith_expr>'],
        []
    ],

    '<relation_op>':[    
        ['>'],
        ['<'],
        ['>='],
        ['<=']
    ],

    '<arith_expr>':[    
        ['<arith_operand>', '<arith_expr_tail>']  
    ],

    '<arith_expr_tail>':[    
        ['+', '<arith_operand>', '<arith_expr_tail>'],
        ['-', '<arith_operand>', '<arith_expr_tail>'],
        []
    ],

    '<arith_operand>':[    
        ['<expo_arith_operand>', '<arith_operand_tail>']
    ],

    '<arith_operand_tail>':[    
        ['*', '<expo_arith_operand>', '<arith_operand_tail>'],
        ['/', '<expo_arith_operand>', '<arith_operand_tail>'],
        ['%', '<expo_arith_operand>', '<arith_operand_tail>'],
        []
    ],

    '<expo_arith_operand>':[    
        ['<operand>', '<expo_arith_operand_tail>']
    ],

    '<expo_arith_operand_tail>':[    
        ['**', '<expo_arith_operand>', '<expo_arith_operand_tail>'],
        []
    ],

    '<operand>':[    
        ['<num_lit>'],
        ['<bool_lit>'],
        ['<spec_built_in>'],
        ['(', '<expr>', ')'],
        ['listen', '(', ')'],
        ['string_lit'],
        ['NOT', '<equal_expr>'],
        ['<unary_op>', 'id', '<indx_access>'],
        ['id', '<id_operand_tail>']
    ],

    '<bool_lit>':[
        ['true'],
        ['false']
    ],

    '<id_operand_tail>':[    
        ['(', '<args>', ')'],
        ['[', '<arith_expr>', ']', '<op_depth_1>'],
        ['<unary_op>'],
        []
    ],

    '<op_depth_1>':[
        ['<unary_op>'],
        ['[', '<arith_expr>', ']', '<op_depth_2>'],
        []
    ],

    '<op_depth_2>':[
        ['<unary_op>'],
        ['[', '<arith_expr>', ']'],
        []
    ],

    '<spec_built_in>':[
        ['tostr', '(', '<expr>', ')'],
        ['toint', '(', '<expr>', ')'],
        ['tofloat', '(', '<expr>', ')'],
        ['tobool', '(', '<expr>', ')'],
        ['len', '(', '<func_arg>', ')'],
        ['upper', '(', '<expr>', ')'],
        ['lower', '(', '<expr>', ')'],
        ['trunc', '(', '<expr>', ',', 'int_lit', ')']
    ],

    '<IO>':[    
        ['say', '(', '<say_arg>', ')'],
        ['listen', '(', ')']
    ],

    '<say_arg>':[
        ['type','(', '<func_arg>', ')'],
        ['<func_arg>']
    ],

    '<func_arg>':[
        ['{', '<mix_lit>', '}'],
        ['<expr>']
    ],

    '<ret_val>':[    
        ['<void>'],
        ['<func_arg>'],
        ['type', '(', '<func_arg>', ')']
    ],

    '<conditional>':[    
        ['when', '(', '<expr>', ')', '{', '<ctrl_block>', '}', '<else_tail>', '<otherwise>'],
        ['choose', '(', 'id', '<indx_access>', ')', '{', '<case_tail>', 'default', ':', '<ctrl_block>', '}']
    ],

    '<ctrl_block>':[    
        ['<ctrl_item>', '<ctrl_block_tail>']
    ],

    '<ctrl_block_tail>':[    
        ['<ctrl_item>', '<ctrl_block_tail>'],
        []
    ],

    '<ctrl_item>':[    
        ['<stmnt>'],
        ['<ctrl_stmnt>', ';']
    ],

    '<ctrl_stmnt>':[    
        ['break'],
        ['continue']
    ],
    
    '<else_tail>':[    
        ['elsewhen', '(', '<expr>', ')', '{', '<ctrl_block>', '}', '<else_tail>'],
        []
    ],

    '<otherwise>':[    
        ['otherwise', '{', '<ctrl_block>', '}'],
        []
    ],

    '<case_tail>':[    
        ['case', '<cases>', ':', '<ctrl_block>', '<case_tail>'],
        []
    ],

    '<cases>':[    
        ['<literal>'],
        ['id', '<indx_access>']
    ],

    '<literal>':[    
        ['<num_lit>'],
        ['string_lit'],
        ['<bool_lit>']
    ],

    '<iterative>':[    
        ['for', '(', '<ctrl_var>', ';', '<expr>', ';', '<unary>', ')', '{', '<ctrl_block>', '}'],
        ['while', '(', '<expr>', ')', '{', '<ctrl_block>', '}']
    ],

    '<ctrl_var>':[    
        ['int', 'id', '=', '<literal>'],
        ['float', 'id', '=', '<literal>'],
        ['id', '<ctrl_id>']
    ],
    
    '<ctrl_id>':[
        ['<indx_access>'],
        ['=', '<literal>']
    ],

    '<unary>':[    
        ['<id_val>', '<unary_op>'],
        ['<unary_op>', '<id_val>']
    ],
}