########## AST (Abstract Syntax Tree) Nodes ##########
# Base class where all elements from the program inherits from
# Each node is a specific element from the source code (int_lit, operators, etc.)
# Each holds a data that represents its value or element (>, +, -, AND, OR)
# Each also has children, a list of nodes, that represents values to be operated on by the node
# These nodes are structural representations of each element in the source code that will be used by Parser

class ASTNode():
    def __init__(self, data, pos_start=None, pos_end=None):
        self.data = data
        self.children = []
        self.parent = None
        self.pos_start = pos_start
        self.pos_end = pos_end

    # Function to add children to the node
    def add_child(self, child):
        child.parent = self
        self.children.append(child)
    
    # Function to get how deep in the tree is a node (for printing AST)
    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent
        return level
    
    def print_tree(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + 'ᴸ--' if self.parent else spaces
        print(prefix + str(self.data))
        if self.children:
            for child in self.children:
                child.print_tree()

    def tree_str(self):
        spaces = ' ' * self.get_level() * 3
        prefix = spaces + 'ᴸ--' if self.parent else spaces
        result = prefix + str(self.data) + '\n'
        if self.children:
            for child in self.children:
                result += child.tree_str()
        return result

########## LITERALS AND IDENTIFIER ##########
# Int and Float Lit         
class NumNode(ASTNode):
    def __init__(self, val, pos_start=None, pos_end=None):
        super().__init__(f'Numlit: {val}', pos_start, pos_end)
        self.val = val

    def __repr__(self):
        return f'{self.val}'
    
# String Lit 
class StrLitNode(ASTNode):
    def __init__(self, val, pos_start=None, pos_end=None):
        super().__init__(f'Stringlit: {val}', pos_start, pos_end)
        self.val = val
    
    def __repr__(self):
        return f'{self.val}'
    
# Bool Lit 
class BoolLitNode(ASTNode):
    def __init__(self, val, pos_start=None, pos_end=None):
        super().__init__(val, pos_start, pos_end)
        self.val = val

    def __repr__(self):
        return f'{self.val}'

# Identifier 
class IdNode(ASTNode):
    def __init__(self, name, pos_start=None, pos_end=None):
        super().__init__(name, pos_start, pos_end)
        self.name = name
    
    def __repr__(self):
        return 'IdNode'

########## EXPRESSIONS ##########
# Binary Arithmetic Operation
class BiArithNode(ASTNode):
    def __init__(self, left, op, right, pos_start=None, pos_end=None):
        super().__init__(f'Binary Arith: {op.type}', pos_start, pos_end)
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)
        self.val = None
    
        try:
            self.val = eval(f'{left.val} {op.type} {right.val}')
        except ZeroDivisionError:
            self.val = 0
        except:
            self.val = None
    
    def __repr__(self):
        return f'Binary Arith: {self.op}'

# Exponentiation 
class ExpoNode(ASTNode):
    def __init__(self, left, op, right, pos_start=None, pos_end=None):
        super().__init__(f'Exponentiation: **', pos_start, pos_end)
        self.left = left
        self.op = op
        self.right = right
        self.add_child(left)
        self.add_child(right)
        # self.val = left.val ** right.val

# Relational Expressions
class RelNode(ASTNode):
    def __init__(self, left, op, right, pos_start=None, pos_end=None):
        super().__init__(f'Relational Expression: {op.type}', pos_start, pos_end)
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

# Logical Expressions
class LogicNode(ASTNode):
    def __init__(self, left, op, right, pos_start=None, pos_end=None):
        super().__init__(f'Logical Expression: {op.type}', pos_start, pos_end)
        self.left = left
        self.op = op.type
        self.right = right
        self.add_child(left)
        self.add_child(right)

# Unary Operator
class UnaryOperatorNode(ASTNode):
    def __init__(self, op, pos_start=None, pos_end=None):
        super().__init__(f'Unary operator: {op.type}', pos_start, pos_end)
        self.op = op.type

    def __repr__(self):
        return f'{self.op}'

# Unary Operation
class UnaryNode(ASTNode):
    def __init__(self, op, operand, prefix=False, postfix=False, pos_start=None, pos_end=None):
        super().__init__("Unary operation", pos_start, pos_end)
        self.op = UnaryOperatorNode(op, pos_start, pos_end)
        self.operand = operand
        self.prefix = prefix
        self.postfix = postfix

        if prefix:
            self.add_child(self.op)
            
        self.add_child(operand)

        if postfix:
            self.add_child(self.op)

    def __repr__(self):
        if self.postfix:
            return f"{self.operand}{self.op}"
        return f"{self.op}{self.operand}"

