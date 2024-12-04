import React, { useState, useCallback } from "react";
// import { ReactTyped } from "react-typed";
import "./App.css";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = useCallback(async (e) => {
    e.preventDefault();
    const trimmedInput = input.trim();
    
    if (!trimmedInput) return;

    // 사용자 메시지 추가
    const userMessage = { 
      id: Date.now(), 
      text: trimmedInput, 
      isUser: true 
    };

    // 메시지 상태 업데이트
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat/', {
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

      // 봇 메시지 추가
      const botMessage = { 
        id: Date.now() + 1, 
        text: data.bot_response, // 서버 응답의 bot_response 필드 사용
        isUser: false 
      };

      // 메시지 상태 최종 업데이트
      setMessages(prevMessages => [...prevMessages, botMessage]);

    } catch (error) {
      console.error("Error details:", error);
      
      const errorMessage = { 
        id: Date.now(), 
        text: `통신 오류: ${error.message}`, 
        isUser: false 
      };

      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [input]);

  return (
    <div className="app">
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
                    {message.text}
                  </div>
                </div>
              </div>
            ))}
            
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
              placeholder="메시지를 입력하세요..."
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