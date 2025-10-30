import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import MainContent from './components/MainContent';

function App() {
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  // ✅ Load from localStorage safely
  useEffect(() => {
    try {
      const saved = localStorage.getItem('mathChatHistory');
      const parsed = JSON.parse(saved);
      if (Array.isArray(parsed)) {
        setChatHistory(parsed);
      }
    } catch (err) {
      console.error("❌ Error parsing chatHistory:", err);
      localStorage.removeItem('mathChatHistory');
    }
  }, []);

  // ✅ Save to localStorage
  useEffect(() => {
    localStorage.setItem('mathChatHistory', JSON.stringify(chatHistory));
  }, [chatHistory]);

  // ✅ Clear chat view
  const handleNewChat = () => {
    setChatHistory([]);
  };

  // ✅ Send question to backend and return result
  const handleSendMessage = async (question) => {
    if (!question.trim()) return;
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      return { result: data }; // ✅ Return result to MainContent
    } catch (error) {
      console.error('❌ Error:', error);
      return {
        result: {
          answer: '⚠️ Error fetching answer.',
          steps: [],
          solution: '',
        },
      };
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden">
      <Sidebar chatHistory={chatHistory} onNewChat={handleNewChat} />
      <MainContent
        chatHistory={chatHistory}
        setChatHistory={setChatHistory}
        onSendMessage={handleSendMessage}
      />
    </div>
  );
}

export default App;
