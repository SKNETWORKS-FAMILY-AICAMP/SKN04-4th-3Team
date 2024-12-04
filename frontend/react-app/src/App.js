import React, { useState, useEffect } from "react";
import { ReactTyped } from "react-typed";
import "./App.css";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [chatHistory, setChatHistory] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const [input, setInput] = useState("");

  const createNewChat = () => {
    const newChatId = Date.now();
    setChatHistory([
      { id: newChatId, title: "New Chat", messages: [] },
      ...chatHistory
    ]);
    setCurrentChatId(newChatId);
    setMessages([]);
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessages = [
      ...messages,
      { text: input, isUser: true },
      { text: `${input}에 대한 응답입니다.`, isUser: false }
    ];
    
    setMessages([
      ...messages,
      { text: input, isUser: true },
      { text: `${input}에 대한 응답입니다.`, isUser: false }
    ]);
    setMessages(newMessages);
    
    // 채팅 히스토리 업데이트
    setChatHistory(prevHistory =>
      prevHistory.map(chat => 
        chat.id === currentChatId 
          ? { ...chat, messages: newMessages, title: input.slice(0, 30) }
          : chat
      )
    );
    setInput("");
  };

  const loadChat = (chatId) => {
    const chat = chatHistory.find(c => c.id === chatId);
    if (chat) {
      setMessages(chat.messages);
      setCurrentChatId(chatId);
    }
  };

  useEffect(() => {
    if (!currentChatId && chatHistory.length === 0) {
      createNewChat();
    }
  }, []);

  return (
    <div className="app">
      <div className="chat-container">
        <div className="sidebar">
        <button className="new-chat" onClick={createNewChat}>
            + New Chat
          </button>
          <div className="chat-history">
            {chatHistory.map((chat) => (
              <div
                key={chat.id}
                className={`history-item ${currentChatId === chat.id ? 'active' : ''}`}
                onClick={() => loadChat(chat.id)} > {chat.title || "New Chat"}
              </div>
            ))}
          </div>
        </div>
        <div className="main-content">
          <div className="messages-list">
            {messages.map((message, index) => (
              <div key={index} className={`message-row ${message.isUser ? 'user' : 'assistant'}`}>
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
          </div>
          <form className="input-container" onSubmit={handleSendMessage}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Send a message..."
              className="message-input"
            />
            <button type="submit" className="send-button">
              ➤
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default App;