########## ASTVisitor #########
# Base class for for the ASTTraverser stating how to "visit" each node
# Each visit has its own way of traversing a node
# vist() - uses getattr() of python to find the correct function that visits a specific node
# generic_visit() - visits the root node or the topmost in the tree. This prevents the compiler from cashing if no function has made for a node
# visit_children() - while a node has a children, it visits its children until to the leaf node
# If there are specific rules for a certain feature in the compiler (e.g. toint() only accepts other data type other than string with letters in it), their visit function woulld be longer
# Otherwise, it would just be visit_children(node) 

"""ANSI escape codes for colors and styles. FOR DEBUGGING PURPOSES ONLY, CAN BE REMOVED"""
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
ENDC = '\033[0m' 

from ..Error import SemanticError
from .SymbolTable import SymbolTable
from .ASTNodes import (
    ASTNode, NumNode, StrLitNode, BoolLitNode, IdNode, BiArithNode, ExpoNode, RelNode, LogicNode, UnaryOperatorNode,
    UnaryNode, DataTypeNode, ConstNode, VoidNode, VarDecNode, AssignNode, MixLitNode, MixDecNode, MixIndxNode, MixIndxAssignNode,
    SpyceNode, ParamNode, MakeDecNode, FuncBodyNode, ArgsNode, FuncCallNode, SayNode, ListenNode, GivebackNode, WhenNode,
    ElsewhenNode, OtherwiseNode, ChooseNode, CaseNode, DefaultNode, ForLoopNode, ForHeaderNode, WhileNode, BreakNode,
    ContNode, ToStrNode, ToIntNode, ToFloatNode, ToBoolNode, TypeNode, LenNode, LowerNode, UpperNode, TruncNode
    )

""" NOTES FOR FUTURE SESSIONS
- Passing constant variables to functions and manipulating does not produce an error
- Line 187 is being appended twice in the errors (adding strings to other types) when assigning to mix index
- Evaluate accesssing index using mixindices
- Returning mix literals must be checked with the functions return type
- problem when the index value is a parameter
- no implementation for string indexing

JANINE'S NOTES
- unused variables should produce a warning
- 1.5 or negative in array size initialization (running semantic analysis only)
- len should only accept strings and mixes
- function inside mixes not allowed
- expressions and relational inside mix elements (running semantic analysis only)
- type(x) (running semantic analysis only)
- type(x) but x is a mix (running semantic analysis only)
- function with same identifier in local variable not allowed
"""

class ASTVisitor:
    def visit(self, node, parent=None):
        if hasattr(node, 'error'): return None
        visitor = getattr(self, f'visit_{type(node).__name__}', self.generic_visit)
        return visitor(node, parent)
    
    def generic_visit(self, node, parent):
        if parent is None: 
            print(f'Visiting root node: {type(node).__name__}')
        self.visit_children(node)

    def visit_children(self, node):
        for child in node.children:
            self.visit(child, node)

########## ASTTraverser ##########
# Main component of the semantic analyzer
# It defines the meaning of the nodes by type checking
# Pushing and popping variables to the symbol table and checks if a variable exists
# It determines the result of an expression and checks of operands are possible to the expression