# VARIABLE DECLARTAION AND ASSIGNMENT
# Data Types
class DataTypeNode(ASTNode):
    def __init__(self, datatype, pos_start=None, pos_end=None):
        super().__init__(datatype, pos_start, pos_end)
        self.datatype = datatype

    def __repr__(self):
        return f'DataTypeNode: {self.datatype}'
    
# Const
class ConstNode(ASTNode):
    def __init__(self, pos_start=None, pos_end=None):
        super().__init__('Const', pos_start, pos_end)
    
    def __repr__(self):
        return f'ConstNode'

class VoidNode(ASTNode):
    def __init__(self, pos_start=None, pos_end=None):
        super().__init__('Void', pos_start, pos_end)

    def __repr__(self):
        return 'VoidNode'

# Variable Declaration
class VarDecNode(ASTNode):
    def __init__(self, const, datatype, name, val, pos_start=None, pos_end=None):
        super().__init__('Variable Declaration', pos_start, pos_end)
        self.const = const
        self.datatype = datatype
        self.name = name
        self.val = val

        if self.const:
            self.add_child(ConstNode(pos_start, pos_end))
        
        self.add_child(DataTypeNode(datatype, pos_start, pos_end))
        self.add_child(IdNode(name, pos_start, pos_end))
        self.add_child(val)

    def __repr__(self):
        return f'VarDecNode'
    
class AssignNode(ASTNode):
    def __init__(self, name, val, pos_start=None, pos_end=None):
        super().__init__('Assignment', pos_start, pos_end)
        self.name = name
        self.val = val
        self.add_child(IdNode(name, pos_start, pos_end))
        self.add_child(val)

    def __repr__(self):
        return f'AssignNode'

# Mix Literals
class MixLitNode(ASTNode):
    def __init__(self, vals, pos_start=None, pos_end=None):
        super().__init__('Mix Literals', pos_start, pos_end)
        self.vals = vals
        if isinstance(self.vals, list):
            for i in self.vals:
                if isinstance(self.vals, list):
                    self.add_child(MixLitNode(i, pos_start, pos_end))
                else:
                    self.add_child(i)
        else:
            self.add_child(vals)

    def __repr__(self):
        return f'{{{", ".join(repr(i) for i in self.vals)}}}'

# Mix Declaration
class MixDecNode(ASTNode):
    def __init__(self, const, name, size1=None, size2=None, val=None, pos_start=None, pos_end=None):
        super().__init__('Mix Declaration', pos_start, pos_end)
        self.const = const
        self.name = name
        self.size1 = size1
        self.size2 = size2
        self.val = val or []

        if self.const:
            self.add_child(ConstNode(pos_start, pos_end))
        self.add_child(IdNode(name, pos_start, pos_end))
        
        if size1: self.add_child(size1)
        if size2: self.add_child(size2)
        if self.val: 
            if isinstance(self.val, list):
                self.add_child(MixLitNode(self.val, pos_start, pos_end))
            else:
                self.add_child(self.val)
        
    def __repr__(self):
        return f'MixDecNode'

# Mix Index Accessing
class MixIndxNode(ASTNode):
    def __init__(self, name, index1, index2, pos_start=None, pos_end=None):
        super().__init__('Mix Index', pos_start, pos_end)
        self.name = name
        self.index1 = index1
        self.index2 = index2
        
        self.add_child(IdNode(name, pos_start, pos_end))
        self.add_child(index1)
        if index2:
            self.add_child(index2)
    
    def __repr__(self):
        return f'MixIndxNode'

# Mix Index Assignment
class MixIndxAssignNode(ASTNode):
    def __init__(self, name, index1, index2, val, pos_start=None, pos_end=None):
        super().__init__('Mix Index Assign', pos_start, pos_end)
        self.name = name
        self.index1 = index1
        self.index2 = index2
        self.val = val

        self.add_child(IdNode(name, pos_start, pos_end))
        self.add_child(index1)
        if self.index2:
            self.add_child(index2)
        self.add_child(val)

    def __repr__(self):
        return f'MixIndxAssignNode'

# FUNCTION DECLARATIONS
# SPyCe Function
class SpyceNode(ASTNode):
    def __init__(self, body, giveback, pos_start=None, pos_end=None):
        super().__init__('Spyce', pos_start, pos_end)
        self.body = body
        self.giveback = giveback
        self.add_child(body)
        self.add_child(giveback)

    def __repr__(self):
        return f'SpyceNode: {self.body}'
    
