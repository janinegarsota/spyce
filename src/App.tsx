import { useEffect, useState } from "react";
import { io, Socket } from 'socket.io-client';
import { Token } from './utils/tokenInterface';
import { Header } from './components/Header';
import { CodeEditor } from './components/CodeEditor';
import { Terminal } from './components/Terminal';
import { LexicalTable } from "./components/LexicalTable";
import './styles/Main.css';
import { error } from "console";

export default function App() {
  const [code, setCode] = useState("spyce() -> void {\n\tsay(\"Hello, World!\");\n\tgiveback void;\n}");
  const [tokens, setTokens] = useState<Token[]>([]);
  const [terminalMsg, setTerminalMsg] = useState("");
  const [showLexical, setShowLexical] = useState(false);
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isListening, setIsListening] = useState(false);

  useEffect(() => {
    const newSocket = io('http://localhost:5000');
    setSocket(newSocket);

    // LEXICAL SOCKET
    newSocket.on('lexical_result', (data: {
      tokens: { type: string, value: string }[];
      errors: string[];
    }) => {
      setTimeout(() => {
        const formattedTokens: Token[] = data.tokens.map(t => ({
          lexeme: t.value,
          token: t.type
        }));

        setTokens(formattedTokens);

        if (data.errors.length > 0) {
          const formattedErrors = data.errors.join('\n');
          setTerminalMsg(`❌ Errors:\n${formattedErrors}`);
        } else {
          setTerminalMsg(`✅ Lexical Analysis Successful`);
        }
      }, 600);
    });

    // SYNTAX SOCKET
    newSocket.on('syntax_result', (data: {
      success: boolean,
      error?: string;
      msg?: string
    }) => {
      setTimeout(() => {
        if (data.success) {
          setTerminalMsg(data.msg || `✅ Syntax Analysis Successful`);
        } else {
          setTerminalMsg(`❌ ${data.error}`);
        }
      }, 600);
    });

    // SEMANTIC SOCKET
    newSocket.on('semantic_result', (data: {
      success: boolean,
      errors?: string[];
      msg?: string
    }) => {
      setTimeout(() => {
        if (data.success) {
          setTerminalMsg(data.msg || `✅ Semantic Analysis Successful`);
        } else {
          setTerminalMsg(`❌ ${data.errors?.join('\n')}`);
        }
      }, 600);
    });

    // CODERUNNER SOCKET
    newSocket.on('code_result', (data: {
      success: boolean,
      errors?: any;
      msg?: any
    }) => {
      setTimeout(() => {
        if (data.success) {
          setTerminalMsg(prev => prev + '\n--- Program Execution Finished ---');
        } else {
          setTerminalMsg(`❌ ${data.msg}`);
        }
      }, 600);
    });

    // SAY FUNCTION SOCKET
    newSocket.on("output_update", (data: { success: boolean, msg: string }) => {
      if (data.success){
        setTerminalMsg(prev => prev + data.msg);
        console.log(data)
      }
      else {
        setTerminalMsg(data.msg)
      }
      newSocket.emit('output_received');
    });

    // LISTEN FUNCTION SOCKET
    newSocket.on("listen_input", () => {
      setIsListening(true);
    })

    return () => {
      newSocket.disconnect();
    }
  }, []);

  const analyzeLexer = () => {
    if (!socket || !socket.connected) {
      setTerminalMsg('❌ Socket not connected');
      return;
    }

    if (code.trim() === "") {
      setTerminalMsg("⚠️ No input detected.")
      setTokens([]);
      return
    }
    setTerminalMsg("⏳ Running Lexical Analysis...");
    setShowLexical(true);

    socket.emit('lexical_analysis', { code });
  };

  const analyzeSyntax = () => {
    if (!socket || !socket.connected) {
      setTerminalMsg('❌ Socket not connected');
      return;
    }
    if (code.trim() === "") {
      setTerminalMsg("⚠️ No input detected.")
      setTokens([]);
      return
    }
    setTerminalMsg("⏳ Running Syntax Analysis...");

    socket.emit('syntax_analysis', { code })
  };

  const analyzeSemantic = () => {
    if (!socket || !socket.connected) {
      setTerminalMsg('❌ Socket not connected');
      return;
    }
    if (code.trim() === "") {
      setTerminalMsg("⚠️ No input detected.")
      setTokens([]);
      return
    }
    setTerminalMsg("⏳ Running Semantic Analysis...");

    socket.emit('semantic_analysis', { code })
  };

  const codeGen = () => {
    if (!socket || !socket.connected) {
      setTerminalMsg('❌ Socket not connected');
      return;
    }
    if (code.trim() === "") {
      setTerminalMsg("⚠️ No input detected.")
      setTokens([]);
      return
    }
    setTerminalMsg('');
    socket.emit('generate_code', { code })
  }

  const closeLexical = () => {
    setShowLexical(false);
  }

  const onInputted = (val: string) => {
    console.log(val, typeof val);
    if (!socket || !socket.connected) {
      setTerminalMsg('❌ Socket not connected');
      return;
    }
    socket.emit('input_response', { value: val });

    setIsListening(false);
    setTerminalMsg(prev => prev + val + "\n");
  }

  const handleOpenFile = () => {

  }

  const handleSaveFile = () => {

  }

  return (
    <main>
      <div className="HeaderWrapper">
        <Header
          openFile={handleOpenFile}
          saveFile={handleSaveFile}
          onRun={() => { codeGen(); }}
          onLexical={analyzeLexer}
          onSyntax={analyzeSyntax}
          onSemantic={analyzeSemantic}
        />
      </div>

      <div className="CodeEditorWrapper">
        <CodeEditor
          code={code}
          setCode={setCode}
          showLexical={showLexical}
        />
      </div>

      <LexicalTable
        tokens={tokens}
        showLexical={showLexical}
        closeLexical={closeLexical}
      />

      <div className="TerminalWrapper">
        <Terminal
          message={terminalMsg}
          showLexical={showLexical}
          isListening={isListening}
          onInputted={onInputted}
        />
      </div>
    </main>
  );
}