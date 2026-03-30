import React from 'react';
import { Token } from '../utils/tokenInterface';
import '../styles/LexicalTable.css';

interface LexicalTableProps {
  tokens: Token[];
  showLexical: boolean;
  closeLexical: () => void;
}

export const LexicalTable: React.FC<LexicalTableProps> = ({ tokens, showLexical, closeLexical }) => {
  return (
    <div className={`lexical_container ${showLexical ? "show" : "hide"}`}>
      <div className="lexical-cont">
        <button className="close_table" onClick={closeLexical}>CLOSE TABLE</button>
        <table className="lexical_table">
          <thead>
            <tr>
              <th>LEXEME</th>
              <th>TOKEN</th>
            </tr>
          </thead>
          <tbody>
            {tokens.length > 0 ? (
              tokens.map((t, index) => (
                <tr key={index}>
                  <td>{t.lexeme}</td>
                  <td>{t.token}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={2} style={{ color: "#aaa" }}>
                  No tokens generated yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};