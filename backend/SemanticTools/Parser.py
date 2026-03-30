########## PARSER ##########
# The Parser is responsible for using the AST Nodes to form the structure of the code
# Behaves like the syntax analyzer but it builds the Tree from the AST Nodes where the Traverser will traverse through

"""ANSI escape codes for colors and styles. FOR DEBUGGING PURPOSES ONLY, CAN BE REMOVED"""
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
ENDC = '\033[0m'
op_brace = '{'
cl_brace = '}' 

from backend.LexerTools.Token import Token
from ..Error import ParseError
from .SymbolTable import SymbolTable
from .ASTNodes import (
    ASTNode, NumNode, StrLitNode, BoolLitNode, IdNode, BiArithNode, ExpoNode, RelNode, LogicNode, UnaryOperatorNode,
    UnaryNode, DataTypeNode, ConstNode, VoidNode, VarDecNode, AssignNode, MixLitNode, MixDecNode, MixIndxNode, MixIndxAssignNode,
    SpyceNode, ParamNode, MakeDecNode, FuncBodyNode, ArgsNode, FuncCallNode, SayNode, ListenNode, GivebackNode, WhenNode,
    ElsewhenNode, OtherwiseNode, ChooseNode, CaseNode, DefaultNode, ForLoopNode, ForHeaderNode, WhileNode, BreakNode,
    ContNode, ToStrNode, ToIntNode, ToFloatNode, ToBoolNode, TypeNode, LenNode, LowerNode, UpperNode, TruncNode
    )

