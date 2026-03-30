import React, { useState, useEffect, useRef } from 'react';
import "../styles/Terminal.css";

interface TerminalProps {
  message: string;
  showLexical: boolean;
  isListening: boolean;
  onInputted: (val: string) => void;
}

export const Terminal: React.FC<TerminalProps> = ({ message, showLexical, isListening, onInputted }) => {
  const [input, setInput] = useState<string>("");
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isListening) {
      inputRef.current?.focus();
    }
  }, [isListening]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      onInputted(input);
      setInput("");
    }
  }

  return (
    <div className={`terminal ${showLexical ? "shrink" : "expand"}`}>
      <div className="terminal-img-cont">
        <div className="terminal-word">TERMINAL</div>
        <hr className="line" />
        <div className="terminal-text">
          <pre style={{ whiteSpace: 'pre-wrap', margin: 0 }}>{message}</pre>

          {isListening && (
            <div className="input-line">
              <span className="prompt">{">"} </span>
              <input
                ref={inputRef}
                type="text"
                className="terminal-input"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type input here..."
                autoFocus
              />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}