# Paramters
class ParamNode(ASTNode):
    def __init__(self, datatype, name, size1=None, size2=None, pos_start=None, pos_end=None):
        super().__init__('Parameters', pos_start, pos_end)
        self.datatype = datatype
        self.name = name
        self.size1 = size1
        self.size2 = size2

        self.add_child(DataTypeNode(datatype, pos_start, pos_end))
        self.add_child(IdNode(name, pos_start, pos_end))
        if size1:
            self.add_child(size1)
            if size2:
                self.add_child(size2)

# Sub-func Declarations
class MakeDecNode(ASTNode):
    def __init__(self, name, params, ret, body, pos_start=None, pos_end=None):
        super().__init__('Sub-Function Declaration', pos_start, pos_end)
        self.name = name
        self.params = params
        self.ret = ret
        self.body = body

        self.add_child(IdNode(name, pos_start, pos_end))
        for param in params:
            self.add_child(param)

        if self.ret == 'void':
            self.add_child(VoidNode(pos_start, pos_end))
        else:
            self.add_child(DataTypeNode(ret, pos_start, pos_end))
        self.add_child(body)

# Function Body
class FuncBodyNode(ASTNode):
    def __init__(self, pos_start=None, pos_end=None):
        super().__init__('Body', pos_start, pos_end)
    def __repr__(self):
        return 'BodyNode'

# Arguments
class ArgsNode(ASTNode):
    def __init__(self, pos_start=None, pos_end=None):
        super().__init__('Arguments', pos_start, pos_end)
    def __repr__(self):
        return 'ArgsNode'

# Function Call
class FuncCallNode(ASTNode):
    def __init__(self, name, args, pos_start=None, pos_end=None):
        super().__init__('Function Call', pos_start, pos_end)
        self.name = name
        self.args = args
        
        self.add_child(IdNode(name, pos_start, pos_end))
        if args:
            args_grp = ArgsNode(pos_start, pos_end)
            for i in args:
                args_grp.add_child(i)
                
            self.add_child(args_grp)

    def __repr__(self):
        return f'FuncCallNode: {self.name}'

# STATEMENTS
# Output
class SayNode(ASTNode):
    def __init__(self, val, pos_start=None, pos_end=None):
        super().__init__('Say Statement', pos_start, pos_end)
        self.val = val
        self.add_child(val)
    
    def __repr__(self):
        return f'SayNode'

# Input 
class ListenNode(ASTNode):
    def __init__(self, pos_start=None, pos_end=None):
        super().__init__('Listen Statement', pos_start, pos_end)
    def __repr__(self):
        return f'ListenNode'

# Giveback
class GivebackNode(ASTNode):
    def __init__(self, val, pos_start=None, pos_end=None):
        super().__init__('Giveback Statement', pos_start, pos_end)
        self.val = val
        if val: self.add_child(val)
    
    def __repr__(self):
        return f'GivebackNode: {self.val}'

# When
class WhenNode(ASTNode):
    def __init__(self, condition, body, elsewhen=None, otherwise_node=None, pos_start=None, pos_end=None):
        super().__init__('When Statement', pos_start, pos_end)
        self.condition = condition
        self.body = body
        self.elsewhen = elsewhen or []
        self.otherwise_node = otherwise_node

        self.add_child(condition)
        self.add_child(body)
        for els in self.elsewhen:
            self.add_child(els)
        if otherwise_node:
            self.add_child(otherwise_node)

    def __repr__(self):
        return f'WhenNode'
    
# Elsewhen
class ElsewhenNode(ASTNode):
    def __init__(self, condition, body, pos_start=None, pos_end=None):
        super().__init__('Elsewhen Statement', pos_start, pos_end)
        self.condition = condition
        self.body = body

        self.add_child(condition)
        self.add_child(body)

    def __repr__(self):
        return f'ElsewhenNode'
    
# Otherwise
class OtherwiseNode(ASTNode):
    def __init__(self, body, pos_start=None, pos_end=None):
        super().__init__('Otherwise Statement', pos_start, pos_end)
        self.body = body
        self.add_child(body)

    def __repr__(self):
        return f'OtherwiseNode'

# Choose
class ChooseNode(ASTNode):
    def __init__(self, condition, cases, pos_start=None, pos_end=None):
        super().__init__('Choose Statement', pos_start, pos_end)
        self.condition = condition
        self.cases = cases

        self.add_child(condition)
        for case in cases: self.add_child(case)
    
    def __repr__(self):
        return f'ChooseNode'

# Case
class CaseNode(ASTNode):
    def __init__(self, condition, body, pos_start=None, pos_end=None):
        super().__init__('Case', pos_start, pos_end)
        self.condition = condition
        self.body = body

        self.add_child(condition)
        self.add_child(body)

    def __repr__(self):
        return f'CaseNode'

