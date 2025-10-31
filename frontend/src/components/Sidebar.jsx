import { FiPlus } from 'react-icons/fi';

const Sidebar = ({ chatHistory, onNewChat }) => {
  // ✅ Filter only user questions
  const userQuestions = chatHistory.filter((msg) => msg.role === 'user');

  return (
    <div className="w-64 bg-[#111] h-screen flex flex-col border-r border-gray-800">
      {/* 🟠 New Chat Button */}
      <div className="p-4 border-b border-gray-800">
        <button
          onClick={onNewChat}
          className="w-full bg-orange-500 hover:bg-orange-600 text-white font-semibold py-2 px-3 rounded-lg transition-all shadow-md flex items-center justify-center gap-2 text-sm"
        >
          <FiPlus className="w-4 h-4" />
          New Chat
        </button>
      </div>

      {/* 📜 Search History */}
      <div className="flex-1 overflow-y-auto p-4">
        <h3 className="text-gray-300 text-sm font-semibold mb-3 uppercase tracking-wide">
          Search History
        </h3>
        {userQuestions.length === 0 ? (
          <p className="text-gray-500 text-xs italic">No searches yet</p>
        ) : (
          <div className="space-y-2">
            {userQuestions.map((chat, index) => (
              <div
                key={index}
                className="p-2 bg-[#1a1a1a] hover:bg-[#222] rounded cursor-pointer transition-all"
              >
                <p className="text-white text-xs font-medium truncate">
                  {chat.content || 'Untitled'}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* ⚙️ Footer */}
      <div className="p-4 border-t border-gray-800">
        <p className="text-white text-sm font-semibold">Math Solver Agent</p>
        <p className="text-gray-400 text-xs mt-1">AI Math Assistant</p>
      </div>
    </div>
  );
};

export default Sidebar;