"""     
HELPER FUNCTIONS THAT CONSUMES NEXT LINE
    - parseExpr 
    - parseCtrlBody 
    - parseUnaryArith 
    - parseId
    - parseIO
    - parseDec
    - parseMixLit

NOTES FOR FUTURE SESSIONS
- IF "NoneType object has no attribute 'parent'" the problem:
    -> CASE 1 (Recursion for counting digits): n / 10 returns a float, but the function only accepts integer
"""

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0
        self.current_token = tokens[self.token_idx]
        self.semantic_errors = []

    def advance(self):
        while True:
            self.token_idx += 1
            if self.token_idx < len(self.tokens):
                self.current_token = self.tokens[self.token_idx]
                if self.current_token.type not in ['\n', ' ', '\\n', 'space']:
                    break
            else:
                self.current_token = None
                break
        return self.current_token
    
    def reset(self):
        self.token_idx = -1
        self.advance()

    def look_ahead(self):
        current_idx = self.token_idx
        while True:
            current_idx += 1
            if current_idx < len(self.tokens):
                next_token = self.tokens[current_idx]
                if next_token.type not in ['\n', ' ', '\\n', 'space']:
                    return next_token
            else: return None
    
    ########## MAIN AST BUILDER FUNCTIONS ##########
    # Functions that builds the tree from tokens from the lexer
    # Works very similar to syntax analyzer
    # Represents the logical structure of the program instead of syntax (e.g. requiring ; at the end of every statement)

    # Function that starts the building of the Tree
    def build_ast(self):
        errors = []
        self.reset()
        root = ASTNode('Program')

        while self.current_token is not None and self.current_token.type != 'EOF':
            if self.current_token is not None and self.current_token.type in ['const', 'int', 'float', 'string', 'bool', 'mix', 'make', 'spyce']:
                dec, err = self.parseDec()
                if dec:
                    if isinstance(dec, list):
                        for d in dec: root.add_child(d)
                    else:
                        root.add_child(dec)
                if err:
                    if isinstance(err, list):
                        errors.extend(err)
                    else: 
                        errors.append(err)
            else: 
                errors.append(ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Invalid token -> {self.current_token.type} <- outside any function'))
                self.advance()
        return root, errors
        
    # Function that puts the tokens read to its corresponding node from the ASTNodes
    # Parses all the possible operands to expressions and arguments to function calls
    def parseFactor(self):
        tkn = self.current_token

        # Numerical Value
        if tkn.type in ('int_lit', 'float_lit'):
            self.advance()
            if tkn.type in ('++', '--'):
                op = self.current_token
                pos_end = self.current_token.pos_end
                self.advance()
                return UnaryNode(op, NumNode(tkn.value, tkn.pos_start, tkn.pos_end), postfix=True, pos_start=tkn.pos_start, pos_end=pos_end), None
            return NumNode(tkn.value, tkn.pos_start, tkn.pos_end), None
        
        # String literal
        elif tkn.type == 'string_lit':
            self.advance()
            return StrLitNode(tkn.value, tkn.pos_start, tkn.pos_end), None
        
        # true
        elif tkn.type == 'true':
            self.advance()
            return BoolLitNode(tkn.value, tkn.pos_start, tkn.pos_end), None

        # false
        elif tkn.type == 'false':
            self.advance()
            return BoolLitNode(tkn.value, tkn.pos_start, tkn.pos_end), None
        
        # nested expression
        elif tkn.type == '(':
            pos_start = tkn.pos_start
            self.advance()
            expr, err = self.parseExpr()
            
            if err: return None, err

            if self.current_token.type == ')':
                self.advance()
                return expr, None
            else:
                return None, ParseError(tkn.pos_start, tkn.pos_end, f'Expected -> ) <-'), None
        
        # Unary operation (prefix)
        elif tkn.type in ('++', '--'):
            indx1, indx2 = None, None
            op = tkn
            self.advance()
                    
            if self.current_token.type != 'id':
                return None, ParseError(tkn.pos_start, self.current_token.pos_end, f'Expected -> id <-')
            name = self.current_token.value
            id_pos_start = self.current_token.pos_start
            id_pos_end = self.current_token.pos_end
            self.advance()

            if self.current_token.type == '[':
                self.advance()
                indx1, err = self.parseExpr()
                if err: return None, err

                if self.current_token.type != ']':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ]')
                id_pos_end = self.current_token.pos_end
                self.advance()

                if self.current_token.type == '[':
                    self.advance()
                    indx2, err = self.parseExpr()
                    if err: return None, err

                    if self.current_token.type != ']':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ]')
                    id_pos_end = self.current_token.pos_end
                    self.advance()

                operand = MixIndxNode(name, indx1, indx2, id_pos_start, id_pos_end)
            else:
                operand = IdNode(name, id_pos_start, id_pos_end)
            
            return UnaryNode(op, operand, prefix=True, pos_start=op.pos_start, pos_end=op.pos_end), None
        
        # NOT
        elif tkn.type == 'NOT':
            op = tkn
            self.advance()
            factor, err = self.parseFactor()
            if err: return None, err

            return UnaryNode(op, factor, prefix=True, pos_start=op.pos_start, pos_end=op.pos_end), None
        
        # Mix index access
        elif tkn.type == 'id' and self.look_ahead().type == '[':
            pos_start = tkn.pos_start
            index1, index2 = None, None
            name = tkn.value
            mix_end = None
            self.advance()
            self.advance()

            index1, err = self.parseExpr()
            if err: return None, err

            if self.current_token.type != ']':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected: -> ] <-')
            self.advance()

            if self.current_token.type == '[':
                self.advance()

                index2, err = self.parseExpr()
                if err: return None, err

                if self.current_token.type != ']':
                    return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected: -> ] <-')
                mix_end = self.current_token.pos_end
                self.advance()

            if self.current_token.type in ['++', '--']:
                op = self.current_token
                self.advance()

                return UnaryNode(op, MixIndxNode(name, index1, index2, pos_start, mix_end), postfix=True, pos_start=pos_start, pos_end=self.current_token.pos_end), None

            return MixIndxNode(name, index1, index2, pos_start, self.current_token.pos_end), None
        
        # Function call
        elif tkn.type == 'id' and self.look_ahead().type == '(':
            pos_start = tkn.pos_start
            name = tkn.value
            args = []
            self.advance()
            self.advance()
            
            while self.current_token.type != ')':
                arg, err = self.parseExpr()

                if err: return None, err
                args.append(arg)

                if self.current_token.type == ',':
                    while self.current_token.type == ',':
                        self.advance()
                        
                        arg, err = self.parseExpr()
                        if err: return None, err
                        args.append(arg)
            
            if self.current_token.type == ')':
                pos_end = self.current_token.pos_end
                self.advance()
                return FuncCallNode(name, args, pos_start, pos_end), None
            else:
                pos_end = self.current_token.pos_end
                self.advance()
                return None, ParseError(pos_start, pos_end, 'Expected: -> ) <-')

        # Unary oepration (postfix)
        elif tkn.type == 'id':
            pos_start = tkn.pos_start
            name = tkn.value
            self.advance()
            if self.current_token.type in ('++', '--'):
                op = self.current_token
                self.advance()
                
                return UnaryNode(op, IdNode(name, pos_start, tkn.pos_end), postfix=True, pos_start=pos_start, pos_end=tkn.pos_end), None
            
            # Id only
            return IdNode(name, pos_start, tkn.pos_end), None

        # Compound assignment
        elif tkn.type == 'id' and self.look_ahead().type in ['+=', '-=', '*=', '/=', '%=', '**=']:
            pos_start = tkn.pos_start
            name = tkn.val
            op = None
            self.advance()
            if self.current_token.type == '+=': op = '+'
            elif self.current_token.type == '-=': op = '-'
            elif self.current_token.type == '*=': op = '*'
            elif self.current_token.type == '**=': op = '**'
            elif self.current_token.type == '/=': op = '/'
            elif self.current_token.type == '%=': op = '%'
            self.advance()
            
            val, err = self.parseExpr()
            if err: return None, err

            left = IdNode(name, pos_start, self.current_token.pos_end)
            right = val
            arith_node = BiArithNode(left, Token(op, pos_start=left.pos_start, pos_end=right.pos_end), right, pos_start, self.current_token.pos_end)

            return AssignNode(name, arith_node, pos_start, self.current_token.pos_end), None

        # listen
        elif tkn.type == 'listen':
            self.advance()
            if self.current_token.type != '(':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> ( <-')
            self.advance()

            if self.current_token.type != ')':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected: -> ) <-')
            self.advance()

            return ListenNode(tkn.pos_start, self.current_token.pos_end), None
        
        # toint
        elif tkn.type == 'toint':
            self.advance()

            if self.current_token.type != '(':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> ( <-')
            self.advance()

            arg, err = self.parseExpr()
            if err: return None, err
            
            if self.current_token.type != ')':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected: -> ) <-')
            self.advance()
        
            return ToIntNode(arg, tkn.pos_start, self.current_token.pos_end), None
        
        # tofloat
        elif tkn.type == 'tofloat':
            self.advance()
            if self.current_token.type != '(':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> ( <-')
            self.advance()

            arg, err = self.parseExpr()
            if err: return None, err
            
            if self.current_token.type != ')':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected: -> ) <-')
            self.advance()
        
            return ToFloatNode(arg, tkn.pos_start, self.current_token.pos_end), None
        
        # tostr
        elif tkn.type == 'tostr':
            self.advance()
            if self.current_token.type != '(':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> ( <-')
            self.advance()

            arg, err = self.parseExpr()
            if err: return None, err
            
            if self.current_token.type != ')':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected: -> ) <-')
            self.advance()

            return ToStrNode(arg, tkn.pos_start, self.current_token.pos_end), None

        # tobool
        elif tkn.type == 'tobool':
            self.advance()
            if self.current_token.type != '(':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> ( <-')
            self.advance()
            
            arg, err = self.parseExpr()
            if err: return None, err
            
            if self.current_token.type != ')':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected: -> ) <-')
            self.advance()

            return ToBoolNode(arg, tkn.pos_start, self.current_token.pos_end), None
        
        # len
        elif tkn.type == 'len':
            pos_start = tkn.pos_start
            len_arg = None
            self.advance()

            if self.current_token.type != '(':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> ( <-')
            self.advance()

            if self.current_token.type == '{':
                len_arg, err = self.parseMixLit()
                if err: return None, err

            else:
                len_arg, err = self.parseExpr()
                if err: return None, err
            
            if self.current_token.type != ')':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> ) <-')
            self.advance()

            return LenNode(len_arg, tkn.pos_start, self.current_token.pos_end), None
        
        # lower
        elif tkn.type == 'lower':
            self.advance()
            if self.current_token.type != '(':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> ( <-')
            self.advance()

            lower_val, err = self.parseExpr()
            if err: return None, err
            
            if self.current_token.type != ')':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> ) <-')
            self.advance()

            return LowerNode(lower_val, tkn.pos_start, self.current_token.pos_end), None

        # upper
        elif tkn.type == 'upper':
            self.advance()
            if self.current_token.type != '(':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> ( <-')
            self.advance()

            upper_val, err = self.parseExpr()
            if err: return None, err
            
            if self.current_token.type != ')':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> ) <-')
            self.advance()

            return UpperNode(upper_val, tkn.pos_start, self.current_token.pos_end), None
            
        # trunc
        elif tkn.type == 'trunc':
            self.advance()
            if self.current_token.type != '(':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> ( <-')
            self.advance()

            arg1, err = self.parseExpr()
            if err: return None, err

            if self.current_token.type != ',':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> , <-')
            self.advance()

            arg2 = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
            self.advance()

            if self.current_token.type != ')':
                return None, ParseError(tkn.pos_start, tkn.pos_end, 'Expected -> ) <-')
            pos_end = self.current_token.pos_end
            self.advance()

            return TruncNode(arg1, arg2, tkn.pos_start, pos_end), None

        else:
            return None, ParseError(tkn.pos_start, tkn.pos_end, f'Unexpected -> {tkn.type} <-. Expected one of [int_lit, float_lit, string_lit, true, false, id, "(", "++", "--", "NOT", "toint", "tofloat", "tostr", "tobool", "len", "lower", "upper", "trunc", "listen"]')
    
    def parseExpr(self):    return self.parseLog()    

    def parseLog(self):     return self.parseBiArith(self.parseEq, ['AND', 'OR'], LogicNode)

    def parseEq(self):      return self.parseBiArith(self.parseRel, ['==', '!='], RelNode)

    def parseRel(self):     return self.parseBiArith(self.parseArith, ['<', '>', '<=', '>='], RelNode)

    def parseArith(self):   return self.parseBiArith(self.parseTerm, ['+', '-'], BiArithNode)

    def parseTerm(self):    return self.parseBiArith(self.parseExpo, ['*', '/', '%'], BiArithNode)

    def parseExpo(self):    return self.parseBiArith(self.parseFactor, ['**'], ExpoNode)

    def parseBiArith(self, func, ops, node): 
        pos_start = self.current_token.pos_start
        left, err = func()
        if err: return None, err

        while self.current_token.type in ops:
            op = self.current_token
            self.advance()
            right, err = func()
            if err: return None, err
            left = node(left, op, right, pos_start, self.current_token.pos_end)
        
        return left, None

    def parseId(self):
        if self.current_token.type != 'id':
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: id')
        
        name = self.current_token.value
        pos_start = self.current_token.pos_start
        id_assign = ['=', '+=', '-=', '*=', '/=', '%=', '**=']
        id_unary = ['++', '--']
        expected_id = id_assign + id_unary + ['(', '[', ',', ';']
        self.advance()

        if self.current_token.type not in expected_id:
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {expected_id}')

        # Calling id only
        elif self.current_token.type in id_assign:
            op = self.current_token.type
            value = None
            pos_end = None
            expected_operand = ['tostr', 'toint', 'tofloat', 'tobool', 'len', 'upper', 'lower', 'trunc', '(', 'listen', 'string_lit', 'NOT', '++', '--', 'id', 'int_lit', 'float_lit', 'true', 'false',]
            self.advance()

            if self.current_token.type not in expected_operand:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {expected_operand}')

            else:
                value, err = self.parseExpr()
                if err: return None, err
            if op == '=':
                pos_end = self.current_token.pos_end

                if self.current_token.type != ';':
                    return None, ParseError(pos_start, pos_end, f"Unexpected -> {self.current_token.type} <-. Expected ;")
                self.advance()

                return AssignNode(name, value, pos_start, pos_end), None
            else:
                left = IdNode(name, pos_start, pos_end)
                arith_op = op[0]
                right = value
                arith_tkn = type('Token', (object,), {'type': arith_op, 'value': arith_op, 'pos_start': self.current_token.pos_start, 'pos_end': self.current_token.pos_end})()
                
                if arith_op == '**':
                    arith_node == ExpoNode(left, arith_tkn, right, pos_start, self.current_token.pos_end)
                else:
                    arith_node = BiArithNode(left, arith_tkn, right, pos_start, self.current_token.pos_end)

                if self.current_token.type != ';':
                    return None, ParseError(pos_start, pos_end, f"Unexpected -> {self.current_token.type} <-. Expected ;")
                pos_end = self.current_token.pos_end
                self.advance()

                return AssignNode(name, arith_node, pos_start, pos_end), None

        # Calling a mix index
        elif self.current_token.type == '[':
            index1, index2 = None, None
            self.advance()

            index1, err = self.parseExpr()
            if err: return None, err

            if self.current_token.type != ']':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, 'Expected: -> ] <-')
            self.advance()

            if self.current_token.type == '[':
                self.advance()
                index2, err = self.parseExpr()
                if err: return None, err

                if self.current_token.type != ']':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, 'Expected: -> ] <-')
                self.advance()

            if self.current_token.type not in id_assign + id_unary:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {id_assign + id_unary}')
            op_type = self.current_token.type
            op = self.current_token
            self.advance()

            if op_type in id_assign:
                val, err = self.parseExpr()
                if err: return None, err

                if op.type == '=':
                    pos_end = self.current_token.pos_end

                    if self.current_token.type != ';':
                        return None, ParseError(pos_start, pos_end, f"Unexpected -> {self.current_token.type} <-. Expected ;")
                    self.advance()

                    return MixIndxAssignNode(name, index1, index2, val, pos_start, pos_end), None
                else:
                    left = MixIndxNode(name, index1, index2, pos_start, self.current_token.pos_end)
                    arith_op = op.type[0]
                    right = val
                    arith_tkn = type('Token', (object,), {'type': arith_op, 'value': arith_op, 'pos_start': self.current_token.pos_start, 'pos_end': self.current_token.pos_end})()

                    if arith_op == '**':
                        arith_node = ExpoNode(left, arith_tkn, right, pos_start, self.current_token.pos_end)
                    else:
                        arith_node = BiArithNode(left, arith_tkn, right, pos_start, self.current_token.pos_end)

                    if self.current_token.type != ';':
                        return None, ParseError(pos_start, pos_end, f"Unexpected -> {self.current_token.type} <-. Expected ;")
                    pos_end = self.current_token.pos_end
                    self.advance()

                    return MixIndxAssignNode(name, index1, index2, arith_node, pos_start, pos_end), None
            
            elif op_type in id_unary:
                pos_end = self.current_token.pos_end
                if self.current_token.type != ';':
                    return None, ParseError(pos_start, pos_end, f"Unexpected -> {self.current_token.type} <-. Expected ;")
                self.advance()

                return UnaryNode(op, MixIndxNode(name, index1, index2, pos_start, pos_end), prefix=False, postfix=True, pos_start=pos_start, pos_end=pos_end), None

        # Calling a function
        elif self.current_token.type == '(':
            self.advance()
            args = []

            while self.current_token.type != ')':
                if self.current_token.type == '{':
                    arg, err = self.parseMixLit()
                    if err: return None, err
                else:
                    arg, err = self.parseExpr()
                    if err: return None, err
                args.append(arg)
                if self.current_token.type == ',':
                    while self.current_token.type == ',':
                        self.advance()
                        arg, err = self.parseExpr()
                        if err: return None, err
                        args.append(arg)
            pos_end = self.current_token.pos_end
            self.advance()

            if self.current_token.type != ';':
                return None, ParseError(pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ;")
            self.advance()

            return FuncCallNode(name, args, pos_start, pos_end), None
        
        # Chain declaration
        elif self.current_token.type == ',':
            self.advance()
            pos_end = self.current_token.pos_end
            val, err = self.parseExpr()
            if err: return None, err

            return AssignNode(name, val, pos_start, pos_end), None

        # Prefix unary operation
        elif self.current_token.type in ('++', '--'):
            op = self.current_token
            self.advance()
            if self.current_token.type != ';':
                return None, ParseError(pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ;")
            pos_end = self.current_token.pos_end
            self.advance()

            return UnaryNode(op, IdNode(name, pos_start, pos_end), postfix=True, pos_start=pos_start, pos_end=pos_end), None
        
        # Assigning using id as operand
        elif self.current_token.type == ';':
            self.advance()
            return IdNode(name, pos_start, self.current_token.pos_end), None

        # Id as operands
        elif self.current_token.type == ')':
            self.advance()
            return IdNode(name, pos_start, self.current_token.pos_end), None
        return None, ParseError(self.current_token.pos_start, self.current_token.pos_start, f'Unexpected -> {self.current_token.type} <-. Expected: id')

    # Declarations for 1s outside functions, subfunctions, and spyce
    def parseDec(self): 
            ret_types =  ['int', 'float', 'string', 'bool', 'mix', 'void']
            all_types =  ['int', 'float', 'string', 'bool', 'mix']
            scal_types = ['int', 'float', 'string', 'bool']
            const_flag = None
            pos_start, var_type = None, None

            # VARIABLE DECLARATION
            # Constant variable declaration
            if self.current_token.type == 'const':
                pos_start = self.current_token.pos_start
                self.advance()
                const_flag = True
                if self.current_token.type not in all_types:
                    return None, ParseError(pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {all_types}')

            # Scalar variable declaration (int, float, string, bool)
            if self.current_token.type in scal_types:
                pos_start = self.current_token.pos_start
                var_type = self.current_token.type
                name = None
                declarations = []
                self.advance()

                while True:
                    if self.current_token.type != 'id':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: id')
                    name = self.current_token.value
                    self.advance()

                    if self.current_token.type != '=':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: =')
                    self.advance()

                    val, err = self.parseExpr()
                    if err: return None, err

                    declarations.append(VarDecNode(const_flag, var_type, name, val, pos_start, self.current_token.pos_end)) 

                    if self.current_token.type == ',':
                        self.advance()
                    else:
                        break

                if self.current_token.type != ';':
                    return None, ParseError(pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected ;')
                self.advance()
                
                if len(declarations) > 1:
                    return declarations, None
                else:
                    return declarations[0], None
            
            # MIX DECLARATION
            elif self.current_token.type == 'mix':
                pos_start = self.current_token.pos_start
                index1, index2 = None, None
                name = None
                mix_lit_expected = ['int_lit', 'float_lit', 'string_lit', 'true', 'false', 'toint', 'tofloat', 'tostring', 'tobool', 'len', 'trunc', 'upper', 'lower', 'id']
                self.advance()

                if self.current_token.type != '[':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: [')
                self.advance()

                if self.current_token.type not in ['int_lit', 'float_lit']:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: [\'int_lit\', \'float_lit\']')
                index1 = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                self.advance()

                if self.current_token.type != ']':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ]')
                self.advance()

                if self.current_token.type not in ['[', 'id']:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: [\'[\', \'id\']')

                # If one dimensional array
                if self.current_token.type == 'id':
                    name = self.current_token.value
                    self.advance()

                    if self.current_token.type != '=':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: =')
                    init_val = []
                    self.advance()

                    expected_init = ['id', '{']
                    if self.current_token.type not in expected_init:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {expected_init}')

                    if self.current_token.type == '{':
                        self.advance()
                        mix_lit_start = self.current_token.pos_start

                        while self.current_token.type != '}':
                            if self.current_token.type not in mix_lit_expected:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: {mix_lit_expected}")
                            val, err = self.parseExpr()
                            if err: return None, err

                            init_val.append(val)

                            expected_chain = [',', '}']
                            if self.current_token.type not in [',', '}']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: {expected_chain}")
                            
                            if self.current_token.type == ',':
                                self.advance()

                        if self.current_token.type != '}':
                            brace = '}'
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: {brace}")
                        pos_end = self.current_token.pos_end
                        self.advance()
                        mix_node = MixLitNode(init_val, mix_lit_start, pos_end)

                        if self.current_token.type != ';':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ;")
                        self.advance()

                    elif self.current_token.type == 'id':
                        name = self.current_token.value
                        name_start = self.current_token.pos_start
                        self.advance()

                        if self.current_token.type not in [';', '[']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: [';', '[']")
                        
                        if self.current_token.type == ';':
                            mix_node = IdNode(name, name_start, self.current_token.pos_end)
                            self.advance()

                        elif self.current_token.type == '[':
                            self.advance()

                            index_val, err = self.parseExpr()
                            if err: return None, err

                            if self.current_token.type != ';':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ';'")
                            mix_node = MixIndxNode(name, index_val, index2=None, pos_start=name_start, pos_end=self.current_token.pos_end)
                            self.advance()

                    return MixDecNode(const_flag, name, index1, index2, mix_node, pos_start, pos_end), None

                # If two dimensional array
                elif self.current_token.type != '[':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: [')
                self.advance()

                if self.current_token.type not in ['int_lit', 'float_lit']:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: [\'int_lit\', \'float_lit\']')
                index2 = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                self.advance()

                if self.current_token.type != ']':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ]')
                self.advance()

                if self.current_token.type != 'id':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: id')
                name = self.current_token.value
                self.advance()

                if self.current_token.type != '=':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: =')
                init_val = []
                self.advance()

                expected_init = ['id', '{']
                if self.current_token.type not in expected_init:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {expected_init}')
                
                if self.current_token.type == '{':
                    self.advance()
                    mix_lit_start = self.current_token.pos_start

                    while self.current_token.type != '}':
                        if self.current_token.type != '{':
                            op_brace = '{'
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {op_brace}')

                        row_start = self.current_token.pos_start
                        self.advance()
                        row_vals = []

                        while self.current_token.type != '}':
                            if self.current_token.type not in mix_lit_expected:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: {mix_lit_expected}")
                            val, err = self.parseExpr()
                            if err: return None, err

                            row_vals.append(val)

                            if self.current_token.type == ',':
                                self.advance()
                            elif self.current_token.type != '}':
                                brace = '}'
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: {brace}")
                        
                        row_end = self.current_token.pos_end
                        self.advance()
                        init_val.append(MixLitNode(row_vals, row_start, row_end))

                        if self.current_token.type == ',':
                            self.advance()

                    if self.current_token.type != '}':
                        brace = '}'
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: {brace}")
                    pos_end = self.current_token.pos_end
                    self.advance()

                    if self.current_token.type != ';':
                        return None, ParseError(pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected ;')
                    self.advance()

                    mix_node = MixLitNode(init_val, mix_lit_start, pos_end)

                elif self.current_token.type == 'id':
                    name = self.current_token.value
                    name_start = self.current_token.pos_start
                    self.advance()

                    if self.current_token.type != ';':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ;")
                    mix_node = IdNode(name, name_start, self.current_token.pos_end)
                    self.advance()

                return MixDecNode(const_flag, name, index1, index2, mix_node, pos_start, pos_end), None

            # FUNCTION DECLARATION
            elif self.current_token.type == 'make':
                pos_start = self.current_token.pos_start
                parameters = []
                self.advance()

                if self.current_token.type != 'id':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: id')
                name = self.current_token.value
                self.advance()
                
                # PARAMETERS
                if self.current_token.type != '(':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: (')
                size1, size2 = None, None
                self.advance()
               
                while self.current_token.type != ')':
                    if self.current_token.type not in all_types:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {all_types}')
                    param_type = self.current_token.type
                    self.advance()

                    if param_type == 'mix':
                        if self.current_token.type != '[':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: [')
                        self.advance()

                        if self.current_token.type not in ['int_lit', 'float_lit']:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: [\'int_lit\', \'float_lit\', \'true\', \'false\']')
                        size1 = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                        self.advance()

                        if self.current_token.type != ']':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ]')
                        self.advance()

                        if self.current_token.type == 'id':
                            param_id = self.current_token.value

                        elif self.current_token.type == '[':
                            self.advance()
                            if self.current_token.type not in ['int_lit', 'float_lit']:
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: [\'int_lit\', \'float_lit\', \'true\', \'false\']')
                            size2 = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()

                            if self.current_token.type != ']':
                                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ]')
                            self.advance()
                            
                    if self.current_token.type != 'id':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: id')
                    param_id = self.current_token.value
                    self.advance()

                    param_node = ParamNode(param_type, param_id, size1, size2, pos_start=pos_start, pos_end=self.current_token.pos_end)
                    parameters.append(param_node)

                    chain_param = [',', ')']
                    if self.current_token.type not in chain_param:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {chain_param}')
                    
                    if self.current_token.type == ',':
                        self.advance()
                self.advance()

                # ARROW
                if self.current_token.type != '->':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ->')
                self.advance()

                # RETURN TYPE
                if self.current_token.type not in ret_types:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {ret_types}')
                
                return_type = self.current_token.type
                if self.current_token.type == 'mix':
                    self.advance()
                    if self.current_token.type != '[':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: [')
                    self.advance()

                    if self.current_token.type != ']':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ]')
                    self.advance()

                    if self.current_token.type == '[':
                        self.advance()
                        if self.current_token.type != ']':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ]')
                        self.advance()
                else:
                    self.advance()
                
                # FUNCTION DEFINITION
                if self.current_token.type != '{':
                    op_brace = '{'
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {op_brace}')
                self.advance()

                body_node, err = self.parseBody()
                if err: return None, err

                if self.current_token.type != '}':
                    cl_brace = '}'
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {cl_brace}')

                pos_end = self.current_token.pos_end
                self.advance()
                return MakeDecNode(name, parameters, return_type, body_node, pos_start, pos_end), None
            
            # SPYCE DECLARATION
            elif self.current_token.type == 'spyce': 
                pos_start = self.current_token.pos_start
                self.advance()

                if self.current_token.type != '(':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: (')
                self.advance()

                if self.current_token.type != ')':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: )')
                self.advance()

                if self.current_token.type != '->':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ->')
                self.advance()

                if self.current_token.type != 'void':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: void')
                self.advance()

                if self.current_token.type != '{':
                    op_brace = '{'
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {op_brace}')
                self.advance()

                spyce_comp, err = self.parseSpyceBody()
                if err: return None, err

                if self.current_token.type != '}':
                    cl_brace = '}'
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {cl_brace}')
                pos_end = self.current_token.pos_end
                self.advance()

                return SpyceNode(spyce_comp['spyce_body'], spyce_comp['giveback'], pos_start, pos_end), None

    # SPYCE FUNCTION
    def parseSpyceBody(self):
        body = FuncBodyNode()
        errors = []

        while self.current_token.type != 'giveback':
            node, err = self.parseStatement()

            if err: 
                errors.append(err)
                continue
            if isinstance(node, list):
                for n in node:
                    body.add_child(n)
            else:
                body.add_child(node)
        
        give_node, give_err = self.parseGiveback()
        if give_err: errors.append(give_err)
        
        return {'spyce_body': body, 'giveback': give_node}, errors

    # SUB-FUNCTIONS
    def parseBody(self):
        body = FuncBodyNode()
        errors = []

        while self.current_token.type != '}':
            if self.current_token.type == 'giveback':
                node, err = self.parseGiveback()
            else:
                node, err = self.parseStatement()

            if err: 
                errors.append(err)
                continue
            body.add_child(node)

        if self.current_token.type != '}':
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {cl_brace}')

        return body, errors

    def parseCtrlStmnt(self):
        print(f'ENTERED PARSECTRLSTMTN -> {self.current_token.type}')
        ctrl_start = self.current_token.pos_start
        ctrl_end = None

        if self.current_token.type == 'break':
            self.advance()
            if self.current_token.type != ';':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ;")
            ctrl_end = self.current_token.pos_end
            self.advance()

            return BreakNode(ctrl_start, ctrl_end), None

        elif self.current_token.type == 'continue':
            self.advance()
            if self.current_token.type != ';':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ;")
            ctrl_end = self.current_token.pos_end
            self.advance()

            return ContNode(ctrl_start, ctrl_end), None

    # CTRL STATEMENTS FOR CONDITIONAL AND ITERATIVE
    def parseCtrlBody(self): 
        ctrl_body_start = self.current_token.pos_start
        ctrl_stmnts = ['break', 'continue']
        ctrl_body = FuncBodyNode()

        if self.current_token.type in ['}', 'case', 'default']:
            return None, ParseError(ctrl_body_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Control statements cannot have empty definitions")

        while self.current_token.type not in ['}', 'case', 'default']:
            # CONTROL STATEMENTS
            if self.current_token.type in ctrl_stmnts:
                node, err = self.parseCtrlStmnt()
                if err: return None, err
                else: ctrl_body.add_child(node)

            # GIVEBACK
            elif self.current_token.type == 'giveback':
                node, err = self.parseGiveback()
                if err: return None, err
                else: ctrl_body.add_child(node)
                    
            # OTHER STATEMENTS
            else:
                stmnt, err = self.parseStatement()
                if err: return None, err
                if stmnt:
                    if isinstance(stmnt, list):
                        for s in stmnt:
                            ctrl_body.add_child(s)
                    else: ctrl_body.add_child(stmnt)
        
        return ctrl_body, None
    
    # UNARY OPERATION
    def parseUnaryArith(self):
        expected_unary = ['id', '++', '--']
        if self.current_token.type not in expected_unary:
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: {expected_unary}")

        if self.current_token.type in ['++', '--']:
            unary_start = self.current_token.pos_start
            op = self.current_token
            self.advance()

            if self.current_token.type != 'id':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: id')
            name = self.current_token.value
            unary_end = self.current_token.pos_end
            self.advance()

            if self.current_token.type == '[':
                index1, index2 = None, None
                self.advance()
                index1, err = self.parseExpr()
                if err: return None, err

                if self.current_token.type != ']':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ]")
                self.advance()
                
                # 2 dimensional mix (add returning nodes)
                if self.current_token.type == '[':
                    self.advance()
                    index2, err = self.parseExpr()
                    if err: return None, err

                    if self.current_token.type != ']':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ]")
                    pos_end = self.current_token.pos_end
                    self.advance()

                    if self.current_token.type == ';' or self.current_token.type == ')':
                        self.advance()

                    return UnaryNode(op, MixIndxNode(name, index1, index2, unary_start, pos_end), prefix=True, postfix=False, pos_start=unary_start, pos_end=pos_end), None

                # 1 dimensional mix (add returning nodes)
                elif self.current_token.type not in [';', ')']:
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: [';', ')']")
                pos_end = self.current_token.pos_end
                self.advance()

                return UnaryNode(op, MixIndxNode(name, index1, index2, unary_start, pos_end), prefix=True, postfix=False, pos_start=unary_start, pos_end=pos_end), None

            elif self.current_token.type == ';' or self.current_token.type == ')':
                self.advance()
            else:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: [';', '[', ')']")

            return UnaryNode(op, IdNode(name, unary_start, unary_end), prefix=True, postfix=False, pos_start=unary_start, pos_end=unary_end), None

        elif self.current_token.type == 'id':
            unary_start = self.current_token.pos_start
            name = self.current_token.value
            self.advance()

            if self.current_token.type not in ['++', '--']:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ['++', '--']")
            op = self.current_token
            unary_end = self.current_token.pos_end
            self.advance()

            return UnaryNode(op, IdNode(name, unary_start, unary_end), postfix=True, pos_start=unary_start, pos_end=unary_end), None

    # INPUT/OUTPUT
    def parseIO(self):
        # SAY
        if self.current_token.type == 'say':
            arg_node = None
            say_start = self.current_token.pos_start
            self.advance()
            if self.current_token.type != '(':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: (')
            self.advance()

            if self.current_token.type == 'type':
                type_start = self.current_token.pos_start
                self.advance()
                
                if self.current_token.type != '(':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: (')
                self.advance()

                typeExpr, err = self.parseExpr()
                if err: return None, err

                if self.current_token.type != ')':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: )')
                type_end = self.current_token.pos_end
                self.advance()

                arg_node = TypeNode(typeExpr, type_start, type_end)

            elif self.current_token.type == '{':
                arg_node, err = self.parseMixLit()
                if err: return None, err

            else:
                arg_node, err = self.parseExpr()
                if err: return None, err

            if self.current_token.type != ')':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: )')
            self.advance()

            if self.current_token.type != ';':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ;')
            say_end = self.current_token.pos_end
            self.advance()

            return SayNode(arg_node, say_start, say_end), None

        # LISTEN  
        elif self.current_token.type == 'listen':
            listen_start = self.current_token.pos_start
            self.advance()

            if self.current_token.type != '(':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: (')
            self.advance()

            if self.current_token.type != ')':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: )')
            self.advance()

            if self.current_token.type != ';':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ;')
            listen_end = self.current_token.pos_end
            self.advance()

            return ListenNode(listen_start, listen_end), None

    # CONDITIONAL
    def parseConditional(self): 
        # when
        if self.current_token.type == 'when':
            when_start = self.current_token.pos_start
            elsewhen = []
            oth_node = None
            self.advance()

            if self.current_token.type != '(':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: (')
            self.advance()

            when_expr, err = self.parseExpr()
            if err:
                return None, err
            
            if self.current_token.type != ')':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: )')
            self.advance()

            if self.current_token.type != '{':
                op_brace = '{'
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {op_brace}')
            self.advance()

            when_block, when_err = self.parseCtrlBody()
            if when_err:
                return None, when_err
            
            if self.current_token.type != '}':
                op_brace = '}'
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {op_brace}')
            self.advance()

            # elsewhen
            if self.current_token.type == 'elsewhen':
                while self.current_token.type == 'elsewhen':
                    ew_start = self.current_token.pos_start
                    self.advance()

                    if self.current_token.type != '(':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: (')
                    self.advance()

                    ew_expr, ew_cond_err = self.parseExpr()
                    if ew_cond_err:
                        return None, ew_cond_err

                    if self.current_token.type != ')':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: )')
                    self.advance()

                    if self.current_token.type != '{':
                        op_brace = '{'
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {op_brace}')
                    self.advance()

                    ew_body, ew_body_err = self.parseCtrlBody()
                    if ew_body_err:
                        return None, ew_body_err
                
                    if self.current_token.type != '}':
                        op_brace = '}'
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {op_brace}')
                    ew_end = self.current_token.pos_end

                    elsewhen.append(ElsewhenNode(ew_expr, ew_body, ew_start, ew_end))
                    self.advance()

            # otherwise
            if self.current_token.type == 'otherwise':
                oth_start = self.current_token.pos_start
                self.advance()

                if self.current_token.type != '{':
                    op_brace = '{'
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {op_brace}')
                self.advance()

                oth_block, oth_err = self.parseCtrlBody()
                if oth_err:
                    return None, oth_err

                if self.current_token.type != '}':
                    op_brace = '}'
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {op_brace}')
                
                oth_end = self.current_token.pos_end
                oth_node = OtherwiseNode(oth_block, oth_start, oth_end)
                self.advance()

            return WhenNode(when_expr, when_block, elsewhen, oth_node, when_start, self.current_token.pos_end), None
        
        elif self.current_token.type == 'choose':
            choose_start = self.current_token.pos_start
            id_node = None
            cases = []
            self.advance()

            if self.current_token.type == '(':
                self.advance()

                if self.current_token.type != 'id':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: id')
                name = self.current_token.value

                id_node = IdNode(name, self.current_token.pos_start, self.current_token.pos_end)
                self.advance()

                if self.current_token.type == '[': 
                    self.advance()
                    val1, err = self.parseExpr()
                    if err: return None, err
                    
                    if self.current_token.type != ']':
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ]')
                    self.advance()

                    if self.current_token.type not in (')', '['):
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: [')', '[']")

                    if self.current_token.type == '[':
                        self.advance()

                        val2, err = self.parseExpr()
                        if err: return None, err
                    
                        if self.current_token.type != ']':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ]')
                        id_node = MixIndxNode(name, val1, val2, choose_start, self.current_token.pos_end)
                        self.advance()

                if self.current_token.type != ')':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: )')     
                self.advance()

                if self.current_token.type != '{':
                    op_brace = '{'
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {op_brace}')
                self.advance()

                expected_cases = ['int_lit', 'float_lit', 'string_lit', 'true', 'false', 'id']
                while self.current_token.type != '}':
                    if self.current_token.type == 'case':
                        case_start = self.current_token.pos_start
                        self.advance()

                        if self.current_token.type not in expected_cases:
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {expected_cases}')               
                        if self.current_token.type in ['int_lit', 'float_lit']:
                            case_cond = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                        elif self.current_token.type in ['true', 'false']:
                            case_cond = BoolLitNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                        elif self.current_token.type == 'string_lit':
                            case_cond = StrLitNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                            self.advance()
                        elif self.current_token.type == 'id':
                            name = self.current_token.value
                            if self.look_ahead().type == '[':
                                indx_start = self.current_token.pos_start
                                indx1, indx2 = None, None
                                self.advance()
                                self.advance()

                                indx1, err = self.parseExpr()
                                if err: return None, err
                                
                                if self.current_token.type != ']':
                                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ]')

                                if self.look_ahead().type == '[':
                                    self.advance()
                                    self.advance()
                                    indx2, err = self.parseExpr()
                                    if err: return None, err

                                    if self.current_token.type != ']':
                                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ]')
                                    case_cond = MixIndxNode(name, indx1, indx2, indx_start, self.current_token.pos_end)
                                    self.advance()

                                else:
                                    case_cond = MixIndxNode(name, indx1, indx2, indx_start, self.current_token.pos_end)
                                    self.advance()
                            elif self.look_ahead().type == ')':
                                case_cond = IdNode(name, self.current_token.pos_start, self.current_token.pos_end)
                                self.advance()
                        else:
                            return None, ParseError(case_start, self.current_token.pos_end, f"Only literals are allowed for for-header initialization part")

                        if self.current_token.type != ':':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: :')
                        self.advance()

                        case_block, err = self.parseCaseBody()
                        if err:
                            return None, err

                        cases.append(CaseNode(case_cond, case_block, case_start, self.current_token.pos_end))
                        
                    elif self.current_token.type == 'default':
                        def_start = self.current_token.pos_start
                        self.advance()

                        if self.current_token.type != ':':
                            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: :')
                        self.advance()

                        def_block, err = self.parseCtrlBody()
                        if err:
                            return None, err
                        
                        cases.append(DefaultNode(def_block, def_start, self.current_token.pos_end))

                    else:
                        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: [\'case\', \'default\']')
                
                if self.current_token.type != '}':
                    op_brace = '}'
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {op_brace}')
                self.advance()

                return ChooseNode(id_node, cases, choose_start, self.current_token.pos_end), None

    # CASE BODY
    def parseCaseBody(self):
        ctrl_stmnts = ['break', 'continue']
        ctrl_body = FuncBodyNode()

        while self.current_token.type not in ['case', 'default']:            
            # CONTROL STATEMENTS
            if self.current_token.type in ctrl_stmnts:
                node, err = self.parseCtrlStmnt()
                if err: return None, err
                else: ctrl_body.add_child(node)

            # GIVEBACK
            elif self.current_token.type == 'giveback':
                node, err = self.parseGiveback()
                if err: return None, err
                else: ctrl_body.add_child(node)
            
            # OTHER STATEMENTS
            else:
                stmnt, err = self.parseStatement()
                if err: return None, err
                else: ctrl_body.add_child(stmnt)

        return ctrl_body, None

    # ITERATIVE
    def parseIterative(self):
        if self.current_token.type == 'for':
            for_start = self.current_token.pos_start
            self.advance()

            if self.current_token.type != '(':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: (')
            self.advance()

            for_head, err = self.parseForHeader()
            if err:
                return None, err

            if self.current_token.type != '{':
                op_brace = '{'
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {op_brace}')
            self.advance()

            for_body, body_err = self.parseCtrlBody()
            if body_err:
                return None, body_err

            if self.current_token.type != '}':
                cl_brace = '}'
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {cl_brace}')
            for_end = self.current_token.pos_end
            self.advance()

            return ForLoopNode(for_head, for_body, for_start, for_end), None

        elif self.current_token.type == 'while':
            while_start = self.current_token.pos_start
            self.advance()

            if self.current_token.type != '(':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: (')
            self.advance()

            while_cond, while_err = self.parseExpr()
            if while_err:
                return None, while_err
            
            if self.current_token.type != ')':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: )')
            self.advance()

            if self.current_token.type != '{':
                op_brace = '{'
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {op_brace}')
            self.advance()

            while_body, whileBody_err = self.parseCtrlBody()
            if whileBody_err:
                return None, whileBody_err

            if self.current_token.type != '}':
                cl_brace = '}'
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: {cl_brace}')
            while_end = self.current_token.pos_end
            self.advance()

            return WhileNode(while_cond, while_body, while_start, while_end), None

    # FOR LOOP HEADER
    def parseForHeader(self): 
        pos_start = self.current_token.pos_start
        init_node = None
        val_node = None

        # INITIALIZATION PART
        if self.current_token.type not in ['int', 'float', 'id']:
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ['int', 'float', 'string', 'bool', 'id']")
        
        if self.current_token.type in ['int', 'float']:
            dtype = self.current_token.type
            self.advance()

            if self.current_token.type != 'id':
                return None, ParseError(pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: id")
            name = self.current_token.value
            self.advance()

            if self.current_token.type != '=':
                return None, ParseError(pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: =")
            self.advance()

            if self.current_token.type not in ['int_lit', 'float_lit', 'string_lit', 'true', 'false']:
                return None, ParseError(pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ['int_lit', 'float_lit', 'string_lit', 'true', 'false']")
            
            if self.current_token.type in ['int_lit', 'float_lit']:
                val_node = NumNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                self.advance()
            elif self.current_token.type in ['true', 'false']:
                val_node = BoolLitNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                self.advance()
            elif self.current_token.type == 'string':
                val_node = StrLitNode(self.current_token.value, self.current_token.pos_start, self.current_token.pos_end)
                self.advance()
            else:
                return None, ParseError(pos_start, self.current_token.pos_end, f"Only literals are allowed for for-header initialization part")
        
            if self.current_token.type != ';':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ;")
            self.advance()

            init_node = VarDecNode(None, dtype, name, val_node, pos_start, self.current_token.pos_end)

        elif self.current_token.type == 'id':
            name = self.current_token.value
            self.advance()

            if self.current_token.type not in [';', '=']:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: [';', '=']")
            
            if self.current_token.type == '=':
                self.advance()

                val, err = self.parseExpr()
                if err: return None, err

                if self.current_token.type != ';':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ;")
                self.advance()

                init_node = AssignNode(name, val, pos_start, self.current_token.pos_end)

            elif self.current_token.type == ';':
                init_node = IdNode(name, pos_start, self.current_token.pos_end)
                self.advance()
            else:
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: [\';\', \'=\']")

        else: 
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"First part of for header must only be scalar variable declarations or assignment")

        # CONDITION PART
        cond, err = self.parseExpr()
        if err: return None, err

        if self.current_token.type != ';':
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: ;")
        self.advance()

        # UNARY OPERATION PART
        unary_node, err = self.parseUnaryArith()
        if err: return None, err

        if self.current_token.type != ')':
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: )")
        self.advance()
       
        return ForHeaderNode(init_node, cond, unary_node, pos_start, self.current_token.pos_end), None

    def parseMixLit(self):
        if self.current_token.type != '{':
            return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: {op_brace}")
        
        mix_lit_start = self.current_token.pos_start
        mix_elements = []
        self.advance()

        if self.current_token.type == '}':
            pos_end = self.current_token.pos_end
            self.advance()

            return MixLitNode(mix_elements, mix_lit_start, pos_end), None

        while self.current_token.type != '}':
            if self.current_token.type == '{':
                row_node, err = self.parseMixLit()
                if err: return None, err
                mix_elements.append(row_node)

            else:
                mix_val, err = self.parseExpr()
                if err: return None, err

                mix_elements.append(mix_val)

                if self.current_token.type == ',':
                    self.advance()

                elif self.current_token.type != '}':
                    return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f"Unexpected -> {self.current_token.type} <-. Expected: {cl_brace}")
            
            pos_end = self.current_token.pos_end
        self.advance()

        return MixLitNode(mix_elements, mix_lit_start, pos_end), None

    # GIVEBACK
    def parseGiveback(self):
        give_start = self.current_token.pos_start
        self.advance()
        give_node = None

        # If void is returned
        if self.current_token.type == 'void':
            void_start = self.current_token.pos_start
            self.advance()
            if self.current_token.type == ';':
                give_node = GivebackNode(VoidNode(void_start, self.current_token.pos_end), give_start, self.current_token.pos_end)
                self.advance()

        elif self.current_token.type == ';':
            give_node = GivebackNode(VoidNode(give_start, self.current_token.pos_end), give_start, self.current_token.pos_end)
            self.advance()

        # If non-void is returned
        elif self.current_token.type == '{':
            give_val, err = self.parseMixLit()
            if err: return None, err

            if self.current_token.type != ';':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ;')
            give_node = GivebackNode(give_val, give_start, self.current_token.pos_end)
            self.advance()

        else:
            give_val, err = self.parseExpr()
            if err:return None, err
            
            if self.current_token.type != ';':
                return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {self.current_token.type} <-. Expected: ;')
            give_node = GivebackNode(give_val, give_start, self.current_token.pos_end)
            self.advance()

        return give_node, None

    # STATEMENTS
    def parseStatement(self):
        token = self.current_token.type
        statements = ['const', 'int', 'float', 'string', 'bool', 'mix', 'id', '++', '--', 'say', 'listen', 'when', 'choose', 'for', 'while']

        if token in ['const', 'int', 'float', 'string', 'bool', 'mix']:
            return self.parseDec()
        elif token == 'id':
            return self.parseId()
        elif token in ['++', '--']:
            return self.parseUnaryArith()
        elif token in ['say', 'listen']:
            return self.parseIO()
        elif token in ['when', 'choose']:
            return self.parseConditional()
        elif token in ['for', 'while']:
            return self.parseIterative()
        
        return None, ParseError(self.current_token.pos_start, self.current_token.pos_end, f'Unexpected -> {token} <-. Expected {statements}')