# Default
class DefaultNode(ASTNode):
    def __init__(self, body, pos_start=None, pos_end=None):
        super().__init__('Default Case', pos_start, pos_end)
        self.body = body

        self.add_child(body)

    def __repr__(self):
        return f'DefaultNode'

# For-loop
class ForLoopNode(ASTNode):
    def __init__(self, header, body, pos_start=None, pos_end=None):
        super().__init__('For-Loop Statement', pos_start, pos_end)
        self.header = header
        self.body = body

        self.add_child(header)
        self.add_child(body)
    
    def __repr__(self):
        return f'ForLoopNode: {self.header} {self.body}'

# For-loop Header
class ForHeaderNode(ASTNode):
    def __init__(self, var, condition, unary, pos_start=None, pos_end=None):
        super().__init__('For-Loop Header', pos_start, pos_end)
        self.var = var
        self.condition = condition
        self.unary = unary

        self.add_child(var)
        self.add_child(condition)
        self.add_child(unary)
    
    def __repr__(self):
        return f'ForHeaderNode: {self.var}; {self.condition}; {self.unary}'

# While loop
class WhileNode(ASTNode):
    def __init__(self, condition, body, pos_start=None, pos_end=None):
        super().__init__('While Statement', pos_start, pos_end)
        self.condition = condition
        self.body = body

        self.add_child(condition)
        self.add_child(body)

    def __repr__(self):
        return f'WhileNode: {self.condition} {self.body}'
    
# Break
class BreakNode(ASTNode):
    def __init__(self, pos_start=None, pos_end=None):
        super().__init__('Break Statement', pos_start, pos_end)
    def __repr__(self):
        return 'BreakNode'

# Continue
class ContNode(ASTNode):
    def __init__(self, pos_start=None, pos_end=None):
        super().__init__('Continue Statement', pos_start, pos_end)
    def __repr__(self):
        return 'ContNode'

# BUILT-IN FUNCTIONS
# toint()
class ToIntNode(ASTNode):
    def __init__(self, arg, pos_start=None, pos_end=None):
        super().__init__('To Int Function', pos_start, pos_end)
        self.arg = arg
        self.add_child(arg)

    def __repr__(self):
        return f'IntNode: {self.arg}'

# tofloat()
class ToFloatNode(ASTNode):
    def __init__(self, arg, pos_start=None, pos_end=None):
        super().__init__('To Float Function', pos_start, pos_end)
        self.arg = arg
        self.add_child(arg)

    def __repr__(self):
        return f'FloatNode: {self.arg}'

# tostr()
class ToStrNode(ASTNode):
    def __init__(self, arg, pos_start=None, pos_end=None):
        super().__init__('To String Function', pos_start, pos_end)
        self.arg = arg
        self.add_child(arg)

    def __repr__(self):
        return f'StrNode: {self.arg}'

# tobool()
class ToBoolNode(ASTNode):
    def __init__(self, arg, pos_start=None, pos_end=None):
        super().__init__('To Bool Function', pos_start, pos_end)
        self.arg = arg
        self.add_child(arg)

    def __repr__(self):
        return f'BoolNode: {self.arg}'

# len()
class LenNode(ASTNode):
    def __init__(self, arg, pos_start=None, pos_end=None):
        super().__init__('Len Function', pos_start, pos_end)
        self.arg = arg
        self.add_child(arg)

    def __repr__(self):
        return f'LenNode: {self.arg}'

# type()
class TypeNode(ASTNode):
    def __init__(self, arg, pos_start=None, pos_end=None):
        super().__init__('Type Function', pos_start, pos_end)
        self.arg = arg
        self.add_child(arg)

    def __repr__(self):
        return f'TypeNode: {self.arg}'

# upper()
class UpperNode(ASTNode):
    def __init__(self, arg, pos_start=None, pos_end=None):
        super().__init__('Upper Function', pos_start, pos_end)
        self.arg = arg
        self.add_child(arg)

    def __repr__(self):
        return f'UpperNode: {self.arg}'

# lower()
class LowerNode(ASTNode):
    def __init__(self, arg, pos_start=None, pos_end=None):
        super().__init__('Lower Function', pos_start, pos_end)
        self.arg = arg
        self.add_child(arg)

    def __repr__(self):
        return f'LowerNode: {self.arg}'

# trunc()
class TruncNode(ASTNode):
    def __init__(self, val, dig, pos_start=None, pos_end=None):
        super().__init__('Truncate Function', pos_start, pos_end)
        self.val = val
        self.dig = dig
        self.add_child(val)
        self.add_child(dig)

    def __repr__(self):
        return f'TruncNode: {self.val}, {self.dig}'