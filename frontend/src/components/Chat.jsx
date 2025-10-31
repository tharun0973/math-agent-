import { useState, useRef, useEffect } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
import { IoMdSend } from "react-icons/io";
import { FaRobot, FaUser } from "react-icons/fa";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  // 🧮 Send user message and get backend response
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/solve", {
        question: input,
        stream: false,
      });

      let cleanAnswer = res.data.answer || "⚠️ No answer returned.";

      // 🧹 Remove "Final Answer" label, ✅ emojis, and extra markdown brackets
      cleanAnswer = cleanAnswer
        .replace(/✅?\s*Final Answer:?/gi, "")
        .replace(/\[|\]/g, "")
        .trim();

      const agentMessage = {
        role: "agent",
        content: cleanAnswer,
      };

      setMessages((prev) => [...prev, agentMessage]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        { role: "agent", content: "⚠️ Error connecting to backend." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // ⌨️ Press Enter to send message
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // 🔽 Auto-scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col h-screen bg-[#0d1117] text-gray-100">
      {/* 💬 Chat Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex items-start gap-3 ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {/* 🤖 Bot Icon */}
            {msg.role === "agent" && (
              <div className="p-2 rounded-full bg-gray-800">
                <FaRobot className="text-green-400" />
              </div>
            )}

            {/* 💬 Message Bubble */}
            <div
              className={`max-w-xl px-4 py-3 rounded-2xl text-sm leading-relaxed shadow-md whitespace-pre-wrap ${
                msg.role === "user"
                  ? "bg-blue-600 text-white rounded-br-none"
                  : "bg-gray-900 text-gray-100 border border-gray-700 rounded-bl-none"
              }`}
            >
              <ReactMarkdown
                remarkPlugins={[remarkMath]}
                rehypePlugins={[rehypeKatex]}
                className="markdown-content"
              >
                {msg.content}
              </ReactMarkdown>
            </div>

            {/* 👤 User Icon */}
            {msg.role === "user" && (
              <div className="p-2 rounded-full bg-blue-600">
                <FaUser className="text-white" />
              </div>
            )}
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* 📝 Input Area */}
      <div className="p-4 bg-[#161b22] border-t border-gray-700 flex items-center gap-3">
        <textarea
          rows={1}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your question and press Enter..."
          className="flex-1 p-3 bg-gray-900 text-gray-100 border border-gray-700 rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="p-3 rounded-xl bg-blue-600 hover:bg-blue-500 text-white disabled:opacity-50"
        >
          <IoMdSend size={20} />
        </button>
      </div>
    </div>
  );
}
