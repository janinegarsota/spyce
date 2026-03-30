from .SemanticTools import SymbolTable, Parser
from .SemanticTools.ASTVisitor import ASTTraverser
from .SemanticTools.ASTNodes import SpyceNode
from .Error import SemanticError

def semantic_analyze(tokens):
    symbol_table = SymbolTable.SymbolTable()
    parser = Parser.Parser(tokens)
    visitor = ASTTraverser(symbol_table)
    ast, parse_err = parser.build_ast()
    tree_str = ""

    if parse_err is None: parse_err = []
    elif not isinstance(parse_err, list): parse_err = [parse_err]

    if not any(isinstance(node, SpyceNode) for node in ast.children):
        parse_err.insert(0, SemanticError(parser.current_token.pos_start, parser.current_token.pos_end, "Spyce function is not defined in the program"))

    if ast:
        visitor.visit(ast)
        # visitor.resolve_unresolved()  
        # print(symbol_table.scopes)
        tree_str = ast.tree_str()
        ast.print_tree()
        # print(visitor.errors)
    
    else:
        print("No AST built")
        return "No AST built", None, tree_str, None

    if visitor.errors:
        parse_err.extend(visitor.errors)
        if parse_err:
            parse_err.sort(key=lambda e: e.pos_start.ln)
        return ast, parse_err, tree_str, None
    
    if parse_err:
        parse_err.sort(key=lambda e: e.pos_start.ln)

    return ast, parse_err, tree_str, symbol_table