########## CodeRunnner #########
# The code runner inherits from the ASTVisitor since both interpreter and semantic do the same thing
# The difference between interpreter and semantic:
#   Semantic - checks if the code written is semantically correct
#   Interpreter - runs the code it visits
# Both uses the ASTVistior to traverse through the built Abstract Tree Syntax

"""ANSI escape codes for colors and styles. FOR DEBUGGING PURPOSES ONLY, CAN BE REMOVED"""
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
ENDC = '\033[0m' 

import threading, copy
from .SemanticTools.ASTVisitor import ASTVisitor
from .Error import SemanticError, RuntimeError, ContIteration, ReturnException
from .SemanticTools.ASTNodes import (
    NumNode, StrLitNode, BoolLitNode, IdNode, BiArithNode, ExpoNode, RelNode, LogicNode, UnaryOperatorNode,
    UnaryNode, DataTypeNode, ConstNode, VoidNode, VarDecNode, AssignNode, MixLitNode, MixDecNode, MixIndxNode, MixIndxAssignNode,
    SpyceNode, ParamNode, MakeDecNode, FuncBodyNode, ArgsNode, FuncCallNode, SayNode, ListenNode, GivebackNode, WhenNode,
    ElsewhenNode, OtherwiseNode, ChooseNode, CaseNode, DefaultNode, ForLoopNode, ForHeaderNode, WhileNode, BreakNode,
    ContNode, ToStrNode, ToIntNode, ToFloatNode, ToBoolNode, TypeNode, LenNode, LowerNode, UpperNode, TruncNode
)

"""
=== NOTE FOR FUTURE SESSIONS ===
Ongoing
- mix literals, index, and declaration implementation
- string indexing implementation
- Testing built in functions functionality
- Working on len function
- Functions returning mix
- Importing and exporting files
"""

