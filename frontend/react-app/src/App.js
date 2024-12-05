import React, { useState, useCallback, useRef, useEffect } from "react";
import { ReactTyped } from "react-typed";
import "./App.css";
import InsuranLogo from './images/Insuran.png';

const API_URL = `${window.location.protocol}//${window.location.host}/api/chat/`;

const Header = () => {
  return (
    <div className="header">
      <img src={InsuranLogo} alt="Insurance King Logo" className="logo" />
      <p id="BannerLetter">Insurance King</p>
      <img src={InsuranLogo} alt="Insurance King Logo" className="logo" />
    </div>
  );
};

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = useCallback(async (e) => {
    e.preventDefault();
    const trimmedInput = input.trim();
    
    if (!trimmedInput) return;

    const userMessage = { 
      id: Date.now(), 
      text: trimmedInput, 
      isUser: true 
    };

    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: trimmedInput })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      const botMessage = { 
        id: Date.now() + 1, 
        text: data.bot_response, 
        isUser: false 
      };

      setMessages([...newMessages, botMessage]);

    } catch (error) {
      console.error("Error details:", error);
      
      const errorMessage = { 
        id: Date.now(), 
        text: `통신 오류: ${error.message}`, 
        isUser: false 
      };

      setMessages([...newMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [input, messages]);

  return (
    <div className="app">
      <Header />
      <div className="chat-container">
        <div className="main-content">
          <div className="messages-list">
            {messages.map((message) => (
              <div 
                key={message.id} 
                className={`message-row ${message.isUser ? 'user' : 'assistant'}`}
              >
                <div className="message-content">
                  <div className="avatar">
                    {message.isUser ? '👤' : '🤖'}
                  </div>
                  <div className="message-bubble">
                    {message.isTyping ? (
                      <ReactTyped
                        strings={[message.text]}
                        typeSpeed={20}
                        showCursor={false}
                      />
                    ) : (
                      message.text
                    )}
                  </div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
            {isLoading && (
              <div className="message-row assistant loading">
                <div className="message-content">
                  <div className="avatar">🤖</div>
                  <div className="message-bubble">
                    답변 생성 중...
                  </div>
                </div>
              </div>
            )}
          </div>
          
          <form className="input-container" onSubmit={handleSendMessage}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Send a message..."
              className="message-input"
              disabled={isLoading}
            />
            <button 
              type="submit" 
              className="send-button"
              disabled={isLoading}
            >
              ➤
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default App;
