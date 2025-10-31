import MathBlock from "./MathBlock";
import { useState, useEffect, useRef } from "react";
import { IoMdSend } from "react-icons/io";
import { FiUpload } from "react-icons/fi";
import { BiCopy, BiLike, BiDislike } from "react-icons/bi";
import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";

const streamByChunks = async (text, onChunk, delay = 40) => {
  const chunks = text.split(/(?<=\n)/);
  for (const chunk of chunks) {
    await new Promise((res) => setTimeout(res, delay));
    onChunk(chunk);
  }
};

const ThinkingIndicator = () => (
  <div className="text-sm text-gray-500 italic mb-2 ml-2">
    🤖 Agent is thinking...
  </div>
);

const Markdown = ({ children, className = "text-gray-100" }) => (
  <ReactMarkdown
    remarkPlugins={[remarkMath]}
    rehypePlugins={[rehypeKatex]}
    components={{
      p: ({ node, ...props }) => (
        <p className={`${className} leading-relaxed`} {...props} />
      ),
      code: ({ inline, ...props }) =>
        inline ? (
          <code
            className="bg-gray-800 px-1.5 rounded text-sm font-mono"
            {...props}
          />
        ) : (
          <pre
            className="bg-[#111] p-3 rounded-lg overflow-x-auto text-sm"
            {...props}
          />
        ),
    }}
  >
    {children}
  </ReactMarkdown>
);

export default function MainContent({ chatHistory, setChatHistory }) {
  const [input, setInput] = useState("");
  const [isThinking, setIsThinking] = useState(false);
  const [streamingText, setStreamingText] = useState("");
  const [feedback, setFeedback] = useState({});
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatHistory, streamingText, isThinking]);

  const copyToClipboard = (text) => navigator.clipboard.writeText(text);

  const cleanSteps = (steps) => {
    if (!steps) return [];
    if (Array.isArray(steps)) return steps;
    return String(steps)
      .split(/\n+/)
      .map((s) => s.trim())
      .filter(Boolean);
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    const q = input.trim();
    setChatHistory((prev) => [...prev, { role: "user", content: q }]);
    setInput("");
    setIsThinking(true);
    setStreamingText("");

    try {
      const res = await fetch("http://localhost:8000/solve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });

      if (!res.ok) throw new Error("Backend error " + res.status);
      const data = await res.json();
      const rawAnswer = (data.answer || "").replace(/Sure,.*?:?\s*/i, "");

      await streamByChunks(rawAnswer, (chunk) => {
        setStreamingText((prev) => prev + chunk);
      }, 30);

      const finalAgent = {
        role: "agent",
        content: {
          question: q,
          answer: rawAnswer,
          steps: Array.isArray(data.steps)
            ? data.steps
            : cleanSteps(data.steps),
          solution: data.solution || "",
        },
      };

      setChatHistory((prev) => [...prev, finalAgent]);
      setStreamingText("");
    } catch (err) {
      console.error(err);
      setChatHistory((prev) => [
        ...prev,
        { role: "agent", content: { answer: "⚠️ Error contacting backend." } },
      ]);
    } finally {
      setIsThinking(false);
    }
  };

  const handleFeedback = (msgIndex, type) => {
    setFeedback((prev) => ({ ...prev, [msgIndex]: type }));
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const simulated = `📄 Uploaded: ${file.name}`;
    setChatHistory((prev) => [...prev, { role: "user", content: simulated }]);
  };

  return (
    <div className="flex flex-col flex-1 bg-[#0a0a0a] text-white">
      {chatHistory.length === 0 && !isThinking ? (
        // 🏠 Landing Page
        <div className="flex flex-col flex-1 items-center justify-center text-center p-6">
          <h1 className="text-4xl font-bold mb-3">Math Solver Agent</h1>
          <p className="text-gray-400 mb-8 max-w-md">
            Ask math questions and get step-by-step solutions beautifully rendered with LaTeX.
          </p>

          <div className="w-full max-w-xl flex items-center gap-3 bg-[#111] border border-orange-500 rounded-full px-5 py-3">
            <label className="cursor-pointer text-gray-300 hover:text-orange-400">
              <FiUpload className="w-5 h-5" />
              <input type="file" className="hidden" onChange={handleFileUpload} />
            </label>
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              rows={1}
              placeholder="Ask a math question..."
              className="flex-1 bg-transparent outline-none px-3 text-white placeholder-gray-500 resize-none"
            />
            <button
              onClick={handleSend}
              className="bg-orange-500 hover:bg-orange-600 text-white rounded-full p-2"
            >
              <IoMdSend className="w-5 h-5" />
            </button>
          </div>

          <div className="text-xs text-gray-600 mt-6">
            Built by Tharun Kumar • Math Routing Agent
          </div>
        </div>
      ) : (
        <>
          {/* 💬 Chat Section */}
          <div className="flex-1 overflow-y-auto px-6 py-6 space-y-6">
            {chatHistory.map((msg, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className={`flex w-full ${
                  msg.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div className="flex flex-col max-w-[70%]">
                  {msg.role === "agent" &&
                    idx === chatHistory.length - 1 &&
                    isThinking && <ThinkingIndicator />}

                  <div className="p-4 rounded-2xl bg-[#111]">
                    {msg.role === "agent" ? (
                      <>
                        <Markdown>
                          {streamingText && idx === chatHistory.length - 1
                            ? streamingText
                            : msg.content.answer}
                        </Markdown>

                        {(msg.content.steps || []).length > 0 && (
                          <div className="mt-4 space-y-2">
                            {msg.content.steps.map((step, i) => (
                              <div key={i} className="text-sm text-gray-300">
                                <span className="text-orange-400 font-semibold">
                                  Step {i + 1}:
                                </span>{" "}
                                <Markdown>{step}</Markdown>
                              </div>
                            ))}
                          </div>
                        )}

                        <div className="flex gap-3 mt-3 text-gray-400 text-sm justify-start">
                          <button
                            onClick={() => handleFeedback(idx, "like")}
                            className={`text-xl ${
                              feedback[idx] === "like"
                                ? "text-green-400"
                                : "hover:text-green-400"
                            }`}
                          >
                            <BiLike />
                          </button>
                          <button
                            onClick={() => handleFeedback(idx, "dislike")}
                            className={`text-xl ${
                              feedback[idx] === "dislike"
                                ? "text-red-400"
                                : "hover:text-red-400"
                            }`}
                          >
                            <BiDislike />
                          </button>
                        </div>
                      </>
                    ) : (
                      <div className="text-gray-100">{msg.content}</div>
                    )}
                  </div>
                </div>
              </motion.div>
            ))}
            <div ref={bottomRef} />
          </div>

          {/* 🧠 Input Box */}
          <div className="border-t border-gray-800 p-3 bg-[#080808] flex items-center gap-3 sticky bottom-0">
            <div className="flex items-center w-full max-w-3xl mx-auto bg-[#111] border border-orange-500 rounded-full px-5 py-2.5">
              <label className="cursor-pointer text-gray-300 hover:text-orange-400">
                <FiUpload className="w-5 h-5" />
                <input
                  type="file"
                  className="hidden"
                  onChange={handleFileUpload}
                />
              </label>
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Type your question..."
                rows={1}
                className="flex-1 bg-transparent outline-none px-3 text-white placeholder-gray-500 resize-none"
              />
              <button
                onClick={handleSend}
                className="bg-orange-500 hover:bg-orange-600 text-white rounded-full p-2"
              >
                <IoMdSend className="w-5 h-5" />
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
