import React, { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import MessageBubble from './MessageBubble';
import LoadingIndicator from './LoadingIndicator';

export default function InterviewChat({ messages, loading, onSendMessage, disabled }) {
  const [inputText, setInputText] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputText.trim() || loading || disabled) return;
    onSendMessage(inputText);
    setInputText('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="chat-workspace">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <MessageBubble key={index} message={msg} />
        ))}
        {loading && <LoadingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <form className="chat-input-form" onSubmit={handleSubmit}>
          <textarea
            className="chat-input"
            placeholder={disabled ? "Interview completed. View feedback below." : "Type your technical response... (Press Enter to send, Shift+Enter for newline)"}
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading || disabled}
            rows={2}
          />
          <button 
            type="submit" 
            className="btn-primary" 
            disabled={!inputText.trim() || loading || disabled}
            style={{ opacity: (!inputText.trim() || loading || disabled) ? 0.5 : 1, padding: '0 1.25rem' }}
          >
            <Send size={18} />
          </button>
        </form>
      </div>
    </div>
  );
}