class ASTTraverser(ASTVisitor):
    def __init__(self, STable):
        self.STable = STable
        self.errors = []
        self.unresolved = []

    ##################
    # HELPER FUNCTIONS
    ##################
    # Returns the data type of a node
    def infer_type(self, node):
        print(f'INFERING NODE: {node}')
        if      isinstance(node, NumNode):                                          return 'int' if isinstance(node.val, int) else 'float'
        elif    isinstance(node, StrLitNode):                                       return 'string'
        elif    isinstance(node, (BoolLitNode, RelNode, LogicNode)):                return 'bool'
        elif    isinstance(node, UnaryNode):                                        return self.infer_type(node.operand)
        elif    isinstance(node, ExpoNode):                                         return 'float' if node.left == 'float' or node.right == 'float' else 'int'
        elif    isinstance(node, IdNode):                                           return self.STable.get_type(node.name) if self.STable.get_type(node.name) else 'unknown'
        elif    isinstance(node, BiArithNode):
            if node.op in ['<', '>', '<=', '>=', '==', '!=', 'AND', 'OR', 'NOT']:   return 'bool'
            left_type = self.infer_type(node.left)
            right_type = self.infer_type(node.right)
            if node.op == '+' and left_type == 'string' and right_type == 'string':return 'string'
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

    # Evaluates expressions
    def eval_node(self, node):
        try:
            if isinstance(node, NumNode): 
                return node.value
            elif isinstance(node, BiArithNode): 
                left_val = self.eval_node(node.left)
                right_val = self.eval_node(node.right)
                try:
                    return eval(f'{left_val} {node.op} {right_val}')
                except:
                    return None
        except:
            return None
    
    ##################
    # VISIT FUNCTIONS
    ##################
    def visit_NumNode(self, node, parent):
        print(f'Visiting NumNode: {node.val}')
        self.visit_children(node)

    def visit_StrLitNode(self, node, parent):
        print(f'Visiting StrLitNode: {node.val}')
        self.visit_children(node)

    def visit_BoolLitNode(self, node, parent):
        print(f'Visiting BoolLitNode: {node.val}')
        self.visit_children(node)

    def visit_IdNode(self, node, parent):
        print(f'Visiting IdNode: {node.name}')
        if not self.STable.get(node.name) and not isinstance(parent, (FuncCallNode, MixIndxNode)):
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Variable '{node.name}' is not defined"))
        else:
            filtered_instance = (AssignNode, VarDecNode, FuncCallNode, MixIndxNode, MixIndxAssignNode, LenNode, GivebackNode, BiArithNode, ToIntNode, ToFloatNode, ToStrNode, ToBoolNode, TruncNode, UpperNode, LowerNode)
            id = self.STable.get(node.name)
            main_parent = parent
            while main_parent.parent and not isinstance(main_parent, filtered_instance):
                main_parent = main_parent.parent

                if isinstance(main_parent, filtered_instance):
                    if isinstance(id, MakeDecNode) and not isinstance(main_parent, FuncCallNode):
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot call '{node.name}' without arguments"))
                    elif isinstance(id, MixDecNode) and not isinstance(main_parent, (MixIndxNode, MixIndxAssignNode, LenNode, ToIntNode, ToFloatNode, ToStrNode, ToBoolNode, TruncNode, UpperNode, LowerNode)):
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot call '{node.name}' without specified index"))

    def visit_BiArithNode(self, node, parent):
        print(f'Visiting BiArithNode: {node.val}')
        self.visit_children(node)

        left_type = self.infer_type(node.left)
        right_type = self.infer_type(node.right)
        op_type = self.infer_type(node)
        answer = None

        ############ TEMPORARY FIX ########### 
        if node.op in ['/', '%']:
            if isinstance(node.right, NumNode) and node.right.val == 0:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, 'Division by zero'))
                return

        if isinstance(left_type, MixDecNode):
            if not hasattr(node.left, 'index1'):
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Whole mix variables cannot be used as operands"))
                return 
            if left_type.size2 is None:
                left_type = self.infer_type(left_type.val.vals[parent.index1.val])
            elif left_type.size2 and left_type.size1:
                left_type = self.infer_type(left_type.val.vals[parent.index1.val][parent.index2.val])

        if isinstance(right_type, MixDecNode):
            if not hasattr(node.right, 'index1'):
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Whole mix variables cannot be used as operands"))
                return 
            if right_type.size2 is None:
                right_type = self.infer_type(right_type.val.vals[parent.index2.val])
            elif right_type.size2 and right_type.size1:
                right_type = self.infer_type(right_type.val.vals[parent.index1.val][parent.index2.val])

        if left_type == 'string' and right_type == 'string':
            if node.op != '+':
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Operation '{node.op}' cannot be performed on strings"))

        elif left_type != right_type:
            if left_type == 'string' and right_type in ['int', 'float', 'bool']:
                if node.op == '+':
                    self.errors.append(SemanticError(parent.pos_start, parent.pos_end, f'Strings cannot be added to other types'))
                else:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Operation '{node.op}' cannot be performed on strings"))
            elif left_type in ['int', 'float', 'bool'] and right_type == 'string':
                if node.op == '+':
                    self.errors.append(SemanticError(parent.pos_start, parent.pos_end, f'Strings cannot be added to other types'))
                else:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Operation '{node.op}' cannot be performed on strings"))

        elif isinstance(parent, BiArithNode):
            num_operand = ['int', 'float', 'true', 'false']
            if left_type in num_operand and right_type in num_operand:
                try:
                    answer = eval(f'{node.left.val} {node.op} {node.right.val}')
                except Exception as e:
                    print(str(e))
                
                if answer == 0:
                    if isinstance(parent, BiArithNode) and parent.op == '/' and parent.right == node:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Division by zero'))
            
            # If the operation is returned by a function
            if isinstance(parent, GivebackNode):
                func = parent.parent
                while not isinstance(func, MakeDecNode):
                    if func.parent:
                        func = func.parent
                    else:
                        break
                
                if isinstance(func, MakeDecNode) and func.ret != op_type: 
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type Mismatch: Function '{func.name}' returns {func.ret}, but got {op_type}"))
            
            if node.op == '/' or node.op == '%':
                # If the right operand is a literal
                if isinstance(node.right, NumNode) and node.right.val == 0:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Division by zero'))

                # If the right operand is an id 
                elif isinstance(node.right, IdNode):
                    if self.STable.get(node.right.name):
                        id = self.STable.get(node.right.name)
                        if isinstance(id, VarDecNode) and isinstance(id.val, NumNode) and id.val.val == 0:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Division by zero'))

                # If the right operand is a mix index    
                elif isinstance(node.right, MixIndxNode):
                    value = None

                    # Look up the mix in the symbol table
                    if self.STable.get(node.right.name):
                        id = self.STable.get(node.right.name)

                        if isinstance(id, MixDecNode):
                            size1 = id.size1
                            size2 = id.size2
                            index1, index2 = None

                            # If two brackets are used but the mix is only one dimension
                            if node.right.index2 and not id.size2:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Index Out of bounds: "{node.right.name}" is a one-dimension mix'))

                            # If one bracket is used but the mix is two dimenions
                            elif not node.right.index2 and id.size2:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Cannot use whole mix as an operand'))

                            # Evalute the first index access
                            try:    index1 = self.eval_node(node.right.index1)
                            except: index1 = None

                            # Evalute the second index access if provided
                            if node.right.index2:
                                try:    index2 = self.eval_node(node.righ.index2)
                                except: index2 = None
                            else: index2 = None

                        if index1 is not None and size1 is not None and (index1 < 0 or index1 >= self.size1):
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Index out of bounds'))
                        if index2 is not None and size2 is not None and (index2 < 0 or index2 >= self.size1):
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Index out of bounds'))
                        if index1 is not None and (index2 is None or index2 is not None):
                            if index2 is None:
                                try:
                                    value = id.val.vals[index1]
                                except IndexError:
                                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Index out of bounds'))
                            else:
                                value = id.val[index1].vals[index2]

                            if isinstance(value, NumNode) and value.val == 0:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Division by zero'))
                            elif isinstance(value, IdNode) and isinstance(value.parent, BiArithNode):
                                id_symbol = self.STable.get(value.name)
                                if id_symbol:
                                    if isinstance(id_symbol, VarDecNode) and isinstance(id_symbol.val, NumNode) and id_symbol.val.val == 0:
                                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Division by zero'))
                            elif isinstance(value, BiArithNode):
                                value = self.eval_node(value)
                                if value == 0:
                                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Division by zero'))

                elif isinstance(node.right, FuncCallNode):
                    func_id = self.STable.get(node.right.name)
                    if func_id:
                        if isinstance(func_id, MakeDecNode):
                            if isinstance(func.id.ret, NumNode):
                                if func_id.ret == 0:
                                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Division by zero'))    

    def visit_ExpoNode(self, node, parent):
        print('Visiting ExpoNode')
        self.visit_children(node)
        left_type = self.infer_type(node.left)
        right_type = self.infer_type(node.right)

        if isinstance(left_type, MixDecNode):
            if not hasattr(node.left, 'index1'):
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Whole mix variables cannot be used as operands"))
                return 

        if isinstance(right_type, MixDecNode):
            if not hasattr(node.right, 'index1'):
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Whole mix variables cannot be used as operands"))
                return 

    def visit_RelNode(self, node, parent):
        print(f'Visiting RelNode: {node.op}')
        self.visit_children(node)
        left_type = self.infer_type(node.left)
        right_type = self.infer_type(node.right)

        if isinstance(left_type, MixDecNode):
            if not hasattr(node.left, 'index1'):
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Whole mix variables cannot be used as operands"))
                return 

        if isinstance(right_type, MixDecNode):
            if not hasattr(node.right, 'index1'):
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Whole mix variables cannot be used as operands"))
                return 
            
        if left_type != right_type: pass

    def visit_LogicNode(self, node, parent):
        print(f'Visiting RelNode: {node.op}')
        self.visit_children(node)

    def visit_UnaryNode(self, node, parent):
        print(f'Visiting UnaryNode: {node.op.op}')
        self.visit_children(node)
        main_parent = parent

        while main_parent.parent and not isinstance(main_parent, GivebackNode):
            main_parent = main_parent.parent
        
        if node.op.op in ['++', '--']:
            if not isinstance(node.operand, (IdNode, MixIndxNode)):
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f'{node.op.op} cannot be used to non-variables'))
            else:
                unary_id = self.STable.get(node.operand.name)
                if unary_id.datatype == 'string':
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform unary opeartions on strings"))

                if unary_id.const:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot modify constant variable '{unary_id.name}'"))
                    
                if not unary_id:
                    pass
                elif isinstance(unary_id, MixDecNode):
                    if self.infer_type(unary_id) == 'mix' and not hasattr(node.operand, 'index1'):
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform '{node.op.op}' to whole mix variable"))

                    else:
                        size1 = unary_id.size1
                        size2 = unary_id.size2 if unary_id.size2 else None
                        index1 = node.operand.index1
                        index2 = node.operand.index2 if node.operand.index2 else None
                        index1_accessed, index2_accessed = None, None
                        if index1.val < 0:
                            pass
                        elif index1.val >= size1.val:
                            pass
                        else:
                            index1_accessed = unary_id.val.vals[index1.val]

                            if self.infer_type(index1_accessed) not in ['int', 'float', 'bool']:
                                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform '{node.op.op}' to {index1_accessed} of type {self.infer_type(index1_accessed)}"))
                            
                        if index2:
                            if index2.val < 0:
                                pass
                            elif index2.val >= size1.val:
                                pass
                            else:
                                index2_accessed = unary_id.val.vals[index2.val]

                                if self.infer_type(index2_accessed) not in ['int', 'float', 'bool']:
                                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot perform '{node.op.op}' to {index2_accessed} of type {self.infer_type(index2_accessed)}"))

                elif unary_id and not isinstance(unary_id, VarDecNode) and not isinstance(main_parent, GivebackNode):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"'{node.op.op}' cannot be used to non-variables"))

    def visit_DataTypeNode(self, node, parent):
        print(f'Visiting DataTypeNode: {node.datatype}')
        self.visit_children(node)

    def visit_VarDecNode(self, node, parent):
        print(f'Visiting VarDecnode: {node.datatype} {node.name}')

        if not self.STable.get_local(node.name):
            self.STable.set_local(node.name, node)
        else:
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Variable '{node.name}' is already declared"))

        val_type = self.infer_type(node.val)
        var_type = self.STable.get_type(node.name)

        if var_type != val_type:
            if var_type == 'int' or var_type == 'float':
                if val_type == 'string':
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"String values cannot be assigned to {var_type} variables"))
            elif var_type == 'string' and val_type != 'string':
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"{val_type.capitalize()} values cannot be assigned to string variables"))

        self.visit_children(node)

    def visit_AssignNode(self, node, parent): 
        print(f'Visiting AssignNode: {node.name}')
        self.visit_children(node)
        id = self.STable.get(node.name)

        if id:
            if id.const and hasattr(id, 'const'):
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Cannot modify constant variable {id.name}'))
            elif isinstance(id, MixDecNode):
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Cannot assign whole mix to {id.name}'))
            elif isinstance(id, MakeDecNode):
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Cannot whole function to {id.name}'))
            else:                
                val_type = self.infer_type(node.val)
                var_type = self.STable.get_type(node.name)

                if var_type != val_type:
                    if var_type == 'int' or var_type == 'float':
                        if val_type == 'string':
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"String values cannot be assigned to {var_type} variables"))
                    elif var_type == 'string' and val_type != 'string':
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"{val_type.capitalize()} values cannot be assigned to string variables"))

    def visit_MixLitNode(self, node, parent):
        print(f'Visiting MixLitNode: {node.vals}')
        self.visit_children(node)
    
    def visit_MixDecNode(self, node, parent):
        print(f'Visiting MixDecNode: {node.name}')
        size1 = node.size1.val
        size2 = None if node.size2 is None else node.size2.val

        if self.STable.get(node.name):
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Variable '{node.name}' already declared"))
        else:
            self.STable.set(node.name, node)
        
        if size1:
            if self.infer_type(node.size1) not in ('int', 'float'):
                self.errors.append(SemanticError(node.size1.pos_start, node.size1.pos_end, f"'{self.infer_type(size1)}' cannot be used for mix size declaration"))
            elif size1 <= 0:
                self.errors.append(SemanticError(node.size1.pos_start, node.size1.pos_end, f'Mix size must be greater than 0'))
        if size2:
            if self.infer_type(node.size2) not in ('int', 'float'):
                self.errors.append(SemanticError(node.size2.pos_start, node.size2.pos_end, f"'{self.infer_type(size2)}' cannot be used for mix size declaration"))

        # Single-dimension mix
        if size1 and not size2:
            if size1 is not None:
                if not isinstance(node.val, MixLitNode):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, "Invalid value to initialize mix"))
                elif len(node.val.vals) > size1:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Mix overload: number of mix literals ({len(node.val.vals)}) cannot be greater than the size declared ({int(size1)}))'))
                else:
                    while len(node.val.vals) < size1:
                        node.val.vals.append(NumNode(0))

        # 2-dimensional mix
        if size1 and size2:
            if size1 is not None and size2 is not None:
                if size1 <= 0:
                    pass
                elif size2 <= 0:
                    self.errors.append(SemanticError(node.size2.pos_start, node.size2.pos_end, f'Mix size2 must be greater than 0'))
                elif len(node.val.vals) > size1:
                    pass
                for inner_node in node.val.vals:
                    if not isinstance(inner_node, MixLitNode):
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, "Invalid value to initialize 2-dimensional mix"))
                    if len(inner_node.vals) > size2:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Mix overload: number of mix literals ({len(inner_node.vals)}) cannot be greater than the size declared ({int(size2)})'))
                    else:
                        while len(inner_node.vals) < size2:
                            inner_node.vals.append(NumNode(0, None, None))
        self.visit_children(node)

    def visit_MixIndxNode(self, node, parent):
        print(f'Visiting MixIndxNode: {node}[{node.index1}][{node.index2}]')

        symbol = self.STable.get(node.name)
        if symbol is None:
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Mix {node.name} is not declared"))
            return
        
        if node.index1:
            if isinstance(symbol, FuncCallNode) and not self.STable.get(node.index1.name):
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f"'{node.index1.name}' is not declared"))
            else:
                index1_type = self.infer_type(node.index1)
                print(f"{RED}index1_type -> {index1_type}{ENDC}")
                if index1_type not in ['int', 'float', 'bool']:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Invalid type used for mix index"))
                else:
                    pass

            if node.index2:
                if isinstance(symbol, FuncCallNode) and not self.STable.get(node.index2.name):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"'{node.index2.name}' is not declared"))
                else:
                    index2_type = self.infer_type(node.index2)
                    if index2_type not in ['int', 'float', 'bool',]:
                        print(f"{RED}index2_type -> {index2_type}{ENDC}")
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Invalid type used for mix index"))
                    else:
                        pass

            if isinstance(symbol, MixDecNode):
                if node.index2 and not symbol.size2:
                    print(f"\n\n{type(symbol.val.vals[node.index2.val])}\n\n")
                    if isinstance(symbol.val.vals[node.index2.val], StrLitNode):
                        pass
                    else:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"{node.name} is a 1-dimension mix only, unexpected 2nd pair of bracket"))

                size1_val = symbol.size1.val
                size2_val = symbol.size2.val if symbol.size2 else None
                index1_val = None
                index2_val = None
    
                if isinstance(node.index1, IdNode):
                    index_sym = self.STable.get(node.index1.name)
                    print(f"index_sym -> {index_sym}: {dir(index_sym)}")
                    if self.infer_type(index_sym.val) not in ['int', 'float', 'bool']:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Invalid type used for mix index"))
                        return
                    index1_val = index_sym.val.val
                else:
                    index1_val = node.index1.val

                if node.index2:
                    if isinstance(node.index2, IdNode):
                        index_sym = self.STable.get(node.index2.name)
                        if self.infer_type(index_sym.val) not in ['int', 'float', 'bool']:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Invalid type used for mix index"))
                            return
                        index2_val = index_sym.val.val
                    else:
                        index2_val = node.index2.val
                print(f'{RED}size1_val -> {size1_val}\nsize2_val -> {size2_val}\nindex1_val -> {index1_val}\nindex2_val -> {index2_val}{ENDC}')
            
                if index1_val and index1_val < 0:
                    self.errors.append(SemanticError(node.index1.pos_start, node.pos_end, f"Index cannot be a negative value"))
                elif index1_val > size1_val:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index cannot be greater than the mix size"))
            
                if index2_val and index2_val < 0:
                    self.errors.append(SemanticError(node.index2.pos_start, node.pos_end, f"Index cannot be a negative value"))
                elif index2_val > size2_val:
                    print(f'\n\n{index2_val} -> {size2_val}\n\n')
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index cannot be greater than the mix size"))

        self.visit_children(node)

    def visit_MixIndxAssignNode(self, node, parent): 
        print(f'Visiting MixIndxAssignNode {node.name}[{node.index1}][{node.index2}]')
        self.visit_children(node)
        symbol = self.STable.get(node.name)

        if not symbol:
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f'{node.name} is not declared'))
        else:
            if hasattr(symbol, 'const') and symbol.const:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Constant mix element cannot be modified'))
                return

            if node.index1:
                if isinstance(symbol, FuncCallNode) and not self.STable.get(node.index1.name):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"'{node.index1.name}' is not declared"))
                else:
                    index1_type = self.infer_type(node.index1)
                    print(f"{RED}index1_type -> {index1_type}{ENDC}")
                    if index1_type not in ['int', 'float', 'bool']:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Invalid type used for mix index"))
                    else:
                        pass

            if node.index2:
                if isinstance(symbol, FuncCallNode) and not self.STable.get(node.index2.name):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"'{node.index2.name}' is not declared"))
                else:
                    index2_type = self.infer_type(node.index2)
                    if index2_type not in ['int', 'float', 'bool',]:
                        print(f"{RED}index2_type -> {index2_type}{ENDC}")
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Invalid type used for mix index"))
                    else:
                        pass

            if isinstance(symbol, MixDecNode):
                if node.index2 and not symbol.size2:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"{node.name} is a 1-dimension mix only, unexpected 2nd pair of bracket"))

                size1_val = symbol.size1.val
                size2_val = symbol.size2.val if symbol.size2 else None
                index1_val = None
                index2_val = None

                if isinstance(node.index1, IdNode):
                    index_sym = self.STable.get(node.index1.name)
                    if self.infer_type(index_sym.val) not in ['int', 'float', 'bool']:
                        self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Invalid type used for mix index"))
                        return
                    index1_val = index_sym.val.val
                else:
                    index1_val = node.index1.val

                if node.index2:
                    if isinstance(node.index2, IdNode):
                        index_sym = self.STable.get(node.index2.name)
                        if self.infer_type(index_sym.val) not in ['int', 'float', 'bool']:
                            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Invalid type used for mix index"))
                            return
                        index2_val = index_sym.val.val
                    else:
                        index2_val = node.index2.val
                print(f'{RED}size1_val -> {size1_val}\nsize2_val -> {size2_val}\nindex1_val -> {index1_val}\nindex2_val -> {index2_val}{ENDC}')
            
                if index1_val and index1_val < 0:
                    self.errors.append(SemanticError(node.index1.pos_start, node.pos_end, f"Index cannot be a negative value"))
                elif index1_val > size1_val:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index cannot be greater than the mix size"))
            
                if index2_val and index2_val < 0:
                    self.errors.append(SemanticError(node.index2.pos_start, node.pos_end, f"Index cannot be a negative value"))
                elif index2_val and size2_val:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Index cannot be greater than the mix size"))
            self.visit_children(node)

    def visit_SpyceNode(self, node, parent):
        print('Visiting SpyceNode')
        if self.STable.get('spyce'):
            self.errors.append(SemanticError(node.pos_start, node.pos_end, "Only one spyce function must be present"))
            return

        self.STable.set('spyce', node)
        self.STable.push()
        for child in list(node.children):
            if isinstance(child, MakeDecNode):
                if self.STable.get(child.name):
                    self.errors.append(SemanticError(child.pos_start, child.pos_end, f"Function '{child.name}' already declared in this scope"))
                else:
                    self.STable.set(child.name, child)
        self.visit_children(node)
        self.STable.pop()

    def visit_ParamNode(self, node, parent):
        print(f'Visiting ParamNode: {node.name}')
        if self.STable.get_local(node.name):
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Parameter '{node.name}' already declared"))
        else:
            node.const = self.STable.get(node.name).const if self.STable.get(node.name) else False
            self.STable.set(node.name, node)
        self.visit_children(node)

    def visit_MakeDecNode(self, node, parent):
        print(f'Visiting MakeDecNode: {node.name}')
        if self.STable.get(node.name) and not isinstance(parent.parent, (MakeDecNode, SpyceNode)):
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"'{node.name}' is already declared"))
        else:
            self.STable.set(node.name, node)
        self.STable.push()
        self.visit_children(node)

        def check_ret(node):
            if isinstance(node, GivebackNode): return True
            if hasattr(node, 'children'): 
                for ch in node.children:
                    if check_ret(ch): return True
            return False
        
        if node.ret and node.ret != 'void':
            ret_flag = False

            cchild = node.body.children[:]
            for ch in cchild:
                if check_ret(ch):
                    ret_flag = True
                    break
        self.STable.pop()

    def visit_FuncBodyNode(self, node, parent):
        print('Visiting FuncBodyNode')
        self.STable.push()
        self.visit_children(node)

        for child in list(node.children):
            if isinstance(child, MakeDecNode):
                if self.STable.get(child.name):
                    self.errors.append(SemanticError(child.pos_start, child.pos_end, f"Function '{child.name}' already declared in this scope"))
                else:
                    self.STable.set(child.name, child)
        self.STable.pop()

    def visit_FuncCallNode(self, node, parent): 
        print('Visiting FuncCallNode')
        self.visit_children(node)
        symbol = self.STable.get(node.name)

        if symbol is None:
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Function "{node.name}" undefined'))
        else:
            for arg in node.args:
                print(f'{RED}{arg} with type{type(arg)}and datatype of {self.infer_type(arg)}{ENDC}')
            for param in symbol.params:
                print(f'{RED}{param} with type{type(param)}and datatype of {param.datatype}{ENDC}')

            if isinstance(symbol, MakeDecNode):
                if len(symbol.params) != len(node.args):
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Expected {len(symbol.params)} arguments for {node.name}, but got {len(node.args)}'))
                else:
                    for i in range(0, len(symbol.params)):
                        if self.infer_type(node.args[i]) != symbol.params[i].datatype:
                            self.errors.append(SemanticError(node.args[i].pos_start, node.args[i].pos_end, f"Type Mismatch: Expected argument of type {symbol.params[i].datatype}, but got {self.infer_type(node.args[i])}"))
            else:
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f'{node.name} is not a function'))

    def visit_SayNode(self, node, parent):
        print('Visiting SayNode')
        self.visit_children(node)

    def visit_ListenNode(self, node, parent):
        print(f'Visiting ListenNode')
        self.visit_children(node)

    def visit_GivebackNode(self, node, parent): 
        print('Visiting GivebackNode')
        self.visit_children(node)
        main_parent = parent

        while main_parent and not isinstance(main_parent, (MakeDecNode, SpyceNode)):
            if main_parent: main_parent = main_parent.parent

        if isinstance(main_parent, MakeDecNode) and main_parent.ret != None:
            if isinstance(node.val, FuncCallNode):
                func_node = self.STable.get(node.value.name)
                func_ret = 'void' if func_node.ret is None else func_node.ret
                if main_parent.ret != func_ret:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Type Mismatch: Expected {main_parent.ret} but returns {func_ret}'))
            elif isinstance(node.val, MixIndxNode):
                pass
            elif isinstance(node.val, IdNode):
                if self.infer_type(node.val) != main_parent.ret:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Type Mismatch: Expected {main_parent.ret} but returns {self.infer_type(node.val)}'))

            elif isinstance(node.val, BiArithNode):
                ret_type = self.infer_type(node.val)

                if main_parent.ret != ret_type:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Type Mismatch: Expected {main_parent.ret} but returns {ret_type}"))
            else:
                func_ret = 'void' if self.infer_type(node.val) == None else self.infer_type(node.val)
                if main_parent.ret != func_ret:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Type Mismatch: Expected {main_parent.ret} but returns {func_ret}')) 

        elif isinstance(main_parent, SpyceNode):
            if not isinstance(node.val, VoidNode):
                self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Unexpected: -> {node.val} <-Spyce function must only return void or none'))
            elif node.val is None:
                pass

        else:
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Function must have return type'))

    def visit_WhenNode(self, node, parent): 
        print('Visiting WhenNode')
        self.visit_children(node)

    def visit_ElsewhenNode(self, node, parent): 
        print('Visiting ElsewhenNode')
        self.visit_children(node)

    def visit_OtherwiseNode(self, node, parent): 
        print('Visiting OtherwiseNode')
        self.visit_children(node)

    def visit_ChooseNode(self, node, parent):
        print('Visiting ChooseNode')
        self.visit_children(node)

    def visit_CaseNode(self, node, parent):
        print('Visiting CaseNode')
        self.visit_children(node)

        if isinstance(node.condition, IdNode):
            if self.STable.get(node.condition.name):
                cond_type = self.STable.get_type(node.condition.name)
                if cond_type in ['mix', 'void']:
                    self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Cases cannot be of type {cond_type}'))
                else:
                    pass

    def visit_DefaultNode(self, node, parent):
        print('Visiting DefaultNode')
        self.visit_children(node)

    def visit_ForLoopNode(self, node, parent):
        print(f'Visiting ForLoopNode')
        self.STable.push()
        self.visit_children(node)
        self.STable.pop()

    def visit_ForHeaderNode(self, node, parent):
        print(f'Visiting ForHeaderNode')
        self.visit_children(node)

    def visit_WhileNode(self, node, parent):
        print(f'Visiting WhileNode')
        self.visit_children(node)

    def visit_BreakNode(self, node, parent): 
        print('Visiting BreakNode')
        self.visit_children(node)

    def visit_ContNode(self, node, parent): 
        print('Visiting ContNode')
        self.visit_children(node)

    def visit_ToIntNode(self, node, parent):
        print('Visiting ToIntNode')
        self.visit_children(node)
        arg = node.arg
        operand_type = self.infer_type(arg)

        # If argument is a mix
        if isinstance(arg, IdNode):
            symbol = self.STable.get(arg.name)
            if isinstance(symbol, MixDecNode):
                self.errors.append(SemanticError(arg.pos_start, arg.pos_end, "Cannot convert whole mix to integer"))
                return

        # If argument is a string not made up of numbers
        if operand_type == 'string':
            if isinstance(arg, StrLitNode):
                clean_val = arg.val.strip('"').strip("'")
                if not clean_val.lstrip('-').isdigit():
                    self.errors.append(SemanticError(arg.pos_start, arg.pos_end, f"Cannot convert non-numeric string '{clean_val}' to int"))
            else:
                pass

        # Valid arguments
        elif operand_type in ['int', 'float', 'bool']:
            pass

        else:
            self.errors.append(SemanticError(arg.pos_start, arg.pos_end, f"Cannot convert type '{operand_type}' to int"))

    def visit_ToFloatNode(self, node, parent):
        print('Visiting ToFloatNode')
        self.visit_children(node)
        arg = node.arg
        operand_type = self.infer_type(arg)

        # If argument is a mix
        if isinstance(arg, IdNode):
            symbol = self.STable.get(arg.name)
            if isinstance(symbol, MixDecNode):
                self.errors.append(SemanticError(arg.pos_start, arg.pos_end, "Cannot convert whole mix to float"))
                return

        # If argument is a string not made up of numbers
        if operand_type == 'string':
            if isinstance(arg, StrLitNode):
                clean_val = arg.val.strip('"').strip("'")
                if not clean_val.lstrip('-').isdigit():
                    self.errors.append(SemanticError(arg.pos_start, arg.pos_end, f"Cannot convert non-numeric string '{clean_val}' to float"))
            else:
                pass

        # Valid arguments
        elif operand_type in ['int', 'float', 'bool']:
            pass

        else:
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f"Cannot convert type '{operand_type}' to float"))

    def visit_ToStrNode(self, node, parent):
        print('Visiting ToSTrNode')
        self.visit_children(node)

    def visit_ToBoolNode(self, node, parent):
        print('Visiting ToBoolNode')
        self.visit_children(node)

    def visit_LenNode(self, node, parent):
        print('Visiting LenNode')
        self.visit_children(node)
        arg = node.arg

        if isinstance(arg, IdNode):
            symbol = self.STable.get(arg.name)

            if symbol:
                symbol_type = self.infer_type(arg)

                if not isinstance(symbol_type, MixDecNode) and symbol_type != 'string':
                    self.errors.append(SemanticError(node.arg.pos_start, node.arg.pos_end, f'Invalid argument for len(). Only strings and mix are allowed'))
        else:
            if not isinstance(arg, (StrLitNode, MixLitNode, ToStrNode)):
                self.errors.append(SemanticError(node.arg.pos_start, node.arg.pos_end, f'Invalid argument for len(). Only strings and mix are allowed'))


    def visit_TypeNode(self, node, parent):
        print('Visiting TypeNode')
        self.visit_children(node)

    def visit_UpperNode(self, node, parent):
        print('Visiting UpperNode')
        self.visit_children(node)
        arg = node.arg
        operand_type = self.infer_type(arg)
        print(operand_type)

        if operand_type != 'string':
            self.errors.append(SemanticError(arg.pos_start, arg.pos_end, f'Only string values accepted for function upper() function'))
        else:
            pass

    def visit_LowerNode(self, node, parent):
        print('Visiting LowerNode')
        self.visit_children(node)
        arg = node.arg
        operand_type = self.infer_type(arg)

        if operand_type != 'string':
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Only string values accepted for function lower() function'))
        else:
            pass

    def visit_TruncNode(self, node, parent): 
        print('Visiting TruncNode')
        self.visit_children(node)
        arg1 = node.val
        arg2 = node.dig

        if self.infer_type(arg1) not in ['int', 'float']:
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Only integer and float values allowed for first argument in trunc(number, int_lit)'))
        elif self.infer_type(arg2) != 'int':
            self.errors.append(SemanticError(node.pos_start, node.pos_end, f'Only integer values allowed for second argument in trunc(number, int_lit)'))
        elif arg2.val < 0 or arg2.val > 5:
            self.errors.append(SemanticError(arg2.pos_start, arg2.pos_end, f'Invalid value for truncating. Only 0-5'))