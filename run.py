from flask import Flask
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from backend.lexer import lexical_analyze
from backend.syntax import syntax_analyze
from backend.semantic import semantic_analyze
from backend.interpreter import CodeRunner
from backend.Error import ReturnException

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('lexical_analysis')
def handle_analyze_code(data):
    code = data.get('code', '')
    if not code.strip():
        emit('lexical_result', {'tokens': [], 'errors': ['No input detected.']})
        return
    
    tokens, errors = lexical_analyze(code)
    
    token_dicts = [{'type': token.type, 'value': str(token.value)} for token in tokens]
    err_dicts = [str(error) for error in errors]

    emit('lexical_result', {'tokens': token_dicts, 'errors': err_dicts})

@socketio.on('syntax_analysis')
def handle_syntax_analysis(data):
    code = data.get('code', '')
    tokens, lexical_err = lexical_analyze(code)

    if lexical_err:
        emit('syntax_result', {'sucess': False, 'error': 'Syntax Error due to Lexical Errors'})
        return

    msg, syntax_err = syntax_analyze(tokens)
    if syntax_err:
        emit('syntax_result', {'success': False, 'error': str(syntax_err)})
        print('########## SUCCESSFUL SYNTAX ANALYZATION ##########')

    else:
        emit('syntax_result', {'success': True, 'msg': msg})

@socketio.on('semantic_analysis')
def handle_semantic_analysis(data):
    code = data.get('code', '')
    tokens, lexical_err = lexical_analyze(code)

    if lexical_err:
        emit('semantic_result', {'success': False, 'errors': ['Semantic Error due to Lexical Errors']})
        return

    msg, syntax_err = syntax_analyze(tokens)
    if syntax_err:
        emit('semantic_result', {'success': False, 'errors': ['Semantic Error due to Syntax Errors']})
        return

    ast, semantic_err, tree_str, stable = semantic_analyze(tokens)
    if semantic_err:
        err_dicts = [str(error) for error in semantic_err]
        emit('semantic_result', {'success': False, 'errors': err_dicts})
        return
    
    emit('semantic_result', {'success': True, 'msg': '✅ Successful from Semantic Analyzer'})
    print('########## SUCCESSFUL SEMANTIC ANALYZATION ##########')

@socketio.on('generate_code')
def handle_generate_code(data):
    code = data.get('code', '')
    tokens, lexical_err = lexical_analyze(code)

    if lexical_err:
        lex_err_dicts = [str(error) for error in lexical_err]
        emit('code_result', {'success': False, 'msg': lex_err_dicts})
        return
    
    msg, syntax_err = syntax_analyze(tokens)
    if syntax_err:
        emit('code_result', {'success': False, 'msg': str(syntax_err)})
        return
    
    ast, semantic_err, tree_str, stable = semantic_analyze(tokens)
    if semantic_err:
        semantic_err_dicts = [str(error) for error in semantic_err]
        emit('code_result', {'success': False, 'msg': semantic_err_dicts})
        return
           
    if ast:
        global runner
        runner = CodeRunner(stable, socketio=socketio)
        try:
            runner.visit(ast)
        except ReturnException as r:
            print("Program Finished")
        output = runner.output
        error = runner.error
        print(f"ERORR: {error}")
        if error:
            emit('code_result', {'success': False, 'msg': str(error)})
            return
        
        emit('code_result', {'success': True, 'msg': "".join(output)})

@socketio.on('input_response')
def handle_input_response(data):
    val = data.get('value')
    
    if runner:
        runner.input_data = val
        runner.input_received.set() 
    else:
        print("⚠️ Received input, but no program is currently running.")

@socketio.on('output_received')
def handle_output_received():
    if runner:
        runner.output_ack.set()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)