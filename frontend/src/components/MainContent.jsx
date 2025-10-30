import { useState, useEffect, useRef } from "react"
import { IoMdSend } from "react-icons/io"
import { FiUpload } from "react-icons/fi"
import { BiCopy, BiLike, BiDislike } from "react-icons/bi"
import ReactMarkdown from "react-markdown"
import remarkMath from "remark-math"
import rehypeKatex from "rehype-katex"
import "katex/dist/katex.min.css"

const useTypingEffect = (text, speed = 15) => {
  const [displayedText, setDisplayedText] = useState("")
  useEffect(() => {
    if (!text) return
    setDisplayedText("")
    let i = 0
    const interval = setInterval(() => {
      setDisplayedText((prev) => prev + text.charAt(i))
      i++
      if (i >= text.length) clearInterval(interval)
    }, speed)
    return () => clearInterval(interval)
  }, [text])
  return displayedText
}

export default function MainContent({ chatHistory, setChatHistory, onSendMessage }) {
  const [input, setInput] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [chatHistory, isTyping])

  const handleSend = async () => {
    if (!input.trim()) return
    const userMessage = { role: "user", content: input }
    setChatHistory((prev) => [...prev, userMessage])
    setInput("")
    setIsTyping(true)
    try {
      // Call backend API
      const response = await fetch("http://localhost:8000/solve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: input, stream: false })
      })
      const data = await response.json()
      
      // Add agent response to history
      setChatHistory((prev) => [...prev, { 
        role: "agent", 
        content: { 
          answer: data.answer, 
          steps: data.steps || [], 
          solution: data.solution || "",
          question: input // Store original question for feedback
        } 
      }])
    } catch (error) {
      console.error("Error:", error)
      setChatHistory((prev) => [...prev, { role: "agent", content: { answer: "⚠️ Error fetching answer.", steps: [], solution: "" } }])
    }
    setIsTyping(false)
  }

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleSend()
  }

  const handleFileUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      const simulated = `Extracted question from ${file.name}`
      setChatHistory((prev) => [...prev, { role: "user", content: simulated }])
      onSendMessage(simulated)
    }
  }

  const copyToClipboard = (text) => navigator.clipboard.writeText(text)
  
  const handleFeedback = async (msg, rating) => {
    try {
      const response = await fetch("http://localhost:8000/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: msg.content.question || "",
          answer: msg.content.answer,
          rating: rating,
          comment: ""
        })
      })
      const result = await response.json()
      console.log("✅ Feedback submitted:", result)
    } catch (error) {
      console.error("❌ Error submitting feedback:", error)
    }
  }
  
  const lastAgent = chatHistory.filter((m) => m.role === "agent").slice(-1)[0]
  const animatedText = useTypingEffect(lastAgent?.content?.answer || "")

  return (
    <div className="flex flex-col h-screen bg-[#121212] text-white w-full">
      {chatHistory.length === 0 && !isTyping ? (
        <div className="flex flex-col flex-1 justify-center items-center text-center px-6">
          <h1 className="text-4xl font-bold mb-4">Welcome to Math Routing Agent</h1>
          <p className="text-gray-400 max-w-xl mb-8">Your AI-powered mathematics assistant. Get instant help with complex problems, step-by-step solutions, and personalized learning support.</p>
          <div className="w-full max-w-xl flex items-center gap-3 bg-[#1E1E1E] border border-orange-500 rounded-full px-5 py-3 shadow-lg">
            <label className="cursor-pointer text-gray-300 hover:text-orange-400 transition-colors">
              <FiUpload className="w-5 h-5" />
              <input type="file" className="hidden" accept=".pdf,.jpg,.jpeg,.png,.txt" onChange={handleFileUpload} />
            </label>
            <input type="text" value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={handleKeyPress} placeholder="Ask your math question..." className="flex-1 bg-transparent outline-none px-3 text-white placeholder-gray-500" />
            <button onClick={handleSend} className="bg-orange-500 hover:bg-orange-600 text-white rounded-full p-2 transition-colors">
              <IoMdSend className="w-5 h-5" />
            </button>
          </div>
          <div className="text-xs text-gray-500 text-center mt-4">Powered by Math Routing Agent • Built by Tharun Kumar</div>
        </div>
      ) : (
        <>
          <div className="flex-1 overflow-y-auto p-6 space-y-4 leading-relaxed">
            {chatHistory.map((msg, idx) => (
              <div key={idx} className={`p-4 rounded-2xl max-w-2xl ${msg.role === "agent" ? "bg-gray-900 border border-gray-700 text-white self-start" : "bg-[#1E1E1E] border border-orange-500 text-white self-end ml-auto"}`}>
                {msg.role === "agent" ? (
                  <>
                    <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]} className="prose prose-invert max-w-none">
                      {idx === chatHistory.length - 1 && isTyping ? animatedText : msg.content.answer}
                    </ReactMarkdown>
                    {msg.content.steps?.filter((step) => step && step.trim()).map((step, i) => (
                      <div key={i} className="text-gray-300 text-sm mt-2">
                        <span className="font-semibold text-orange-400">Step {i + 1}:</span>{" "}
                        <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]} className="inline">
                          {step}
                        </ReactMarkdown>
                      </div>
                    ))}
                    {msg.content.solution && (
                      <div className="mt-3 text-green-400 font-semibold flex items-center gap-2">
                        Final Solution: {msg.content.solution}
                        <button onClick={() => copyToClipboard(msg.content.solution)} className="text-gray-400 hover:text-white transition">
                          <BiCopy />
                        </button>
                      </div>
                    )}
                    <div className="flex gap-3 mt-3 text-gray-500">
                      <button onClick={() => handleFeedback(msg, 5)} className="hover:text-green-400 transition"><BiLike className="w-5 h-5" /></button>
                      <button onClick={() => handleFeedback(msg, 1)} className="hover:text-red-400 transition"><BiDislike className="w-5 h-5" /></button>
                    </div>
                  </>
                ) : (
                  <div>{msg.content}</div>
                )}
              </div>
            ))}
            <div ref={bottomRef} />
          </div>
          <div className="border-t border-gray-700 p-3 bg-[#121212] flex items-center gap-3 sticky bottom-0">
            <label className="cursor-pointer text-gray-300 hover:text-orange-400 transition-colors">
              <FiUpload className="w-5 h-5" />
              <input type="file" className="hidden" accept=".pdf,.jpg,.jpeg,.png,.txt" onChange={handleFileUpload} />
            </label>
            <input type="text" value={input} onChange={(e) => setInput(e.target.value)} onKeyDown={handleKeyPress} placeholder="Type your question..." className="flex-1 bg-transparent outline-none px-3 text-white placeholder-gray-500" />
            <button onClick={handleSend} className="bg-orange-500 hover:bg-orange-600 text-white rounded-full p-2 transition-colors">
              <IoMdSend className="w-5 h-5" />
            </button>
          </div>
        </>
      )}
    </div>
  )
}