class CodeRunner(ASTVisitor):
    def __init__(self, STable, socketio=None):
        self.STable = STable
        self.output = []
        self.error = None
        self.socketio = socketio
        self.input_data = None
        self.input_received = threading.Event()
        self.output_ack = threading.Event()

    ##################
    # HELPER FUNCTIONS
    ##################
    def eval_node(self, node):
        print(f'evalNode: {node} -> {type(node)}')
        if   isinstance(node, NumNode): return node.val, None
        elif isinstance(node, StrLitNode): return node.val, None
        elif isinstance(node, BoolLitNode): return node.val, None
        elif isinstance(node, IdNode): 
            symbol = self.STable.get(node.name)
            if symbol is None:
                return None, SemanticError(node.pos_start, node.pos_end, f"Variable '{node.name}' is already declared")
            print(f"{RED}\nSYMBOL: {symbol} ->\n{ENDC}")
            if isinstance(symbol, VarDecNode):
                val, err = self.eval_node(symbol.val)
                if err: return None, err
            
            elif isinstance(symbol, MixDecNode):
                val = symbol.val
                if isinstance(val, MixLitNode):
                    val = val.vals

            elif isinstance(symbol, MakeDecNode):
                print(f"{RED}\nHERE\n{ENDC}")
                return None, RuntimeError(node.pos_start, node.pos_end, f"Functions must be called with () after the function name")

            return val, None

        elif isinstance(node, (BiArithNode, ExpoNode, RelNode, LogicNode)): 
            # HANDLING OF RECURSIVE CALL
            in_recursive = False
            main_parent = node.parent
            while main_parent and hasattr(main_parent, 'parent'):
                if isinstance(main_parent, MakeDecNode) and hasattr(node, 'left') and hasattr(node, 'right'):
                    if isinstance(node.left, FuncCallNode) and isinstance(node.right, FuncCallNode):
                        in_recursive = True
                        break
                main_parent = main_parent.parent
            if in_recursive: main_scopes = copy.deepcopy(self.STable.scopes)

            left_val, left_err = self.eval_node(node.left)
            if left_err: return None, left_err

            if in_recursive: self.STable.scopes = copy.deepcopy(main_scopes)

            right_val, right_err = self.eval_node(node.right)
            if right_err: return None, right_err

            if isinstance(left_val, NumNode):   left_val = left_val.val
            if isinstance(right_val, NumNode):  right_val = right_val.val

            # MAIN EXPRESSION HANDLING
            if not isinstance(node, ExpoNode):
                try:
                    if left_val is not None and right_val is not None:
                        if isinstance(left_val, bool):  left_val = 1 if left_val else 0
                        if isinstance(right_val, bool): right_val = 1 if right_val else 0

                        # ARITHMETIC OPERATIONS
                        if node.op == '+':
                            return left_val + right_val, None
                        elif node.op == '-':
                            return left_val - right_val, None
                        elif node.op == '*':
                            return left_val * right_val, None
                        elif node.op == '/':
                            if right_val == 0:
                                return None, RuntimeError(node.pos_start, node.pos_end, f"Invalid division by zero")
                            if isinstance(left_val, int) and isinstance(right_val, int):
                                return left_val // right_val, None 
                            return ((left_val / right_val) * (10**5)) / 10**5, None
                        elif node.op == '%':
                            if right_val == 0:
                                return None, RuntimeError(node.pos_start, node.pos_end, f"Invalid modulus by zero")
                            return left_val % right_val, None
                            
                        # RELATIONAL OPERATIONS
                        elif node.op == '==':
                            return left_val == right_val, None
                        elif node.op == '!=':
                            return left_val != right_val, None
                        elif node.op == '>':
                            if isinstance(left_val, str) and isinstance(right_val, str):
                                return left_val > right_val, None
                            elif isinstance(left_val, str) and not isinstance(right_val, str):
                                left_val = 1 if left_val != "" else 0
                                return left_val > right_val, None
                            elif isinstance(right_val, str) and not isinstance(left_val, str):
                                right_val = 1 if right_val != "" else 0
                                return left_val > right_val, None
                            else:
                                return left_val > right_val, None
                        elif node.op == '<':
                            if isinstance(left_val, str) and isinstance(right_val, str):
                                return left_val < right_val, None
                            elif isinstance(left_val, str) and not isinstance(right_val, str):
                                left_val = 1 if left_val != "" else 0
                                return left_val < right_val, None
                            elif isinstance(right_val, str) and not isinstance(left_val, str):
                                right_val = 1 if right_val != "" else 0
                                return left_val < right_val, None
                            else:
                                return left_val < right_val, None
                        elif node.op == '>=':
                            if isinstance(left_val, str) and isinstance(right_val, str):
                                return left_val >= right_val, None
                            elif isinstance(left_val, str) and not isinstance(right_val, str):
                                left_val = 1 if left_val != "" else 0
                                return left_val >= right_val, None
                            elif isinstance(right_val, str) and not isinstance(left_val, str):
                                right_val = 1 if right_val != "" else 0
                                return left_val >= right_val, None
                            else:
                                return left_val >= right_val, None
                        elif node.op == '<=':
                            if isinstance(left_val, str) and isinstance(right_val, str):
                                return left_val <= right_val, None
                            elif isinstance(left_val, str) and not isinstance(right_val, str):
                                left_val = 1 if left_val != "" else 0
                                return left_val <= right_val, None
                            elif isinstance(right_val, str) and not isinstance(left_val, str):
                                right_val = 1 if right_val != "" else 0
                                return left_val <= right_val, None
                            else:
                                return left_val <= right_val, None
                            
                        # LOGICAL OPERATIONS
                        elif node.op == 'AND':  return self.to_bool(left_val) and self.to_bool(right_val), None
                        elif node.op == 'OR':   return self.to_bool(left_val) or self.to_bool(right_val), None

                        else: 
                            return None, RuntimeError(node.pos_start, node.pos_end, f"Unknown operator: {node.op}")

                except Exception as e:
                    return None, RuntimeError(node.pos_start, node.pos_end, f"Error at {node.op}, {str(e)}")
            else:
                return left_val ** right_val, None
            
        elif isinstance(node, UnaryNode): 
            if node.op.op == 'NOT' and node.prefix is True:
                not_val, not_err = self.eval_node(node.operand)
                if not_err: return None, not_err

                if isinstance(not_val, BoolLitNode): return not not_val, None
                elif isinstance(not_val, bool): return not not_val, None
                elif isinstance(not_val, str): 
                    if not_val == '': return not False, None
                    else: return not True, None
                else: return not not_val, None

            elif node.op.op in ['++', '--']:
                u_val, u_err = self.eval_node(node.operand)
                if u_err: return None, u_err

                if node.op.op == '++' and node.prefix is True:
                    return u_val + 1, None
                elif node.op.op == '++' and node.prefix is False:
                    return u_val + 1, None
                elif node.op.op == '--' and node.prefix is True:
                    return u_val - 1, None
                elif node.op.op == '--' and node.prefix is False:
                    return u_val - 1, None

        elif isinstance(node, MixIndxNode): 
            mix = self.STable.get(node.name)
            if isinstance(mix, VarDecNode):
                if mix.datatype != 'string':
                    return None, SemanticError(node.pos_start, node.pos_end, f"Variable of type {mix.datatype} cannot be indexed")
                elif mix.datatype == 'string' and node.index2:
                    return None, SemanticError(node.pos_start, node.pos_end, f"String variables cannot be accessed with 2d indexing")
                else:
                    index_val, index_err = self.eval_node(node.index1)
                    if index_err: return None, index_err

                    if index_val < 0:
                        return None, SemanticError(node.pos_start, node.pos_end, f"Invalid index value of < 0")

                    return mix.val.val.replace('"', '')[index_val], None
            if isinstance(mix, MixDecNode):
                index1, index1_err = self.eval_node(node.index1)
                if index1_err: return None, index1_err

                if node.index2 and mix.size2:
                    index2, index2_err = self.eval_node(node.index2)
                    if index2_err: return None, index2_err

                    try:
                        return mix.val.vals[index1].vals[index2], None
                    except IndexError:
                        return None, SemanticError(node.pos_start, node.pos_end, f"Index out of bounds")
                
                elif node.index2 and not mix.size2:
                    if isinstance(mix.val.vals[node.index2.val], StrLitNode):
                        return mix.val.vals[node.index2.val].val.replace('"', "")[node.index2.val], None
                    else:
                        return None, SemanticError(node.pos_start, node.pos_end, f"{symbol.name} is a 1-dimension mix only, unexpected 2nd pair of bracket ")

                try:
                    return mix.val.vals[index1], None
                except IndexError:
                    return None, SemanticError(node.pos_start, node.pos_end, f"Index out of bounds")

        elif isinstance(node, FuncCallNode): 
            func_call = self.STable.get(node.name)
            print(func_call.ret)
        
            if len(node.args) != len(func_call.params): pass

            self.STable.push()
            for param, arg in zip(func_call.params, node.args):
                arg_val, arg_err = self.eval_node(arg)
                if arg_err: return None, arg_err

                print(f"{RED}{param.datatype} vs {arg_val} -> {type(arg_val)}: {ENDC}")

                if param.datatype == 'int' and isinstance(arg, float):
                    arg_val = int(arg_val)
                elif param.datatype == 'float' and isinstance(arg, int):
                    arg_val = float(arg_val)
                elif param.datatype != self.infer_type(arg_val):
                    return None, SemanticError(node.pos_start, node.pos_end, f"Type mismatch: '{param.datatype}' is expected but given '{self.infer_type(arg_val)}'")
                
                self.STable.set_local(param.name, VarDecNode(False, param.datatype, param.name, NumNode(arg_val, None, None), param.pos_start, param.pos_end))
            
            if func_call.ret == 'void':
                print(f"{RED}givebackval is null here{ENDC}")
                try:
                    self.visit(func_call.body, func_call)
                    self.STable.pop()
                    return None, None
                except ReturnException:
                    self.STable.pop()
                    return None, None
            else:
                giveback_val = None
                try:
                    self.visit(func_call.body, func_call)
                except ReturnException as r:
                    giveback_val = r.value
                self.STable.pop()

                if giveback_val != 'void':
                    return giveback_val, None
                else:
                    if self.error:
                        return None, None
                    else:
                        return None, RuntimeError(node.pos_start, node.pos_end, f"Function '{node.name}' does not return a value")

        elif isinstance(node, ListenNode):
            return self.visit_ListenNode(node, node.parent), None

        elif isinstance(node, LenNode):
            if isinstance(node.arg, IdNode):
                symbol = self.STable.get(node.arg.name)
                if symbol is None:
                    return None, SemanticError(node.pos_start, node.pos_end, f"'{node.arg.name}' is not defined")
            elif isinstance(node.arg, StrLitNode):
                symbol = node.arg.val
            elif isinstance(node.arg, str):
                symbol = node.arg
            elif isinstance(node.arg, MixIndxNode):
                symbol = self.symbol_table.get(node.name.name)
                if symbol is None:
                    return None, SemanticError(node.pos_start, node.pos_end, f"'{node.arg.name}' is not declared")
            elif isinstance(node.arg, MixLitNode):
                symbol = node.arg.vals
            else:
                symbol = node.arg.val

            if isinstance(symbol, VarDecNode):
                if symbol.datatype != 'string':
                    self.error = SemanticError(node.pos_start, node.pos_end, f"Invalid argument for len()")
                else: 
                    pass
            else: 
                self.error = SemanticError(node.pos_start, node.pos_end, f"Expected mix or string, got {type(symbol)}")
                return None, SemanticError(node.pos_start, node.pos_end, f"Expected mix or string")

            # Main counting
            if isinstance(symbol, MixDecNode):
                pass
            elif isinstance(symbol, StrLitNode):
                return len(symbol), None
            elif isinstance(symbol, VarDecNode):
                if symbol.datatype == 'string':
                    return len(symbol.val.val), None
                
        elif isinstance(node, ToIntNode):
            arg_val, arg_err = self.eval_node(node.arg)
            if arg_err: return None, arg_err

            if isinstance(arg_val, str):
                if any(c.isalpha() for c in arg_val):
                    return None, RuntimeError(node.pos_start, node.pos_end, f"Cannot convert to integer string values with non-numeric characters")
                return int(arg_val), None
            else:
                return int(arg_val), None

        elif isinstance(node, ToFloatNode):
            arg_val, arg_err = self.eval_node(node.arg)
            if arg_err: return None, arg_err

            if isinstance(arg_val, str):
                if any(c.isalpha() for c in arg_val):
                    return None, RuntimeError(node.pos_start, node.pos_end, f"Cannot convert to float string values with non-numeric characters")
                return float(arg_val), None
            else:
                return float(arg_val), None

        elif isinstance(node, ToStrNode):
            arg_val, arg_err = self.eval_node(node.arg)
            if arg_err: return None, arg_err

            return str(arg_val), None

        elif isinstance(node, ToBoolNode):
            arg_val, arg_err = self.eval_node(node.arg)
            if arg_err: return None, arg_err

            return self.to_bool(arg_val), None

        elif isinstance(node, TypeNode):
            arg_val, arg_err = self.eval_node(node.arg)
            if arg_err: return None, arg_err

            return self.give_type(arg_val), None

        elif isinstance(node, TruncNode):
            arg_val, arg_err = self.eval_node(node.val)
            if arg_err: return None, arg_err

            if isinstance(arg_val, (int, float, NumNode)) and isinstance(node.dig, (NumNode)):
                factor = 10 ** node.dig.val
                new_val = int(arg_val * factor) / factor
                return (int(new_val) if node.dig == 0 else new_val), None
            else:
                return None, None

        elif isinstance(node, UpperNode):
            arg_val, arg_err = self.eval_node(node.arg)
            if arg_err: return None, arg_err

            if not isinstance(arg_val, (str, StrLitNode)):
                return None, SemanticError(node.pos_start, node.pos_end, f"Invalid argument for upper(). Must only be string values")

            if isinstance(arg_val, str):
                return arg_val.upper(), None
            elif isinstance(arg_val, StrLitNode):
                return arg_val.val.upper(), None

        elif isinstance(node, LowerNode):
            arg_val, arg_err = self.eval_node(node.arg)
            if arg_err: return None, arg_err

            if not isinstance(arg_val, (str, StrLitNode)):
                return None, SemanticError(node.pos_start, node.pos_end, f"Invalid argument for lower(). Must only be string values")

            if isinstance(arg_val, str):
                return arg_val.lower(), None
            elif isinstance(arg_val, StrLitNode):
                return arg_val.val.lower(), None

        elif isinstance(node, (str, int, float)): return node, None
        else:   return None, None

    def infer_type(self, node):
        print(f'INFERING NODE: {node} -> {type(node)}')
        if      isinstance(node, NumNode):                                          return 'int' if isinstance(node.val, int) else 'float'
        elif    isinstance(node, StrLitNode):                                       return 'string'
        elif    isinstance(node, (BoolLitNode, RelNode, LogicNode)):                return 'bool'
        elif    isinstance(node, UnaryNode):                                        return self.infer_type(node.operand)
        elif    isinstance(node, ExpoNode):                                         return 'float' if node.left == 'float' or node.right == 'float' else 'int'
        elif    isinstance(node, IdNode):                                           return self.STable.get_type(node.name) if self.STable.get_type(node.name) else 'unknown'
        elif    isinstance(node, BiArithNode):
            left_type = self.infer_type(node.left)
            right_type = self.infer_type(node.right)
            if node.op in ['<', '>', '<=', '>=', '==', '!=', 'AND', 'OR', 'NOT']:   return 'bool'
            elif node.op == '+' and left_type == 'string' and right_type == 'string':return 'string'
            else:
                if left_type in ['int', 'bool'] and right_type in ['int', 'bool']:  return 'int'
                elif left_type == 'float' or right_type == 'float':                 return 'float'
                elif left_type == 'bool' and right_type == 'bool':                  return 'int'
        elif    isinstance(node, MixIndxNode):                                      return self.STable.get_type(node.name)
        elif    isinstance(node, MixDecNode):                                       return 'mix'
        elif    isinstance(node, MixLitNode):                                       return 'mix'
        elif    isinstance(node, FuncCallNode):                                     return self.STable.get(node.name).ret if self.STable.get(node.name) else None
        elif    isinstance(node, ToIntNode):                                        return 'int'
        elif    isinstance(node, ToFloatNode):                                      return 'float'
        elif    isinstance(node, ToStrNode):                                        return 'string'
        elif    isinstance(node, ToBoolNode):                                       return 'bool'
        elif    isinstance(node, LenNode):                                          return 'int'
        elif    isinstance(node, TypeNode):                                         return 'type'
        elif    isinstance(node, UpperNode):                                        return 'string'
        elif    isinstance(node, LowerNode):                                        return 'string'
        elif    isinstance(node, TruncNode):                                        return 'float'
        elif    isinstance(node, ListenNode):                                       return 'string'
        elif    isinstance(node, int):                                              return 'int'
        elif    isinstance(node, float):                                            return 'float'
        elif    isinstance(node, str):                                              return 'string'
        elif    isinstance(node, bool):                                             return 'bool'

    def to_bool(self, val):
        if isinstance(val, str):
            if val == 'true': return True
            elif val == 'false': return False
            return True if val != '' else False
        elif isinstance(val, (int, float)):
            return val != 0
        elif isinstance(val, bool):
            return val
        return bool(val)

    def give_type(self, val):
        if isinstance(val, (BoolLitNode, bool)):        return '<type: bool>'
        elif isinstance(val, int):                      return '<type: int>'
        elif isinstance(val, float):                    return '<type: float>'
        elif isinstance(val, (StrLitNode, str)):        return '<type: bool>' if val in ['true', 'false'] else '<type: string>'
        elif isinstance(val, (MixDecNode, MixLitNode)): return '<type: mix>'
        else:                                           return 'unknown'

    #################
    # VISIT FUNCTIONS
    #################
    def visit_NumNode(self, node, parent):
        print(f'Visiting NumNode: {node.val}')
        return node.val

    def visit_StrLitNode(self, node, parent):
        print(f'Visiting StrLitNode: {node.val}')
        return node.val

    def visit_BoolLitNode(self, node, parent):
        print(f'Visiting BoolLitNode: {node.val}')
        self.visit_children(node)

    def visit_IdNode(self, node, parent):
        print(f'Visiting IdNode: {node.name}')
        symbol = self.STable.get(node.name)
        if symbol is None:
            self.error = (SemanticError(node.pos_start, node.pos_end, f"Variable '{node.name}' is not defined"))
            return None
        if isinstance(symbol, VarDecNode):
            return symbol.val
        return None
    
    def visit_BiArithNode(self, node, parent):
        print(f'Visiting BiArithNode: {node.val}')
        self.visit_children(node)

    def visit_ExpoNode(self, node, parent):
        print(f'Visiting ExpoNode')

    def visit_RelNode(self, node, parent):
        print(f'Visiting RelNode: {node.op}')

    def visit_LogicNode(self, node, parent):
        print(f'Visiting RelNode: {node.op}')

    def visit_UnaryNode(self, node, parent):
        print(f'Visiting UnaryNode: {node.op.op}')
        value, err = self.eval_node(node.operand)
        if err: 
            self.error = err
            return

        if node.op.op in ['++', '--']:
            if not isinstance(node.operand, IdNode):
                self.error(SemanticError(node.pos_start, node.pos_end, f"{node.op.op} cannot be used to non-variables"))
                return None
            
            var_name = node.operand.name
            symbol = self.STable.get(var_name)
            
            if symbol is None:
                self.error = (SemanticError(node.pos_start, node.pos_end, f"Variable '{node.name}' is not defined"))
                return None
            
            if not isinstance(symbol, VarDecNode):
                self.error(SemanticError(node.pos_start, node.pos_end, f"{node.op.op} cannot be performed on {node.operand}"))
                return None
            
            new_val = value + 1 if node.op.op == '++' else  value - 1
            val_node = NumNode(new_val, None, None)
            new_sym = VarDecNode(symbol.const, symbol.datatype, symbol.name, val_node, symbol.pos_start, symbol.pos_end)
            self.STable.set(node.operand.name, new_sym)

        return value, None
    
    def visit_DataTypeNode(self, node, parent):
        print(f'Visiting DataTypeNode: {node.datatype}')
        self.visit_children(node)

    def visit_VarDecNode(self, node, parent):
        print(f'Visiting VarDecnode: {node.datatype} {node.name}')

        main_parent = parent
        while main_parent and not isinstance(main_parent, (SpyceNode, MakeDecNode)):
            main_parent = main_parent.parent

        if main_parent is None: pass
        else:
            dec_node = self.STable.get_local(node.name)
            if not dec_node and parent is not None:
                self.STable.set_local(node.name, node)
                dec_node = self.STable.get(node.name)

            val, err = self.eval_node(dec_node.val)
            if err:
                self.error = err
                return

            if dec_node.datatype == 'int' and (isinstance(val, float) or isinstance(val, bool)):
                val = int(val)
            elif dec_node.datatype == 'float' and (isinstance(val, int) or isinstance(val, bool)):
                val = float(val)
            elif dec_node.datatype == 'bool' and not isinstance(val, bool):
                val = self.to_bool(val)

            val_node = None
            if isinstance(val, int):
                if val > 9999999999999999999:
                    self.error = RuntimeError(node.pos_start, node.pos_end, f'Integer value cannot exceed maximum liimit of 19 digits')
                    return
                val_node = NumNode(val, None, None)
            elif isinstance(val, float):
                decimal_digits = str(val).split('.')[-1]
                if len(decimal_digits) > 5:
                    val = int(val * (10 ** 5)) / 10 ** 5
                val_node = NumNode(val, None, None)
            elif isinstance(val, str):
                val_node = StrLitNode(val, None, None)
            elif isinstance(val, bool):
                val_node = BoolLitNode(val, None, None)

            new_dec_node = VarDecNode(False, dec_node.datatype, dec_node.name, val_node, dec_node.pos_start, dec_node.pos_end)
            self.STable.set(node.name, new_dec_node)

    def visit_AssignNode(self, node, parent):
        print(f'Visiting VarAssignNode: {node.val}')

        dec_node = self.STable.get(node.name)
        if dec_node is None:
            self.error = SemanticError(node.pos_start, node.pos_end, f"Variable '{node.name}' is not declared")
            return
        
        val, err = self.eval_node(node.val)
        if err:
            self.error = err
            return
        
        if dec_node.datatype == 'int' and (isinstance(val, (float, int)) or isinstance(val, bool)):
            val = int(val)
        elif dec_node.datatype == 'float' and (isinstance(val, (int, float)) or isinstance(val, bool)):
            val = float(val)
        elif dec_node.datatype == 'bool' and not isinstance(val, bool):
            val = self.to_bool(val)

        val_node = None
        if isinstance(val, int):
            if val > 9999999999999999999:
                self.error = RuntimeError(node.pos_start, node.pos_end, f'Integer value cannot exceed maximum liimit of 19 digits')
                return
            val_node = NumNode(val, None, None)
        elif isinstance(val, float):
            decimal_digits = str(val).split('.')[-1]
            print(decimal_digits)
            if len(decimal_digits) > 5:
                val = int(val * (10 ** 5)) / 10 ** 5
            val_node = NumNode(val, None, None)
        elif isinstance(val, str):
            val_node = StrLitNode(val, None, None)
        elif isinstance(val, bool):
            val_node = BoolLitNode(val, None, None)

        new_dec_node = VarDecNode(False, dec_node.datatype, dec_node.name, val_node, dec_node.pos_start, dec_node.pos_end)
        self.STable.set(node.name, new_dec_node)

    def visit_MixLitNode(self, node, parent):
        print('Visiting MixLitNode')
        self.visit_children(node)

    def visit_MixDecNode(self, node, parent):
        print('Visisting MixDecNode')
        main_parent = parent
        while main_parent and not isinstance(main_parent, (MakeDecNode, SpyceNode)):
            main_parent = parent.parent
        
        if main_parent is None or not isinstance(main_parent, (MakeDecNode, SpyceNode)):
            pass
        else:
            if self.STable.get(node.name):
                self.error = SemanticError(node.pos_start, node.pos_end, f"'{node.name}' is already declared")
            else:
                self.STable.set(node.name, node)

        if node.size1 and not node.size2:
            size1_val, size1_err = self.eval_node(node.size1)
            if size1_err:
                self.error = size1_err
                return
            if size1_val:
                if not isinstance(node.val, (MixLitNode)):
                    self.error = RuntimeError(node.pos_start, node.pos_end, f"Invalid declaration of mix")
                    return

                while len(node.val.vals) < size1_val:
                    print(f"{RED}node.val.vals -> {node.val.vals} with {type(node.val.vals)}{ENDC}")
                    node.val.vals.append(NumNode(0, None, None))

        elif node.size1 and node.size2:
            size1_val, _ = self.eval_node(node.size1)
            size2_val, _ = self.eval_node(node.size2)

            if len(node.val.vals) > size1_val:
                self.error = RuntimeError(node.pos_start, node.pos_end, "Mix row overload")
                return

            # Loop through each "row" in the 2D mix
            for i in range(len(node.val.vals)):
                inner_row = node.val.vals[i]
                
                if not isinstance(inner_row, MixLitNode):
                    self.error = RuntimeError(node.pos_start, node.pos_end, "2D Mix expects nested brackets { { } }")
                    return

                # Check column size
                if len(inner_row.vals) > size2_val:
                    self.error = RuntimeError(node.pos_start, node.pos_end, f"Row {i} column overload")
                    return

                # Pad columns with 0
                while len(inner_row.vals) < size2_val:
                    inner_row.vals.append(NumNode(0, node.pos_start, node.pos_end))

            # Pad remaining rows with empty MixLitNodes filled with 0s
            while len(node.val.vals) < size1_val:
                empty_row = MixLitNode([NumNode(0) for _ in range(size2_val)], node.pos_start, node.pos_end)
                node.val.vals.append(empty_row)
    
    def visit_MixIndxNode(self, node, parent):
        print('Visiting MixIndxNode')
        self.visit_children(node)

    def visit_MixIndxAssignNode(self, node, parent):
        pass

    def visit_SpyceNode(self, node, parent):
        print('Visiting SpyceNode')
        self.visit_children(node)

    def visit_ParamNode(self, node, parent):
        print('Visiting ParamNode')
        self.visit_children(node)

    def visit_MakeDecNode(self, node, parent):
        print('Visiting MakDecNode')
        main_parent = parent
        while main_parent and not isinstance(main_parent, (MakeDecNode, SpyceNode)):
            main_parent = main_parent.parent

        if main_parent is None or not isinstance(main_parent, (MakeDecNode, SpyceNode)):
            pass
        else:
            if self.STable.get(node.name) and not isinstance(parent.parent, (MakeDecNode, SpyceNode)):
                self.error = SemanticError(node.pos_start, node.pos_end, f"'{node.name}' is already declared")
            else:
                self.STable.set(node.name, node)

    def visit_FuncBodyNode(self, node, parent):
        print('Visiting FuncBodyNode')
        self.STable.push()
        for child in list(node.children):
            if isinstance(node, MakeDecNode):
                if self.STable.get(child.name):
                    self.errors = SemanticError(child.pos_start, child.pos_end, f"Function '{child.name}' already declared")
                else:
                    self.STable.set(child.name, child)

        self.visit_children(node)
        self.STable.pop()

    def visit_FuncCallNode(self, node, parent):
        print('Visiting FuncCallNode')

        func_node = self.STable.get(node.name)

        # Early return if a function is returning something other than void
        if func_node.ret != 'void': 
            return

        self.STable.push()
        try:
            for param, arg in zip(func_node.params, node.args):
                arg_val, arg_err = self.eval_node(arg)
                if arg_err: 
                    self.error = arg_err
                    return
                
                if param.datatype in ['int', 'float']:
                    val_node = NumNode(arg_val, None, None)
                elif param.datatype == 'string':
                    val_node = StrLitNode(arg_val, None, None)
                elif param.datatype == 'bool':
                    val_node = BoolLitNode(self.to_bool(arg_val), None, None)
                else:
                    pass
                self.STable.set(param.name, VarDecNode(False, param.datatype, param.name, val_node, param.pos_start, param.pos_end))

            self.visit(func_node.body, func_node)
        except RecursionError:
            self.error = SemanticError(node.pos_start, node.pos_end, f"Recursion limit exceeded")
        finally:
            self.STable.pop()

    def visit_SayNode(self, node, parent):
        print('Visiting SayNode')
        val, err = self.eval_node(node.val)
        
        if err:
            self.error = err
            return
        
        if val is None: 
            val = getattr(node.val, 'val', str(node.val))
            return

        if isinstance(val, str):
            val = val.replace('"', '')
            try:
                val = val.encode('utf-8').decode('unicode_escape')
            except Exception as e:
                print(f"Escape sequence error: {e}")

        self.output.append(str(val))
        
        if self.socketio:
            self.output_ack.clear()
            if self.error:
                self.socketio.emit('output_update', {'success': False, 'msg': str(self.error)})
            else:
                self.socketio.emit('output_update', {'success': True, 'msg': str(val)})
            
            self.output_ack.wait(timeout=0.5) 

    def visit_ListenNode(self, node, parent):
        print('Visiting ListenNode')
        if self.socketio:
            self.input_received.clear()
            self.socketio.emit('listen_input')
            self.input_received.wait()

            val = self.input_data
            return val

    def visit_GivebackNode(self, node, parent):
        print('Visiting GivebackNode')
        value = None
        if node.val:
            value, error = self.eval_node(node.val)
            if error:
                self.error = error
                return
        raise ReturnException(value)

    def visit_WhenNode(self, node, parent):
        print('Visiting WhenNode')
        cond_val, cond_err = self.eval_node(node.condition)

        if cond_err:
            self.error = cond_err
            return
        
        if cond_val:
            self.visit(node.body, node)
            return
        else:
            for ew in node.elsewhen:
                ew_val, ew_err = self.eval_node(ew.condition)
                if ew_err:
                    self.error = ew_err
                    return

                if ew_val:
                    self.visit(ew.body, ew)
                    return
            else:
                if node.otherwise_node:
                    self.visit(node.otherwise_node.body, node.otherwise_node)
                    return

    def visit_ElsewhenNode(self, node, parent):
        pass

    def visit_OtherwiseNode(self, node, parent):
        pass

    def visit_ChooseNode(self, node, parent):
        print('Visiting ChooseNode')
        choose_var, choose_err = self.eval_node(node.condition)
        if choose_err:
            self.error = choose_err
            return
        
        for case in node.cases:
            if isinstance(case, CaseNode):
                case_val, case_err = self.eval_node(case.condition)

                if choose_var == case_val:
                    try:
                        self.visit(case.body, case)
                    except ContIteration:
                        continue
                    except StopIteration:
                        break
            
            elif isinstance(case, DefaultNode):
                self.visit(case.body, case)
                break

    def visit_CaseNode(self, node, parent):
        pass

    def visit_DefaultNode(self, node, parent):
        pass

    def visit_ForLoopNode(self, node, parent):
        print('Visiting ForLoopNode')
        self.STable.push()
        self.visit(node.header.var, node)

        while True:
            try:
                cond_val, cond_err = self.eval_node(node.header.condition)
                if cond_err:
                    self.error = cond_err
                    self.STable.pop()
                    return

                if not cond_val:
                    break

                self.visit(node.body, node)
                self.visit(node.header.unary, node)
            except ContIteration:
                self.visit(node.header.unary, node)
                continue
            except StopIteration:
                break
        self.STable.pop()

    def visit_ForHeaderNode(self, node, parent):
        print('Visiting ForHeaderNode')

    def visit_WhileNode(self, node, parent):
        print('Visiting WhileNode')
        self.STable.push()
        while True:
            try:
                cond_val, cond_err = self.eval_node(node.condition) 
                if cond_err:
                    self.error = cond_err
                    self.STable.pop()
                    return
                
                if not cond_val:
                    break

                self.visit(node.body, node)
            except ContIteration:
                continue
            except StopIteration:
                break
        self.STable.pop()

    def visit_BreakNode(self, node, parent):
        print('Visiting BreakNode')
        raise StopIteration

    def visit_ContNode(self, node, parent):
        print('Visiting ContNode')
        raise ContIteration

    def visit_ToIntNode(self, node, parent):
        print('Visiting ToIntNode')
        val, err = self.eval_node(node.arg)
        if err:
            self.error = err
            return
        print(f'Value {type(val)} -> is now {type(int(val))}')
        return int(val), None

    def visit_ToFloatNode(self, node, parent):
        print('Visiting ToFloatNode')
        val, err = self.eval_node(node.arg)
        if err:
            self.error = err
            return
        return float(val), None

    def visit_ToStrNode(self, node, parent):
        print('Visiting ToStrNode')
        val, err = self.eval_node(node.arg)
        if err:
            self.error = err
            return
        return str(val), None

    def visit_ToBoolNode(self, node, parent):
        print('Visiting ToBoolNode')
        val, err = self.eval_node(node.arg)
        if err:
            self.error = err
            return
        return self.to_bool(val), None

    def visit_LenNode(self, node, parent):
        pass

    def visit_TypeNode(self, node, parent):
        pass

    def visit_UpperNode(self, node, parent):
        pass

    def visit_LowerNode(self, node, parent):
        pass

    def visit_TruncNode(self, node, parent):
        pass