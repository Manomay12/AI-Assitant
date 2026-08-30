"use client";

import { memo, useCallback, useRef, useState } from "react";

interface HudInputBarProps {
  onSendMessage: (text: string) => void;
  isListening: boolean;
  onToggleMic: () => void;
}

function HudInputBar({ onSendMessage, isListening, onToggleMic }: HudInputBarProps) {
  const [value, setValue] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSend = useCallback(() => {
    const text = value.trim();
    if (!text) return;
    setValue("");
    onSendMessage(text);
  }, [value, onSendMessage]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="hud-bottom-bar">
      <div className="input-group">
        <button
          type="button"
          className={`mic-btn ${isListening ? "listening" : ""}`}
          onClick={onToggleMic}
          title={isListening ? "Listening... (Click to stop)" : "Click to speak via Microphone"}
        >
          {isListening ? "🔴 LISTENING..." : "🎙 MIC"}
        </button>

        <input
          ref={inputRef}
          type="text"
          className="hud-input"
          placeholder="Speak or type a command... (e.g. 'Search YouTube for Avengers' or 'Open Google')"
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          autoComplete="off"
          spellCheck={false}
        />

        <button type="button" className="send-btn" onClick={handleSend}>
          TRANSMIT
        </button>
      </div>
    </div>
  );
}

export default memo(HudInputBar);
