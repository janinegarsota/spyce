import React from 'react';
import Editor, { OnMount } from '@monaco-editor/react';
import '../styles/CodeEditor.css';

interface CodeEditorProps {
  code: string;
  setCode: (val: string) => void;
  showLexical: boolean;
}

export const CodeEditor: React.FC<CodeEditorProps> = ({ code, setCode, showLexical }) => {
  const handleEditorOnMount: OnMount = (editor, monaco) => {
    monaco.languages.register({ id: 'spyce' })

    monaco.languages.setLanguageConfiguration('spyce', {
      brackets: [
        ['{', '}'],
        ['[', ']'],
        ['(', ')'],
      ],
      autoClosingPairs: [
        { open: '{', close: '}' },
        { open: '[', close: ']' },
        { open: '(', close: ')' },
        { open: '"', close: '"' },
        { open: '~~', close: '~~' },
      ],
      surroundingPairs: [
        { open: '{', close: '}' },
        { open: '[', close: ']' },
        { open: '(', close: ')' },
        { open: '"', close: '"' },
      ],
    });

    monaco.languages.setMonarchTokensProvider('spyce', {
      keywords:     ['break', 'const', 'continue', 'listen', 'say', 'spyce', 'giveback', 'true', 'false'],
      datatypes:    ['int', 'float', 'char', 'string', 'bool', 'mix'],
      logops:       ['AND', 'OR', 'NOT'],
      ctrlstructs:  ['for', 'while', 'when', 'elsewhen', 'otherwise', 'choose', 'case', 'default'],
      builtins:     ['toint', 'tofloat', 'tostr', 'tobool', 'trunc', 'upper', 'lower', 'type', 'len'],

      tokenizer: {
        root: [
          // comments
          // [/~~[\s\S]*?~~/, 'comment'], 
          [/~~/, {token: 'comment', next: '@comment'}],

          // keyowrds and idenfitiers
          [/[A-Za-z_][A-Za-z0-9_]*/, {    
            cases: {
              '@keywords'     : 'keyword',
              '@datatypes'    : 'datatype',
              '@logops'       : 'logop',
              '@ctrlstructs'  : 'ctrlstruct',
              '@builtins'     : 'builtin',
              'make'          : 'make',
              'void'          : 'void',
              '@default'      : 'identifier'
            }
          }],

          // string and char
          // [/"(?:\\.|[^"\\])*"/, "string"], 
          [/"/, {token: 'string', next: '@string'}],

          // numbers
          [/\d+(\.\d+)?/, "number"],

          // operators
          [/[%!=+\-*/{}();<>]/, "operator"],
          [/->/, "operator"],
          
        ],
        comment: [
          [/~~/, 'comment', '@pop'],
          [/./, 'comment'],
        ],
        string: [
          [/"/, 'string', '@pop'],
          [/./, 'string'],
        ]
      }
    });

    monaco.editor.defineTheme('spyceTheme', {
      base: 'vs-dark',
      inherit: true,
      rules: [
        { token: 'keyword', foreground: 'FFD700' },                       // yellow 
        { token: 'identifier', foreground: 'F3DFDF' },                    // white
        { token: 'string', foreground: '3FF33F' },                        // green
        { token: 'comment', foreground: 'A3A3A3', fontStyle: 'italic' },  // grey
        { token: 'number', foreground: 'E13998' },                        // reddish pink
        { token: 'operator', foreground: 'DF7852' },                      // orange
        { token: 'datatype', foreground: '00deff' },                      // cyan
        { token: 'logop', foreground: 'a2d827' },                         // yellow green
        { token: 'ctrlstruct', foreground: 'ff00ff' },                    // pink
        { token: 'builtin', foreground: 'e21d60' },                       // red
        { token: 'make', foreground: 'FF7700' },                          // bright orange
        { token: 'void', foreground: '509faf' }                           // dark blue
      ],
      colors: {
        'editor.background': '#490009',
        'editorLineNumber.foreground': '#FFFFFF',
        'editorCursor.foreground': '#FFFFFF',
        'editorLineNumber.activeForeground': '#FFFFFF',
        'editorLineHighlightBackground': '#FFFFFF',
        'editor.lineHighlightBorder': '#ffffff7a'
      }
    });

    monaco.languages.registerCompletionItemProvider('spyce', {
      provideCompletionItems: (model, position) => {
        const word = model.getWordUntilPosition(position);
        const range = {
          startLineNumber: position.lineNumber,
          endLineNumber: position.lineNumber,
          startColumn: word.startColumn,
          endColumn: word.endColumn,
        };

        const suggestions = [
          // SPYCE FUNCTION SNIPPET
          {label: 'spyce (spy)', kind: monaco.languages.CompletionItemKind.Snippet, insertText: 'spyce() -> void {\n\tgiveback void;\n}', documentation: 'Main function in SPyCe', range: range},
          
          // DATA TYPES AND VARIABLES
          {label: 'int (int)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'int', documentation: 'Represents an integer data type', range: range},
          {label: 'float (flo)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'float', documentation: 'Represents a float data type', range: range},
          {label: 'string (str)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'string', documentation: 'Represents a string data type', range: range},
          {label: 'bool (boo)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'bool', documentation: 'Represents a boolean type', range: range},
          {label: 'mix (mix)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'mix', documentation: 'Represents a mix type', range: range},
          
          // IO
          {label: 'say (say)', details: 'Output function', kind: monaco.languages.CompletionItemKind.Function, insertText: 'say(${1:argument});$0', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Outputs text, variables, or results to the screen. Only accepts one argument', range: range},
          {label: 'listen (lis)', details: 'Input function', kind: monaco.languages.CompletionItemKind.Function, insertText: 'listen()', documentation: 'Used to accept user input and store it to to where it is assigned', range: range},

          // LOGICAL OPERATORS
          {label: 'AND (and)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'AND', documentation: 'Returns true only if both operands are true', range: range},
          {label: 'OR (or)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'OR', documentation: 'Returns true if at least one operand is true', range: range},
          {label: 'NOT (not)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'NOT', documentation: 'Returns the reversed the truth value', range: range},

          // CONDITIONALS
          {label: 'when (whe)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'when(${1:condition}){\n\t${2:say("Hello, World!");}\n}$0', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Executes a block of code if a certain condition is true', range: range},
          {label: 'elsewhen (els)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'elsewhen(${1:condition}){\n\t${2:say("Hello, World!");}\n}$0', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Executes a block of code if a previous conditional was false and this condition is true', range: range},
          {label: 'otherwise (oth)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'otherwise{\n\t${1:say("Hello, World!");}\n}$0', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Executes when no previous conditions were true', range: range},
          {label: 'choose (cho)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'choose(${1:variable}){\n\n}', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Used to select one of many code blocks to be executed', range: range},
          {label: 'case (cas)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'case ${1:condition}:\nsay("Hello, World!");', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Defines a specific case inside a choose conditional', range: range},
          {label: 'default (def)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'default:\nsay("Hello, World!");', documentation: 'Fallback if no other case matches', range: range},

          // ITERATION
          {label: 'for (for)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'for(${1:init};${2:condition};${3:unary}){\n\t${4:say("Hello, World!");}\n}$0', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Loops over a range, sequence,  or iterable', range: range},
          {label: 'while (whi)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'while(${1:condition}){\n\t${2:say("Hello, World!");}\n}$0', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Fallback if no other case matches', range: range},
          {label: 'break (bre)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'break;', documentation: 'Exits immediately', range: range},
          {label: 'continue (con)' , kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'continue;', documentation: 'Skips current iteration and goes to the next loop cycle', range: range},

          // OTHERS
          {label: 'true (tru)', kind: monaco.languages.CompletionItemKind.Value, insertText: 'true', documentation: 'Boolean literal for truth', range: range},
          {label: 'false (fal)', kind: monaco.languages.CompletionItemKind.Value, insertText: 'false', documentation: 'Boolean literal for falsehood', range: range},
          {label: 'make (mak)', kind: monaco.languages.CompletionItemKind.Function, insertText: 'make ${1:funcname}(${2:parameters}) -> ${3:retType} {\n\tsay("Hello, World!");\n}$0', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Defines a function', range: range},
          {label: 'const (con)', kind: monaco.languages.CompletionItemKind.Constant, insertText: 'const', documentation: 'Declares a constant variable', range: range},
          {label: 'void (voi)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'void', documentation: 'Indicates no return value from a function', range: range},
          {label: 'giveback (giv)', kind: monaco.languages.CompletionItemKind.Keyword, insertText: 'giveback ${1:value};$0', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Ends a function and sends a value back to where the function was called', range: range},

          // BUILT IN FUNCTIONS
          {label: 'toint (toin)', kind: monaco.languages.CompletionItemKind.Method, insertText: 'toint(${1:argument})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Converts its arguments to integer', range: range},  
          {label: 'tofloat (tofl)', kind: monaco.languages.CompletionItemKind.Method, insertText: 'tofloat(${1:argument})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Converts its arguments to float', range: range},  
          {label: 'tostr (tost)', kind: monaco.languages.CompletionItemKind.Method, insertText: 'tostr(${1:argument})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Converts its arguments to string', range: range},  
          {label: 'tobool (tost)', kind: monaco.languages.CompletionItemKind.Method, insertText: 'tobool(${1:argument})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Converts its arguments to boolean', range: range},  
          {label: 'upper (upp)', kind: monaco.languages.CompletionItemKind.Method, insertText: 'upper(${1:argument})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Returns a new string in lowercase', range: range},  
          {label: 'lower (low)', kind: monaco.languages.CompletionItemKind.Method, insertText: 'lower(${1:argument})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Returns a new string in uppercase', range: range},  
          {label: 'trunc (trun)', kind: monaco.languages.CompletionItemKind.Method, insertText: 'trunc(${1:argument1},${2:argument2})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Truncates decimal digits to n digits', range: range},  
          {label: 'len (len)', kind: monaco.languages.CompletionItemKind.Method, insertText: 'len(${1:argument})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Returns the length of a string or mix', range: range},  
          {label: 'type (typ)', kind: monaco.languages.CompletionItemKind.Method, insertText: 'type(${1:argument})', insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, documentation: 'Returns the type of its arguments', range: range}  
        ];
        return { suggestions };
      }
    });

    monaco.editor.setTheme('spyceTheme');
  };

  return (
    <div className="codeWrapper">
      <Editor
        height='100%'
        language='spyce'
        theme='spyceTheme'
        value={code}
        onMount={handleEditorOnMount}
        onChange={(val) => setCode(val || "")}
        options={{
          fontSize: 20,
          fontFamily: "'Fira Code', monospace",
          minimap: { enabled: false },
          automaticLayout: true,
          fixedOverflowWidgets: true,
          lineNumbers: "on",
          scrollBeyondLastLine: false,
          renderLineHighlight: "all",
          lineDecorationsWidth: 10
        }}
      />
    </div>
  )
}